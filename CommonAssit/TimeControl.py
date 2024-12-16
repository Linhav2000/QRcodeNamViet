import time as _time
from datetime import  datetime

def time():
    #milisecond
    return 1000 * _time.time()


def sleep(miliSec):
    _time.sleep(miliSec / 1000)

def logTime():
    return datetime.now()

def ymdFormat():
    return datetime.now().strftime("%Y/%m/%d")

def y_m_dFormat():
    return datetime.now().strftime("%Y_%m_%d")

def ymd_HMSFormat():
    return datetime.now().strftime("%Y/%m/%d - %H:%M:%S")

def HMSFormat():
    return datetime.now().strftime("%H:%M:%S")

def H_M_SFormat():
    return datetime.now().strftime("%H_%M_%S")

def y_m_d_H_M_S_format():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
