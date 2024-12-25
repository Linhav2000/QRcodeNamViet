import traceback

import cv2 as cv
import numpy as np
import math
from tkinter import messagebox
from Modules.Camera.CameraParameter import CameraRotate
from pyzbar import pyzbar
from pylibdmtx import pylibdmtx
# import pytesseract
import threading
from imutils.object_detection import non_max_suppression
from multiprocessing import Process,  Queue, Lock
from scipy import ndimage

def affineTransform():
    global source, adjustedImage
    source = np.zeros((7680, 10240), np.float32)
    color = (0, 0, 0)

    cvSource = cv.cvtColor(source, cv.COLOR_GRAY2BGR).astype(np.uint8)
    cvSource[:] = tuple(reversed(color))

    points = [(101, 201), (100, 200), (401, 201), (501, 601),(110, 120), (200, 200), (140, 120), (350, 160),
              (210, 220), (5200, 3200), (4240, 220), (7250, 8260)]

    refPoint1 = [(1400, 1120),(1760, 1580), (1126, 1490)]
    refPoint2 = [(2000, 1720),(2360, 2180), (1726, 2090)]
    cvSource = cv.cvtColor(cvSource, cv.COLOR_BGR2GRAY)
    for point in points:
        cvSource = cv.circle(cvSource, point, 5, 255, -1)

    for ref in refPoint1:
        cvSource = cv.circle(cvSource, ref, 60, 255, -1)
    # cvSource = cv.circle(cvSource, refPoint1[2], 60, 0, -1)

    pts1 = np.float32([refPoint1[0], refPoint1[1], refPoint1[2]])
    pts2 = np.float32([refPoint2[0], refPoint2[1], refPoint2[2]])

    matrix = cv.getAffineTransform(pts1, pts2)
    adjustPoint = []
    for point in refPoint1:
        x1 = point[0]*matrix[0][0] + point[1]*matrix[0][1] + matrix[0][2]
        y1 = point[0]*matrix[1][0] + point[1]*matrix[1][1] + matrix[1][2]
        adjustPoint.append((int(x1), int(y1)))
        # print("x1={}, y1={}".format(int(x1), int(y1)))
    for point in points:
        x1 = point[0] * matrix[0][0] + point[1] * matrix[0][1] + matrix[0][2]
        y1 = point[0] * matrix[1][0] + point[1] * matrix[1][1] + matrix[1][2]
        adjustPoint.append((int(x1), int(y1)))
        # print("x1={}, y1={}".format(int(x1), int(y1)))
    retMatrix = cv.getAffineTransform(pts2, pts1)
    angleMatrix = cv.getRotationMatrix2D((cvSource.shape[1]/2, cvSource.shape[0]/2), 20, 1)

    adjustedImage = cv.warpAffine(cvSource, matrix, (10240, 7680))
    angleImage = cv.warpAffine(adjustedImage, angleMatrix, (10240, 7680))

    for point in adjustPoint:
        x1 = point[0] * angleMatrix[0][0] + point[1] * angleMatrix[0][1] + angleMatrix[0][2]
        y1 = point[0] * angleMatrix[1][0] + point[1] * angleMatrix[1][1] + angleMatrix[1][2]
        print("x1={}, y1={}".format(int(x1), int(y1)))
    print("------------")

    contours, _ = cv.findContours(angleImage, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        contourArea = cv.contourArea(contour)
        (x, y, w, h) = cv.boundingRect(contour)
        center = (int(x + (w / 2)), int(y + (h / 2)))
        print(contourArea)
        print(center)

    angleRefPoint = [(1463, 2915), (1959, 3224), (1332, 3357)]

    deg = findAngleByLine((angleRefPoint[0],angleRefPoint[2]),(refPoint2[0],refPoint2[2]))
    print(deg)
    retAngleMatrix = cv.getRotationMatrix2D((cvSource.shape[1]/2, cvSource.shape[0]/2), -deg, 1)
    undoImage = cv.warpAffine(angleImage, retAngleMatrix, (10240, 7680))
    undoImage = cv.warpAffine(undoImage, retMatrix, (10240, 7680))

    cvSource = cv.resize(cvSource, (1600, 1200))
    adjustedImage = cv.resize(adjustedImage, (1600, 1200))
    angleImage = cv.resize(angleImage, (1600, 1200))
    undoImage = cv.resize(undoImage, (1600, 1200))
    cv.imshow("image", cvSource)
    cv.imshow("affine", adjustedImage)
    cv.imshow("angle", angleImage)
    cv.imshow("undo", undoImage)

    return cvSource

def findAngleByLine(line1, line2):
    deg1 = findAngleByVector(line1[0], line1[1])
    deg2 = findAngleByVector(line2[0], line2[1])
    return deg2 - deg1

def findAngleByVector(vec1, vec2):
    v1x, v1y = vec1
    v2x, v2y = vec2
    rad = math.atan2(v2y - v1y, v2x - v1x)

    deg = math.degrees(rad)
    return deg


def angleFrom2Vec(vec1, vec2):
    unit_vector_1 = vec1 / np.linalg.norm(vec1)
    unit_vector_2 = vec2 / np.linalg.norm(vec2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    radian = np.arccos(dot_product)
    degrees = math.degrees(radian)
    print("the deviation degree: {}".format(degrees))
    return degrees


def calculateDistanceBy2Points(point1, point2):
    try:
        x1, y1 = point1
        x2, y2 = point2
        distance = math.sqrt((int(x2) - int(x1)) ** 2 + (int(y2) - int(y1)) ** 2)
        return distance
    except:
        return
def distance_point_to_line(point=(0, 0), line=((0, 0), (1, 1))):
    norm = np.linalg.norm
    try:
        point_line1 = np.array(line[0])
        point_line2 = np.array(line[1])

        single_point = np.array(point)

        d = np.abs(norm(np.cross(point_line2 - point_line1, point_line1 - single_point))) / norm(point_line2 - point_line1)
        return True, d
    except Exception as error:
        print(f"{error}")
        return False, 0

def project_from_point_to_line(point=(0, 0), line=((0, 0), (1, 1))):
    try:
        point_line1 = np.array(line[0])
        point_line2 = np.array(line[1])

        single_point = np.array(point)
        line_length = np.sum((point_line1 - point_line2) ** 2)
        if line_length == 0:
            print('p1 and p2 are the same points')
        t = max(0, min(1, np.sum((single_point - point_line1) * (point_line2 - point_line1)) / line_length))

        projection = point_line1 + t * (point_line2 - point_line1)
        return True, (int(projection[0]), int(projection[1]))
    except Exception as error:
        print(f"{error}")
        return False, None

def createBlackImage(size=(600, 800)):
    global source, adjustedImage
    source = np.zeros(size, np.float32)
    color = (0, 0, 0)

    try:
        source = cv.cvtColor(source, cv.COLOR_GRAY2BGR).astype(np.uint8)
        source[:] = tuple(reversed(color))

        source = cv.cvtColor(source, cv.COLOR_BGR2GRAY)
    except:
        pass
    return source.copy()

def createWhiteImage(size=(600, 800)):
    global source, adjustedImage
    source = np.zeros(size, np.float32)
    color = (255, 255, 255)

    try:
        source = cv.cvtColor(source, cv.COLOR_GRAY2BGR).astype(np.uint8)
        source[:] = tuple(reversed(color))

        source = cv.cvtColor(source, cv.COLOR_BGR2GRAY)
    except:
        pass
    return source.copy()

def createSilverImage(size=(600, 800)):
    global source, adjustedImage
    source = np.zeros(size, np.float32)
    color = (105, 105, 105)

    try:
        source = cv.cvtColor(source, cv.COLOR_GRAY2BGR).astype(np.uint8)
        source[:] = tuple(reversed(color))

        source = cv.cvtColor(source, cv.COLOR_BGR2GRAY)
    except:
        pass
    return source.copy()

def processThreshold(source, thresh, maxval, type):
    if len(source.shape) > 2:
        try:
            sourceImage = processCvtColor(source, cv.COLOR_BGR2GRAY)
        except:
            sourceImage = processCvtColor(source, cv.COLOR_RGB2GRAY)
    else:
        sourceImage = source.copy()
    ret = cv.threshold(sourceImage, thresh, maxval, type)
    return ret

def processConnectContours(sourceContours, image, size=1, distance=1, location=-1):
    # firstContour = sourceContours[0]
    # (x, y, w, h) = cv.boundingRect(firstContour)
    # first_center = (int(x + (w / 2)), int(y + (h / 2)))
    # list_contours_dist = []
    # for contour in sourceContours:
    #     (x, y, w, h) = cv.boundingRect(contour)
    #     center = (int(x + (w / 2)), int(y + (h / 2)))
    #     contoursDist = calculateDistanceBy2Points(center, first_center)
    #     list_contours_dist.append((contoursDist, contour))
    #
    # list_contours_dist.sort(key=sortContourDist)
    #
    list_contours_dist = sourceContours

    LENGTH = len(list_contours_dist)
    # status = np.zeros((LENGTH, 1))
    pare_queue = Queue()
    i = 0
    while i < LENGTH:
        processes = []
        for processing_index in range(6):
            cnt1 = list_contours_dist[i]
            processes.append(Process(target=find_close_processing, args=(pare_queue, list_contours_dist, LENGTH, i, cnt1, distance, 20)))
            i += 1

        for process in processes:
            process.start()

        for process in processes:
            process.join()


    for i in range(LENGTH):
        cnt1 = list_contours_dist[i]
        # (x, y, w, h) = cv.boundingRect(cnt1)
        # center1 = (int(x + (w / 2)), int(y + (h / 2)))
        for j in range(i + 1, LENGTH):
            if j - i > 20:
                break
            cnt2 = list_contours_dist[j]
            # (x, y, w, h) = cv.boundingRect(cnt2)
            # center2 = (int(x + (w / 2)), int(y + (h / 2)))
            # contoursDist = calculateDistanceBy2Points(center1, center2)
            # # if contoursDist > distance * 5:
            #     break
            isClosed, connectPoint1, connectPoint2 = find_if_close(cnt1, cnt2, distance)
            if isClosed:
                cv.line(image, pt1=connectPoint1, pt2=connectPoint2, color=(255, 255, 255), thickness=int(math.sqrt(distance)))
            #     val = min(status[i], status[x])
            #                 #     status[x] = status[i] = val
            #                 # else:
            #                 #     if status[x] == status[i]:
            #                 #         status[x] = i + 1
                break
    return image
def find_close_processing(pare_queue, list_contours_dist, LENGTH, i, cnt1, distance, limit_compare=20):
    for j in range(i + 1, LENGTH):
        if j - i > limit_compare:
            break
        cnt2 = list_contours_dist[j]
        isClosed, connectPoint1, connectPoint2 = find_if_close(cnt1, cnt2, distance)
        if isClosed:
            pare_queue.put((connectPoint1, connectPoint2))
            break

def sortContourDist(e):
    return e[0]

def find_if_close(cnt1,cnt2, minDist):
    closedDist = None
    connectPoint1 = (0, 0)
    connectPoint2 = (0, 0)
    for pt1 in cnt1:
        point1 = (pt1[0][0], pt1[0][1])
        for pt2 in cnt2:
            point2 = (pt2[0][0], pt2[0][1])
            dist = calculateDistanceBy2Points(point1, point2)
            if closedDist is None:
                connectPoint1 = point1
                connectPoint2 = point2
                closedDist = calculateDistanceBy2Points(connectPoint1, connectPoint2)
            elif dist < closedDist:
                closedDist = dist
                connectPoint1 = point1
                connectPoint2 = point2
    # return False, connectPoint1, connectPoint2
    if closedDist < minDist:
        return True, connectPoint1, connectPoint2
    else:
        return False, connectPoint1, connectPoint2
    # ext1s = processFindExtremeOfContour(cnt1)
    # ext2s = processFindExtremeOfContour(cnt2)
    # for ext1 in ext1s:
    #     for ext2 in ext2s:
    #         if closedDist is None:
    #             connectPoint1 = ext1
    #             connectPoint2 = ext2
    #             closedDist = calculateDistanceBy2Points(ext1, ext2)
    #         elif calculateDistanceBy2Points(ext1, ext2) < closedDist:
    #             closedDist = calculateDistanceBy2Points(ext1, ext2)
    #             connectPoint1 = ext1
    #             connectPoint2 = ext2
    # if closedDist < dist:
    #     return True, connectPoint1, connectPoint2
    # else:
    #     return False, connectPoint1, connectPoint2

def  processFindContours(source, minArea = -1, maxArea=-1, minWidth=-1,
                         maxWidth=-1, maxHeight=-1, minHeight=-1,
                         minAspectRatio=-1, maxAspectRatio=-1):
    sourceImage = source.copy()
    areaDetectList = []
    if len(sourceImage.shape) == 3:
        try:
            sourceImage = processCvtColor(sourceImage, cv.COLOR_BGR2GRAY)
        except:
            sourceImage = processCvtColor(sourceImage, cv.COLOR_RGB2GRAY)

    listContours = []
    contours, _ = cv.findContours(sourceImage, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[-2:]
    i = 0
    for contour in contours:
        passed = False
        contourArea = cv.contourArea(contour)
        # (x, y, w, h) = cv.boundingRect(contour)
        (x, y), (e1, e2), angle = cv.minAreaRect(contour)
        if e1 == 0:
            e1 = 1
        if e2 == 0:
            e2 = 1
        w = min(e1, e2)
        h = max(e1, e2)

        aspect_ratio = h / w
        # center = (int(x + (w / 2)), int(y + (h / 2)))
        # print(contourArea)
        # print(center)

        if (contourArea > minArea > 0 or minArea < 0)\
            and (maxArea > contourArea > 0 or maxArea < 0)\
            and (w > minWidth > 0 or minWidth < 0)\
            and(maxWidth > w > 0 or maxWidth < 0)\
            and (h > minHeight > 0 or minHeight < 0)\
            and (maxHeight > h > 0 or maxHeight < 0)\
            and (aspect_ratio > minAspectRatio > 0 or minAspectRatio < 0)\
            and (maxAspectRatio > aspect_ratio > 0 or maxAspectRatio < 0):
            passed = True
            # cv.putText(img=sourceImage, text=f"{i}", org=(int(x), int(y)), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color = (255, 255, 255), thickness=5)
            i += 1
        # else:
            # cv.drawContours(image=sourceImage, contours=[contour], color=0, thickness=-1)
            # cv.fillPoly(img=sourceImage, pts=[contour], color=0)

        (x, y, w, h) = cv.boundingRect(contour)
        if passed:
            listContours.append(contour)
            areaDetectList.append([x, y, x + w, y + h])
    return listContours, areaDetectList, sourceImage


def processFindExtremeOfContour(contour):
    extLeft = None
    extRight = None
    extTop = None
    extBot = None

    extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
    extRight = tuple(contour[contour[:, :, 0].argmax()][0])
    extTop = tuple(contour[contour[:, :, 1].argmin()][0])
    extBot = tuple(contour[contour[:, :, 1].argmax()][0])

    return extTop, extRight, extBot, extLeft

def processFindExtremeOfContourList(contourList):
    extLeft = None
    extRight = None
    extTop = None
    extBot = None
    for contour in contourList:
        extreme = processFindExtremeOfContour(contour)
        if extLeft is None:
            extTop, extRight, extBot, extLeft = extreme
        if extreme[0][1] < extTop[1]:
            extTop = extreme[0]
        if extreme[1][0] > extRight[0]:
            extRight = extreme[1]
        if extreme[2][1] > extBot[1]:
            extBot = extreme[2]
        if extreme[3][0] < extLeft[0]:
            extLeft = extreme[3]

    return extTop, extRight, extBot, extLeft

def processSubtract(sourceImage1, sourceImage2):
    return None

def processBS_KNN(sourceImage, history=None, dist2Threshold=None, detectShadows=None, existBackSub = None):
    knnFrame = None
    backSub = None
    text = ""
    if sourceImage is None:
        text = "The input image of background subtraction algorithm is None"
        return False, (knnFrame, backSub), text

    try:
        if existBackSub is None:
            backSub = cv.createBackgroundSubtractorKNN(history=history, dist2Threshold=dist2Threshold, detectShadows=detectShadows)
        else:
            backSub = existBackSub
        knnFrame = backSub.apply(sourceImage)
        return True, (knnFrame, backSub), text
    except Exception as error:
        text = "Cannot apply algorithm background subtraction. Please check the input parameter.\nDetail: {}".format(error)
        return False, (knnFrame, backSub), text


def processBS_Mog2(sourceImage, history=None, varThreshold=None, detectShadows=None, existBackSub=None):
    mogFrame = None
    backSub = None
    text = ""
    if sourceImage is None:
        text = "The input image of background subtraction algorithm is None"
        return False, (mogFrame, backSub), text

    try:
        if existBackSub is None:
            backSub = cv.createBackgroundSubtractorMOG2(history=history, varThreshold=varThreshold,
                                                        detectShadows=detectShadows)
        else:
            backSub = existBackSub
        mogFrame = backSub.apply(sourceImage)
        return True, (mogFrame, backSub), text
    except Exception as error:
        text = "Cannot apply algorithm background subtraction. Please check the input parameter.\nDetail: {}".format(
            error)
        return False, (mogFrame, backSub), text
def processHoughLine(sourceImage,workingArea, rho=1, theta=np.pi / 180, threshold=150, lines=None, srn=0, stn=0, min_theta=None, max_theta=None):
    image = sourceImage.copy()
    if len(image.shape) == 3:
        try:
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        except:
            image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    lineList = []
    dataList = cv.HoughLines(image=image,rho=rho,theta=theta,threshold=threshold,lines=lines,srn=srn,stn=stn,min_theta=min_theta,max_theta=max_theta)

    if dataList is not None:
        for i in range(0, len(dataList)):
            rho = dataList[i][0][0]
            theta = dataList[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 10000*(-b) + workingArea[0]), int(y0 + 10000*(a)) + workingArea[1])
            pt2 = (int(x0 - 10000*(-b) + workingArea[0]), int(y0 - 10000*(a)) + workingArea[1])

            lineList.append([pt1, pt2])

    return lineList

def processHoughLinesP(sourceImage, rho=1, theta=np.pi / 180, threshold=150, lines=None, minLineLength=100, maxLineGap=10):
    image = sourceImage.copy()
    if len(image.shape) == 3:
        try:
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        except:
            image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    lineList = []
    dataList = cv.HoughLinesP(image=image,rho=rho,theta=theta,threshold=threshold, lines=lines, minLineLength=minLineLength, maxLineGap=maxLineGap)

    if dataList is not None:
        for line in dataList:
            x1, y1, x2, y2 = line[0]
            pt1 = (x1, y1)
            pt2 = (x2, y2)
            lineList.append([pt1, pt2])

    return lineList

def processHoughCircle(image, workingArea, minDist=1,  param1=100, param2=50, minRadius=269, maxRadius=333):
    img = image.copy()
    if len(img.shape) == 3:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(img, 5)
    listCircle = []
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, minDist=minDist,  param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is None:
        return img, listCircle

    circles = np.uint16(np.around(circles))
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    for circle in circles[0, :]:
        # draw the outer circle
        cv.circle(img, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv.circle(img, (circle[0], circle[1]), 2, (0, 0, 255), 3)

        adjustCircle = ((workingArea[0] + circle[0], workingArea[1] + circle[1]), circle[2])
        listCircle.append(adjustCircle)
    return img, listCircle
class HoughCirclePointInfo:
    enumerateCircleX = 0
    enumerateCircleY = 0
    enumerateCircleR = 0
    baseCircle = (0, 0)
    betweenDist = 0
    numOfCircle = 0
    def __init__(self, baseCircle = (0, 0), betweenDist=100):
        self.betweenDist = betweenDist
        self.enumerateCircleX = 0
        self.enumerateCircleY = 0
        self.enumerateCircleR = 0
        self.numOfCircle = 0
        self.baseCircle = baseCircle
        self.checkCircle(circle=baseCircle)


    def checkCircle(self, circle):
        (centerX, centerY), radius = circle
        if calculateDistanceBy2Points((centerX, centerY), self.baseCircle[0]) < self.betweenDist:
            # Nếu đường tròn thỏa mãn điều kiện gần nhau
            self.enumerateCircleX += centerX
            self.enumerateCircleY += centerY
            self.enumerateCircleR += radius
            self.numOfCircle += 1
            return True
        else:
            # khi không thỏa mãn điều kiện gần nhau
            return False


    def calculateAverage(self):
        # Tình trung bình các thông số của nhóm
        circle = ((int(self.enumerateCircleX / self.numOfCircle), int(self.enumerateCircleY / self.numOfCircle)),
                  int(self.enumerateCircleR / self.numOfCircle))

        return circle

def processAverageHoughCircle(image, workingArea, minDist=1,  param1=100, param2=50, minRadius=269,
                              maxRadius=333, betweenDist=100, trustNumber=1):
    averageImage = image.copy()
    hougCircleImage, listCicles = processHoughCircle(image, workingArea, minDist=minDist,  param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    emurateCircleX = 0
    emurateCircleY = 0
    emurateCircleR = 0
    pointInfoList = []
    finalCircleList = []

    for circle in listCicles:
        if len(pointInfoList) < 1:
            # khi chưa có nhóm nào thì khởi tạo nhóm đầu tiên
            pointInfoList.append(HoughCirclePointInfo(baseCircle=circle, betweenDist=betweenDist))
        else:
            # khi đã có nhóm rồi thì cho check từng nhóm một
            ret = False
            for pointInfo in pointInfoList:
                # Duyệt từng nhóm một xem đường tròn có thỏa mãn hay không
                ret = pointInfo.checkCircle(circle=circle)
                if ret:
                    break
            if not ret:
                # nếu đường tròn không thuộc nhóm nào thì thêm 1 nhóm mới
                pointInfoList.append(HoughCirclePointInfo(baseCircle=circle, betweenDist=betweenDist))

    pointInfoList = [pointInfo for pointInfo in pointInfoList if pointInfo.numOfCircle >= trustNumber]
    for pointInfo in pointInfoList:
        finalCircle = pointInfo.calculateAverage()
        cv.circle(averageImage, (finalCircle[0][0] - workingArea[0], finalCircle[0][1] - workingArea[1]), finalCircle[1], (0, 255, 0), 5)
        cv.circle(averageImage, (finalCircle[0][0] - workingArea[0], finalCircle[0][1] - workingArea[1]), 10, (0, 255, 0), -1)

        finalCircleList.append(finalCircle)

    # for circle in listCicles:
    #     emurateCircleX += circle[0][0]
    #     emurateCircleY += circle[0][1]
    #     emurateCircleR += circle[1]
    # circle = None
    # if len(listCicles) > 0:
    #     circle = (int(emurateCircleX / len(listCicles)),
    #               int(emurateCircleY / len(listCicles)),
    #               int(emurateCircleR / len(listCicles)))
    #     cv.circle(averageImage, (circle[0] - workingArea[0], circle[1] - workingArea[1]), circle[2], (0, 255, 0), 5)
    #     cv.circle(averageImage, (circle[0] - workingArea[0], circle[1] - workingArea[1]), 10, (0, 255, 0), -1)

    if len(finalCircleList) <= 0:
        return None, averageImage, hougCircleImage
    else:
        return finalCircleList, averageImage, hougCircleImage # (x, y, radius)

def equilateralTriangleFrom2Points(point1, point2, isRightSide=True):
    try:
        if isRightSide:
            angleMatrix = cv.getRotationMatrix2D(point2, -60, 1)
        else:
            angleMatrix = cv.getRotationMatrix2D(point2, 60, 1)

        point3 = transformPoint(point1, angleMatrix)
        print(point3)
        return True, point3
    except:
        return False, (0, 0)

def rotatePointWithTransform(origin, point, angle):
    try:
        angleMatrix = cv.getRotationMatrix2D(center=origin, angle=angle, scale=1)
        retPoint = transformPoint(point, angleMatrix)
        return True, retPoint, ""
    except Exception as error:
        text = "Cannot not rotate point. Detail: {}".format(error)
        return False, (0, 0), text

def transformPoint(point, matrix):
    x1 = point[0] * matrix[0][0] + point[1] * matrix[0][1] + matrix[0][2]
    y1 = point[0] * matrix[1][0] + point[1] * matrix[1][1] + matrix[1][2]
    return int(x1), int(y1)


def processAffineTransformImage(sourceImage, realRef, originalRef):
    try:
        matrix = getAffineTransFormMatrix(realRef, originalRef)
        res = cv.warpAffine(sourceImage.copy(), matrix, (sourceImage.shape[1], sourceImage.shape[0]))
        return res
    except:
        return None

def getAffineTransFormMatrix(refFrom, refTo):
    refPoints = np.float32([refFrom[0], refFrom[1], refFrom[2]])
    realPoints = np.float32([refTo[0], refTo[1], refTo[2]])

    matrix = cv.getAffineTransform(realPoints, refPoints)
    return matrix

def transformPointWithMatrix(point, matrix):
    x = point[0] * matrix[0][0] + point[1] * matrix[0][1] + matrix[0][2]
    y = point[0] * matrix[1][0] + point[1] * matrix[1][1] + matrix[1][2]
    return x, y

def processTransMoveImage(sourceImage, move_x=0, move_y=0):
    text = ""
    dst = None
    try:
        cols = sourceImage.shape[1]
        rows = sourceImage.shape[0]
        M = np.float32([[1, 0, move_x], [0, 1, move_y]])
        dst = cv.warpAffine(sourceImage, M, (cols, rows))
        return True, dst, text
    except Exception as error:
        text = "ERROR Translation Image. Please check paramter. Deatail: {}".format(error)
        return False, dst, text

def processTemplateMatching(sourceImage, template, minMatchingValue, multiMatchingFlag = False):
    image = sourceImage.copy()
    if image is None or len(image) == 0:
        return []
    resultList = []
    if len(image.shape) == 3:
        image = processCvtColor(image, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    w, h = template.shape[::-1]
    if multiMatchingFlag:
        loc = np.where(res >= minMatchingValue)
        for pt in zip(*loc[::-1]):
            resultList.append([pt[0], pt[1], pt[0] + w, pt[1] + h, 0])
        # apply non-maxima suppression to the rectangles
        resultList = non_max_suppression(np.array(resultList))
    else:
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if max_val >= minMatchingValue:
            top_left = max_loc
            suit = [top_left[0], top_left[1], top_left[0] + w, top_left[1] + h, max_val]
            resultList.append(suit)
    return resultList

def processCvtColor(sourceImage, code):
    try:
        res = cv.cvtColor(sourceImage.copy(), code)
        return res.copy()
    except:
        return None

def processDilate(sourceImage, kernelSizeX=3, kernelSizeY=3, iterations=1):
    source = sourceImage.copy()
    try:
        kernel = np.ones((kernelSizeX, kernelSizeY), np.uint8)
        dilateImage = cv.dilate(source, kernel, iterations=iterations)
        return dilateImage
    except Exception as error:
        messagebox.showwarning("ERROR Dilate image", "{}".format(error))


def processErode(sourceImage, kernelSizeX=3, kernelSizeY=3, iterations=1):
    source = sourceImage.copy()
    try:
        kernel = np.ones((kernelSizeX, kernelSizeY), np.uint8)
        erodeImage = cv.erode(source, kernel, iterations=iterations)
        return erodeImage.copy()
    except Exception as error:
        messagebox.showwarning("ERROR Erode image", "{}".format(error))

def flipVertical(sourceImage):
    res = processFlip(sourceImage.copy(), 0)
    return res.copy()

def flipHorizontal(sourceImage):
    res = processFlip(sourceImage.copy(), 1)
    return res.copy()

def flipBoth(sourceImage):
    res = processFlip(sourceImage.copy(), -1)
    return res.copy()

def processFlip(sourceImage, code):
    if code == 2:
        return sourceImage.copy()
    return cv.flip(sourceImage.copy(), code)

def processAdaptiveThreshold(sourceImage, maxValue, adaptiveMethod, thresholdType, blockSize, C):
    processImage = sourceImage.copy()
    if len(processImage.shape) == 3:
        try:
            processImage = processCvtColor(processImage, cv.COLOR_BGR2GRAY)
        except:
            processImage = processCvtColor(processImage, cv.COLOR_RGB2GRAY)

    _image = cv.adaptiveThreshold(processImage, maxValue=maxValue, adaptiveMethod=adaptiveMethod, thresholdType=thresholdType, blockSize=blockSize, C=C)
    return _image.copy()

def processBitwise_and(source1, source2, mask=None):
    if mask is not None:
        _mask = mask.copy()
        if len(_mask.shape) == 3:
            _mask = processCvtColor(_mask, cv.COLOR_BGR2GRAY)
    else:
        _mask = None
    ret = cv.bitwise_and(source1, source2, mask=_mask)
    return ret.copy()

def processBitwise_or(source1, source2, mask=None):
    if mask is not None:
        _mask = mask.copy()
        if len(_mask.shape) == 3:
            _mask = processCvtColor(_mask, cv.COLOR_BGR2GRAY)
    else:
        _mask = None
    ret = cv.bitwise_or(source1, source2, mask=_mask)
    return ret.copy()

def processBitwise_not(source1, source2, mask=None):
    if mask is not None:
        _mask = mask.copy()
        if len(_mask.shape) == 3:
            _mask = processCvtColor(_mask, cv.COLOR_BGR2GRAY)
    else:
        _mask = None

    ret = cv.bitwise_not(source1, source2, mask=_mask)
    return ret.copy()

def processBitwise_xor(source1, source2, mask=None):
    if mask is not None:
        _mask = mask.copy()
        if len(_mask.shape) == 3:
            _mask = processCvtColor(_mask, cv.COLOR_BGR2GRAY)
    else:
        _mask = None

    ret = cv.bitwise_xor(source1, source2, mask=_mask)
    return ret.copy()

def setBrightnessForPoint():
    return

def processBlur(image, ksize):
    _image = cv.blur(image, ksize=(ksize, ksize))
    return _image.copy()

def processMedianBlur(image, ksize):
    _image = cv.medianBlur(image.copy(), ksize=ksize)
    return _image.copy()

def processGaussianBlur(image, ksize, sigmaX):
    _image = cv.GaussianBlur(image.copy(), ksize=(ksize, ksize), sigmaX=sigmaX)
    return _image.copy()

def processBilateralFilter():
    return

def processMorphologyEx():
    return

def processClosingMorphology():
    return

def processOpeningMorphology():
    return

def processGradientMorphology():
    return

def processTopHatMorphology():
    return

def processBlackHatMorphology():
    return

def processDrawContours():
    return

def processDrawRectangle():
    return

def processInRange(sourceImage, lower, upper):
    mask = cv.inRange(sourceImage, lower, upper)
    return mask.copy()

def processCountNonzero(sourceImage):
    ret = cv.countNonZero(sourceImage)
    return ret

def processCombineInRange():
    return

def detectAndDraw():
    return

def processCanny(sourceImage, minThresh, maxThresh, apertureSize=3):
    processImage = sourceImage.copy()
    if len(processImage.shape) == 3:
        try:
            processImage = processCvtColor(processImage, cv.COLOR_BGR2GRAY)
        except:
            processImage = processCvtColor(processImage, cv.COLOR_RGB2GRAY)

    processImage = cv.Canny(processImage, threshold1=minThresh, threshold2=maxThresh, apertureSize=apertureSize)
    return processImage.copy()

def rotateImageWithAngle(sourceImage, angle, reshape=True):
    return ndimage.rotate(sourceImage, angle=angle, reshape=reshape)

def rotateImage90Clockwise(sourceImage):
    if sourceImage is not None:
        return  processRotateImage(sourceImage.copy(), cv.ROTATE_90_CLOCKWISE)
    else:
        return None

def rotateImage90CounterClockwise(sourceImage):
    return  processRotateImage(sourceImage.copy(), cv.ROTATE_90_COUNTERCLOCKWISE)

def rotateImage180Clockwise(sourceImage):
    return  processRotateImage(sourceImage, cv.ROTATE_180)

def processRotateImage(sourceImage, key):
    if key == -1:
        return sourceImage.copy()
    return cv.rotate(sourceImage.copy(), key)

def rotateImageWithStringKey(sourceImage, rotateStringKey):
    image = sourceImage.copy()
    if rotateStringKey == CameraRotate._90ClockWise.value:
        return rotateImage90Clockwise(image)
    elif rotateStringKey == CameraRotate._90CounterClockWise.value:
        return rotateImage90CounterClockwise(image)
    elif rotateStringKey == CameraRotate._180degrees.value:
        return rotateImage180Clockwise(image)
    else:
        return image

def rotateImage(sourceImage, angle, centerPoint):
    text = ""
    try:
        original_point = [0, 0]
        image = sourceImage.copy()
        if centerPoint[0] == -1:
            original_point[0] = int(image.shape[1] / 2)
        if centerPoint[1] == -1:
            original_point[1] = int(image.shape[0] / 2)

        angleMatrix = cv.getRotationMatrix2D(original_point, angle, 1)
        angleImage = cv.warpAffine(image, angleMatrix, (image.shape[1], image.shape[0]))

        return True, angleImage, text
    except Exception as error:
        text = "ERROR Cannot rotate image. Detail: {}".format(error)
        return False, sourceImage.copy(), text

def rotatePoint(origin, point, angle):
    try:
        """
        Rotate a point counterclockwise by a given angle around a given origin.
    
        The angle should be given in radians.
        """
        rad = angle * np.pi / 180
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(rad) * (px - ox) - math.sin(rad) * (py - oy)
        qy = oy + math.sin(rad) * (px - ox) + math.cos(rad) * (py - oy)
        return True, (int(qx), int(qy)), ""
    except Exception as error:
        text = "Cannot not rotate point. Detail: {}".format(error)
        return False, (0, 0), text

def getVarianceOfLaplacian(image):
    if len(image.shape) > 2:
        try:
            sourceImage =  processCvtColor(image, cv.COLOR_BGR2GRAY)
        except:
            sourceImage =  processCvtColor(image, cv.COLOR_RGB2GRAY)
    else:
        sourceImage = image.copy()

    return cv.Laplacian(sourceImage, cv.CV_64F).var()

def paint(sourceImage, paintArea, color):
    if sourceImage is None:
        return False, None, ""
    ret = sourceImage.copy()
    try:
        cv.rectangle(img=ret, pt1=(paintArea[0], paintArea[1]),pt2=(paintArea[2], paintArea[3]),
                     color=color, thickness=-1, lineType=cv.LINE_AA)
        return True, ret, ""
    except:
        return False, ret, " ERROR Cannot paint. Please check the image - color or area"

def getMinAreaRect(contour):
    try:
        minRect = cv.minAreaRect(contour)
        boxPoint = cv.boxPoints(minRect)
        box = np.int0(boxPoint)
        center = (int((box[0][0] + box[2][0]) / 2), int((box[0][1] + box[2][1]) / 2))
        ret = ((tuple(box[0]), tuple(box[1]), tuple(box[2]), tuple(box[3])), minRect[2], center)
        return True, ret, ""

    except Exception as error:
        text = "ERROR cannot get min area rectangle. Detail: {}".format(error)
        return False, None, text

def readBarcode(sourceImage):
    try:
        barcodes = pyzbar.decode(sourceImage)
        return True, barcodes, ""
    except Exception as error:
        text = "ERROR cannot read barcode. Detail: {}".format(error)
        return False, None, text

def readDataMatrixCode(sourceImage):
    try:
        dataMatrixCodes = pylibdmtx.decode(sourceImage)
        return True, dataMatrixCodes, ""
    except Exception as error:
        text = "ERROR cannot read barcode. Detail: {}".format(error)
        return False, None, text

def findChessBoardCorner(sourceImage, boardSize):
    text = ""
    if sourceImage is None:
        return False, None, "ERROR Find chess board corners. The input image is None"
    try:
        if len(sourceImage.shape) > 2:
            grayImage = processCvtColor(sourceImage, cv.COLOR_BGR2GRAY)
        else:
            grayImage = sourceImage.copy()

        ret, corners = cv.findChessboardCorners(grayImage, boardSize,None)

        if ret:
            return ret, corners, text
        else:
            return ret, corners, "ERROR Cannot find corners. Please check the parameter"
    except Exception as error:
        text = "ERROR Find chess board corners. Detail: {}".format(error)
        return False, None, text

def undistort(image):
    try:
        mtx = np.loadtxt('./CaliImage/cameraMatrix.txt')
        dist = np.loadtxt('./CaliImage/distortionCoefficient.txt')
        h, w = image.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        # undistort
        dst = cv.undistort(image, mtx, dist, None, newcameramtx)
        return dst
    except:
        return image

def processSplitChannel(sourceImage, channelId):
    if len(sourceImage.shape) < 3:
        return False, sourceImage, "Image has only one channel"

    if channelId + 1 > sourceImage.shape[2]:
        return False, sourceImage, "ERROR Split channel The channel ID is bigger than channels of Image"

    return  True, cv.split(sourceImage)[channelId], ""


def process_ocr_tesseract(sourceImage, lang='eng'):
    if len(sourceImage.shape) == 3:
        sourceImage = processCvtColor(sourceImage, code=cv.COLOR_BGR2RGB)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  # your path may be different
    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    try:
        text = pytesseract.image_to_string(sourceImage, lang=lang)
        return True, text
    except:
        return False, "ERROR Cannot read the image. Please check Tesseract library installation or image"

def change_brightness(sourceImage, type, value):
    matrix_change = np.ones(sourceImage.shape, dtype="uint8") * value
    change_brightness_image = None
    if type == "Lighter":
        change_brightness_image = cv.add(sourceImage, matrix_change)
    elif type == "Darker":
        change_brightness_image = cv.subtract(sourceImage, matrix_change)

    return change_brightness_image

def adjust_gamma(sourceImage, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
    return cv.LUT(sourceImage, table)

def get_intersect_from_2_lines(line1, line2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([line1[0],line1[1],line2[0],line2[1]])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return float('inf'), float('inf')
    return x/z, y/z

# from sklearn.linear_model import LinearRegression
def sk_learn_lr(x, y):
    """
    :param x: list of x value with shape (-1,1)
    :param y: list of y value with shape (-1,1)
    :return: a, b with y = a + b*x
    """
    try:
        regr = LinearRegression()
        regr.fit(x,y)
        return regr.intercept_, regr.coef_[0]
    except Exception as error:
        print(error)
        return None

def fit_line_contour_with_linear_regression(contours):
    list_coef = []
    for contour in contours:
        x_min = contour[:,:, 0].min()
        x_max = contour[:,:, 0].max()
        points = np.empty((0, 1, 2), dtype=contour.dtype)
        for x_value in range(x_min, x_max):
            x_points = contour[np.where(contour[:, :, 0] == x_value)[0]]
            if len(x_points) == 2:
                point = np.array(np.mean(x_points, axis=0, dtype=contour.dtype))
                points = np.concatenate([points, [point]])

        x = points[:, : , 0]
        y = points[:, :, 1]
        #
        # x = contour[:, : , 0]
        # y = contour[:, :, 1]
        list_coef.append(sk_learn_lr(x, y))
    return list_coef

def process_contours_approximation(contours, epsilon_percent=0.1, closed=True):
    """
    :param contours: contours, polygon we want to approximate
    :param epsilon_percent: the percent of maximum distance  between  the original curve  and it's approximation
    :param closed: if True, the approximated curve is closed otherwise, not
    :return:
    """
    list_approx = []
    try:
        for cnt in contours:
            epsilon = epsilon_percent * cv.arcLength(cnt, closed)
            list_approx.append(cv.approxPolyDP(cnt, epsilon, closed))
        # cv2.drawContours(img, [approx], 0, (0), 3)
        return True, list_approx, ""
    except Exception as error:
        return False, [], error

def convert_to_bgr_image(image):
    try:
        if len(image.shape) < 3:
            return cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        else:
            return image
    except Exception as error:
        print(error)
        return image

def process_contours_fit_line(contour, distance_type=cv.DIST_L2, param=0, reps=0.01, aeps=0.01):
     return cv.fitLine(contour, distance_type, param, reps, aeps) #[vx, vy, x, y]

def process_segmentation_yolov8(model_yolo, image, iou=0.25, conf=0.5, batch=4, workers=32, imgsz=640):
    try:
        results = model_yolo(image, iou=iou, conf=conf, batch=batch, workers=workers, imgsz=imgsz)
    except:
        print(traceback.format_exc())
        return False, None

    list_result = []  # ['class', 'conf', [box], [mask]]
    for detection in results[0]:
        # mask
        list_point_mask = []
        mask = detection.masks
        if mask is not None:
            for val in mask.xy[0].tolist():
                point = (round(val[0]), round(val[1]))
                list_point_mask.append(point)
        # box
        object_val = detection.boxes

        class_id = int(object_val.cls.tolist()[0])
        conf = float(object_val.conf.tolist()[0])
        box = [round(val_box, ) for val_box in object_val.xyxy.tolist()[0]]

        # name
        name = detection.names
        name_class = name[class_id]
        detect = [class_id, name_class, conf, box, list_point_mask]
        list_result.append(detect)
    return True, list_result