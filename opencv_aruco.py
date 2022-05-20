from tkinter import N
import cv2
import cv2.aruco as aruco
import numpy as np

class Corner:
    x=0
    y=0
    def __init__(self,x,y):
        self.x=x
        self.y=y
class Tag:
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

def coords(bbox):
    tags_array=[]
    for i in range(0,len(bbox)):
        aux=[]
        for j in range(0,4):
            corner_aux=Corner(int(bbox[i][0][j][0]),int(bbox[i][0][j][1]))
            aux.append(corner_aux)
            #print(aux[len(aux)-1].x,aux[len(aux)-1].y)
        tag_aux=Tag(aux[0],aux[1],aux[2],aux[3])
        tags_array.append(tag_aux)
    return tags_array

img = cv2.imread('img/singlemarkerssource.png')
img = cv2.resize(img,(752,480))
bbox,ids = findaruco(img)
tags_array=coords(bbox)

# Green color in BGR
red  = (0,0,255)  
blue  = (255,0,0)  
green = (0,255,0)  
morado = (226,53,226)
#  Line thickness of 9 px
thickness = 2

for i in range(0,len(tags_array)):
    tag=tags_array[i]
    cv2.line(img, (tag.corner1.x,tag.corner1.y), (tag.corner2.x,tag.corner2.y), red, thickness)
    cv2.line(img, (tag.corner2.x,tag.corner2.y), (tag.corner3.x,tag.corner3.y), blue, thickness)
    cv2.line(img, (tag.corner3.x,tag.corner3.y), (tag.corner4.x,tag.corner4.y), green, thickness)
    cv2.line(img, (tag.corner4.x,tag.corner4.y), (tag.corner1.x,tag.corner1.y), morado, thickness)
cv2.imshow('test tags',img)
cv2.waitKey(10000)