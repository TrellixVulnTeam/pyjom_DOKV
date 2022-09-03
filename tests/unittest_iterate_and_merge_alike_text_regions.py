# finite state machine.
sample = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [[98, 206, 37, 9]],
    [[98, 200, 165, 137]],
    [[98, 200, 165, 137]],
    [[98, 200, 165, 137]],
    [[98, 200, 165, 137]],
    [[98, 200, 165, 137]],
    [[98, 200, 165, 137]],
    [],
    [[5, 118, 88, 362]],
    [[5, 118, 88, 362]],
    [[5, 115, 89, 365]],
    [[5, 115, 89, 365]],
    [[2, 115, 92, 365]],
    [[2, 115, 92, 365]],
    [[2, 115, 92, 365]],
    [[2, 115, 92, 365]],
    [[2, 116, 91, 364]],
    [[2, 116, 52, 364]],
    [[2, 116, 52, 364]],
    [[58, 242, 93, 238], [2, 117, 52, 363]],
    [[58, 241, 94, 239], [7, 117, 47, 363]],
    [[58, 240, 94, 240]],
    [[58, 240, 94, 240]],
    [[58, 240, 94, 240]],
    [[58, 240, 94, 240]],
    [[59, 240, 93, 240]],
    [[59, 240, 93, 240]],
    [[59, 241, 93, 239]],
    [[59, 241, 93, 239]],
    [[59, 241, 93, 239]],
    [[59, 241, 93, 239]],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [[92, 190, 23, 290]],
    [[92, 190, 23, 290]],
    [[92, 190, 23, 290]],
    [[90, 190, 25, 290]],
    [[90, 190, 25, 290]],
    [[90, 190, 25, 290]],
    [[90, 190, 25, 290]],
    [[90, 190, 25, 290]],
    [[90, 190, 25, 290]],
    [[92, 190, 23, 290]],
    [[92, 190, 23, 290]],
    [[92, 190, 23, 290]],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [[31, 151, 7, 329]],
    [[31, 151, 7, 329]],
    [[31, 151, 7, 329]],
    [[31, 149, 7, 331]],
    [[31, 149, 7, 331]],
    [[31, 149, 7, 331]],
    [[31, 149, 7, 331]],
    [[31, 149, 7, 331]],
    [[31, 149, 7, 331]],
    [[31, 149, 7, 331]],
    [[31, 149, 7, 331]],
    [],
    [],
    [],
    [],
]

prevList = []
newList = []
import numpy as np
def alike(array0,array1, threshold):
    npArray0, npArray1 = np.array(array0, array1)
    return max(abs(npArray0-npArray1)) <= threshold

for item in sample:
    newItem = []
    for elem in item:
        for prevElem in prevList:
            if alike(prevElem, elem,10):
                # mAlike = True
                elem = prevElem.copy()
                break
        newItem.append(elem.copy())
    prevList = newItem.copy()