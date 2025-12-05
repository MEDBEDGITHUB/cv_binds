import cv2
import os
import mediapipe


class Gesture:
    def __init__(self, found_hands):
        self.found_hands = found_hands
        self.pos = self.save_gesture()

    def __eq__(self, other):
        for i in range(len(self.pos)):
            if self.pos:
                if self.pos[i % 20] > self.pos[i // 20]:
                    continue
                else:
                    return False
            else:
                if self.pos[i % 20] < self.pos[i // 20]:
                    continue
                else:
                    return False

    def save_gesture(self):
        if self.found_hands.multi_handedness:
            a = ""
            for t in range(20):
                for i in range(20):
                    a += "1" if self.found_hands.multi_hand_landmarks[0].landmark[t].x > \
                                self.found_hands.multi_hand_landmarks[0].landmark[i].x else "0"
                    a += "1" if self.found_hands.multi_hand_landmarks[0].landmark[t].y > \
                                self.found_hands.multi_hand_landmarks[0].landmark[i].y else "0"
            return a
