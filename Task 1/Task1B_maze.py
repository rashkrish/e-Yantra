import numpy as np
import cv2
import csv
import pandas as pd


def applyPerspectiveTransform(input_img):

    warped_img = None
    img_gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)  #convert BGR to gray scale image
    blur = cv2.GaussianBlur(img_gray,(5,5),0)  #apply gaussianblur filter
    _,imthresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) #after appling gaussianblur filter on gray image, here we convert it to binary image

    contours,_= cv2.findContours(imthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find contours
    
    contours = sorted(contours,key=cv2.contourArea,reverse=True)[:2] # sorted contours and to get two largest contours
    
    approx = cv2.approxPolyDP(contours[1],0.1*cv2.arcLength(contours[1],True),True) #to get coordinates of second largest contour
    draw = cv2.drawContours(input_img,[approx],0,(0,0,0),5) #draw contour
    
    
    X,Y,W,H = cv2.boundingRect(contours[0])
    tsum=[]
    cropset=[]

    #to set the vertices of contour in order
    for i in range(0,4):
        su=0
        for j in range(0,2):
            su=su+approx[i,0,j]
        tsum.append(su)
    o=np.argmin(tsum)
    p=0
    if o!=0:
        for i in range(0,4):
            if(o+i<4):
                
                cropset.append(approx[o+i,0])
                
            else:
                cropset.append(approx[p,0])
                p=p+1
               
    else:
        cropset=approx
    t=np.array(cropset,dtype="int32")

    new= np.array([[X, Y],[X+W,Y],[X+W,Y+H],[X,Y+H]], dtype="int32")

    Homo,status = cv2.findHomography(t,new)  #transform the perspective of image
    warped_img=cv2.warpPerspective(input_img,Homo,(W,H)) #wrap Homography transformed image in input one
    
    return warped_img


def detectMaze(warped_img):

    maze_array = []
    img_gray = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY) # BGR to gray scaled image
    blur = cv2.GaussianBlur(img_gray, (5,5), 0) #apply gaussianblur filter
    _,thresh = cv2.threshold(blur, 0,255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)#after appling gaussianblur filter on gray image, here we convert it to binary image
   
    newImg = cv2.resize(thresh,(100, 100)) # resize the image

    #get matrix value for vertical and horizontal lines
    w,h=11,11
    k=0
    vertical=[[0 for x in range(w)] for y in range(h)]
    horizontal=[[0 for x in range(w)] for y in range(h)]
    maze_array=[[0 for x in range(10)] for y in range(10)]

    # check and input values in vertical according to the vertical line pixel in image
    for i in range(5,100,10):
        l=0
        for j in range(0,100,10):
            if (newImg[i][j]==0) and (newImg[i+1][j]==0) and (newImg[i-1][j]==0) and (newImg[i][j-1]==0) and (newImg[i][j+1]==0):
                vertical[k][l]=0
            else :
                vertical[k][l]=1
            l=l+1
        vertical[k][l]=1
        k=k+1

    # check and input values in horizontal according to the horizontal line pixel in image
    k=0
    for i in range(5,100,10):
        l=0
        for j in range(0,100,10):
            if (newImg[j][i]==0) and (newImg[j+1][i]==0)and (newImg[j-1][i]==0) and (newImg[j][i-1]==0) and (newImg[j][i+1]==0):
                horizontal[l][k]=0
            else:
                horizontal[l][k]=1
            l=l+1
            horizontal[l][k]=1
        k=k+1    

    # calculate values for a cell in the image
    for i in range(0,10):
        for j in range(0,10):
            sum1=vertical[i][j]*(2**0)+vertical[i][j+1]*(2**2)+horizontal[i][j]*(2**1)+horizontal[i+1][j]*(2**3)
            maze_array[i][j]=sum1
            sum1=0

    return maze_array

def writeToCsv(csv_file_path, maze_array):

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)
		
#---------------------------------------------------------------------------------------------------------------------------------------------------
#input_img = cv2.imread("C:/Users/hp/Desktop/E-yantra_Comp/Completed E-Yantra_Tasks/E-yantra_Task_1/task_1b_detect_and_encode_maze/task_1b_detect_and_encode_maze/test_cases/a.png")
input_img = cv2.imread("C:/Users/hp/Desktop/E-yantra_Comp/Completed E-Yantra_Tasks/E-yantra_Task_1/task_1b_detect_and_encode_maze/task_1b_detect_and_encode_maze/test_cases/maze02.jpg")
cv2.imshow("o",input_img)
warped_img = applyPerspectiveTransform(input_img)

maze_array = detectMaze(warped_img)

print("Maze array:-\n",pd.DataFrame(maze_array))

csv_file_path="C:/Users/hp/Desktop/E-yantra_Comp/file.csv"
writeToCsv(csv_file_path, maze_array)






