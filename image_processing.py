#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:40:46 2020

@author: prituldave
"""
import cv2
import numpy as np

THRESH = 40.0

def l2_norm(pts1,pts2):
    pts1 = np.array(pts1)
    pts2 = np.array(pts2)
    return np.linalg.norm(pts1-pts2)

def obtain_centroid(x1,y1,x2,y2):
    return((x1+x2)//2,(y1+y2)//2)

def draw_circle(centroid,frame):
    temp = frame.copy()
    temp = cv2.circle(temp,(centroid[0],centroid[1]),3,(0,69,255),-1)
    return temp

def draw_line(img,li,bbox):
    global THRESH
    store_danger = []
    for i in range(len(li)):
        for j in range(i,len(li)):
            eu_dist = round(l2_norm(li[i],li[j]),2)
            if eu_dist<=THRESH and eu_dist !=0:
                color = (255,0,0)
                store_danger.append(bbox[i])
                store_danger.append(bbox[j])
            else:
                color = (0,255,0)
            img = cv2.line(img,li[i],li[j],color,1,cv2.LINE_AA)
            if eu_dist != 0:
                img = cv2.putText(img,str(eu_dist),((li[i][0]+li[j][0])//2,(li[i][1]+li[j][1])//2),cv2.FONT_HERSHEY_SIMPLEX,0.6,color,2)
    for i in range(len(bbox)):
        if bbox[i] in store_danger:
            img = cv2.rectangle(img,tuple(bbox[i][0]),tuple(bbox[i][1]),(255,0,0),1)
        else:
            img = cv2.rectangle(img,tuple(bbox[i][0]),tuple(bbox[i][1]),(0,255,0),1)
    return img