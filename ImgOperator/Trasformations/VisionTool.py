#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def normalization(dim, x):
    """
    Normalise les coordonées (centre a l'origine)
    :param dim: Dimention des point donnée 3 pour DLT 3D 2 pour DLT 2D
    :param x: point qui dois êtres normaliser
    :return: Tr = Matrice de transformation
             x = Valeur transformer
    """

    x = np.asarray(x)
    m, s = np.mean(x, 0), np.std(x)
    if dim == 2:
        Tr = np.array([[s, 0, m[0]], [0, s, m[1]], [0, 0, 1]])
    else:
        Tr = np.array([[s, 0, 0, m[0]], [0, s, 0, m[1]], [0, 0, s, m[2]], [0, 0, 0, 1]])
    Tr = np.linalg.inv(Tr)
    x = np.dot(Tr, np.concatenate((x.T, np.ones((1, x.shape[0])))))
    x = x[0:dim, :].T
    return Tr, x


def dlt_reconstruction(dim, view_number, camera_dlt, image_point):
    """
    Converti un point image en point objet
    Fonctione pour des point 2D ou 3D
    :param dim: Dimention des point donnée 3 pour DLT 3D 2 pour DLT 2D
    :param view_number: Nombre de vue (ou caméras utiliser)
    :param camera_dlt: Calibration de la camera valeur renvoyer par la DLT
    :param image_point: Coordonée des point image a convertir en poitn objet
    :return: Les point dans l'espace (point objet)
    """
    # Convert Ls to array:
    camera_dlt = np.asarray(camera_dlt)
    # Check the parameters:
    if camera_dlt.ndim == 1 and view_number != 1:
        raise ValueError('Number of views ({}) and number of sets of camera calibration parameters (1) are different.'.
                         format(view_number))

    if camera_dlt.ndim > 1 and view_number != camera_dlt.shape[0]:
        raise ValueError('Number of views ({}) and number of sets of camera calibration parameters ({}) are different.'.
                         format(view_number, camera_dlt.shape[0]))

    if dim == 3 and camera_dlt.ndim == 1:
        raise ValueError('At least two sets of camera calibration parameters are needed for 3D point reconstruction.')

    # Si on est en 2D avec une caméra
    if view_number == 1:
        # 2D and 1 camera (view), the simplest (and fastest) case
        # One could calculate inv(H) and input that to the code to speed up things if needed.
        # (If there is only 1 camera, this transformation is all Floatcanvas2 might need)
        Hinv = np.linalg.inv(camera_dlt.reshape(3, 3))
        # Point coordinates in space:
        xyz = np.dot(Hinv, [image_point[0], image_point[1], 1])
        xyz = xyz[0:2] / xyz[2]
    else:
        M = []
        for i in range(view_number):
            L = camera_dlt[i, :]
            u, v = image_point[i][0], image_point[i][1]  # this indexing works for both list and numpy array
            if dim == 2:
                M.append([L[0] - u * L[6], L[1] - u * L[7], L[2] - u * L[8]])
                M.append([L[3] - v * L[6], L[4] - v * L[7], L[5] - v * L[8]])
            elif dim == 3:
                M.append([L[0] - u * L[8], L[1] - u * L[9], L[2] - u * L[10], L[3] - u * L[11]])
                M.append([L[4] - v * L[8], L[5] - v * L[9], L[6] - v * L[10], L[7] - v * L[11]])

        # Find the xyz coordinates:
        U, S, Vh = np.linalg.svd(np.asarray(M))
        # Point coordinates in space:
        xyz = Vh[-1, 0:-1] / Vh[-1, -1]

    return xyz


def dlt(dim, object_point, img_point):
    """
    Calibration de point (2D ou 3D) a l'aide d'une DLT
    :param dim: Dimention des point donnée 3 pour DLT 3D 2 pour DLT 2D
    :param object_point: Position 2D ou 3D du dans l'espace qui dois être calibrer
    :param img_point: Position dans l'image de l'objet a calibrer
    :return: L: Une liste de 8 ou 11 parametres de la la matric de calibartion
            err: erreur de la dlt (résidu de la transformation)
    """

    object_point = np.asarray(object_point)
    img_point = np.asarray(img_point)
    number_point = object_point.shape[0]

    # vérifiaction des paramètre donnée
    if img_point.shape[0] != number_point:
        raise ValueError('object_point ({} points) est image point ({} points) nons pas le maime nombre de points.'.
                         format(number_point, img_point.shape[0]))

    if (dim == 2 and object_point.shape[1] != 2) or (dim == 3 and object_point.shape[1] != 3):
        raise ValueError('Le nomnre de coordonées et incorect ({}) pour {} DLT (il ne faudrait {}).'.
                         format(object_point.shape[1], dim, dim))

    if dim == 3 and number_point < 6 or dim == 2 and number_point < 4:
        raise ValueError('{} DLT a besoin {} calibration points. Que {} points on été entrer.'.
                         format(dim, 2 * dim, number_point))

    # Normalisation des point données cela permais d'augmenter la qualiter de la DLT
    Txyz, xyzn = normalization(dim, object_point)
    T_img_point, img_point_norm = normalization(2, img_point)

    A = []
    # Si on est en DLT 2D
    if dim == 2:
        # Création de la matrice 2D
        for i in range(number_point):
            x, y = xyzn[i, 0], xyzn[i, 1]
            u, v = img_point_norm[i, 0], img_point_norm[i, 1]
            A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
            A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    # Si on est en DLT 3D
    elif dim == 3:
        for i in range(number_point):
            x, y, z = xyzn[i, 0], xyzn[i, 1], xyzn[i, 2]
            u, v = img_point_norm[i, 0], img_point_norm[i, 1]
            A.append([x, y, z, 1, 0, 0, 0, 0, -u * x, -u * y, -u * z, -u])
            A.append([0, 0, 0, 0, x, y, z, 1, -v * x, -v * y, -v * z, -v])

    A = np.asarray(A)
    # Find the 11 (or 8 for 2D DLT) parameters:
    U, S, Vh = np.linalg.svd(A)
    # The parameters are in the last line of Vh and normalize them:
    L = Vh[-1, :] / Vh[-1, -1]
    # Camera projection matrix:
    H = L.reshape(3, dim + 1)
    # Denormalization:
    H = np.dot(np.dot(np.linalg.pinv(T_img_point), H), Txyz)
    H = H / H[-1, -1]
    L = H.flatten(0)
    # Mean error of the DLT (mean residual of the DLT transformation in units of camera coordinates):
    img_point_2 = np.dot(H, np.concatenate((object_point.T, np.ones((1, object_point.shape[0])))))
    img_point_2 = img_point_2 / img_point_2[2, :]
    # mean distance:
    err = np.sqrt(np.mean(np.sum((img_point_2[0:2, :].T - img_point) ** 2, 1)))

    return L, err


if __name__ == "__main__":
    pass
