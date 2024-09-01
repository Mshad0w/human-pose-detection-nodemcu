import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose=mp.solutions.pose
import requests
import time
text_data = "hello buddy" 

#curl counter

cap = cv2.VideoCapture("rtsp://192.168.1.53:554/user=admin&password=admin&channel=1&stream=0.sdp")

#curl counter variables
counter=0
stage=None
#Claculate angle
def calculate_angle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)
    
    radians=np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
    
    if angle>180.0:
        angle=360-angle
        
    return angle
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            shoulder2 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist2 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
            angle2 = calculate_angle(shoulder2, elbow2, wrist2)
            # Visualize angle
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(angle2), 
                           tuple(np.multiply(elbow2, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            #curl counter logic
            if 75<=angle<=105 and 75<=angle2<=105:
                response = requests.post("http://192.168.1.20:8888/body", 
                data=text_data,headers={'Content-Type': 'text/plain'})
                #time.sleep(10)
                print(response.status_code)
                print(response.text)
				
            if angle < 30 and stage=="down":
                stage="up"
                counter+=1
                print(counter)
                       
        except:
            pass
        
        #render curl counter
        #setup status box
        cv2.rectangle(image,(0,0),(225,73),(245,177,16),-1)
        
        #Rep data
        cv2.putText(image,"Reps",(15,12),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
        cv2.putText(image,str(counter),(10,60),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
        
        #Stage data
        cv2.putText(image,"Stage",(65,12),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
        cv2.putText(image,stage,(60,60),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)   
             
         
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()