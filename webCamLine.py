import cv2
import numpy as np
import mediapipe as mp
import serial

#Serial takes these two parameters: serial device and baudrate
#ser = serial.Serial('COM4', 9600)

circles = np.zeros((4,2), np.int16)
counter = 0

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def mousePoints(event,x,y,flags,params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        circles[counter] = x,y
        counter = counter + 1
        print(circles)

# Capture video from the default camera

cap = cv2.VideoCapture("media/Video/BabeVideo2.mp4")
#cap = cv2.imread("media/Video/BabyFull2.jpg")

height, width = 600, 800
circles = [[75,106],[718,106],[718,540],[75,540]]

pTime = 0

while True:

    # Read a frame from the video
    
    success, frame = cap.read()
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 2, (255, 0, 0), cv2.FILLED)

            if ((circles[0][0] > cx) | (circles[1][0] < cx)  | (circles[2][1] < cy)):
                cv2.rectangle(frame,(0,int(height)),(180,int(height)-20),(0,0,255),-1)
                cv2.putText(frame, "Baby Going Out...!", (12, int(height)-5), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)
                #ser.write('T'.encode()) 


            # else:
            #     #cv2.rectangle(frame,(0,int(height)),(130,int(height)-20),(0,168,24),-1)
            #     #cv2.putText(frame, "Baby is Safe", (12, int(height)-5), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)
            #     ser.write('F'.encode()) 
                
    #------------------------------------------------------------------------------------------

    if counter == 4:
        
        # Define the color and thickness of the line
        color = (0, 0, 255)
        thickness = 2

        for i in range(1,4):
            # Draw the line on the image
            img = cv2.line(frame, circles[i-1], circles[i], color, thickness)

            if i == 3:
                img = cv2.line(frame, circles[0], circles[i], color, thickness)

    for x in range(0,4):
        cv2.circle(frame,(circles[x][0],circles[x][1]),4,(0,200,255),cv2.FILLED)

    pt1 = width/2 - 150
    pt2 = width/2 + 120
    
    position = ((int) (width/2 - 225/2), (int) (26))

    cv2.rectangle(frame,(0,0),(int(width),40),(255,255,255),-1)

    cv2.putText(
                frame, #numpy array on which text is written
                "SMART BABY SHEET", #text
                position, #position at which writing has to start
                cv2.FONT_HERSHEY_COMPLEX_SMALL, #font family
                0.9, #font size
                (56, 37, 7), #font color
                1) #font stroke

    # Show the frame
    cv2.imshow("Webcam", frame)

    cv2.setMouseCallback("Webcam", mousePoints)
    cv2.waitKey(1)
