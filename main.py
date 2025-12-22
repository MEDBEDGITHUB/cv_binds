import cv2
import numpy as np
import mediapipe as mp
import os
import pyautogui
# import pygame
import sign_record
import time
# Подключаем камеру
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Length
cap.set(10, 100)  # Brightness

mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
npDraw = mp.solutions.drawing_utils

saved_gesture = False
gesture_has_name = 0
callibrating_stage = -1

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
        if callibrating_stage == -1:
            dir = 'hands/'
            if not os.listdir(dir):
                cv2.putText(img, "Press enter to bind gesture", (60, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            else:
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
                                    binded = file.readline()
                                    if binded == "lmb":
                                        pyautogui.leftClick()
                                    elif binded == "rmb":
                                        pyautogui.rightClick()
                                    elif binded == "scroll_down":
                                        pyautogui.scroll(-100)
                                    elif binded == "scroll_up":
                                        pyautogui.scroll(100)
                                    elif "+" in binded:
                                        pyautogui.hotkey(binded.split("+"))
                                    elif binded == "volume_up":
                                        pyautogui.press("volumeup")
                                    elif binded == "volume_down":
                                        pyautogui.press("volumedown")
                                    elif binded == "volume_mute":
                                        pyautogui.press("volumemute")
                                    else:
                                        pyautogui.press(binded)
                                else:
                                    cv2.putText(img, "Press enter to bind gesture", (60, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                        except Exception as e:
                            print(f"Error opening {filename}: {e}")

        elif callibrating_stage == 2 or callibrating_stage == 5:
            cv2.putText(img, "Press enter when you shown gesture one more time", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        elif callibrating_stage == 3:
            cv2.putText(img, "Remove your hand", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        elif callibrating_stage == 1 or callibrating_stage == 4:
            callibrating_stage += 1

        if cv2.waitKey(10) == 13:
            cv2.putText(img, "Look in console", (10, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.imshow('cv2 binds cam', img)
            gesture_has_name = False
            while True:
                saved_gesture = sign_record.Gesture(results)
                if callibrating_stage == -1:
                    if gesture_has_name == False:
                        gesture_name = input("What will you call this gesture? ")
                        gesture_has_name = True
                    gesture_bind = input('What do you want to bind(type "help" for more info)? ')
                    if gesture_bind == "help":
                        print("You can bind: \n"
                              'Any button("button")\n'
                              'Hotkey("button1+button2+...+buttonN")\n'
                              'Scroll up("scroll_up")\n'
                              'Scroll down("scroll_down")\n'
                              'Left mouse button("lmb")\n'
                              'Right mouse button("rmb")\n'
                              'Volume up("volume_up")\n'
                              'Volume down("volume_down")\n'
                              'Volume mute("volume_mute")')
                        continue
                    print("Look in your camera again")
                    cv2.putText(img, "Remove your hand", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    callibrating_stage += 1
                    break
                elif callibrating_stage == 2:
                    saved_gesture_1 = sign_record.Gesture(results)
                    callibrating_stage += 1
                    break
                elif callibrating_stage == 5:
                    saved_gesture_2 = sign_record.Gesture(results)
                    try:
                        with open(f"hands\{gesture_name}.hand", "x") as f:
                            f.write(saved_gesture.pos)
                            f.write("\n" + saved_gesture_1.pos)
                            f.write("\n" + saved_gesture_2.pos)
                            f.write("\n" + gesture_bind)
                        print("Saved!")
                        callibrating_stage = -1
                        time.sleep(0.5)
                        break
                    except:
                        a = int(input(
                            "You already have gesture with this name, do you want to rewrite old file(1) or rename again new gesture(2)? "))
                        if a == 1:
                            with open(f"hands\{gesture_name}.hand", "w") as f:
                                f.write(saved_gesture.pos)
                                f.write("\n" + saved_gesture_1.pos)
                                f.write("\n" + saved_gesture_2.pos)
                                f.write("\n" + gesture_bind)
                            print("Saved!")
                            callibrating_stage = -1
                            time.sleep(0.5)
                            break
                        elif a == 2:
                            continue
                else:
                    break


    elif callibrating_stage == 1 or callibrating_stage == 4:
        cv2.putText(img, "Show hand again", (10, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    elif callibrating_stage == 0 or callibrating_stage == 3:
        callibrating_stage += 1


    cv2.imshow('cv2 binds cam', img)
    if cv2.waitKey(20) == 27:  # exit on ESC
        break

cv2.destroyWindow("cv2 binds cam")
cap.release()
cv2.waitKey(1)
