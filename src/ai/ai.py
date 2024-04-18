import cv2
import numpy as np
import tensorflow as tf
import streamlink

occupancy = 0
run = False
LIVESTREAM_URL = "[LIVESTREAM_URL]"
VIDEO_FILE_PATH = '../Engineering_Project/src/test_video.mov'
USE_LIVESTREAM = False
SHOW_VIDEO = True
FLIP_VIDEO = True


class AI():
    @staticmethod
    def ai_stuff():
        global run
        global occupancy

        if run:
            return

        run = True

        IMAGE_SIZE = 100
        resize = tf.keras.Sequential(
            [tf.keras.layers.Resizing(IMAGE_SIZE, IMAGE_SIZE)])
        model = tf.keras.models.load_model('model.h5')

        def currentVal(frame):
            frame = resize(frame)
            if FLIP_VIDEO:
                frame = tf.image.flip_left_right(frame)
            output = model(np.array([frame])).numpy()[0][0]
            print(output)
            if output < -0.5:
                return -1
            if output > 0.5:
                return 1
            return 0

        def check_frames(newVal, vid):
            for i in range(DELAY_FRAMES):
                ret, frame = vid.read()
                if SHOW_VIDEO:
                    cv2.imshow('frame', cv2.resize(frame, dsize=(
                        IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_CUBIC))
                    cv2.waitKey(1)
                output = currentVal(frame)
                if output != newVal:
                    return False
            return True

        prev = 0
        current = 0
        frames = 0
        DELAY_FRAMES = 7
        video_link = None
        if USE_LIVESTREAM:
            video = streamlink.streams(LIVESTREAM_URL)
            video_link = video['best'].args['url']
        else:
            video_link = VIDEO_FILE_PATH
        vid = cv2.VideoCapture(video_link)

        while (True):
            try:
                ret, frame = vid.read()
                if SHOW_VIDEO:
                    cv2.imshow('frame', cv2.resize(frame, dsize=(
                        IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_CUBIC))
                    cv2.waitKey(1)
                current = currentVal(frame)
                if current != prev:
                    real = check_frames(current, vid)
                    if real:
                        occupancy += prev
                        if prev != 0:
                            print('Occupancy Update: ' +
                                  str(occupancy) + ' People')
                        prev = current

            except Exception as e:
                print(e)
                return

    @staticmethod
    def get_occupancy():
        global occupancy
        return occupancy
