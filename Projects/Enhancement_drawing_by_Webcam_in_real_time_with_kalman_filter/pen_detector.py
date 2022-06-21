"""
@Project: Enhancement drawing with a pen by Webcam in real time with the Kalman filter
@author: Mhd Ali Harmalani
@supervisor: Dr. Raouf Hamdan
"""

import cv2
import numpy as np

# create 6 trackbars that will control the lower and upper range of
# H,S and V channels. The Arguments are like this: Name of trackbar,
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",250,350)
def nothing(x):
    pass

cv2.createTrackbar("L - H", "Trackbars", 79, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 184, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 129, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 144, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

class PenDetector:
    def __init__(self):
        
        # Get the new values of the trackbar in real time as the user changes them
         l_h = cv2.getTrackbarPos("L - H", "Trackbars")
         l_s = cv2.getTrackbarPos("L - S", "Trackbars")
         l_v = cv2.getTrackbarPos("L - V", "Trackbars")
         u_h = cv2.getTrackbarPos("U - H", "Trackbars")
         u_s = cv2.getTrackbarPos("U - S", "Trackbars")
         u_v = cv2.getTrackbarPos("U - V", "Trackbars")
     
         # Set the lower and upper HSV range according to the value selected
         # by the trackbar
         # Create mask for color
         self.low_orange = np.array([l_h, l_s, l_v])
         self.high_orange = np.array([u_h, u_s, u_v])

    def detect(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
       # Get the new values of the trackbar in real time as the user changes them
        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
        # Set the lower and upper HSV range according to the value selected
        # by the trackbar
        self.low_orange = np.array([l_h, l_s, l_v])
        self.high_orange = np.array([u_h, u_s, u_v])
         
        # Create masks with color ranges
        mask = cv2.inRange(frame, self.low_orange, self.high_orange)
           
        # Find Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        box = (0, 0, 0, 0)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            area = w * h
            # print(area)
            if (area < 50):
               # print("small contour")
               break
            elif (area >= 50 and area <= 5000):
               # print("object contour")
               box = (x, y, x + w, y + h)
               break
            # else:
            #    # print("big contour")
            #    break

        return frame, mask, box
    