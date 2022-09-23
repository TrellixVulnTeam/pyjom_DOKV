# order:
# remove watermark, remove text, remove potential watermark around corners using inpainting
# use ffmpeg cropdetect, if has significant area change then no further processing
# if no significant area change, use this blur detection to 

import os
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2
import numpy

# import logger
import BlurDetection

# img_path = raw_input("Please Enter Image Path: ")
# img_path = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"
# img_path = "/root/Desktop/works/pyjom/samples/image/blur_sample.webp"
# img_path = "/root/Desktop/works/pyjom/samples/image/blur_sample_2.webp"
img_path="/root/Desktop/works/pyjom/samples/image/dog_with_black_borders.png"
# ffmpeg -loop 1 -i /root/Desktop/works/pyjom/samples/image/dog_with_black_borders.png -t 15 -vf cropdetect -f null -
# img_path="/root/Desktop/works/pyjom/samples/image/husky_cry.png"
assert os.path.exists(img_path), "img_path does not exists"
img = cv2.imread(img_path)
img_fft, val, blurry = BlurDetection.blur_detector(img)
print("this image {0} blurry".format(["isn't", "is"][blurry]))
msk, result, blurry = BlurDetection.blur_mask(img, max_thresh=120)

inv_msk = 255-msk
# import numpy as np
# print(np.max(msk), np.min(msk))
# print(msk.shape)
# breakpoint()

def display(title, img, max_size=200000):
    assert isinstance(img, numpy.ndarray), "img must be a numpy array"
    assert isinstance(title, str), "title must be a string"
    scale = numpy.sqrt(min(1.0, float(max_size) / (img.shape[0] * img.shape[1])))
    print("image is being scaled by a factor of {0}".format(scale))
    shape = (int(scale * img.shape[1]), int(scale * img.shape[0]))
    img = cv2.resize(img, shape)
    cv2.imshow(title, img)


# BlurDetection.scripts.display('img', img)
display("img", img)
# display("msk", msk)
display("inv_msk", inv_msk)
# BlurDetection.scripts.display('msk', msk)
cv2.waitKey(0)
