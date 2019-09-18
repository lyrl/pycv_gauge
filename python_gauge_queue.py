"""
Copyright (C) 2018 FireEye, Inc., created by Andrew Shay. All Rights Reserved.
"""

import queue, threading
import PIL
from imutils.video import FPS
from PIL import Image
import cv2
import numpy
import time
from datetime import datetime

current_milli_time = lambda: int(round(time.time() * 1000))



class VideoCapture:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


class GaugeDraw:
    def __init__(self, width=640, hight=480):
        self.__needle = Image.open('needle3.png')
        self.__gauge = Image.open('gauge2.png')
        self.__loc = (300, 300)
        self.__width = width
        self.__hight = hight

    def refresh(self, rotate):
        dial_copy = self.__needle.copy()
        dial_copy = dial_copy.rotate(rotate, resample=PIL.Image.BICUBIC, center=self.__loc)  # Rotate needle

        gauge = self.__gauge.copy()
        gauge.paste(dial_copy, mask=dial_copy)  # Paste needle onto gauge

        blank = Image.new('RGB', (self.__width, self.__hight))
        # blank = Image.new('RGBA', (640, 480), (255, 255, 255, 0))
        resized = gauge.resize((150, 150), Image.BICUBIC)
        blank.paste(resized, mask=resized)

        numpy_image = numpy.array(blank)
        merged_img = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        return merged_img



cap = VideoCapture(0)
#cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 30)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
fps = FPS().start()

gauge = GaugeDraw()
rotation = 0
merged_img = None

current = current_milli_time()

while True:
    frame = cap.read()
    if True:
        rotation = rotation + 1

        if rotation > 360:
            rotation = 0

        if merged_img is None:
            merged_img = gauge.refresh(rotation)

        if current_milli_time() - current >= 100:
            merged_img = gauge.refresh(rotation)
            current = current_milli_time()

        added_image = cv2.addWeighted(merged_img, 1, frame, 1, 0.0)

        date = datetime.today()
        position = ((int)(added_image.shape[1] / 2 - 268 / 2), (int)(added_image.shape[0] / 2 - 36 / 2))
        # position = (10,160)
        cv2.putText(
            added_image,  # numpy array on which text is written
            date.strftime("%Y-%m-%d %H:%M:%S"),  # text
            position,  # position at which writing has to start
            cv2.FONT_HERSHEY_SIMPLEX,  # font family
            0.5,  # font size
            (209, 80, 0, 255),  # font color
            1)  # font stroke

        cv2.imshow('frame', added_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()
    else:
        break
# cap.release()
# out.release()
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()

