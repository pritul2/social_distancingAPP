from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
import image_processing as ip

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    store_centroid = []
    store_bbox = []
    for detection in detections:
        class_label = (detection[0]).decode('utf-8')
        confidence_ratio = detection[1]
        if class_label=='person' and confidence_ratio>0.25:
            x, y, w, h = detection[2][0],detection[2][1],detection[2][2],detection[2][3]
            xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))
            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)
            
            centroids = ip.obtain_centroid(xmin,ymin,xmax,ymax)
            store_centroid.append(centroids)
            store_bbox.append([[xmin,ymin],[xmax,ymax]])
            img = ip.draw_circle(centroids,img)
            
    img = ip.draw_line(img,store_centroid,store_bbox)
    return img


netMain = None
metaMain = None
altNames = None


def YOLO():

    global metaMain, netMain, altNames
    configPath = "./cfg/yolov4-tiny.cfg"
    weightPath = "yolov4-tiny.weights"
    metaPath = "./cfg/coco.data"

    netMain = darknet.load_net_custom(configPath.encode("ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    metaMain = darknet.load_meta(metaPath.encode("ascii"))
    
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("/Users/prituldave/projects/yolov4/darknet/social_distancing_dataset/data1.mp4")
    cap.set(3, 512)
    cap.set(4, 512)
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
        (darknet.network_width(netMain), darknet.network_height(netMain)))
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    while True:
        prev_time = time.time()
        ret, frame_read = cap.read()
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
        image = cvDrawBoxes(detections, frame_resized)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print("FPS ",1/(time.time()-prev_time))
        out.write(image)
        '''
        cv2.imshow('Demo', image)
        cv2.waitKey(3)
        '''
    cap.release()
    out.release()

if __name__ == "__main__":
    YOLO()
