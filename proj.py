import cv2
import numpy as np
import mediapipe as mp
import time
import os
import pyautogui
import math

# Подключаем камеру
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Lenght
cap.set(10, 100)  # Brightness

mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
npDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

class Point:
    def __init__(self, x, y=None, polar=False):
        if not polar:
            self.x = x
            self.y = y
        else:
            self.x = x * math.cos(y)
            self.y = x * math.sin(y)
        self.polar = polar

    def __abs__(self):
        return math.hypot(self.y, self.x)

    def __str__(self):
        return str((self.x, self.y))

    def dist(self, x=0, y=0):
        if isinstance(x, Point):
            y = x.y
            x = x.x
        return math.hypot(y - self.y, x - self.x)


class Vector(Point):
    def __init__(self, x1, y1=0, x2=None, y2=None):
        if isinstance(x2, int):
            super().__init__(x2 - x1, y2 - y1)
        elif not isinstance(x2, int):
            super().__init__(x1, y1)
        if isinstance(x1, Point):
            super().__init__(x1.x, x1.y)
        if isinstance(y1, Point):
            super().__init__(y1.x - x1.x, y1.y - x1.y)


    def __mul__(self, other):
        try:
            return self.dot_product(other)
        except:
            self.x, self.y = self.x * other, self.y * other
            return self

    def dot_product(self, other: "Vector"):
        return self.x * other.x + self.y * other.y

    def cross_product(self, other):
        return self.x * other.y - self.y * other.x

    __xor__ = cross_product
    __rmul__ = __mul__

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        if "Left" in str(results.multi_handedness[0]):
            isleft = 1
        else:
            isleft = 0
        cv2.putText(img, str(Point(results.multi_hand_landmarks[0].landmark[4].x, results.multi_hand_landmarks[0].landmark[4].y).dist(results.multi_hand_landmarks[0].landmark[8].x, results.multi_hand_landmarks[0].landmark[8].y)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        if (isleft == 0 and results.multi_hand_landmarks[0].landmark[4].x < results.multi_hand_landmarks[0].landmark[
            20].x) or (
                isleft == 1 and results.multi_hand_landmarks[0].landmark[4].x >
                results.multi_hand_landmarks[0].landmark[20].x):
            if results.multi_hand_landmarks[0].landmark[4].y > results.multi_hand_landmarks[0].landmark[8].y and results.multi_hand_landmarks[0].landmark[4].y > results.multi_hand_landmarks[0].landmark[12].y and results.multi_hand_landmarks[0].landmark[4].y < results.multi_hand_landmarks[0].landmark[16].y:
                if Point(results.multi_hand_landmarks[0].landmark[4].x, results.multi_hand_landmarks[0].landmark[4].y).dist(results.multi_hand_landmarks[0].landmark[8].x, results.multi_hand_landmarks[0].landmark[8].y) < 0.1:
                    pyautogui.click(interval=0.5)
                elif Point(results.multi_hand_landmarks[0].landmark[4].x, results.multi_hand_landmarks[0].landmark[4].y).dist(results.multi_hand_landmarks[0].landmark[12].x, results.multi_hand_landmarks[0].landmark[12].y) < 0.1:
                    cv2.putText(img, str(Point(results.multi_hand_landmarks[0].landmark[4].x,
                                               results.multi_hand_landmarks[0].landmark[4].y).dist(
                        results.multi_hand_landmarks[0].landmark[12].x,
                        results.multi_hand_landmarks[0].landmark[12].y) < 0.1), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 0, 0), 2)
                    pyautogui.click(button="secondary", interval=0.5)
                pyautogui.moveTo(results.multi_hand_landmarks[0].landmark[4].x * 2520, results.multi_hand_landmarks[0].landmark[4].y * 1680)
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8 or id == 12:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                elif id == 4:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            npDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow('python', img)
    if cv2.waitKey(20) == 27:  # exit on ESC
        break

cv2.destroyWindow("python")
cap.release()
cv2.waitKey(1)