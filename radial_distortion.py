import numpy as np
import cv2 as cv
import glob

class Parameters:
    ret   = None
    mtx   = None
    dist  = None
    rvecs = None
    tvecs = None
    def __init__(self,ret, mtx, dist, rvecs, tvecs):
        self.ret   = ret
        self.mtx   = mtx
        self.dist  = dist
        self.rvecs = rvecs
        self.tvecs = tvecs

def calibrate(path_images,extension_images,size_chessboard): #'img/images/far/ path example
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, size_chessboard, 0.001)
    a,b=9,6
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob(path_images+'*.'+extension_images)
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(img, (a,b), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (a,b), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            #cv.drawChessboardCorners(img, (a,b), corners2, ret)
            #cv.imshow('img '+str(fname), cv.resize(img,(600,400)))
            #cv.waitKey(100)
    #cv.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return Parameters(ret,mtx,dist,rvecs,tvecs)

def radial_correction(path_images,extension_images,parameters):
    images = glob.glob(path_images+'*.'+extension_images)
    for fname in images:
        img = cv.imread(fname)
        h,  w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(parameters.mtx, parameters.dist, (w,h), 1, (w,h))
        # undistort
        dst = cv.undistort(img, parameters.mtx, parameters.dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite(fname, dst)

def radial_correction_beta(path_images,extension_images,parameters):
    images = glob.glob(path_images+'*.'+extension_images)
    for fname in images:
        img = cv.imread(fname)
        h,  w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(parameters.mtx, parameters.dist, (w,h), 1, (w,h))
        # undistort
        mapx, mapy = cv.initUndistortRectifyMap(parameters.mtx, parameters.dist, None, newcameramtx, (w,h), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite(fname, dst)