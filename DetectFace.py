import numpy as np
import cv2 as cv

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

img = cv.imread('tree.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
if len(faces) == 0:
    print("No faces found")
else:
    print("Number or faces:", faces.shape[0])
    
    for (x,y,w,h) in faces:
        cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
    cv.rectangle(img, ((0,img.shape[0] -25)),(270, img.shape[0]), (255,255,255), -1)
    cv.putText(img, "Number of faces detected: " + str(faces.shape[0]), (0,img.shape[0] -10), cv.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
    
    cv.imshow('Image with faces',img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    

