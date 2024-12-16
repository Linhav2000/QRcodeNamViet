import numpy as np
import cv2 as cv
import glob
import datetime
import os
import sys

class CameraCalibration:
    # termination criteria
    checkerboard = (9,7)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((checkerboard[1] * checkerboard[0], 3), np.float32)
    objp[:, :2] = np.mgrid[0:checkerboard[0], 0:checkerboard[1]].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('./CaliImage/standard.jpg')



    def __init__(self):
        return

    def calibrate(self):
        for fname in self.images:
            img = cv.imdecode(np.fromfile(fname, dtype=np.uint8), cv.IMREAD_COLOR)
            self.gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            # corners = cv.goodFeaturesToTrack(gray, 25, 0.01, 10)
            # ret, corners = cv.findChessboardCorners(gray, self.chekerboard, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FILTER_QUADS);
            ret, corners = cv.findChessboardCorners(self.gray, self.checkerboard, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
            # If found, add object points, image points (after refining them)
            if ret:
                self.objpoints.append(self.objp)
                corners2 = cv.cornerSubPix(self.gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgpoints.append(corners2)

                # Draw and display the corners
                img = cv.drawChessboardCorners(img,self.checkerboard, corners2, ret)
                cv.imshow('img', img)
                cv.waitKey(500)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
        np.savetxt('./CaliImage/cameraMatrix.txt', mtx)
        np.savetxt('./CaliImage/distortionCoefficient.txt', dist)
        # print(mtx)
        # print(dist)
        # Check the min mean_error

        # print(objpoints.shape[0])
        # print(len(objpoints))
        total_error = 0
        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv.projectPoints(self.objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(self.imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
            total_error += error
        mean_error = total_error / len(self.objpoints)
        print("total error: ", mean_error)

    def undistort(self, image):
        mtx = np.loadtxt('./CaliImage/cameraMatrix.txt')
        dist = np.loadtxt('./CaliImage/distortionCoefficient.txt')
        h, w = image.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        # undistort
        dst = cv.undistort(image, mtx, dist, None, newcameramtx)
        return dst
        # name = datetime.datetime.now().strftime("%H_%M_%S")
        # cv.imshow("result", dst)
        # cv.waitKey(500)
        # if not os.path.exists("./afterCali"):
        #     os.makedirs("./afterCali")
        # cv.imwrite("./afterCali/" + name + ".png", dst)

if __name__ == '__main__':
    cal = CameraCalibration()
    cal.calibrate()
    images = glob.glob('./CaliImage/*.jpg')
    for fname in images:
        adjustedImage = cv.imdecode(np.fromfile(fname, dtype=np.uint8), cv.IMREAD_COLOR)
        cal.undistort(adjustedImage)

    cv.waitKey(0)
    cv.destroyAllWindows()
