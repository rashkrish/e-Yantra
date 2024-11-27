import cv2
import numpy as np

# function to get value of color for shapes
def color_find(imhsv,cY,cX):
    h,s,v=imhsv[cX,cY]
    if h>=58 and h<=62:
        Color='green'
    elif h>=118 and h<=122:
        Color='blue'
    elif h>=0 and h<=2:
        Color='red'
    return Color

# function to calculate distance
def dist(a,b):
    return ((a[0][0]-b[0][0])**2+(a[0][1]-b[0][1])**2)**0.5


def scan_image(img_file_path):

    global shapes
    shapes={}

    img=cv2.imread(img_file_path) #read image
    imgrey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert BGR to Grayscale image
    _,imthresh=cv2.threshold(imgrey,225,255,cv2.THRESH_BINARY) #convert BGR to Binary image
    imhsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert BGR to HSV

    contours,_=cv2.findContours(imthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find contour

    for contour in contours[1:]:
        approx=cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)  #get vertices of contour
    
        #for coordinates of centroid x and y
        M = cv2.moments(contour)
        cX = int(M['m10']/M['m00'])   
        cY = int(M['m01']/M['m00'])   
  
        #drawing contours
        m=cv2.drawContours(img,[approx],0,(0,0,0),2)
        cv2.imshow("aaa",m)
        cv2.waitKey(0)
        
        #checking for triangle  
        if len(approx)==3:
            color=color_find(imhsv,cX,cY)
            area=cv2.contourArea(contour)
            val=[color,area,cX,cY]
            shapes["Triangle"]=(val)
        
        #checking for shapes with 4 vertices
        elif len(approx)==4:
        
            # calculate the distance between vertices
            d1=dist(approx[0],approx[1])
            d2=dist(approx[1],approx[2])
            d3=dist(approx[2],approx[3])
            d4=dist(approx[3],approx[0])
        
            # ratio of lengths
            lenratio1=d1/d3
            lenratio2=d2/d4
        

            if lenratio1>=0.95 and lenratio1<=1.05 and lenratio2>=0.95 and lenratio2<=1.05:
            
                # ratio of adjacent sides
                lenratio3=d1/d2
            
                # for approximation to have perpendicular line
                sub1=abs(approx[1,0,1]-approx[0,0,1])
                sub2=abs(approx[3,0,0]-approx[0,0,0]) 
            
                # checking shape is either square or rhombus
                if lenratio3>=0.95 and lenratio3<=1.05:
                
                    # for square
                    if sub1<3 and sub2<3:
                        area=cv2.contourArea(contour)
                        color=color_find(imhsv,cX,cY)
                        val=[color,area,cX,cY]
                        shapes["Square"]=val
                        continue
                    
                    # for rhombus
                    else:
                        area=cv2.contourArea(contour)
                        color=color_find(imhsv,cX,cY)
                        val=[color,area,cX,cY]
                        shapes["Rhombus"]=val
                        continue
                    
                
                # for rectangle
                elif sub1<3 and sub2<3:
                    color=color_find(imhsv,cX,cY)
                    area=cv2.contourArea(contour)
                    val=[color,area,cX,cY]
                    shapes["Rectangle"]=(val)
                    continue
            
                # for parallelogram
                elif sub1<3 and sub2>3 :
                    area=cv2.contourArea(contour)
                    color=color_find(imhsv,cX,cY)
                    val=[color,area,cX,cY]
                    shapes["Parallelogram"]=val
                    continue
        
            # the opposite sides are not equal in trapezium and quandrilateral
            else:
                sub3=abs(approx[1,0,1]-approx[0,0,1])
                sub4=abs(approx[3,0,1]-approx[2,0,1])
                sub5=abs(approx[3,0,0]-approx[0,0,0])
                sub6=abs(approx[2,0,0]-approx[1,0,0])
                an1=abs(sub3-sub4)
                an2=abs(sub5-sub6)
            
                # for trapezium 2 sides are parallel
                if an1<3 or an2<3:
                    area=cv2.contourArea(contour)
                    color=color_find(imhsv,cX,cY)
                    val=[color,area,cX,cY]
                    shapes["Trapeium"]=val
                    continue
                else:
                    area=cv2.contourArea(contour)
                    color=color_find(imhsv,cX,cY)
                    val=[color,area,cX,cY]
                    shapes["Quadrilateral"]=val
                
        # for polygon of side 5
        elif len(approx)==5:
            color=color_find(imhsv,cX,cY)
            area=cv2.contourArea(contour)
            val=[color,area,cX,cY]
            shapes["Pentagon"]=val

        # for polygon of side 6
        elif len(approx)== 6:
            area=cv2.contourArea(contour)
            color=color_find(imhsv,cX,cY)
            val=[color,area,cX,cY]
            shapes["Hexagon"]=val
    
        # for circle 
        else:
            area=cv2.contourArea(contour)
            color=color_find(imhsv,cX,cY)
            val=[color,area,cX,cY]
            shapes["Circle"]=val

    shapes= dict( sorted(shapes.items(), key=lambda x: x[1][1],reverse=True))
    
    return shapes

path="F:\Robotics\E-yantra_Comp/Completed E-Yantra_Tasks/E-yantra_Task_1/task_1a_explore_opencv/task_1a_explore_opencv/Task_1A_Part1/Test_Images/Test2.png"
shape=scan_image(path)
print(shape)
