#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob, os


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


if __name__ == "__main__":
    pass
