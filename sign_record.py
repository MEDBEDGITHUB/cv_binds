import cv2
import os
import mediapipe


class Gesture:
    def __init__(self, found_hands):
        self.found_hands = found_hands
        self.pos = self.save_gesture()

    def __eq__(self, other):
        return self.pos == other.pos

    def save_gesture(self):
        if self.found_hands.multi_handedness:
            a = ""
            for i in range(20):
                a += "1" if self.found_hands.multi_hand_landmarks[0].landmark[0].x > \
                            self.found_hands.multi_hand_landmarks[0].landmark[i].x else "0"
                a += "1" if self.found_hands.multi_hand_landmarks[0].landmark[0].y > \
                            self.found_hands.multi_hand_landmarks[0].landmark[i].y else "0"
            for i in range(4, 20, 4):
                a += "1" if self.found_hands.multi_hand_landmarks[0].landmark[i].y > \
                            self.found_hands.multi_hand_landmarks[0].landmark[i-2].y else "0"
            return a
