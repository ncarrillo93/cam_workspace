from tkinter import N
import cv2
import cv2.aruco as aruco
import numpy as np
import math

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


# Main:

img = cv2.imread('img/proy4.jpeg')
img = cv2.resize(img,(1024,720))
bbox,ids = findaruco(img)
tags_array=coords(bbox)
print(img.shape[0])



'''
pts_src y pts_dst son matrices de puntos numpy
en las imágenes de origen y destino. necesitamos al menos
puntos correspondientes.
'''
tag=tags_array[0]
print(' [',tag.corner1.x,tag.corner1.y,'] ',
      ' [',tag.corner2.x,tag.corner2.y,'] ',
      ' [',tag.corner3.x,tag.corner3.y,'] ',
      ' [',tag.corner4.x,tag.corner4.y,'] ')
pts_src=np.array([[tag.corner1.x , tag.corner1.y],
                  [2*tag.corner2.x - tag.corner1.x , 2*tag.corner2.y -tag.corner1.y],
                  [2*tag.corner3.x - tag.corner1.x , 2*tag.corner3.y-tag.corner1.y],
                  [2*tag.corner4.x - tag.corner1.x , 2*tag.corner4.y-tag.corner1.y]])

dist =int(math.sqrt(pow(tag.corner2.x-tag.corner1.x,2)+pow(tag.corner2.y-tag.corner1.y,2)))
dist1=int(math.sqrt(pow(tag.corner3.x-tag.corner2.x,2)+pow(tag.corner3.y-tag.corner2.y,2)))
dist2=int(math.sqrt(pow(tag.corner4.x-tag.corner3.x,2)+pow(tag.corner4.y-tag.corner3.y,2)))
dist3=int(math.sqrt(pow(tag.corner4.x-tag.corner1.x,2)+pow(tag.corner4.y-tag.corner1.y,2)))
pts_dst=np.array([[0,0],
                  [0,2*dist],
                  [2*dist1,2*dist2],
                  [2*dist3,0]])

h, status = cv2.findHomography(pts_src, pts_dst)
'''
La homografía calculada se puede utilizar para deformar
la imagen de origen al destino. El tamaño es el
tamaño (ancho, alto) de im_dst
'''
im_dst = cv2.warpPerspective(img, h, (im_dst.shape[1],im_dst.shape[0])  )

#  Line thickness of 2 px
# Green color in BGR
red  = (0,0,255)  
blue  = (255,0,0)  
green = (0,255,0)  
morado = (226,53,226)

thickness = 2
cv2.line(img,pts_src[0] , pts_src[1], red, thickness)
cv2.line(img,pts_src[1] , pts_src[2], blue, thickness)
cv2.line(img,pts_src[2] , pts_src[3], green, thickness)
cv2.line(img,pts_src[3] , pts_src[0], morado, thickness)


cv2.imshow('test tags',img)
cv2.waitKey(10000) ##milisegundos