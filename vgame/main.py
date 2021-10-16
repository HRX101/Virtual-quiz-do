import cv2 
import csv
from cvzone import *
from cv2 import data
import cvzone
import time

from cvzone.HandTrackingModule import HandDetector
cap=cv2.VideoCapture(0)#for open the camera
cap.set(3,1280)#set the interface
cap.set(4,728)
class MCQ():#oop in python make class MCQ
    def __init__(self,data):
        self.question=data[0]
        self.choice1=data[1]
        self.choice2=data[2]
        self.choice3=data[3]
        self.choice4=data[4]
        self.answer=int(data[5])
        
        self.userans=None
    def update(self,cursor,bboxs):
        for x,bbox in enumerate(bboxs):
            x1,y1,x2,y2=bbox
            if x1<=cursor[0]<x2 and y1<cursor[1]<y2 :
                self.userans=x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)
pathcsv="mcqs.csv"
with open(pathcsv,newline="\n") as f:
    reader=csv.reader(f)
    datall=list(reader)[1:]
mcqlist=[]
for q in datall:
    mcqlist.append(MCQ(q))
qn=0
qtotal=len(datall)
detector=HandDetector(detectionCon=0.8)

while True:#infinity loop untill false 
    success,img=cap.read()#reading 
    img=cv2.flip(img,1)#for flip the camera
    hands,img=detector.findHands(img,flipType=False)

    if qn<qtotal:
        mcq=mcqlist[qn]
        img,bbox=cvzone.putTextRect(img,mcq.question,[100,100],2,2,offset=50,border=5)
        img,bbox1=cvzone.putTextRect(img,mcq.choice1,[100,250],2,2,offset=50,border=5)
        img,bbox2=cvzone.putTextRect(img,mcq.choice2,[400,250],2,2,offset=50,border=5)
        img,bbox3=cvzone.putTextRect(img,mcq.choice3,[100,400],2,2,offset=50,border=5)
        img,bbox4=cvzone.putTextRect(img,mcq.choice4,[400,400],2,2,offset=50,border=5)
        if hands:
            lmlist=hands[0]['lmList']
            cursor=lmlist[8]
            length,info,img=detector.findDistance(lmlist[8],lmlist[12],img)
            if length<60:
                mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
                if mcq.userans is not None:
                    time.sleep(0.3)
                    qn+=1
    else:
        score=0
        for mcq in mcqlist:
            if mcq.answer==mcq.userans:
                score+=1
            

        score=round((score/qtotal)*100,2)

        img,_=cvzone.putTextRect(img,'quiz end',[250,300],3,3,offset=16,border=20)
        img,_=cvzone.putTextRect(img,f'your score is {score}%',[700,300],3,3,offset=16,border=20)#to show the score 
    barvalue=150+(950//qtotal)*qn
    cv2.rectangle(img,(150,600),(barvalue,650),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(150,600),(1100,650),(255,0,255),5)
    img,_=cvzone.putTextRect(img,f'{round((qn/qtotal)*100)}%',[1138,635],2,2,offset=16,border=10)             
    
    cv2.imshow("img",img)#showing 
    cv2.waitKey(1)#stop the program 

