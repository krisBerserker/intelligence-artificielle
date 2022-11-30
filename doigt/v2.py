import os
from pathlib import Path
import sys
from datetime import datetime
import time
import threading
from threading import Thread
import numpy
import mediapipe as mp
import cv2

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
from cvzone.HandTrackingModule import  HandDetector

detector = HandDetector(maxHands=1, detectionCon=0.8)

class VideoStream:
   
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        """
        Continuously gets frames from CV2 VideoCapture and sets them as self.frame attribute
        """
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

   
    def stop_process(self):
        """
        Sets the self.stopped attribute as True and kills the VideoCapture stream read
        """
        self.stopped = True


def capture_image(frame, captures=0):
   
    cwd_path = os.getcwd()
    Path(cwd_path + '/images').mkdir(parents=False, exist_ok=True)

    now = datetime.now()
    name = "Finger " + now.strftime("%Y-%m-%d") + " at " + now.strftime("%H:%M:%S") + '-' + str(captures + 1) + '.jpg'
    path = 'images/' + name
    cv2.imwrite(path, frame)
    captures += 1
    print(name)
    return captures


def countFingers (frame):
    
    totalFingers = '0'
    
    hand = detector.findHands(frame , draw=False)
    if hand :
        lmlist = hand [0]
        if lmlist :
            fingerup = detector.fingersUp(lmlist)
            if (fingerup == [0,1,0,0,0]) or (fingerup == [0,0,0,1,0]) or (fingerup == [0,0,0,0,1]):
                totalFingers = '1'
            if fingerup == [0,0,1,0,0]:
                totalFingers = 'fuck '
            if fingerup == [1,0,0,0,0]:
                totalFingers = 'good'
                
            if fingerup == [0,1,1,0,0]:
                totalFingers = '2'
            if fingerup == [0,1,0,1,0]:
                totalFingers = '2'
            if fingerup == [0,1,0,0,1]:
                totalFingers = '2'
            if fingerup == [0,0,1,1,0]:
                totalFingers = '2'
            if fingerup == [0,0,0,1,1]:
                totalFingers = '2'
            if fingerup == [0,0,1,0,1]:
                totalFingers = '2'
            if fingerup == [1,1,0,0,0]:
                totalFingers = '2'
            if fingerup == [1,0,1,0,0]:
                totalFingers = '2'
            if fingerup == [1,0,0,1,0]:
                totalFingers = '2'
            if fingerup == [1,0,0,0,1]:
                totalFingers = '2'
                
                    
            if fingerup == [0,1,1,1,0]:
                totalFingers = '3'
            if fingerup == [0,1,1,0,1]:
                totalFingers = '3'
            if fingerup == [0,1,0,1,1]:
                totalFingers = '3'
            if fingerup == [0,0,1,1,1]:
                totalFingers = '3'
            
            if fingerup == [1,1,1,0,0]:
                totalFingers = '3'
            if fingerup == [1,1,0,1,0]:
                totalFingers = '3'
            if fingerup == [1,1,0,0,1]:
                totalFingers = '3'
            if fingerup == [1,0,1,0,1]:
                totalFingers = '3'
            if fingerup == [1,0,0,1,1]:
                totalFingers = '3'
            
                
            if fingerup == [0,1,1,1,1]:
                totalFingers = '4'
            if fingerup == [1,0,1,1,1]:
                totalFingers = '4'
            if fingerup == [1,1,0,1,1]:
                totalFingers = '4'
            if fingerup == [1,1,1,0,1]:
                totalFingers = '4'
            if fingerup == [1,1,1,1,0]:
                totalFingers = '4'
            
            if fingerup == [1,1,1,1,1]:
                totalFingers = '5'
   
    return totalFingers 

def put_text(frame: numpy.ndarray, totalfingers : str) -> numpy.ndarray:
       
    cv2.putText(frame, totalfingers, (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
    return frame



def finger_stream(source: int = 0):
    
    captures = 0  # Number of still image captures during view session

    video_stream = VideoStream(source).start()  # Starts reading the video stream in dedicated thread

    print("finger stream started")
    
#    berserker

    print("Active threads: {}".format(threading.activeCount()))
    
    # Main display loop
    print("\nPUSH c TO CAPTURE AN IMAGE. PUSH q TO VIEW VIDEO STREAM\n")
    
    counter = 1
    
    while True:
        
        # Quit condition:
        pressed_key = cv2.waitKey(1) & 0xFF
        if pressed_key == ord('q'):
            video_stream.stop_process()
            print("finger stream stopped\n")
            print("{} image(s) captured and saved to current directory".format(captures))
            break

        frame = video_stream.frame  # Grabs the most recent frame read by the VideoStream class

        totalfingers = countFingers(frame)
         
        frame = put_text(frame, totalfingers)
                
        print (totalfingers)
     
        cv2.imshow("finger counting", frame)


