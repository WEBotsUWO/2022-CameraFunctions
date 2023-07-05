#pyrealsense libraries
import cv2
import pyrealsense2
from realsense_depth import *

#picture imports
from PIL import Image
from resizeimage import resizeimage


import time
from datetime import datetime

import random

class Camera:

    def show_distance(event, x, y, args, params):
        global point
        point = (x, y)

    #method outputs a raw picture and a resized picture 512x512 to local pics folder
    #takes in tuple of x,y to find distance 
    #returns distance in mm
    def takePicture(x,y):
        # Initialize Camera Intel Realsense
        # dc = DepthCamera()
        point=(x,y)
        # Create mouse event
        cv2.namedWindow("Color frame")
        cv2.setMouseCallback("Color frame", Camera.show_distance)

        ret, depth_frame, color_frame = dc.get_frame()

         #Show distance for a specific point
        #draws circle where looking at based on x,y given
        cv2.circle(color_frame, point, 4, (0, 0, 255))

        #calculates distance from point
        distance = depth_frame[point[1], point[0]]
        
        #displays the distance on the image
        cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        cv2.imshow("depth frame", depth_frame)
        cv2.imshow("Color frame", color_frame)

        now=datetime.now()
        date_time = now.strftime("%H_%M_%S"+ str(random.randint(0, 1000)))

        #write raw image to pics folder
        cv2.imwrite('pics/Frame'+date_time+'.jpg', color_frame)
                
        #crop image given dimensions
        # with open('pics/Frame'+date_time+'.jpg', 'r+b') as f:
        #     with Image.open(f) as image:
        #         cover = resizeimage.resize_cover(image, [512, 512])
        #         cover.save('pics/Frame'+date_time+'_CROPPED.jpg', image.format)

        return distance

    #returns distance from specific point
    def getDistanceFromPoint(x,y):
        # Initialize Camera Intel Realsense
        # dc = DepthCamera()
        point=(x,y)
        # Create mouse event
        cv2.namedWindow("Color frame")
        cv2.setMouseCallback("Color frame", Camera.show_distance)

        ret, depth_frame, color_frame = dc.get_frame()

         #Show distance for a specific point
        #draws circle where looking at based on x,y given
        cv2.circle(color_frame, point, 4, (0, 0, 255))

        #calculates distance from point
        distance = depth_frame[point[1], point[0]]

        #displays the distance on the image
        cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        cv2.imshow("depth frame", depth_frame)
        cv2.imshow("Color frame", color_frame)

        print(distance)
        return distance

    #given 4 points of a square, returns average distance of object in square
    def takeAverageDistance(x1,y1,x2,y2,x3,y3,x4,y4):

        #top left, top right, bottom left, bototm right, middle
        topLeft= (x1+ ((x2-x1)/4),y1+((y3-y1)/4))
        topRight=( x1 + ((x2-x1)*3/4),y1+ ((y3-y1)/4))
        bottomLeft=(x1+ ((x2-x1)/4), y1+((y3-y1)*3/4))
        bottomRight=(x3+ ((x4-x3)*3/4), y1+ ((y3-y1)*3/4))
        middle = (x1+((x2-x1)/2), y1+((y3-y1)/2))
        points=[topLeft,topRight,bottomLeft,bottomRight,middle]
        totalDistance=0
        totalAdded=0

        #go thru each 5 points in the sqaure
        for x in range(5):
            #take 5 pictures with same coordinates to ensure we get at least 1 non zero
            for y in range(5):
                distance =Camera.takePicture( int(points[x][0]), int(points[x][1]) )

                #check for non zero value
                if distance !=0 :
                    totalAdded+=1
                    totalDistance+=distance
        #return average distance
        if totalAdded==0:
            return "error in distance calculation"
        return totalDistance/totalAdded

#must initialize camera globally before running its methods
dc = DepthCamera()
print(Camera.takeAverageDistance(0,0,640,0,0,480,640,480))
# print(Camera.takePicture(int(25.0),int(25.0)))
