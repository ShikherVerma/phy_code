#!/usr/bin/python

'''
Usage:
    houghcircles.py [<image_name>]
'''

import cv2
import numpy as np
import sys

def waiter():
    k = cv2.waitKey(0)
    if k == 27:
        sys.exit(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except IndexError:
        sys.exit("Provide image in arg")

    print("Starting calc")
    src = cv2.imread(fn, 1)
    
    print("Converting to greyscale")
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imshow("original", img)
    waiter()
   
    print("Removing noise")
    img = cv2.fastNlMeansDenoising(img, None, 10, 10, 3)
    cv2.imshow("removing noise", img)
    waiter()

    print("Contrast streching")
    img = cv2.equalizeHist(img)
    cv2.imshow("contrast streched", img)
    waiter()

    print("Bluring")
    img = cv2.medianBlur(img, 5)
    cv2.imshow("after blur", img)
    waiter()
    
    print("Detecting circles")
    cimg = src.copy() # numpy function
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), param1=1, param2=300, minRadius=100, maxRadius=0)

    if circles is not None: # Check if circles have been found and only then iterate over these and add them to the image
        print("Drawing images")
        a, b, c = circles.shape
        for i in range(2):
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv2.LINE_AA)
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), 2, (0, 255, 0), 3, cv2.LINE_AA)  # draw center of circle
        cv2.imshow("detected circles", cimg)
        print("Press key to exit")
        cv2.waitKey(0)
