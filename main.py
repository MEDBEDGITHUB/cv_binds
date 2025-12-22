import cv2
import numpy as np
import mediapipe as mp
import time
import os
import pyautogui
# import pygame
import sign_record
import time
# Подключаем камеру
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Lenght
cap.set(10, 100)  # Brightness

mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
npDraw = mp.solutions.drawing_utils

saved = False
flag = 0
cnt = -1

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8 or id == 12:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                elif id == 4:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            npDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        if cnt == -1:
            dir = 'hands/'
            for filename in os.listdir(dir):
                filepath = os.path.join(dir, filename)
                if os.path.isfile(filepath):
                    try:
                        with open(filepath, 'r') as file:
                            code = file.readline()
                            code1 = file.readline()
                            code2 = file.readline()
                            if int(code) == int(sign_record.Gesture(results).pos) or int(code1) == int(sign_record.Gesture(results).pos) or int(code2) == int(sign_record.Gesture(results).pos):
                                cv2.putText(img, filename, (10, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                                btn = file.readline()

                                if btn == "lmb":
                                    pyautogui.leftClick()
                                elif btn == "rmb":
                                    pyautogui.rightClick()
                                elif btn == "scroll_down":
                                    pyautogui.scroll(-100)
                                elif btn == "scroll_up":
                                    pyautogui.scroll(100)
                                elif "+" in btn:
                                    pyautogui.hotkey(btn.split("+"))
                                elif btn == "volume_up":
                                    pyautogui.press("volumeup")
                                elif btn == "volume_down":
                                    pyautogui.press("volumedown")
                                elif btn == "volume_mute":
                                    pyautogui.press("volumemute")
                                else:
                                    pyautogui.press(btn)
                            else:
                                cv2.putText(img, "Press enter to bind gesture", (60, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    except Exception as e:
                        print(f"Error opening {filename}: {e}")
            if not os.listdir(dir):
                cv2.putText(img, "Press enter to bind gesture", (60, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        elif cnt == 2 or cnt == 5:
            cv2.putText(img, "Press enter when you shown gesture one more time", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        elif cnt == 3:
            cv2.putText(img, "Remove your hand", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        elif cnt == 1 or cnt == 4:
            cnt += 1

        if cv2.waitKey(10) == 13:
            cv2.putText(img, "Look in console", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.imshow('cv2 binds cam', img)
            while True:
                saved = sign_record.Gesture(results)
                if cnt == -1:
                    if flag == 0:
                        gesture_name = input("What will you call this gesture? ")
                    gesture_bind = input('What do you want to bind(type "help" for more info)? ')
                    if gesture_bind == "help":
                        print("You can bind: \n"
                              'Any button("button1")\n'
                              'Hotkey("button1+button2+...+buttonN")\n'
                              'Scroll up("scroll_up")\n'
                              'Scroll down("scroll_down")\n'
                              'Left mouse button("lmb")\n'
                              'Right mouse button("rmb")\n'
                              'Volume up("volume_up")\n'
                              'Volume down("volume_down")\n'
                              'Volume mute("volume_mute")')
                        flag = 1
                        continue
                    print("Look in your camera again")
                    cv2.putText(img, "Remove your hand", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    cnt += 1
                    break
                elif cnt == 2:
                    saved1 = sign_record.Gesture(results)
                    cnt += 1
                    break
                elif cnt == 5:
                    saved2 = sign_record.Gesture(results)
                    try:
                        with open(f"hands\{gesture_name}.hand", "x") as f:
                            f.write(saved.pos)
                            f.write("\n" + saved1.pos)
                            f.write("\n" + saved2.pos)
                            f.write("\n" + gesture_bind)
                        print("Saved!")
                        cnt = -1
                        time.sleep(0.5)
                        break
                    except:
                        a = int(input(
                            "You already have gesture with this name, do you want to rewrite old file(1) or rename again new gesture(2)? "))
                        if a == 1:
                            with open(f"hands\{gesture_name}.hand", "w") as f:
                                f.write(saved.pos)
                                f.write("\n" + saved1.pos)
                                f.write("\n" + saved2.pos)
                                f.write("\n" + gesture_bind)
                            print("Saved!")
                            cnt = -1
                            time.sleep(0.5)
                            break
                        elif a == 2:
                            continue
                else:
                    break


    elif cnt == 1 or cnt == 4:
        cv2.putText(img, "Show hand again", (10, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    elif cnt == 0 or cnt == 3:
        cnt += 1


    cv2.imshow('cv2 binds cam', img)
    if cv2.waitKey(20) == 27:  # exit on ESC
        break

cv2.destroyWindow("cv2 binds cam")
cap.release()
cv2.waitKey(1)
