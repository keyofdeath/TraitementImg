#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator import *
import cv2

if __name__ == "__main__":
    cam = cv2.VideoCapture(1)
    take_pic(cam)
