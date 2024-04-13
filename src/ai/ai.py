import cv2
import numpy as np
import tensorflow as tf
import streamlink

occupancy = 0
run = False
LIVESTREAM_URL = "[LIVESTREAM_URL]"
VIDEO_FILE_PATH = '[VIDEO_FILE_PATH]'
USE_LIVESTREAM = True

class AI():
    @staticmethod
    def ai_stuff():
        global run
        global occupancy

        if run:
            return

        run = True

        image_size = 100

        resize = tf.keras.Sequential(
            [tf.keras.layers.Resizing(image_size, image_size)])
        base_model = tf.keras.applications.ResNet50(input_shape=(image_size,
                                                                 image_size, 3),
                                                    include_top=False)
        input_layer = tf.keras.layers.Input((image_size, image_size, 3))
        scaling_layer = tf.keras.layers.Rescaling(scale=1.0 / 127.5, offset=-1)
        x = scaling_layer(input_layer)
        x = base_model(x, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        output_layer = tf.keras.layers.Dense(1, activation="tanh")(x)
        model = tf.keras.Model(input_layer, output_layer)
        model = tf.keras.models.load_model('ai/model.h5')

        def currentVal(frame):
            frame = resize(frame)
            output = model(np.array([frame])).numpy()[0][0]
            if output < -0.5:
                return -1
            if output > 0.5:
                return 1
            return 0

        def check_frames(newVal, vid):
            if prev != 0:
                for i in range(DELAY_FRAMES):
                    ret, frame = vid.read()
                    output = currentVal(frame)
                    if output != newVal:
                        return False
                return True
            else:
                for i in range(int(DELAY_FRAMES / 2)):
                    ret, frame = vid.read()
                    output = currentVal(frame)
                    if output != newVal:
                        return False
                return True

        prev = 0
        current = 0
        frames = 0
        DELAY_FRAMES = 6
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
                cv2.imshow('frame', frame)
                current = currentVal(frame)
                if current != prev:
                    real = check_frames(current, vid)
                    if real:
                        occupancy += prev
                        if prev != 0:
                            print('Occupancy Update: ' +
                                  str(occupancy) + ' People')
                        prev = current
                cv2.waitKey(1)

            except:
                return

    @staticmethod
    def get_occupancy():
        global occupancy
        return occupancy
