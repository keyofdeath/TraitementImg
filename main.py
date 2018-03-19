#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from ImgOperator.Tool import get_4_point_contour
import numpy as np
import ImgOperator as io
from MtgCardLib import *


def img_card_reco(name):
    """

    :param name:
    :return:
    """
    c = CardGet("kaladesh")
    img = cv2.imread(name)
    screen_cont = get_4_point_contour(img)

    if screen_cont is not None:

        trans = io.ImgTranslation(screen_cont)
        wrap = trans.apply(img)
        cv2.imshow("Transform result", wrap)
        card_info = c.recognize_card(wrap)["name"]
        print(card_info)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(img, card_info, (int(screen_cont[1][0] / 2) + 50, int(screen_cont[2][1] / 2)), font, 1,
                    (255, 255, 255), 1, cv2.LINE_4)
        cv2.imshow("Card found", img)
        cv2.waitKey(0)


def main():

    c = CardGet("kaladesh")
    cap = cv2.VideoCapture(1)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        orginal = frame.copy()
        screenCnt = get_4_point_contour(frame)
        try:
            if screenCnt is not None:
                operator3 = io.ImgOprerator(frame)
                operator3.add_oporation(io.ImgTranslation(screenCnt))
                wrap = operator3.img
                cv2.imshow('img trasform', wrap)
                print(c.recognize_card(wrap)["name"])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite("out.jpg", orginal)
                break
        except Exception as e:
            print(e)


if __name__ == "__main__":
    img_card_reco("imgSample/pic_1.jpg")

