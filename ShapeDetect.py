import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)

def empty(a):
    pass

#Trackbar parameters
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",81,255,empty)
cv2.createTrackbar("Threshold2","Parameters",20,255,empty)
cv2.createTrackbar("Area","Parameters",3000,10000,empty)

def getContours(img,imgContour):

    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:   #cnt is points of our contours
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area","Parameters")
        areaMax = 10000  #bunu deneme için ekledim trackbardan ayarlama yapılabilir :))
        if area> areaMin and area < areaMax:
            #cv2.drawContours(imgContour, contours, -1, (255, 0, 255), 2)
            peri = cv2.arcLength(cnt,True)  #calculating contours length  ** True means that contour is closed
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) #approximate what type of shape is
            #approximation array will have a certain amount of points and based on these points
            #we can determine whether it's a square,triangle,etc.
            #print(len(approx))
            x,y,w,h = cv2.boundingRect(approx) #calculating bounding box parameters of approx array
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2) #drawing bounding box
            if len(approx) == 3:
                cv2.putText(imgContour, "Triangle" + str(len(approx)), (x + w + 10, y + 10), cv2.FONT_HERSHEY_COMPLEX,
                            0.7,(0, 255, 0), 1)
            elif len(approx) == 4:
                cv2.putText(imgContour, "Rectangle" + str(len(approx)), (x + w + 10, y + 10), cv2.FONT_HERSHEY_COMPLEX,
                            0.7,(0, 255, 0), 1)
            elif len(approx) > 4 and len(approx) < 11:
                cv2.putText(imgContour, "Shape " + str(len(approx)), (x + w + 10, y + 10), cv2.FONT_HERSHEY_COMPLEX,
                            0.7, (0, 255, 0), 1)
            else:
                pass
            # else:
            #     cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX,
            #                 0.7,
            #                 (0, 255, 0), 2)
            #     cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
            #                 (0, 255, 0), 2)

while True:
    succes, img = cap.read()
    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (11,11),1)
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny,kernel,iterations=1)

    getContours(imgDil,imgContour)
    cv2.imshow("Canny",imgCanny)
    cv2.imshow("contour",imgContour)
    cv2.imshow("Result",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break