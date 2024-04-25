import cv2
import numpy as np
import HandtrackingVirtualMouse as htm
import time
import autopy
import mouse

wCam, hCam = 640, 480
Reduce_Frame = 110
smoothen=20

prev_x,prev_y=0,0
curr_x,curr_y=0,0

pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector(maxHands=1)
wScreen, hScreen = autopy.screen.size()

last_click_time=time.time()

while True:
    success, image = cap.read()
    image = detector.find_Hands(image)
    fList = detector.find_Position(image)

    if len(fList) != 0:
        x1, y1 = fList[8][1:]
        x2, y2 = fList[12][1:]
        
        fingers = detector.fingersUp()

        print(fingers)
        cv2.rectangle(image, (Reduce_Frame, Reduce_Frame), (wCam - Reduce_Frame, hCam - Reduce_Frame),(255, 0, 255), 2)
        
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3]==0:
            x3 = np.interp(x1, (Reduce_Frame+50, wCam - Reduce_Frame-50), (0, wScreen))
            y3 = np.interp(y1, (Reduce_Frame+50, hCam - Reduce_Frame-50), (0, hScreen))

            curr_x = prev_x+(x3-prev_x)/smoothen
            curr_y = prev_y+(y3-prev_y)/smoothen

            try:
                autopy.mouse.move(wScreen - curr_x, curr_y)
            except:
                print("finger out of range")
            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            prev_x,prev_y=curr_x,curr_y
        
            
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3]==0:
            length, image, extraPts = detector.findDistance(8, 12, image)
           # print(length)
            if length < 40:
                current_time=time.time()
                if current_time - last_click_time >= 2:
                    cv2.circle(image, (extraPts[4], extraPts[5]),15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()
                    last_click_time=current_time
          
        if fingers == [0, 0, 0, 1, 0]:  # Check if only the index finger is up
            mouse.click('right')  # Perform a right-click action
            time.sleep(0.5)

        if fingers == [0, 1, 1, 1, 0]:  # If three fingers are detected
            # Scroll up
            mouse.wheel(5)
        elif fingers == [0, 0, 0, 0, 0]:  # If no fingers are detected
            # Scroll down
            mouse.wheel(-5)

           
   
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(image, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)

    cv2.imshow("Image", image)
    if cv2.waitKey(25) == ord('q'):
        break