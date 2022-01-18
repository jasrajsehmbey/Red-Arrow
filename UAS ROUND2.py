import cv2 as cv
import numpy as np
import math
cap = cv.VideoCapture(0) #captures video feed in our main default camera
print(cap.isOpened())
cap.set(3,400)   #size of video capture
cap.set(4,250)
#kernel value
kernel = np.ones((7,7))
############################################################################
#track bar for hsv
def empty(a): #defined empty value to pass for trackbar
    pass
#to find slope of line
def gradient(pt1,pt2):
    if pt2[0]-pt1[0] != 0:
       return((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))
    else:
       return(90)
#############################################################################
cv.namedWindow("trackbar")
   #for defining the range of red color
cv.resizeWindow("trackbar", 640, 240)
cv.createTrackbar("hue min", "trackbar", 0, 179, empty)
cv.createTrackbar("hue max", "trackbar", 13, 179, empty)
cv.createTrackbar("sat min", "trackbar", 111, 255, empty)
cv.createTrackbar("sat max", "trackbar", 223, 255, empty)
cv.createTrackbar("val min", "trackbar", 167, 255, empty)
cv.createTrackbar("val max", "trackbar", 255, 255, empty)
#main loop
while True:
    ret,frame = cap.read()  #reads the frames from video capture
    hsvform = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #converting rgb to hsv
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(frame, 100, 100)  # getting canny of frame with 100 tolerance
    blur = cv.GaussianBlur(gray,(7,7),1)
    #getting position of trackbar
    hmin = cv.getTrackbarPos("hue min", "trackbar")
    hmax = cv.getTrackbarPos("hue max", "trackbar")
    smin = cv.getTrackbarPos("sat min", "trackbar")
    smax = cv.getTrackbarPos("sat max", "trackbar")
    vmin = cv.getTrackbarPos("val min", "trackbar")
    vmax = cv.getTrackbarPos("val max", "trackbar")
    lower = np.array([hmin,smin,vmin]) #array of all lower values of hsv
    upper = np.array([hmax,smax,vmax]) #array of all upper values of hsv
    mask1 = cv.inRange(hsvform, lower, upper) #black and white mask(shows white in range of lower and upper values of hsvform)
    mask2 = cv.inRange(hsvform,np.array([160,100,20]),np.array([179,255,255])) #another values to mask only red color
    mask = mask1 + mask2 #combines values to mask for mask 1 and mask 2
    mask = cv.erode(mask,kernel) #to remove all small un needed noises
    redpart = cv.bitwise_and(frame,frame,mask=mask) #detects common pixels of white and colorize it with original
    cannyred = cv.Canny(redpart,50,150,apertureSize=3)
    contours= cv.findContours(mask.copy(),cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2] #determines external outlines of the objects
    minLineLength = 100
    maxLineGap = 10
    lines = cv.HoughLinesP(cannyred, 0.5, np.pi / 180, 35, minLineLength, maxLineGap) #detects objects with straight lines only(approx)
    for cnt in contours: #give all small objects of outlines
        if lines is not None: #when a straight line is detected
           # for line in lines:
             #   x1,y1,x2,y2 = line[0] #index value 0 directly gives position of x1,y1,x2,x2 in line
                #cv.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2) #joins and draws inital and final coordinates in yellow
            area = cv.contourArea(cnt) #to get areas of objects
            peri = cv.arcLength(cnt, True) #to get length of perimeter of object

            approx = cv.approxPolyDP(cnt, 0.025 * peri, True) #fnc which calculates and approximates polygonal curve
            if area > 1400: #to remove detection of unneeded small objects
                #cv.drawContours(frame, approx, -1, (255, 0, 0), 2)
                objcorner = len(approx) #all corner points of objects
                x, y, w, h = cv.boundingRect(approx) #give boundary points of rect

                if objcorner == 7:  #when corner points are 7 it prints as a red arrow
                     rect = cv.minAreaRect(approx)  # gives bounding rect with minimum area and rotates with arrow
                     #print(rect)
                     box = cv.boxPoints(rect)  # boxpoints converts 2d structure to 4 rect points
                     box = np.int0(box)  # converting 4 rect points to integer type
                     objectType = "Red Arrow"
                     cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #shows green box around detected object
                     #cv.drawContours(frame,[box],0,(0,255,0),2) #shows green box around detected object by joining int points
                     #line
                     rows,cols = frame.shape[:2]
                     [vx,vy,a,b] = cv.fitLine(cnt,cv.DIST_L2,0,0.01,0.01) #fits a line between the arrow
                     lefty = int((-a*vy/vx)+b)
                     righty = int(((cols-a)*vy/vx)+b)
                     pts1 = [cols-1,righty] #position of one coordinate of line
                     pts2 = [0,lefty] #position of second coordinate of line
                     pts3 = [300,-5000]
                     pts4 = [300,5000]
                     #cv.line(frame, (pts1), (pts2),(0,255,0),2) #joining 2 points to form a line
                     #cv.line(frame, (pts3), (pts4), (0, 255, 0), 2)
                     '''
                     if pts2[1]>= pts1[1]:
                         m1 = gradient(pts1, pts2) #slope of line 1
                     else:
                         m1 = gradient(pts2, pts1)
                     m2 = gradient(pts3, pts4) #slope of line 2
                     '''
                     finalAngleR = math.atan2(pts2[1]-pts1[1],pts2[0] - pts1[0]) #formula to calculate angle between 2 lines
                     a2 = round(math.degrees(finalAngleR)) #rounding off angle in degrees
                     a3 = a2 - 90
                     if a3<0:
                        a3 = 360 + a3
                     finalAngleD = str(a3)
                     angle = rect[2] #in minAreaect() function the 2nd position of tuple gives the angle of rect with horizontal

                     if rect[1][0] < rect[1][1]: #when width of rect < height of rect
                         newangle = round(angle)
                     else:
                         newangle = 90 + round(angle) #to get angle with vertical
                     new = str(newangle)
                else:  #when corner points are not 7 then nothing is printed
                     objectType = ""
                     new = ""
                     finalAngleD =""
                rotAngle = "Angle: " + new
                cv.putText(frame, objectType, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2)#prints red arrow above object
                cv.putText(frame, finalAngleD, (x-40, y+90), cv.FONT_HERSHEY_SIMPLEX, 0.8, (128, 0, 128), 3) #prints angle in degrees
    cv.imshow('frame', frame)
    #cv.imshow('mask', mask)
    #cv.imshow('redpart',redpart)
    #cv.imshow('canny red',cannyred)

    if cv.waitKey(1) & 0xFF == ord('q'): #waitkey(1) is frame rate 1 fpms, when pressed q program exits
        break

cap.release()
cv.destroyAllWindows()
