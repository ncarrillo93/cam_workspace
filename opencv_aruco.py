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
def get_homography(img_src,tags_array):
    tag=tags_array[0]
    pts_src=np.array([[tag.corner1.x , tag.corner1.y],
                      [tag.corner2.x , tag.corner2.y],
                      [tag.corner3.x , tag.corner3.y],
                      [tag.corner4.x , tag.corner4.y]])
    dist =int(math.sqrt(pow(tag.corner2.x-tag.corner1.x,2)+pow(tag.corner2.y-tag.corner1.y,2)))
    pts_dst=np.array([[0,0],[dist,0],[dist,dist],[0,dist]])
    h, status = cv2.findHomography(pts_src, pts_dst)
    '''
    red, blue, green, morado  = (0,0,255), (255,0,0), (0,255,0), (226,53,226)
    thickness = 2
    cv2.line(img_src,pts_src[0] , pts_src[1], red, thickness)
    cv2.line(img_src,pts_src[1] , pts_src[2], blue, thickness)
    cv2.line(img_src,pts_src[2] , pts_src[3], green, thickness)
    cv2.line(img_src,pts_src[3] , pts_src[0], morado, thickness)
    '''
    return cv2.warpPerspective(img_src, h, (img_dst.shape[1] , img_dst.shape[0])  )# Main:
def get_rois(tag,frame,offset):
    frame, offset=100,20
    dist =int(math.sqrt(pow(tag.corner2.x-tag.corner1.x,2)+pow(tag.corner2.y-tag.corner1.y,2))) + offset
    x1,x2,x3,x4 = frame, dist-frame, dist+frame, (2*dist)-frame
    y1,y2,y3,y4 = frame, dist-frame, dist+frame, (2*dist)-frame
    roi1=np.array([[x3,y1],[x4,y1],[x4,y2],[x3,y2]])
    roi2=np.array([[x3,y3],[x4,y3],[x4,y4],[x3,y4]])
    roi3=np.array([[x1,y3],[x2,y3],[x2,y4],[x1,y4]])
    return roi1,roi2,roi3
def print_roi_test(roi,colors,time,thickness):
    for i in roi:
        cv2.line(img_out,i[0],i[1], colors[0], thickness)
        cv2.line(img_out,i[1],i[2], colors[1], thickness)
        cv2.line(img_out,i[2],i[3], colors[2], thickness)
        cv2.line(img_out,i[3],i[0], colors[3], thickness)
    cv2.imshow('Warped Source Image',cv2.resize(img_out,(1024,720)))
    cv2.waitKey(time)

# MAIN:

#import image and generate copy
img_src = cv2.imread('img/proy4.jpeg')
img_dst=img_src.copy()

##get aruco corners 
bbox,ids = findaruco(img_src)
tags_array=coords(bbox)
##get image after homography
img_out=get_homography(img_src,tags_array)

#get colors ROI
bbox,ids = findaruco(img_out)
tags_array=coords(bbox)
roi1,roi2,roi3=get_rois(tag=tags_array[0],frame=100,offset=20)

##print roi's in images
print_roi_test(roi=[roi1,roi2,roi3],
               colors=[(0,0,255), (255,0,0), (0,255,0), (226,53,226)],
               time=10000,
               thickness=2)