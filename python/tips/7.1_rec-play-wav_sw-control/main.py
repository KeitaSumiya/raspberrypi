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
    countToStay = 2
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
    longPushSec = 3.0
    longPushCount = int(longPushSec/deltaSec)
    shortPushSec = 0.2
    shortPushCount = int(shortPushSec/deltaSec)

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    #CHUNK =  8192 #chinese small device 1-in 1-out
    #CHUNK = 32000 #logicool webcam C270
    CHUNK = 10000 #chinese too small usb mic device 1-in
    filename = "file.wav"        
    stateSW = 0
    
    try:
        while True:
            stateSWPre = stateSW
            stateSW = GPIO.input(pinSW)
            #print(stateSW)
            if stateSW == 1:
                countSW += 1
            else:
                if stateSWPre == 1:
                    sleep(1)
                    if countSW >= longPushCount:
                        recording(filename, FORMAT, CHANNELS, RATE, CHUNK, pinSW)
                    elif countSW >= shortPushCount:
                        playing(filename, pinSW)
                    
                countSW = 0
                        
            print( "state=" + str(stateSW) + "  count=" + str(countSW) + " (" + str(shortPushCount) + "," + str(longPushCount) + ")  " + mode)
            sleep(deltaSec)
    except KeyboardInterrupt:
        pass
    
