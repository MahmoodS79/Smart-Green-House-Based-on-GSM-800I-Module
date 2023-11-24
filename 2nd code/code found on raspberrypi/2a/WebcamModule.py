# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 14:53:43 2022

@author: SpeciAl One 1-2
"""


import cv2
 
cap = cv2.VideoCapture(0)
 
def getImg(display= False,size=[480,240]):
    _, img = cap.read()
    img = cv2.resize(img,(size[0],size[1]))
    if display:
        cv2.imshow('IMG',img)
    return img
 
if __name__ == '__main__':
    while True:
        img = getImg(True)