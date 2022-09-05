# motion detectors are used to track objects. though you may want to separate objects with it.
import pybgs as bgs
import numpy as np

import pathlib
import sys

site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages")
cv2_libs_dir = site_path / 'cv2' / \
    f'python-{sys.version_info.major}.{sys.version_info.minor}'
print(cv2_libs_dir)
cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
if len(cv2_libs) == 1:
    print("INSERTING:", cv2_libs[0].parent)
    sys.path.insert(1, str(cv2_libs[0].parent))

import cv2

# suspect by static image analysis, and then create bounding box over the thing.
# check image quality.

# for donga, you must change the framerate to skip identical frames.

# also donga have strange things you may dislike, e.g.: when only part of the image changes.

# algorithm = bgs.FrameDifference() # this is not stable since we have more boundaries. shall we group things?
# can we use something else?
algorithm = bgs.WeightedMovingVariance()
# this one with cropped boundaries.
video_file = "../../samples/video/LiEIfnsvn.mp4"

# moving average, sampler and  similar merge.
# moving average span: -20 frame to +20 frame

# 选区间之内支持的最多的那种

capture = cv2.VideoCapture(video_file)
while not capture.isOpened():
    capture = cv2.VideoCapture(video_file)
    cv2.waitKey(1000)
    print("Wait for the header")

pipFrames = []

pos_frame = capture.get(1)
while True:
    flag, frame = capture.read()

    if flag:
        pos_frame = capture.get(1)
        img_output = algorithm.apply(frame)
        img_bgmodel = algorithm.getBackgroundModel()
        _, contours = cv2.findContours(
            img_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # maybe you should merge all active areas.
        if contours is not None:
            # continue
            counted = False
            for contour in contours:
                [x, y, w, h] = cv2.boundingRect(img_output)
                if not counted:
                    min_x, min_y = x, y
                    max_x, max_y = x+w, y+h
                    counted = True
                else:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x+w)
                    max_y = max(max_y, y+h)
                    # only create one single bounding box.
            cv2.rectangle(frame, (min_x, min_y),
                          (max_x, max_y), (255, 0, 0), 2)
            # how to stablize this shit?
        # cv2.imshow('video', frame)
        # cv2.imshow('img_output', img_output)
        # cv2.imshow('img_bgmodel', img_bgmodel)

    else:
        cv2.waitKey(1000)
        break

    if 0xFF & cv2.waitKey(10) == 27:
        break


cv2.destroyAllWindows()
