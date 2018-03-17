#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from skimage import exposure
import ImgOperator as io


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
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


def get4_point_contour(sigma):

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        # Ramer–Douglas–Peucker algorithm
        approx = cv2.approxPolyDP(c, sigma * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            return approx

    return None


def hand_transform(img, contour):

    operator3 = io.ImgOprerator(img)

    pts = contour.reshape(4, 2)
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
    operator3.add_oporation(io.ImgTranslation(rect))
    return operator3.img


def perspectiv_trasform(img, contour):

    # now that we have our screen contour, we need to determine
    # the top-left, top-right, bottom-right, and bottom-left
    # points so that we can later warp the image -- we'll start
    # by reshaping our contour to be our finals and initializing
    # our output rectangle in top-left, top-right, bottom-right,
    # and bottom-left order
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # compute the difference between the points -- the top-right
    # will have the minumum difference and the bottom-left will
    # have the maximum difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # now that we have our rectangle of points, let's compute
    # the width of our new image
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    # ...and now for the height of our new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # construct our destination points which will be used to
    # map the screen to a top-down, "birds eye" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    M = cv2.getPerspectiveTransform(rect, dst)
    print("M = ", M)
    warp = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    return warp


def nothing(x):
    """
    LA focntion fait...
    :param x: lellel
    :return: eelel
    """
    pass


cv2.namedWindow('img contour')
cap = cv2.VideoCapture(1)
cv2.createTrackbar('low', 'img contour', 0, 100, nothing)
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    orginal = frame.copy()

    low = cv2.getTrackbarPos('low', 'img contour')

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_fram_filtre = cv2.GaussianBlur(gray, (3, 3), 0)
    edge = auto_canny(gray_fram_filtre, 100 / 100)

    cv2.imshow('image edge', edge)

    cntr_frame, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    try:
        sig = 0.03
        screenCnt = get4_point_contour(sig)
        if screenCnt is not None:
            cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)
            cv2.imshow('img contour', frame)
            wrap1 = perspectiv_trasform(orginal, screenCnt)
            # wrap2 = hand_transform(orginal, screenCnt)
            cv2.imshow('img trasform 1', wrap1)
            # cv2.imshow('img trasform 2', wrap2)

    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("out.jpg", orginal)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    pass
