#====================== Importing Libraries ==========================
import socket

from time import sleep

import cv2

import numpy as np

import Action

cap = cv2.VideoCapture(0)

# cap = cv2.VideoCapture('http://192.168.1.100:81/stream')

# cap = cv2.VideoCapture('http://192.168.1.3:8080/video')
# cap = cv2.VideoCapture('http://192.168.30.53:8080/video')


fr=0

def getImg(display = False , size = [480 , 240]) :
    
    _,img = cap.read()
    
    # img = cv2.resize(img , (size[0] , size[1]))
     
    if display :
        
        cv2.imshow('IMG' , img)
        # (h, w) = img.shape[:2]
        # (cX, cY) = (w // 2, h // 2)
        # M = cv2.getRotationMatrix2D((cX, cY), -90, 1.0)
        # rotated = cv2.warpAffine(img, M, (w, h))
        # cv2.imshow('IMG' , img)
    return img

#=======================  Declerating Functions =======================

curveList = []

avgVal = 10

def getlanecurve (img , display = 2):
    
    imgCopy = img.copy()
    
    imgResult = img.copy()
    
    imgThres = Action.thresholding(img)
 
    hT, wT, c = img.shape
     
    points = Action.valTracbars()
    
    imgWarp = Action.warpImg(imgThres , points , wT, hT)
 
    imgwarpPoints = Action.drawPoints(imgCopy , points)
    
    midllePoint , imgHist = Action.getHistogram(imgThres , display = True , minPer = 0.5 , region = 4)
    
    curveAveragePoint , imgHist = Action.getHistogram(imgThres , display = True , minPer = 0.9)
    
    curveRaw = curveAveragePoint - midllePoint
    
    curveList.append(curveRaw)
    
    if len(curveList) > avgVal :
        
        curveList.pop(0)
        
    curve = int(sum(curveList)/len(curveList))
    
    if display != 0 :
        
        imgInvWarp = Action.warpImg(imgWarp , points , wT , hT , inv = True)
        
        imgInvWarp = cv2.cvtColor(imgInvWarp , cv2.COLOR_GRAY2BGR)
        
        imgInvWarp[0:hT // 3 , 0:wT] = 0 , 0 , 0
        
        imgLaneColor = np.zeros_like(img)
        
        imgLaneColor[:] = 0 , 255 , 0
        
        imgLaneColor = cv2.bitwise_and(imgInvWarp , imgLaneColor)
        
        imgResult = cv2.addWeighted(imgResult , 1 , imgLaneColor , 1 , 0)
        
        midY = 450
        
        cv2.putText(imgResult , str(curve) , (wT // 2 - 80, 85) , cv2.FONT_HERSHEY_COMPLEX, 2 , (255,0,255),3)
        
        cv2.line(imgResult, (wT//2 , midY) , (wT // 2 + (curve*3),midY),(255,0,255),5)
        
        cv2.line(imgResult, ((wT // 2 + (curve *3)),midY-25),(wT // 2 + (curve * 3), midY + 25), (0,255,0),5)
        
        for x in range(-30,30):
            
            w = wT // 20
            
            cv2.line(imgResult , (w * x + int(curve // 50) , midY - 10),
                    (w * x + int(curve // 50) , midY + 10) , (0 , 0 , 255 ) , 2)
    
    if display == 2 :
        
        imgStacked = Action.stackImages(0.7 , ([img , imgwarpPoints, imgWarp],
                                               [imgHist, imgLaneColor , imgResult]))
        
        cv2.imshow('ImageStack', imgStacked)
    
    elif display == 1 :
        
        cv2.imshow('Result' , imgResult)
        
    curve = curve / 100
    
    if curve > 1 : curve == 1
    
    if curve < -1 : curve == -1
        
    cv2.imshow('imgThres' , imgThres)
    
    cv2.imshow('imgWarp' , imgWarp)
    
    cv2.imshow('imgwarpPoints' , imgwarpPoints)
    
    cv2.imshow('imgHist' , imgHist)
    
    return curve




    
#========================= Main Function ==========================

if __name__ == '__main__' :
    
    
    # host = '169.254.159.208'
    # port = 5000  # initiate port no above 1024

    # server_socket = socket.socket()  # get instance
    #     # look closely. The bind() function takes tuple as argument
    # server_socket.bind((host, port))  # bind host address and port together

    #     # configure how many client the server can listen simultaneously
    # server_socket.listen(2)
    # conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: " + str(address))


    # s = socket.socket()         # Create a socket object
    # host = '192.168.30.121'    # esp32 ip
    # port = 12345                # Reserve a port for your service.
    # s.connect((host, port))
        

    intialTrackBarVals = [ 101 , 0 , 0 , 100 ]
    
    Action.initializeTrackbars(intialTrackBarVals)
    
    curveList = []
    
    x='{"a":0,"d":0,"w":0,"s":0,"+":0,"-":0,"de+":0,"de-":0}'
    oldcurve=0
    while True :
        
        img = getImg(True)

        if img is not None:
            fr+=1
        if fr%1!=0:
           continue        
        curve = getlanecurve(img , display = 1)
        
        if curve > oldcurve :
            # print(curve)
            oldcurve=curve
        
        if curve > 0.01 :
            
            data = "R"
            x='{"a":0,"d":1,"w":0,"s":0,"+":0,"-":0,"de+":0,"de-":0}'
               
        
        elif curve < -0.01 :
            
            data = "L"
            x='{"a":1,"d":0,"w":0,"s":0,"+":0,"-":0,"de+":0,"de-":0}'
          
        # else:
        #     data = "F"
        #     x='{"a":0,"d":0,"w":0,"s":1,"+":0,"-":0,"de+":0,"de-":0}'

            # x='{"a":0,"d":0,"w":0,"s":0,"+":0,"-":0,"de+":0,"de-":0}'
        
            
            
        #
        ######################################################################

        # x='{"a":1,"d":0,"w":0,"s":0,"+":0,"-":0}'
        # msg = str.encode(x, 'utf-8')
      
        # try:

        # for ii in range(1):
            # x='{"a":0,"d":0,"w":0,"s":1,"+":0,"-":0,"de+":0,"de-":0}'
            # s.send(msg)
            # data1 = s.recv(1024)
             
        # s.send(msg)
        # data1 = s.recv(1024)
        # print(msg)
        # print(data)
                
        # cv2.imshow('Original' , img)
            
        cv2.waitKey(1)


    
# conn.close()  # close the connection
# print("conn closed")