import cv2
import numpy as np
import mediapipe as mp
import time
import os
import pyautogui
from vector import *
# import pygame
import sign_record

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
saved = False
flag = 0
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

        cv2.putText(img, str(Point(results.multi_hand_landmarks[0].landmark[4].x,
                                   results.multi_hand_landmarks[0].landmark[4].y).dist(
            results.multi_hand_landmarks[0].landmark[8].x, results.multi_hand_landmarks[0].landmark[8].y)), (10, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8 or id == 12:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                elif id == 4:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            npDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        if saved:
            if saved == sign_record.Gesture(results):
                flag += 1
                print(f"yeah {flag}")

        if cv2.waitKey(10) == 13:
            saved = sign_record.Gesture(results)
            print("Saved!")
    cv2.imshow('python', img)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if cv2.waitKey(20) == 27:  # exit on ESC
        break

cv2.destroyWindow("python")
cap.release()
cv2.waitKey(1)
