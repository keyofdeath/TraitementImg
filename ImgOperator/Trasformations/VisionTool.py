#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def tnormalisation(x):
    """

    :param x:
    :return:
    """
    x = np.asarray(x)
    m, s = np.mean(x, 0), np.std(x)

    Tr = np.array([[s, 0, m[0]], [0, s, m[1]], [0, 0, 1]])

    Tr = np.linalg.inv(Tr)

    return Tr


def DLT(img, obj):
    """

    :param img:
    :param obj:
    :return:
    """

    imgrows, imgcols = np.shape(img)
    objrows, objcols = np.shape(obj)

    T = tnormalisation(img)
    Tprime = tnormalisation(obj)

    Tinv = np.linalg.inv(T)

    imgtilde = np.dot(T, img)
    objtilde = np.dot(Tprime, obj)

    zeros = np.zeros(objrows)
    Htilde = np.empty((0, imgrows * 3))

    vect_obj_transpose = np.transpose(objtilde)
    vect_img_transpose = np.transpose(imgtilde)
    for i in range(objcols):
        h1 = np.concatenate((zeros, -vect_obj_transpose[i, :],
                             vect_obj_transpose[i, :] * vect_img_transpose[i, 1]))

        h2 = np.concatenate((vect_obj_transpose[i, :], zeros,
                             -vect_obj_transpose[i, :] * vect_img_transpose[i, 0]))

        h = np.vstack((h1, h2))

        Htilde = np.concatenate((Htilde, h))

    u, s, vh = np.linalg.svd(Htilde)

    Htilde = np.reshape(vh[np.shape(vh)[0] - 1, :], (imgrows, objrows))

    H = np.dot(Tinv, np.dot(Htilde, Tprime))
    H = H / H[-1, -1]

    return H


if __name__ == "__main__":
    pass
