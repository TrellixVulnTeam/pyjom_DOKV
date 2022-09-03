from pyjom.medialang.functions import *
from pyjom.medialang.commons import *
import tempfile
import ffmpeg

# import cv2

def getVideoFrameIterator(videoPath, start, end, sample_rate):
    cap = cv2.VideoCapture(videoPath)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    (cv2.CAP_PROP_FPS)
    success, img = cap.read() # ignore first frame.
    fno = 0
    while success:
        if fno % sample_rate == 0:
            # do_something(img)
            if fno > startFrame and fno < stopFrame:
                yield img
        # read next frame
        success, img = cap.read()

def getPreviewPixels(defaultWidth, defaultHeight, maxPixel):
    mList = [defaultWidth, defaultHeight]
    # if defaultWidth < defaultHeight:
    #     reverseFlag = True
    maxDim = max(mList)
    shrinkRatio = maxPixel/maxDim
    getRounded = lambda num, rounder: (num//rounder)*rounder
    newFrameWork = [getRounded(x*shrinkRatio,4) for x in mList]
    return newFrameWork[0], newFrameWork[1]

def getVideoPreviewPixels(videoPath, maxPixel=200):
    from MediaInfo import MediaInfo
    info = MediaInfo(filename = videoPath)
    infoData = info.getInfo()
    # print(infoData)
    # breakpoint()
    defaultWidth = infoData["videoWidth"]
    defaultHeight = infoData["videoHeight"]
    # print(infoData)
    # print(infoData.keys())
    # breakpoint()
    start = 0
    end = float(infoData['videoDuration'])

    # maxPixel = 200

    previewWidth, previewHeight = getPreviewPixels(defaultWidth, defaultHeight, maxPixel)
    return previewWidth, previewHeight

def executeEditlyScript(medialangTmpDir, editly_json):
    editlyJsonSavePath = os.path.join(medialangTmpDir, "editly.json")
    with open(editlyJsonSavePath, "w+", encoding="utf8") as f:
        f.write(json.dumps(editly_json, ensure_ascii=False))
    print("EXECUTING EDITLY JSON AT %s" % editlyJsonSavePath)
    commandline = ["xvfb-run","editly","--json",editlyJsonSavePath]
    print(commandline)
    status = subprocess.run(commandline) # is it even successful?
    returncode = status.returncode
    assert returncode == 0
    print("RENDER SUCCESSFUL")


def ffmpegVideoPreProductionFilter(filepath, start=None, end=None, cachePath=None, filters=["pipCrop","textRemoval","logoRemoval"], preview=True): # what is the type of this shit?
    # enable that 'fast' flag? or we use low_resolution ones? not good since that will ruin our detection system!
    # anyway it will get processed? or not?
    # uncertain. very uncertain.
    assert cachePath is not None
    assert start is not None
    assert end is not None
    stream = ffmpeg.input(filepath,ss=start, to=end) # from 4 to 10 seconds?
    if preview:
        previewWidth, previewHeight = getVideoPreviewPixels(filepath)
        stream = stream.filter('scale',previewWidth, previewHeight)
    # stream = ffmpeg.hflip(stream)
    # this fliping may be useful for copyright evasion, but not very useful for filtering. it just adds more computational burden.
    # we just need to crop this.
    stream = ffmpeg.output(stream, cachePath)
    ffmpeg.run(stream, overwrite_output=True)
    
    # procedureList = []
    stream = ffmpeg.input
    no_processing = True # change this flag if anything need to change in original video according to filter results.

    # logo removal/text removal first, pipCrop last.
    # if overlap, we sort things.
    # if not, no sorting is needed.
    if "textRemoval" in filters:
        # process the video, during that duration. fast seek avaliable?
        pass
    if "logoRemoval" in filters:
        pass
    if "pipCrop" in filters:
        pass

    return cachePath

def dotVideoProcessor(item, previous, format=None, verbose=True, medialangTmpDir="/dev/shm/medialang/"):
    # print("DOTVIDEO ARGS:", item, previous, format)
    # this item is the video output config, medialang item.
    itemArgs = item.args
    if format is None:
        format = item.path.split(".")[-1]
    backend = itemArgs.get(
        "backend", "editly" # this is mere assumption!
    )  # so all things will be assumed to put directly into editly render json, unless explicitly specified under other medialang or other backend and need to be resolved into media file format before rendering. sure?
    fast = itemArgs.get("fast", True)
    bgm = itemArgs.get("bgm", None)
    # outputPath = itemArgs.get("",None)
    randomUUID = str(uuid.uuid4())
    outputPath = os.path.join(medialangTmpDir,randomUUID+"."+format) # this is temporary!
    # usually we choose to use something under medialang tempdir as the storage place.
    print(format, backend, fast, bgm)

    # the "previous" is the clips, was fucked, filled with non-existant intermediate mpegts files, but no source was out there.
    # this is initially decided to output mp4, however you might want to decorate it.
    if verbose:
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
        print("ITEM:", item)
        print("PREVIOUS:", previous)
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
    with tempfile.TemporaryDirectory(dir=medialangTmpDir) as tmpdirname: # maybe you should take care of the directory prefix?
        # wtf are you doing over here?
        # find out where our cache leads to!
        # maybe the final product is one move away.
        tmpdirname = os.path.abspath(tmpdirname)
        print('created temporary directory', tmpdirname)
        
        output_path = os.path.join(tmpdirname,randomUUID+"."+format) # this is temporary!
        # that is the tweak. we have successfully changed the directory!
        if backend == "editly":
            # iterate through all items.
            template = {
                "width": 1920,
                "height": 1080,
                "fast": fast,
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
                    cachePath = layerElem["cache"]
                    # breakpoint()
                    layerElemItem = layerElem["item"]
                    filepath = layerElemItem.path
                    # what type is this damn media?
                    filetype = getFileType(filepath)
                    if layerElemItem.args.get("backend","editly") == "editly":
                        if filetype == "video":
                            videoInfo = get_media_info(filepath)
                            endOfVideo = videoInfo["duration"]

                            cutFrom = layerElemItem.args.get("cutFrom",0)
                            cutTo = layerElemItem.args.get("cutTo",endOfVideo)
                            layerOriginalDuration = cutTo-cutFrom

                            processedFilePath= ffmpegVideoPreProductionFilter(filepath, start=cutFrom, end=cutTo, cachePath=cachePath)
                            videoFilePath = processedFilePath # what is this filepath? man how do i handle this?
                            # get video information!
                            # if processed:
                            # this must be true now.
                            cutFrom = 0
                            cutTo = layerOriginalDuration

                            speed = layerElemItem.args.get("speed",1)
                            layerDuration = (cutTo-cutFrom)/speed #was wrong.
                            layer_durations.append(layerDuration)
                            mute = layerElemItem.args.get("slient",False)
                            layer= { 
                                    "type": "video",
                                    "path": videoFilePath,
                                    "resizeMode": "contain",
                                    "cutFrom": cutFrom,
                                    "cutTo": cutTo,
                                    "mixVolume": 1-int(mute) # that's how we mute it.
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
            if verbose:
                print("________________editly template________________")
                print(json.dumps(template, ensure_ascii=False, indent=4)) # let's view it elsewhere? or in `less`?
                print("________________editly template________________")
            # breakpoint()
            # return template
            executeEditlyScript(medialangTmpDir,template)
            os.rename(output_path, outputPath)
            return outputPath
