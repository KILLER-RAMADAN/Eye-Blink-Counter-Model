import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot



reading_video=cv2.VideoCapture("man.mp4")# to play video..
detect_face=FaceMeshDetector(maxFaces=1)# to detect one face
dimintions_list=[22,23,24,26,110,157,158,159,160,161,130,243]# drawing dimintions of eyes
liveplot=LivePlot(600,500,[0,36])# live plot actions

ratio_list=[]
count_plink=0
counter=0
color=(255,0,255)# default color

while True:
    if reading_video.get(cv2.CAP_PROP_POS_FRAMES)==reading_video.get(cv2.CAP_PROP_FRAME_COUNT): #if video frames == count frame of video we will loop the video
        reading_video.set(cv2.CAP_PROP_POS_FRAMES,0)# looping video
    reading,img=reading_video.read()# reading video in frame  
    img,faces=detect_face.findFaceMesh(img,draw=False)# to find face in the video   
    if faces:# if found faces
        face=faces[0] # to choose only one face
        for di in dimintions_list:# loop in dimintions
            cv2.circle(img,face[di],5,color,cv2.FILLED)# to draw a circle around eye...
        up_area=face[159]# up area of face
        down_erea=face[23]# down area of face
        left_area=face[130]# left area of face
        right_area=face[243]# right area of face
        find_dist1, _=detect_face.findDistance(up_area,down_erea) # to find the distance petwean up area and down area  
        find_dist2, _=detect_face.findDistance(right_area,left_area)# to find the distance petwean right area and left area  
        full_dist=(find_dist1 / find_dist2)*100 # to remove dicemsal number
        print(full_dist)
        cv2.line(img,up_area,down_erea,(0,200,0),3)# upper and down line 
        cv2.line(img,left_area,right_area,(0,200,0),3)# left and right  line
        
        ratio_list.append(full_dist)# appending numbers in list
        if len(ratio_list)>4:# if the ratiolist==4 remove the first index
            ratio_list.pop(0)# remove the first index
        ratio_avg=sum(ratio_list)/len(ratio_list) # avg of ratio
        print(ratio_avg)
        
        if ratio_avg < 30 and counter==0: # if ratio < 30 and counter ==0 (counter+=1)..
            count_plink +=1 # add 1
            color=(0,200,0)
            counter=1 # add 1 to counter 
        if counter !=0:# if the counter !=0 add 1 to counter 
                counter+=1
                if counter>10: # reset counter if counter > 10...
                    counter=0
                    color=(250,0,250)
        
        cvzone.putTextRect(img, f"Plink Counter is :{count_plink}",(80,350),colorR=color)
        
        img_plot=liveplot.update(ratio_avg,color)# live plot of video
        
        img=cv2.resize(img,(600,500))# resize video frame
        images_marge=cvzone.stackImages([img,img_plot],2,1) # to mage live plot with the video
    else:
        img=cv2.resize(img,(600,500))# resize video frame
        images_marge=cvzone.stackImages([img,img],2,1)# to mage live plot with the video
        
    
    cv2.imshow("plinkink",images_marge)# to show video frame
    cv2.waitKey(1)# to control speed of video (delay)...