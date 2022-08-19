from pyjom.medialang.functions import *
from pyjom.medialang.commons import *
import tempfile

def executeEditlyScript(medialangTmpDir, editly_json):
    editlyJsonSavePath = os.path.join(medialangTmpDir, "editly.json")
    with open(editlyJsonSavePath, "w+", encoding="utf8") as f:
        f.write(json.dumps(editly_json, ensure_ascii=False))
    print("EXECUTING EDITLY JSON AT %s" % editlyJsonSavePath)
    os.system(" ".join(["editly","--json",editlyJsonSavePath]))

def dotVideoProcessor(item, previous, format=None, verbose=True):
    # print("DOTVIDEO ARGS:", item, previous, format)
    # this item is the video output config, medialang item.
    itemArgs = item.args
    if format is None:
        format = item.path.split(".")[-1]
    backend = itemArgs.get(
        "backend", "editly"
    )  # so all things will be assumed to put directly into editly render json, unless explicitly specified under other medialang or other backend and need to be resolved into media file format before rendering. sure?
    fast = itemArgs.get("fast", True)
    bgm = itemArgs.get("bgm", None)
    outputPath = itemArgs.get("",None)
    print(format, backend, fast, bgm)

    # the "previous" is the clips, was fucked, filled with non-existant intermediate mpegts files, but no source was out there.
    # this is initially decided to output mp4, however you might want to decorate it.
    if verbose:
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
        print("ITEM:", item)
        print("PREVIOUS:", previous)
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
    with tempfile.TemporaryDirectory(prefix="/dev/shm/medialang/") as tmpdirname: # maybe you should take care of the directory prefix?
        # wtf are you doing over here?
        # find out where our cache leads to!
        # maybe the final product is one move away.
        tmpdirname = os.path.abspath(tmpdirname)
        print('created temporary directory', tmpdirname)
        randomUUID = str(uuid.uuid4())
        output_path = os.path.join(tmpdirname,randomUUID+"."+format) # this is temporary!
        # that is the tweak. we have successfully changed the directory!
        if backend == "editly":
            # iterate through all items.
            template = {
                "width": 1920,
                "height": 1080,
                "fps": 60,
                "outPath": output_path,
                "defaults": {"transition": None},
                "clips": [],
            }
            if bgm is not None:
                template.update({"audioFilePath": bgm})
            for elem in previous:
                duration = 3 # default duration
                clip = {
                    "duration": duration,
                    "layers": [
                    ],
                }
                layer_durations = []
                for layerElem in elem:
                    layer = None
                    # print(layerElem) # {"item":<item>, "cache": <cache_path>}
                    # breakpoint()
                    layerElemItem = layerElem["item"]
                    filepath = layerElemItem.path
                    # what type is this damn media?
                    filetype = getFileType(filepath)
                    if layerElemItem.args.get("backend","editly") == "editly":
                        if filetype == "video":
                            videoFilePath = filepath
                            # get video information!
                            videoInfo = get_media_info(filepath)
                            endOfVideo = videoInfo["duration"]
                            cutFrom = layerElemItem.args.get("cutFrom",0)
                            cutTo = layerElemItem.args.get("cutTo",endOfVideo)
                            speed = layerElemItem.args.get("speed",1)
                            layerDuration = speed*(cutTo-cutFrom)
                            layer_durations.append(layerDuration)
                            layer= {
                                    "type": "video",
                                    "path": videoFilePath,
                                    "resizeMode": "contain",
                                    "cutFrom": cutFrom,
                                    "cutTo": cutTo,
                                }
                            removeKeys = []
                            for key, elem in layer.items():
                                if elem is None:
                                    removeKeys.append(key)
                            for key in removeKeys: del layer[key]
                    if layer is not None:
                        clip["layers"].append(layer)
                    else: raise Exception("NOT IMPLEMENTED LAYER FORMAT:", layerElem)
                maxDuration = max(layer_durations)
                clip["duration"] = maxDuration
                template["clips"].append(clip)
                # then just execute this template, or let's just view it.
            # print("________________editly template________________")
            # print(json.dumps(template, ensure_ascii=False, indent=4)) # let's view it elsewhere? or in `less`?
            # print("________________editly template________________")
            # return template
            executeEditlyScript(medialangTmpDir,template)
            return outputPath
