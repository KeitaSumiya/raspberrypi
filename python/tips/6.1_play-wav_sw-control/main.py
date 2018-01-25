import pyaudio
import wave
import RPi.GPIO as GPIO
from time import sleep


def playing(filename, pinSW):
    wf = wave.open(filename, 'rb')
    wavLength = wf.getnframes()

    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    countSW = 0
    countToPause = 1
    stateStream = "play"
    while True:
        stateSW = GPIO.input(pinSW)
        if stateSW  == 1:
            countSW += 1
            if countSW == countToPause:
                if stateStream == "play":
                    stateStream = "pause"
                    stream.stop_stream()
                elif stateStream == "pause":
                    stream.start_stream()
                    stateStream = "play"

                print(stateStream)
                sleep(0.1)
        else:
            countSW = 0

        if wf.tell() == wavLength:
            break
        sleep(0.1)

    stream.close()
    wf.close()
    p.terminate()

    print ("finished playing")
    sleep(1)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    pinSW = 14
    GPIO.setup(pinSW, GPIO.IN)

    mode = "stay"
    countSW = 0

    deltaSec = 0.01
    count1Sec = int(1.0/deltaSec)
    shortPushSec = 0.2
    shortPushCount = int(shortPushSec/deltaSec)

    filename = "file.wav"        
    
    try:
        while True:
            stateSW = GPIO.input(pinSW)
            print(stateSW)
            if stateSW == 1:
                countSW += 1
                if countSW == shortPushCount:
                    if mode == "stay":
                        sleep(1)
                        playing(filename, pinSW)
            else:
                countSW = 0
                        
            print(mode)
            sleep(deltaSec)
    except KeyboardInterrupt:
        pass
    
