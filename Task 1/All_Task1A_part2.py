import cv2
import numpy as np

frame_details={}

def process_video(vid, frame_list):
    
    global frame_details
    
    for i in frame_list:
        vid.set(cv2.CAP_PROP_POS_FRAMES, i-1)
        _, frame = vid.read()
        
        original = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        lower = np.array([0,100, 0], dtype="uint8")
        upper = np.array([10, 255,255], dtype="uint8")
        mask = cv2.inRange(frame, lower, upper)
        #cv2.imshow("mask",mask)
        #cv2.waitKey(0)
        kernel = np.ones((12,12),np.uint8)
        mor=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                           
        contours = cv2.findContours(mor, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        result = cv2.bitwise_and(original,original,mask=mor)
        #cv2.imshow("result",result)
        #cv2.waitKey(0)


        for contour in contours[0]:
            approx=cv2.approxPolyDP(contour,0.001*cv2.arcLength(contour,True),True) 
    
            M = cv2.moments(contour)
            m=cv2.drawContours(result,[approx],0,(255,255,255),2)
        
        
            cX = int(M['m10']/M['m00']) 
            cY = int(M['m01']/M['m00'])
        
        frame_details.update({i:[cX,cY]})
        
    return frame_details

        
##############################################################################################################################################3    

#vid= cv2.VideoCapture('C:/Users/hp/Desktop/E-yantra_Comp/Completed E-Yantra_Tasks/E-yantra_Task_1/task_1a_explore_opencv/task_1a_explore_opencv/Task_1A_Part2/Videos/ballmotion.m4v')
vid= cv2.VideoCapture('F:/Robotics/E-yantra_Comp/Completed E-Yantra_Tasks/E-yantra_Task_1/task_1a_explore_opencv/task_1a_explore_opencv/Task_1A_Part2/Videos/ballmotionWhite.m4v')
frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
print('Frame count:', frame_count)

frame_list=[55, 110, 165, 220, 275, 330, 385]
#frame_list=[69,138,207]
frame_details=process_video(vid, frame_list)
print(frame_details)


