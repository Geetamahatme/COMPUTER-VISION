import cv2
import mediapipe as mp
import time
import math

class HandDetector():
    def __init__(self, mode=False, maxHands=2, modelComp=1, detectionConf = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackCon = trackCon
        self.modelComp = modelComp
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComp, self.detectionConf, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.fingertipIDS = [4, 8, 12, 16, 20]

    def find_Hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_Position(self, img, handNo=0, draw=True):
        List_x = []
        List_y = []
        self.fList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                height, width, colorChannel = img.shape
                fx, fy = int(lm.x * width), int(lm.y * height)
                List_x.append(fx)
                List_y.append(fy)
                self.fList.append([id, fx, fy])
                if draw:
                    cv2.circle(img, (fx, fy), 5, (255, 0, 255), cv2.FILLED)
            xMin, xMax = min(List_x), max(List_x)
            yMin, yMax = min(List_y), max(List_y)
            if draw:
                cv2.rectangle(img, (xMin-20, yMin-20), (xMax+20, yMax+20), (0, 255, 0), 2)
        return self.fList

    def fingersUp(self):
        fingers = []

        # Thumb Finger:
        if self.fList[self.fingertipIDS[0]][1] > self.fList[self.fingertipIDS[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers:
        for id in range(1, 5):
            if self.fList[self.fingertipIDS[id]][2] < self.fList[self.fingertipIDS[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15):
        x1, y1 = self.fList[p1][1:]
        x2, y2 = self.fList[p2][1:]
        fx, fy = (x1+x2) // 2, (y1+y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255)),
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (fx, fy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        return length, img, [x1, y1, x2, y2, fx, fy]

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        fList, bbox = detector.findPosition(img)
        if len(fList) != 0:
            print(fList[4])
            fingers = detector.fingersUp()
            print(fingers)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()