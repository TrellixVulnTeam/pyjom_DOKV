import requests
import schedule

def checkGPT2Status():
    gpt2status = getGPT2Status()
    

schedule.every(1).minute.do(checkGPT2Status) # shall place a flag if the training is complete.
# schedule.every(1).minute.do(checkGPT2TrainServer)