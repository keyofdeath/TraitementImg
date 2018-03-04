#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
# l = Laplacien()
#
# img = ImgOprerator("meme run.png")
# img.apply(l)
# img.show_img("Res")


def auto_canny(image, sigma=0.33):
    """
    Applique un filtre canny automatiquement en fonction de la median de l'image
    :param image:
    :param sigma:
    :return:
    """
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    print(lower)
    upper = int(min(255, (1.0 + sigma) * v))
    print(upper)
    print("rrr")
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


def nothing(x):
    pass


cv2.namedWindow('image')
cap = cv2.VideoCapture(1)
cv2.createTrackbar('low','image',0,200,nothing)
cv2.createTrackbar('hight','image',0,200,nothing)
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    low = cv2.getTrackbarPos('low','image')
    hight = cv2.getTrackbarPos('hight','image')

    # Display the resulting frame
    cv2.imshow('image', cv2.Canny(gray, low, hight))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
if __name__ == "__main__":
    pass
