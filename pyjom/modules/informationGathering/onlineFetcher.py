from pyjom.commons import *
from typing import Literal

@decorator
def OnlineFetcher(infoList, source:Literal['giphy']='giphy', filter:dict={'width'}):
    # how do you chain this shit up?
    for info in infoList: # generator most likely
        if source=='giphy':
            # (id, {width, height, url})