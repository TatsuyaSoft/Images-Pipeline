import os
import cv2

IMAGE_DIR = "images/"

def load_images():
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            yield filename, cv2.imread(os.path.join(IMAGE_DIR, filename))