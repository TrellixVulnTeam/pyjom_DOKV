# it contains subpixel motion vectors. fucking hell

source = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
from mvextractor.videocap import VideoCap
from caer.video.frames_and_fps import count_frames, get_res

framesCount = count_frames(source)
res = get_res(source) # (width, height)
print("RES: %s" % str(res))
res_x, res_y = res

# 如果整除16那么就在这个范围里面 如果不整除范围就要扩大 扩大到相应的16的倍数

cap = VideoCap()
cap.open(source)  # wtf is going on here?
# if there is nothing we will breakup

# so there can only be one such macroblock
def checkMacroBlock(value):
    for mod in [16,8]:
        modValue = value % mod
        if modValue == mod/2:
            return mod
    # if not satisfied, we are shit.
import progressbar
import numpy as np
# max_dst_x, max_dst_y = 0,0

def averageMotionVectors(motion_vector_list):
    if len(motion_vector_list) == 0:
        return 
    if len(motion_vector_list) > 1:
        marray = np.array(motion_vector_list)
        average = np.average(marray, axis=1)
        average_tuple = tuple(average[0])
    else:
        return 

for _ in progressbar.progressbar(range(framesCount)):
    success, frame, motion_vectors, frame_type, timestamp = cap.read()
    height, width, channels =  frame.shape
    # breakpoint()
    if success:
        # what is the content of this motion vector?
        # print(motion_vectors)
        # import pandas as pd
        # df = pd.DataFrame(motion_vectors)
        # df = pd.DataFrame(motion_vectors,index=['source_index','unk0','unk1','src_x','src_y','dst_x','dst_y','motion_x','motion_y','motion_scale'])
        # breakpoint()
        motion_vectors_simplified = motion_vectors[:,[0,5,6,7,8]]
        motion_vectors_simplified_unique = np.unique(motion_vectors_simplified, axis=0)
        # print(motion_vectors_simplified_unique.shape, motion_vectors.shape)
        # breakpoint()
        motion_vectors_dict = {}
        for mv in motion_vectors_simplified:
            # drop duplicates first!
            (
                source_index,
                dst_x, # corresponding macro block.
                dst_y, # for destination only
                motion_x,
                motion_y,
            ) = mv.tolist()
            # if dst_x>max_dst_x:
            #     max_dst_x = dst_x
            # if dst_y>max_dst_y:
            #     max_dst_y = dst_y
            destCoord = (dst_x, dst_y)
            motion_vector = (motion_x, motion_y)
            # print(destCoord)
            # breakpoint()
            if motion_vector == (0,0):
                # print("zero motion vector detected. skipping")
                # breakpoint()
                continue
            motion_vectors_dict.update({destCoord:motion_vectors_dict.get(destCoord,[])+[motion_vector]})
            # you know, different frame sources may lead to different results.
            # these vectors could overlap. which one you want to keep? the smaller ones or the bigger ones?

            # if destCoord in destCoords:
            #     print("SKIPPING DUPLICATE DESTCOORD:", destCoord)
            #     print("PREVIOUS MV",prevMV)
            #     print("CURRENT MV", mv)
            #     continue
            # else:
            #     destCoords.add(destCoord)
            # prevMV = mv
            # try:
            #     # src_x, src_y may not apply the same rule.
            #     # assert src_x % 16 == 8
            #     # assert src_y % 16 == 8
            #     assert checkMacroBlock(dst_x) is not None
            #     assert checkMacroBlock(dst_y) is not None
            #     # assert dst_x<=res_x # dst_x can go beyond the res_x
            #     # assert dst_y<=res_y
            #     # so all rules applied.
            # except:
            #     # print('source',src_x, src_y)
            #     print("res", res_x, res_y)
            #     print('destionation',dst_x, dst_y)
            #     print('motion',motion_x, motion_y)
            #     print("scale",motion_scale)
        motion_vectors_dict_averaged = {key: averageMotionVectors(motion_vectors_dict[key]) for key in motion_vectors_dict.keys()}
        for key, average_motion_vector in motion_vectors_dict_averaged.items():
            if average_motion_vector == (0,0):
                print('skipping zero avergage motion vector')
                print("destination coords", key)
                # print('average motion vector', average_motion_vector)
        # print(motion_vectors.shape)
        breakpoint()
    else:
        break

# print('max_dst_x', max_dst_x)
# print('max_dst_y', max_dst_y)
