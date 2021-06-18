import cv2
import numpy as np

t2 = cv2.imread('/home/fece/PycharmProjects/DEU_ROV/photos/image102.jpg')
thresh = cv2.cvtColor(t2, cv2.COLOR_BGR2GRAY) #converting gray scale
median = cv2.medianBlur(thresh,5)  #blur operation 
cv2.imshow('median',median)
sub = cv2.subtract(median, thresh) #subtraction operation on images for the clearest image
cv2.imshow('sub',sub)

contours,hierarchy = cv2.findContours(sub,2,1) #finding contours in sub image
cnt = contours
big_contour = []
max = 0
for i in cnt:
   area = cv2.contourArea(i)  # finding the contour having biggest area
   if area <= max:
       continue
   max = area
   big_contour = i

#big_contour[n][0] coordinate of nth point of contour ([0] for x , [1] for y)
len = len(big_contour) # length of contour array
print(len)

###################################
# Finding center point of contour #
l = int(len/2) #1/2 of the contour length (to calculate y coordinate of the ellipse)
k = int(len/4) #1/4 of the contour length (to calculate x coordinate of the ellipse)
m = len -k #3/4 of the contour length (to calculate x coordinate of the ellipse)


center= int((big_contour[m][0][0] - big_contour[k][0][0])/2),int((big_contour[l][0][1] - big_contour[0][0][1])/2)
print("Calculated center point =",center) #calculating middle of the found coordinates

if center[0] < 35 and center[1] < 35:   #if contour points too close each other we assume that there is no ellipse
   print("middle point of the contour:",center)
   print("Ellipse not found")
   cv2.imshow("Image",t2)
else:
   center2 = big_contour[k][0][0] + center[0] ,  big_contour[0][0][1] +  center[1] #k[0] + middle[0] to calculate x coordinate, 0[0] + middle[1] to calculate y coordinate
   final = cv2.drawContours(t2, big_contour, -1, (0,0,255), 2)  #drawing contour
   #print(final[0][0]) #bgr value of the coordinate
   final = cv2.circle(final,center2,3,(0,255,255),3)   #drawing center point of contour we found
   cv2.imshow('final', final)

##################################


cv2.waitKey()
