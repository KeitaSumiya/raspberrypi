import pyaudio
import wave
import RPi.GPIO as GPIO
from time import sleep

def recording(WAVE_OUTPUT_FILENAME, FORMAT, CHANNELS, RATE, CHUNK, pinSW):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=0,
                        frames_per_buffer=CHUNK)
    frames = []
    print ("start recording")
    MAX_RECORD_SECONDS = 1000
    countSW = 0
    countToStay = 5
    for i in range(0, int(MAX_RECORD_SECONDS * RATE / CHUNK)):
        data = stream.read(CHUNK)
        frames.append(data)

        stateSW = GPIO.input(pinSW)
        if stateSW  == 1:
            countSW += 1
            print(countSW)
            if countSW == countToStay:
                break
        else:
            countSW = 0
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    print ("finished recording")
    sleep(1)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    pinSW = 14
    GPIO.setup(pinSW, GPIO.IN)

    mode = "stay"
    countSW = 0

    deltaSec = 0.01
    count1Sec = int(1.0/deltaSec)
    longPushSec = 1.0
    longPushCount = int(longPushSec/deltaSec)

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    #CHUNK =  8192 #chinese small device 1-in 1-out
    #CHUNK = 32000 #logicool webcam C270
    CHUNK = 10000 #chinese too small usb mic device 1-in
    WAVE_OUTPUT_FILENAME = "file.wav"        
    
    try:
        while True:
            stateSW = GPIO.input(pinSW)
            print(stateSW)
            if stateSW == 1:
                countSW += 1
                if countSW == longPushCount:
                    if mode == "stay":
                        sleep(1)
                        recording(WAVE_OUTPUT_FILENAME, FORMAT, CHANNELS, RATE, CHUNK, pinSW)
            else:
                countSW = 0
                        
            print(mode)
            sleep(deltaSec)
    except KeyboardInterrupt:
        pass
    
