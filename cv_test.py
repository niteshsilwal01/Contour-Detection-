import cv2 as cv 
import numpy as np 
import stack_images

def empty(a):
    pass

cv.namedWindow('Params')
cv.resizeWindow('Params',640,90)
cv.createTrackbar('Threshold1','Params',109,255,empty)
cv.createTrackbar('Threshold2','Params',103,255,empty)

#create function to generate contours
def getContours(img,imgContour):
    
    contours,hierarchy =cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 100:
            cv.drawContours(imgContour,cnt,-1,(0,255,0),5)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv.boundingRect(approx) 
            cv.rectangle(imgContour,(x ,y ),(x+w ,y+h ),(255,0,0),4)

            text ='Area :' + str(int(area))
            cv.putText(imgContour,text,
                    (x+w+20,y+20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)

diluted_frame = list()
#Function to calculate mean frames 
def mean_of_frames(frames :list) -> list:
        mean_frames = np.mean(frames, axis=0).astype(dtype=np.uint8)
        return mean_frames 

#img = cv.imread('E:/OpenCV tutorial/assets/Opencv/Resources/lena.png')

#url = 'http://192.168.10.65:8080/shot.jpg?'
'''while True:
    imgUrl = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgUrl.read()),dtype=np.uint8)
    img = cv.imdecode(imgNp,-1)'''

cap = cv.VideoCapture('Resources\potato in belt.mp4')
while True:
    bool,img = cap.read()
    imgContour = img.copy()

    imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (7,7),1)

    thres1 = cv.getTrackbarPos('Threshold1','Params')
    thres2 = cv.getTrackbarPos('Threshold2','Params')
    imgCanny = cv.Canny(imgBlur,thres1,thres2)

    kernel = np.ones((5,5))
    imgDil = cv.dilate(imgCanny,kernel,iterations = 1)
                
    diluted_frame.append(imgDil)
    if len(diluted_frame)==10:
        mean_frame = mean_of_frames(diluted_frame)
        diluted_frame = list()

    getContours(mean_frame ,imgContour)
    images= stack_images.stackImages([[img,imgCanny,imgContour]],0.8)
    cv.namedWindow('Results',cv.WINDOW_NORMAL)
    cv.resizeWindow('Results',800,800)
    cv.imshow('Results',images)

    if cv.waitKey(10) & 0xFF == ord('c'):
        break