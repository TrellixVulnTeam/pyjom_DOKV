from test_commons import *
from pyjom.mathlib import *

inputList = [[(0, 1), (1, 1.1), (2, 3)], [(0.5, 1.5), (1.6, 2.5)]]

mRangesDict = {"sample_%s" % num: inputList[num] for num in range(len(inputList))}

result_0 = getContinualNonSympyMergeResult(inputList)
print(result_0)
print("_"*20)

# want to build a language?
result_1 = getContinualMappedNonSympyMergeResult(mRangesDict, concatSymbol="|")
print(result_1)
print("_"*20)

result_2 = getContinualMappedNonSympyMergeResult(mRangesDict, concatSymbol="|",noEmpty=False)
print(result_2)