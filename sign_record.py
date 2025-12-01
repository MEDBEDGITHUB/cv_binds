import cv2
import os
import mediapipe

def save_gesture(found_hands):
    if found_hands.multi_handedness:
        a = ""
        for t in range(20):
            for i in range(20):
                a += "1" if found_hands.multi_hand_landmarks[0].landmark[t].x > found_hands.multi_hand_landmarks[0].landmark[i].x else "0"
                a += "1" if found_hands.multi_hand_landmarks[0].landmark[t].y > found_hands.multi_hand_landmarks[0].landmark[i].y else "0"
        return a