import cv2
import numpy as np
from mss import mss
from PIL import Image
import time
import sys
import keyboard
import pyautogui

right_bounding_box = {'top': 522, 'left': 1065, 'width': 10, 'height': 280}
left_bounding_box = {'top': 522, 'left': 750, 'width': 10, 'height': 280}

left_upper_box = {'top': 535, 'left': 715, 'width': 100, 'height': 90}
right_upper_box = {'top': 535, 'left': 1065, 'width': 100, 'height': 90}

current_side = left_upper_box

sct = mss()

min_interval = 0.05
interval = min_interval
interval_acc = 0.04

def detect_edges(box):
    sct_img = sct.grab(box)
    img = np.array(sct_img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)

    edges = cv2.Canny(image=img_blur, threshold1=400, threshold2=500)
    return edges

def contains_edges(img, threshold):
    h, w = img.shape[:2]
    white_pixels = 0

    for x in range(0, w):
        for y in range(0, h):
            if img[y, x] != 0:
                white_pixels += 1

    if white_pixels >= threshold:
        return True
    return False


def run():
    global current_side
    global interval
    while True:
        if keyboard.is_pressed('y'):
            time.sleep(interval)
            edges = detect_edges(current_side)
            
            if contains_edges(edges, 100):
                interval = min_interval
                if current_side == left_upper_box:
                    edges = detect_edges(right_bounding_box)

                    if not contains_edges(edges, 100):
                        print('go to right')
                        pyautogui.press('d')
                        current_side = right_upper_box
                else:
                    edges = detect_edges(left_bounding_box)

                    if not contains_edges(edges, 100):
                        print('go to left')
                        pyautogui.press('a')
                        current_side = left_upper_box
            else:
                if current_side == left_upper_box:
                    print('stay left')
                    pyautogui.press('a')
                else:
                    print('stay right')
                    pyautogui.press('d')
                
                interval = interval - interval_acc
                if interval < 0:
                    interval = 0

        if keyboard.is_pressed('q'):
            sys.exit(0)

run()
