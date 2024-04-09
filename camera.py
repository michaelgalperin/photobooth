import os
import sys
from datetime import datetime
import gphoto2 as gp
import cv2
import time


class Camera:

    def __init__(self):
        print("INIT CAMERA...")

        # Macbook self-facing camera is almost always port 0
        self.cam_port = 0
        self.current_fileno = 0

        # Initialize camera and wait 1 sec so it adjusts to room lighting
        self.cam = cv2.VideoCapture(self.cam_port)
        time.sleep(1)

        # Make sure we can take a photo
        self.result, self.image = self.cam.read()
        if self.result:
            print("DONE")
        else:
            print("No image detected. I am sad!")

    def capture(self, target_dir):
        print(datetime.now().strftime("%H:%M:%S"), file=sys.stderr) 

        # Take a new photo
        result, image = self.cam.read()

        if result:
            cv2.imwrite(os.path.join(target_dir, f"{self.current_fileno}.jpg"), image)
            self.current_fileno += 1
            print(datetime.now().strftime("%H:%M:%S"), file=sys.stderr)
        else:
            print("No image detected. I am sad!")
    
    def reset_counter(self):
        self.current_fileno = 0
