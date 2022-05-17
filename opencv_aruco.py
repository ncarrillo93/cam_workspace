import cv2
import cv2.aruco as aruco
import numpy as np

def findaruco(img,marker_size=6,total_markers=250,draw=True):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key =getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    bbox,ids,_=aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    print(ids)
    if draw:
        aruco.drawMarkers(img,bbox)
    return bbox,ids

#from pupil_apriltags as apriltags
img = cv2.imread('singlemarkerssource.png')
img = cv2.resize(img,(1920,1080))
bbox,ids = findaruco(img)
cv2.imshow('test tags',img)
cv2.waitKey(0)