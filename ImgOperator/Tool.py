#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
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
    return np.zeros((height, width, 3), np.uint8)


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


if __name__ == "__main__":
    pass
