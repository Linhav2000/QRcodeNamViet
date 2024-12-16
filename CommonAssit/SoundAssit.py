from CommonAssit import TimeControl
import winsound
import threading

_time = None

def playMissingErrorSound():
    global _time
    if _time is not None and TimeControl.time() - _time < 3000:
        return
    else:
        _time = TimeControl.time()

    playSound('./resource/alarmSound.wav')

def playSoundThread(fileName):
    try:
        winsound.PlaySound(fileName, winsound.SND_FILENAME | winsound.SND_NOWAIT)
    except:
        pass

def playSound(fileName):
    threadSound = threading.Thread(target=playSoundThread,args=[fileName])
    threadSound.start()
