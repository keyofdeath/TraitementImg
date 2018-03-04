#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator import *


if __name__ == "__main__":
    operator = ImgOprerator("../imgSample/pic_1.jpg")
    # operator.add_oporation(ImgRotation([[89, 230], [92, 456], [426, 207], [431, 469]]))
    operator.add_oporation(ImgTranslation([[89, 431], [230, 469]]))
