import numpy as np
import cv2
import csv


def applyPerspectiveTransform(input_img):

    warped_img = None
    blurimg = cv2.GaussianBlur(input_img,(5,5),0)
    _,imthresh = cv2.threshold(blurimg,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    contours,_= cv2.findContours(imthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours,key=cv2.contourArea,reverse=True)[:2]
    
    approx = cv2.approxPolyDP(contours[1],0.1*cv2.arcLength(contours[1],True),True)
    draw = cv2.drawContours(input_img,[approx],0,(0,0,0),5)
    cv2.imshow("contour",draw)
    print("\napp",approx)
    print("\napp0",approx[0])
    a=approx.ravel()
    print("a",a)

    X,Y,W,H = cv2.boundingRect(contours[0])
    L=len(a)
    
    if (a[0]+a[1]) > (a[L-2]+a[L-1]):
        new= np.array([[X+W,Y],[X+W,Y+H],[X,Y+H],[X, Y]], dtype = "float32")
    else:
        new= np.array([[X, Y],[X+W,Y],[X+W,Y+H],[X,Y+H]], dtype = "float32")
    print("n",new)

    Homo,status = cv2.findHomography(approx,new)
    warped_img=cv2.warpPerspective(input_img,Homo,(W,H))
    #cv2.imshow("warrapped",warped_img)

    return warped_img

       
def detectMaze(warped_image):
    
    maze_array = []
    blur = cv2.GaussianBlur(warped_image, (5,5), 0)
    _,thresh = cv2.threshold(blur, 0,255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)
    cv2.imshow("thresh",thresh)

    shape=warped_img.shape
    cell_l=shape[0]//10
    cell_b=shape[1]//10
    print(shape)
    
    # Obtain horizontal lines mask
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cell_l,1))
    horizontal_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
    horizontal_mask = cv2.dilate(horizontal_mask, horizontal_kernel, iterations=18)

    # Obtain vertical lines mask
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,cell_b))
    vertical_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
    vertical_mask= cv2.dilate(vertical_mask, vertical_kernel, iterations=18)

    # Bitwise-and masks together
    result = 255 - cv2.bitwise_or(vertical_mask, horizontal_mask)

    # Fill individual grid holes
    contours = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(result, (x, y), (x + w, y + h), 255, -1)

    cv2.imshow('result', result)
    cv2.waitKey()


    
    return maze_array
    


#---------------------------------------------------------------------------------------------------------------------------------------------------
input_img = cv2.imread("C:/Users/hp/Desktop/E-yantra_Comp/task_1b_detect_and_encode_maze/task_1b_detect_and_encode_maze/test_cases/maze03.jpg",0)
warped_img = applyPerspectiveTransform(input_img)

detectMaze(warped_img)
