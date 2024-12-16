import cv2 as cv
import numpy as np
import math
from ImageProcess import ImageProcess

def test():
    originalImage = ImageProcess.createBlackImage()
    point1 = (100, 100)
    point2 = (100, 500)

    ret, point3 = ImageProcess.equilateralTriangleFrom2Points(point1, point2)
    if ret:
        image = cv.circle(originalImage, point1, 5, 255, -1)
        image = cv.circle(image, point2, 5, 255, -1)
        image = cv.circle(image, point3, 5, 255, -1)
        cv.imshow("image", image)
    else:
        return
test()

cv.waitKey(0)
cv.destroyAllWindows()