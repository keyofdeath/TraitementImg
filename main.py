#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from ImgOperator.Tool import get_4_point_contour
import numpy as np
import ImgOperator as io


def main():

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

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite("out.jpg", orginal)
                break
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()

