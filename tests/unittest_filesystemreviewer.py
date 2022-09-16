from test_commons import *
from pyjom.modules.contentReviewer import filesystemReviewer
from pyjom.commons import keywordDecorator

autoArgs = {
    "subtitle_detector": {"timestep": 0.2},
    "yolov5_detector": {"model": "yolov5x"}, # will this run? no OOM?
}

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
videoPath = ""
fileList = [{'type':'video','path':videoPath}]

resultGenerator = reviewer(fileList,generator=True) # or at least a generator?

for result in resultGenerator:
    print(result)
    breakpoint()