import cv2
import HandtrackingVirtualMouse as htm
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
import pygame
import time

wCam, hCam = 1280, 720
cam=cv2.VideoCapture(0)
cam.set(3,wCam)
cam.set(4,hCam)

pTime = 0

pygame.mixer.init()
pygame.mixer.set_num_channels(17)
effect1=pygame.mixer.Sound('./piano_sound/key01.mp3')
effect2=pygame.mixer.Sound('./piano_sound/key02.mp3')
effect3=pygame.mixer.Sound('./piano_sound/key03.mp3')
effect4=pygame.mixer.Sound('./piano_sound/key04.mp3')
effect5=pygame.mixer.Sound('./piano_sound/key05.mp3')
effect6=pygame.mixer.Sound('./piano_sound/key06.mp3')
effect7=pygame.mixer.Sound('./piano_sound/key07.mp3')
effect8=pygame.mixer.Sound('./piano_sound/key08.mp3')
effect9=pygame.mixer.Sound('./piano_sound/key09.mp3')
effect10=pygame.mixer.Sound('./piano_sound/key10.mp3')
effect11=pygame.mixer.Sound('./piano_sound/key11.mp3')
effect12=pygame.mixer.Sound('./piano_sound/key12.mp3')
effect13=pygame.mixer.Sound('./piano_sound/key13.mp3')
effect14=pygame.mixer.Sound('./piano_sound/key14.mp3')
effect15=pygame.mixer.Sound('./piano_sound/key15.mp3')
effect16=pygame.mixer.Sound('./piano_sound/key16.mp3')
effect17=pygame.mixer.Sound('./piano_sound/key17.mp3')



detector = htm.HandDetector(maxHands=2,detectionConf=0.8)
width=65
start=[5,70,145,220,295,370,445,520,595,670,745,820,895,970,1045,1120,1195]  #17
end=[60,135,210,285,360,435,510,585,660,735,810,885,960,1035,1110,1185,1260]

last_click_time=time.time()

while True:
    ret,frame=cam.read()

    if not ret:
        break

    img=detector.find_Hands(frame)
    fList = detector.find_Position(img)
    
    

    for i in range(len(start)):
        cv2.rectangle(frame, (start[i],0), (end[i],250), (255, 255, 255),cv2.FILLED)
        cv2.rectangle(frame, (start[i],0), (end[i],250), (0,0,0),5)

    if fList:
        for i in range(len(start)):
            x1=start[i]
            x2=end[i]

            # print(fList[8][1])

            if x1<=fList[8][1]<=x2 and 0<=fList[8][2]<=260:
                cv2.rectangle(frame, (x1,0), (x2,250), (255,0,255),1)

                length, image, extraPts = detector.findDistance(8, 12, frame)
                # print(length)
                if length < 50:
                    curr_time=time.time()
                    cv2.rectangle(frame, (x1,0), (x2,250), (0,0,255),1)
                    
                    if curr_time-last_click_time>=0.5:
                        if i == 0:
                            effect1.play()
                            # effect1.fadeout(1000)
                        elif i == 1:
                            effect2.play()
                            # effect2.fadeout(1000)
                        elif i == 2:
                            effect3.play()
                            # effect3.fadeout(1000)
                        elif i == 3:
                            effect4.play()
                            # effect4.fadeout(1000)
                        elif i == 4:
                            effect5.play()
                            # effect5.fadeout(1000)
                        elif i == 5:
                            effect6.play()
                            # effect6.fadeout(1000)
                        elif i == 6:
                            effect7.play()
                            # effect7.fadeout(1000)
                        elif i == 7:
                            effect8.play()
                            # effect8.fadeout(1000)
                        elif i == 8:
                            effect9.play()
                            # effect9.fadeout(1000)
                        elif i == 9:
                            effect10.play()
                            # effect10.fadeout(1000)
                        elif i == 10:
                            effect11.play()
                            # effect11.fadeout(1000)
                        elif i == 11:
                            effect12.play()
                            # effect12.fadeout(1000)
                        elif i == 12:
                            effect13.play()
                            # effect13.fadeout(1000)
                        elif i == 13:
                            effect14.play()
                            # effect14.fadeout(1000)
                        elif i == 14:
                            effect15.play()
                            # effect15.fadeout(1000)
                        elif i == 15:
                            effect16.play()
                            # effect16.fadeout(1000)
                        elif i==16:
                            effect17.play()
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    print(fps)
    cv2.putText(img, str(int(fps)), (20,550), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)      
    cv2.imshow("Frame",img)
    
    if cv2.waitKey(25) == ord('q'):
        break