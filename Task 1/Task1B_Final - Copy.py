
import numpy as np
import cv2
import csv
import pandas as pd


def applyPerspectiveTransform(input_img):

    warped_img = None
    image = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(img_gray,(5,5),0)
    _,imthresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    newImg = cv2.resize(imthresh,(500,500))
    cv2.imshow("i",newImg)
    cv2.waitKey(0)
    
    contours,_= cv2.findContours(imthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    
    contours = sorted(contours,key=cv2.contourArea,reverse=True)
    """
    for contour,i in zip(contours,[120,255,205]):
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        draw = cv2.drawContours(input_img,[approx],0,(0,255,i),5)
        newImg = cv2.resize(draw,(500,500))
        cv2.imshow("draw",newImg)
    cv2.waitKey(0)
    """
    approx = cv2.approxPolyDP(contours[1],0.01*cv2.arcLength(contours[1],True),True)
    draw = cv2.drawContours(input_img,[approx],0,(0,120,0),5)
    newImg = cv2.resize(draw,(500,500))
    cv2.imshow("draw",newImg)
    a=approx.ravel()
    #X,Y,W,H = cv2.boundingRect(contours[0])
    L=len(a)
    tsum=[]
    cropset=[]
    
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
    print(t)

    #new= np.array([[X,Y],[X+W,Y],[X+W,Y+H],[X,Y+H]], dtype="int32")
    new=np.array([[0, 0],[1280,0],[1280,1280],[0,1280]],dtype="int32")

    Homo,status = cv2.findHomography(t,new)
    warped_img=cv2.warpPerspective(image,Homo,(1280,1280))

    newImg = cv2.resize(warped_img,(500,500))
    cv2.imshow("warped",newImg)
    cv2.waitKey(0)
    
    return warped_img

"""    
def detectMaze(warped_img):
    maze_array = []
    img_gray = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    _,thresh = cv2.threshold(blur, 0,255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)
    cv2.imshow("thresh",thresh)
   
    newImg = cv2.resize(thresh,(100, 100))

    w,h=11,11
    k=0
    vertical=[[0 for x in range(w)] for y in range(h)]
    horizontal=[[0 for x in range(w)] for y in range(h)]
    maze_array=[[0 for x in range(10)] for y in range(10)]
    for i in range(4,100,10):
        l=0
        for j in range(0,100,10):
            #print("i,j",newImg[i,j])
            if (newImg[i][j]==0) and (newImg[i+1][j]==0) and (newImg[i-1][j]==0):
                vertical[k][l]=0
            else :
                vertical[k][l]=1
            l=l+1
        vertical[k][l]=1
        k=k+1     
    k=0
    for i in range(5,100,10):
        l=0
        for j in range(0,100,10):
            if (newImg[j][i]==0) and (newImg[j+1][i]==0)and (newImg[j-1][i]==0):
                horizontal[l][k]=0
            else:
                horizontal[l][k]=1
            l=l+1
            horizontal[l][k]=1
        k=k+1    

    for i in range(0,10):
        for j in range(0,10):
            sum1=vertical[i][j]*(2**0)+vertical[i][j+1]*(2**2)+horizontal[i][j]*(2**1)+horizontal[i+1][j]*(2**3)
            maze_array[i][j]=sum1
            sum1=0

    #print("h\n\n",pd.DataFrame(horizontal).T)
    #print("v\n\n",pd.DataFrame(vertical))
    return maze_array

def writeToCsv(csv_file_path, maze_array):

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)
"""

#---------------------------------------------------------------------------------------------------------------------------------------------------
#input_img = cv2.imread("C:/Users/hp/Desktop/E-yantra_Comp/Completed E-Yantra_Tasks/E-yantra_Task_1/task_1b_detect_and_encode_maze/task_1b_detect_and_encode_maze/test_cases/a.png")
input_img = cv2.imread("C:/Users/hp/Desktop/E-yantra_Comp/Completed E-Yantra_Tasks/E-yantra_Task_1/task_1b_detect_and_encode_maze/task_1b_detect_and_encode_maze/test_cases/maze03.jpg")
cv2.imshow("input",input_img)
warped_img = applyPerspectiveTransform(input_img)

#maze_array = detectMaze(warped_img)
"""
print("Maze array:-\n",pd.DataFrame(maze_array))

csv_file_path="C:/Users/hp/Desktop/E-yantra_Comp/file.csv"
writeToCsv(csv_file_path, maze_array)
"""




