import cv2
import numpy as np
import os

var={}
shapes = {}
Color=""


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

    img1=cv2.imread(img_file_path) #read image

    img=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)

    imgrey=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #convert BGR to Grayscale image
    #_,imthresh=cv2.threshold(imgrey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _,imthresh=cv2.threshold(imgrey,225,255,cv2.THRESH_BINARY)

    imhsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV) #convert BGR to HSV
    cv2.imshow("i",imhsv)
    cv2.waitKey(0)

    contours,_=cv2.findContours(imthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find contour

    for contour,i in zip(contours[1:],[120,255,205]):
        approx=cv2.approxPolyDP(contour,0.003*cv2.arcLength(contour,True),True)  #get vertices of contour
        draw = cv2.drawContours(img1,[approx],0,(0,255,i),5)
        newImg = cv2.resize(draw,(500,500))
        cv2.imshow("draw",newImg)
    
        #for coordinates of centroid x and y
        M = cv2.moments(contour)
        cX = int(M['m10']/M['m00'])   
        cY = int(M['m01']/M['m00'])
  
        #drawing contours
        m=cv2.drawContours(img,[approx],0,(0,0,0),2)

        #checking for triangle  
        if len(approx)==3:
            color=color_find(imhsv,cX,cY)
            area=cv2.contourArea(contour)
            val=[color,area,cX,cY]

            if "Triangle" not in shapes:
                shapes["Triangle"]=[val]
            else:
                shapes["Triangle"].extend([val])
        
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
                        val=[color,cX,cY]

                        if "Square" not in shapes:
                            shapes["Square"]=[val]
                        else:
                            shapes["Square"].extend([val])
                    
                    # for rhombus
                    else:
                        area=cv2.contourArea(contour)
                        color=color_find(imhsv,cX,cY)
                        val=[color,cX,cY]

                        if "Rhombus" not in shapes:
                            shapes["Rhombus"]=[val]
                        else:
                            shapes["Rhombus"].extend([val])
                    
                
                # for rectangle
                elif sub1<3 and sub2<3:
                    color=color_find(imhsv,cX,cY)
                    area=cv2.contourArea(contour)
                    val=[color,cX,cY]

                    if "Rectangle" not in shapes:
                        shapes["Rectangle"]=[val]
                    else:
                        shapes["Rectangle"].extend([val])
            
                # for parallelogram
                elif sub1<3 and sub2>3 :
                    area=cv2.contourArea(contour)
                    color=color_find(imhsv,cX,cY)
                    val=[color,cX,cY]

                    if "Parallelogram" not in shapes:
                        shapes["Parallelogram"]=[val]
                    else:
                        shapes["Parallelogram"].extend([val])
        
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
                    val=[color,cX,cY]

                    if "Trapezium" not in shapes:
                        shapes["Trapezium"]=[val]
                    else:
                        shapes["Trapezium"].extend([val])
                    
                else:
                    area=cv2.contourArea(contour)
                    color=color_find(imhsv,cX,cY)
                    val=[color,cX,cY]

                    if "Quadrilateral" not in shapes:
                        shapes["Quadrilateral"]=[val]
                    else:
                        shapes["Quadrilateral"].extend([val])
                
        # for polygon of side 5
        elif len(approx)==5:
            color=color_find(imhsv,cX,cY)
            area=cv2.contourArea(contour)
            val=[color,cX,cY]

            if "Pentagon" not in shapes:
                shapes["Pentagon"]=[val]
            else:
                shapes["Pentagon"].extend([val])

        # for polygon of side 6
        elif len(approx)== 6:
            area=cv2.contourArea(contour)
            color=color_find(imhsv,cX,cY)
            val=[color,cX,cY]
            
            if "Hexagon" not in shapes:
                shapes["Hexagon"]=[val]
            else:
                shapes["Hexagon"].extend([val])
    
        # for circle 
        else:
            area=cv2.contourArea(contour)
            color=color_find(imhsv,cX,cY)
            val=[color,area,cX,cY]

            if "Circle" not in shapes:
                shapes["Circle"]=val
                var["Circle"]=[val]
            else:
                shapes={}
                shapes=var
                shapes["Circle"].extend([val])
                for i, j in shapes.items():
                    shapes={i:sorted(j)}
    cv2.waitKey(0)
    return shapes

path="C:/Users/hp/Desktop/2.png"
shape=scan_image(path)
print(shape)
