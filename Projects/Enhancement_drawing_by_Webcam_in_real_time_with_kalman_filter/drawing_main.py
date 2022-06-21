"""
@Project: Enhancement drawing with a pen by Webcam in real time with the Kalman filter
@author: Mhd Ali Harmalani
@supervisor: Dr. Raouf Hamdan
"""

import cv2
import numpy as np
from pen_detector import PenDetector
from kalmanfilter import KalmanFilter


cap = cv2.VideoCapture(0)
# Load detector
od = PenDetector()
# Load Kalman filter to predict the trajectory
kf = KalmanFilter()

accumulator_frame = None ## drawing frame
cxP,cyP=0,0
predicted = [0,0]
penS=0 #PenUp
Ukf = 1 # using kalman filter

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    fs = frame.shape
    if accumulator_frame is None:
        accumulator_frame = np.zeros(fs, dtype=np.uint8)
        
    frame, mask, orange_bbox = od.detect(frame)
    x, y, x2, y2 = orange_bbox
    cx = int((x + x2) / 2)
    cy = int(y)    #int((y + y2) / 2)
    
    if (cx == 0 and cy == 0):
        cx,cy = cxP,cyP
 
 
    cv2.circle(frame, (cx, cy), 20, (0, 0, 255), 4) ## detect object
    if (cx != 0 or cy != 0):
        if penS==1:
            cv2.circle(accumulator_frame, (cx, cy), 10, (0, 255, 255), -1)  ## with out kalman filter
        predicted = kf.predict(cxP, cyP)
        
 
    print("difference:",abs(cx-cxP),abs(cy-cyP))
    ## with kalman filter 
    if (penS == 1 and Ukf == 1):
        cv2.circle(accumulator_frame, (predicted[0], predicted[1]), 10, (0, 255, 255), -1)
   
    if (cx != 0 or cy != 0):    
        cxP,cyP = cx,cy 
        
    cv2.imshow("Mask", mask)
    cv2.imshow("Drawing", accumulator_frame)
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('c'):
        accumulator_frame = np.zeros(fs, dtype=np.uint8) # ClearAll
    elif key == ord('u'):
        penS = 0 # PenUp
    elif key == ord('d'):
        penS = 1 # Pendown
    elif key == ord('k'):
        Ukf = 1 # using kalman filter
    elif key == ord('n'):
        Ukf = 0 # normal drawing without kalman filter
        
        

cap.release()
cv2.destroyAllWindows()