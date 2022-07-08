import numpy as np
import cv2 as cv
import glob

<<<<<<< HEAD

=======
>>>>>>> b1dfc7e94ae5aaea4d537a56a649ff424c0a1bef
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
a,b=6,9
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
<<<<<<< HEAD
images = glob.glob('img/images/far/*.jpg')
print(images)
=======

images = glob.glob('img/images/*.jpg')

>>>>>>> b1dfc7e94ae5aaea4d537a56a649ff424c0a1bef
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (a,b), None)
    # If found, add object points, image points (after refining them)
<<<<<<< HEAD
    #print(ret)
=======
>>>>>>> b1dfc7e94ae5aaea4d537a56a649ff424c0a1bef
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (a,b), (-1,-1), criteria)
        imgpoints.append(corners)

print(np.size(objpoints),np.size(imgpoints))

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv.imread('img/chessboard/patron_1.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('img/calibresult.png', dst)


# undistort
mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('img/calibresult.png', dst)
