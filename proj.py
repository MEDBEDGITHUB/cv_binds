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


        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8 or id == 12:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                elif id == 4:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            npDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        dir = 'hands/'
        for filename in os.listdir(dir):
            filepath = os.path.join(dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r') as file:  # 'r' for reading, use 'rb' for binary
                        code = file.readline()
                        if int(code) == int(sign_record.Gesture(results).pos):
                            cv2.putText(img, filename, (10, 50),
                                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                            btn = file.readline()
                            if btn == "lbm":
                                pyautogui.leftClick()
                            elif btn == "rbm":
                                pyautogui.rightClick()
                            elif btn == "scroll":
                                print(btn)
                                pyautogui.scroll(-100)
                            else:
                                pyautogui.press(btn)
                except Exception as e:
                    print(f"Error opening {filename}: {e}")
        if cv2.waitKey(10) == 13:
            while True:
                saved = sign_record.Gesture(results)
                gesture_name = input("What will you call this gesture? ")
                gesture_bind = input("What do you want to bind? ")
                try:
                    with open(f"hands\{gesture_name}.hand", "x") as f:
                        f.write(saved.pos)
                        f.write("\n" + gesture_bind)
                    print("Saved!")
                    break
                except:
                    a = int(input("You already have gesture with this name, do you want to rewrite old file(1) or rename again new gesture(2)?"))
                    if a == 1:
                        with open(f"hands\{gesture_name}.hand", "w") as f:
                            f.write(saved.pos)
                            f.write("\n" + gesture_bind)
                        print("Saved!")
                        break
                    elif a == 2:
                        continue


    cv2.imshow('python', img)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if cv2.waitKey(20) == 27:  # exit on ESC
        break

cv2.destroyWindow("python")
cap.release()
cv2.waitKey(1)
