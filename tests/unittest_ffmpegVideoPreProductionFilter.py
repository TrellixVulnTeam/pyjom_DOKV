from test_commons import *
from pyjom.medialang.processors.dotProcessor import ffmpegVideoPreProductionFilter
import tempfile

tempDir = '/dev/shm/medialang' # anyway we just want something else...
with tempfile.TemporaryDirectory(prefix = tempDir):
    