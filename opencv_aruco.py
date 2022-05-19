from tkinter import N
import cv2
import cv2.aruco as aruco
import numpy as np

class corner:
    x=0
    y=0
    def __init__(self,x,y):
        self.x=x
        self.y=y
class tag:
    corner1=None
    corner2=None
    corner3=None
    corner4=None
    def __init__(self,corner1,corner2,corner3,corner4):
        self.corner1=corner1
        self.corner2=corner2
        self.corner3=corner3
        self.corner4=corner4
    
def findaruco(img,marker_size=6,total_markers=250,draw=True):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key =getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    bbox,ids,_=aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)    
    if draw:
        aruco.drawDetectedMarkers(img,bbox)
    return bbox,ids
    
#def coords(bbox):
#    for i in 
img = cv2.imread('singlemarkerssource.png')
img = cv2.resize(img,(752,480))
bbox,ids = findaruco(img)
aux=[]
for i in range(0,len(bbox)):
    aux.append([bbox[i][0][0],bbox[i][0][1],bbox[i][0][2],bbox[i][0][3]])
    print(i,'  ',bbox[i][0][0],bbox[i][0][1],bbox[i][0][2],bbox[i][0][3])
# Green color in BGR
color = (0,0,255)  
# Line thickness of 9 px
#thickness = 9
#image = cv2.line(img, (432,349), (500,349), color, thickness)
#cv2.imshow('test tags',img)
#cv2.waitKey(0)