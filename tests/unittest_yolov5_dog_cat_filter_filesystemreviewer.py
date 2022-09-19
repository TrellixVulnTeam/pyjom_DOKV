from test_commons import *
from pyjom.modules.contentReviewer import filesystemReviewer
from pyjom.commons import keywordDecorator
from lazero.utils.logger import sprint

autoArgs = {
    "subtitle_detector": {"timestep": 0.2},
    "yolov5_detector": {"model": "yolov5x"},  # will this run? no OOM?
} # threshold: 0.4

from pyjom.mathlib import superMean, superMax

def extractYolov5DetectionData(detectionData, mimetype="video", debug=False):
    # plan to get some calculations!
    filepath, review_data = detectionData["review"]["review"]
    timeseries_data = review_data["yolov5_detector"]["yolov5"]["yolov5_detector"]
    data_dict = {}
    if mimetype == "video":
        dataList = []
        for frameData in timeseries_data:
            timestamp, frameNumber, frameDetectionData = [
                frameData[key] for key in ["time", "frame", "yolov5_detector"]
            ]
            if debug:
                sprint("timestamp:", timestamp)
            current_shot_detections = []
            for elem in frameDetectionData:
                location, confidence, identity = [
                    elem[key] for key in ["location", "confidence", "identity"]
                ]
                identity = identity["name"]
                if debug:
                    print("location:", location)
                    print("confidence:", confidence)
                    sprint(
                        "identity:", identity
                    )  # we should use the identity name, instead of the identity dict, which is the original identity object.
                current_shot_detections.append(
                    {
                        "location": location,
                        "confidence": confidence,
                        "identity": identity,
                    }
                )
            dataList.append(
                {"timestamp": timestamp, "detections": current_shot_detections}
            )
        data_dict.update({"data": dataList})
    else:
        frameDetectionData = timeseries_data
        current_shot_detections = []
        for elem in frameDetectionData:
            location, confidence, identity = [
                elem[key] for key in ["location", "confidence", "identity"]
            ]
            identity = identity["name"]
            if debug:
                print("location:", location)
                print("confidence:", confidence)
                sprint("identity:", identity)
        data_dict.update(
            {"data": current_shot_detections}
        )  # just detections, not a list in time series order
    data_dict.update({"path": filepath, "type": mimetype})
    return data_dict


def calculateVideoMaxDetectionConfidence(
    dataList, identities=["dog", "cat"]
):  # does it have a dog?
    report = {identity: 0 for identity in identities}
    for elem in dataList:
        detections = elem["detections"]
        for detection in detections:
            identity = detection["identity"]
            if identity in identities:
                if report[identity] < detection["confidence"]:
                    report[identity] = detection["confidence"]
    return report


from typing import Literal
import numpy as np


def calculateVideoMeanDetectionConfidence(
    dataList: list,
    identities=["dog", "cat"],
    framewise_strategy: Literal["mean", "max"] = "max",
    timespan_strategy: Literal["max", "mean", "mean_no_missing"] = "mean_no_missing",
):
    report = {identity: [] for identity in identities}
    # report = {}
    for elem in dataList:  # iterate through selected frames
        # sprint("ELEM")
        # sprint(elem)
        # breakpoint()
        detections = elem["detections"]
        frame_detection_dict_source = {}
        # frame_detection_dict = {key:[] for key in identities}
        for (
            detection
        ) in detections:  # in the same frame, iterate through different detections
            identity = detection["identity"]
            if identity in identities:
                frame_detection_dict_source[identity] = frame_detection_dict_source.get(
                    identity, []
                ) + [detection["confidence"]]
        frame_detection_dict = {}
        for key in identities:
            valueList = frame_detection_dict_source.get(key, [0])
            if framewise_strategy == "mean":
                frame_detection_dict.update({key: superMean(valueList)})
            elif framewise_strategy == "max":
                frame_detection_dict.update({key: superMax(valueList)})
        # now update the report dict.
        for identity in identities:
            value = frame_detection_dict.get(identity, 0)
            if timespan_strategy == "mean_no_missing":
                if value == 0:
                    continue
            report[identity].append(value)
    final_report = {}
    for identity in identities:
        valueList = report.get(identity, [0])
        if timespan_strategy in ["mean_no_missing", "mean"]:
            final_report[identity] = superMean(valueList)
        else:
            final_report[identity] = superMax(valueList)
    return final_report


from pyjom.commons import checkMinMaxDict


def detectionConfidenceFilter(
    detectionConfidence: dict,
    filter_dict={
        "dog": {"min": 0.5},
        "cat": {"min": 0.5},
    },  # both have certainty of 0.69 or something. consider to change this value higher?
    logic: Literal["AND", "OR"] = "OR",
):  # what is the logic here? and? or?
    assert logic in ["AND", "OR"]
    for identity in filter_dict.keys():
        value = detectionConfidence.get(identity, 0)
        key_filter = filter_dict[identity]
        result = checkMinMaxDict(value, key_filter)
        if result:
            if logic == "OR":
                return True
        else:
            if logic == "AND":
                return False
    if logic == "AND":
        return True  # for 'AND' this will be True, but for 'OR' this will be False
    elif logic == "OR":
        return False
    else:
        raise Exception("Invalid logic: %s" % logic)

def yolov5VideoDogCatDetector(videoPath, debug=False):

    template_names = ["yolov5_detector.mdl.j2"]
    semiauto = False
    dummy_auto = False

    reviewer = keywordDecorator(
        filesystemReviewer,
        auto=True,
        semiauto=semiauto,
        dummy_auto=dummy_auto,
        template_names=template_names,
        args={"autoArgs": autoArgs},
    )
    # videoPath = "/root/Desktop/works/pyjom/samples/image/dog_with_text2.png"
    # fileList = [{"type": "image", "path": videoPath}]

    fileList = [{"type": "video", "path": videoPath}]
    # fileList = [{"type": "video", "path": videoPath} for videoPath in videoPaths]

    # resultGenerator, function_id = reviewer(
    #     fileList, generator=True, debug=False
    # )  # or at least a generator?

    resultList, function_id = reviewer(
        fileList, generator=False, debug=False
    )  # or at least a generator?
    result = resultList[0]

    detectionData = extractYolov5DetectionData(result, mimetype=fileList[0]["type"])
    # sprint("DETECTION DATA:")
    # sprint(detectionData)
    filepath = detectionData["path"]
    if debug:
        sprint("FILEPATH: %s" % filepath)
    filetype = detectionData["type"]
    dataList = detectionData["data"]
    detectionConfidence = calculateVideoMeanDetectionConfidence(dataList)
    if debug:
        sprint("DETECTION CONFIDENCE:", detectionConfidence)
    filter_result = detectionConfidenceFilter(detectionConfidence)
    return filter_result

    @lru_cache(maxsize=3)
    def labelFileReader(filename):
        with open(filename, 'r') as f:
            content = f.read()
            content = content.split("\n")
            content = [elem.replace("\n","").strip() for elem in content]
            content = [elem for elem in content if len(elem)>0]
        return content
# {'input_bias': 0.0830047243746045, 'skew': -0.4986098769473948}
from functools import lru_cache
def bezierPaddleHubResnet50VideoDogCatDetector(videoPath, input_bias=0.0830047243746045, skew=-0.4986098769473948, threshold=0.5):
    from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
    from pyjom.imagetoolbox import resizeImageWithPadding
    import paddlehub as hub



    dog_suffixs = ["狗", "犬", "梗"]
    cat_suffixs = ["猫"]  # ends with this, and not containing forbidden words.
    dog_labels = labelFileReader("/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt")
    cat_labels = labelFileReader("/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt")

    forbidden_words = [
        "灵猫",
        "熊猫",
        "猫狮",
        "猫头鹰",
        "丁丁猫儿",
        "绿猫鸟",
        "猫鼬",
        "猫鱼",
        "玻璃猫",
        "猫眼",
        "猫蛱蝶",
    ]

    def dog_cat_name_recognizer(name):
        if name in dog_labels:
            return "dog"
        elif name in cat_labels:
            return "cat"
        elif name not in forbidden_words:
            for dog_suffix in dog_suffixs:
                if name.endswith(dog_suffix):
                    return "dog"
            for cat_suffix in cat_suffixs:
                if name.endswith(cat_suffix):
                    return "cat"
        return None

    return result

videoPaths = [
    # "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4",
    # "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4",
    # "/root/Desktop/works/pyjom/samples/video/cat_invalid_without_mestimate.mp4",
    "/root/Desktop/works/pyjom/samples/video/kitty_flash_15fps.gif",
    # "/root/Desktop/works/pyjom/samples/video/kitty_flash_15fps.mp4",
    # "/root/Desktop/works/pyjom/samples/video/kitty_flash_scaled.mp4",
    # "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.mp4",
]
for videoPath in videoPaths:  # this is for each file.
    # sprint(result)
    sprint("FILTER PASSED?", filter_result)
    if not filter_result:
        sprint("CHECKING WITH BEZIER CURVE AND RESNET50")

    # if not passed, hit it with the bezier curve and resnet50
    # breakpoint()
