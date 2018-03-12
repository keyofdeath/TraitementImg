#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
from ImgOperator.Filtration.Canny import ImgCanny
from copy import deepcopy


def take_pic(cam):
    """

    :param cam:
    :return:
    """
    while True:
        ret, frame = cam.read()
        cv2.imshow("main", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(33) == ord('y'):
            try:
                # nom sous la form pic_x.jpg ou x est le numéros de l'image
                num = int(glob.glob("*.jpg")[-1].split("_")[1][0])
                cv2.imwrite("pic_{}.jpg".format(num + 1), frame)
            except Exception as _:
                cv2.imwrite("pic_1.jpg", frame)
            finally:
                print("take")
            break


def creat_empty_img(height, width):
    """

    :return:
    """
    return np.zeros((int(height) + 1, int(width) + 1, 3), np.uint8)


def get_all_pix_between_2_point(point_a, point_b, axe):
    """

    :param point_a:
    :param point_b:
    :param axe: 0 sur l'axe des y (pour savoir la valeur de x)
                1 sur la l'axe des x (pour savoir la valeur de y)
    :return:
    """
    # fonction de calcule selon l'axe demander

    # si on est sur l'axe des y (axe = 0) on cherche donc les valeur de x (y - p) / m
    fx = lambda y, m, p: (y - p) / m if axe == 0 else lambda x, m, p: x
    # si on est sur l'axe des x (axe = 1) on cherche donc les valeur de y (m * x + p)
    fy = lambda y, m, p: y if axe == 0 else lambda x, m, p: m * x + p
    m = (point_b[0] - point_a[0]) / (point_b[1] - point_a[1])
    p = point_a[0] - m * point_a[1]
    res = list()
    incr = 1 if point_a[axe] < point_b[axe] else -1
    for a in range(point_a[axe], point_b[axe], incr):
        res.append([int(fy(a, m, p)), int(fx(a, m, p))])
    return res


def get_4_point_contour(img):
    """

    :param img:
    :return:
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_fram_filtre = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = ImgCanny()
    edge = canny.apply(gray_fram_filtre)
    cntr_frame, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    sigma = 0.03
    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        # Ramer–Douglas–Peucker algorithm
        approx = cv2.approxPolyDP(c, sigma * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            pts = approx.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")
            # on somme chaque position
            s = pts.sum(axis=1)
            # le coin haut gauche est la somme la plus petit
            rect[0] = pts[np.argmin(s)]
            # Le coin bas droit est la somme la plus grande
            rect[3] = pts[np.argmax(s)]
            # on calcule la difference entre chaque position
            diff = np.diff(pts, axis=1)
            # La position haut gauche aura la plus petit diférence
            rect[1] = pts[np.argmin(diff)]
            # La position bas gauche aura la plus grande différence
            rect[2] = pts[np.argmax(diff)]
            return rect

    return None


if __name__ == "__main__":
    pass
