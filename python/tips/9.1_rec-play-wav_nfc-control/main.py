import pyaudio
import wave
import RPi.GPIO as GPIO
from time import sleep
import nfc
import subprocess


#########################################
def connected (tag):
    pass

clf = nfc.ContactlessFrontend("usb")

def playing(filename):
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
    while stream.is_active():
        sleep(0.1)
        
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

    print ("finished playing")
    sleep(1)


                

def recording(WAVE_OUTPUT_FILENAME, FORMAT, CHANNELS, RATE, CHUNK, SEC):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=0,
                        frames_per_buffer=CHUNK)
    frames = []
    print ("start recording")
    MAX_RECORD_SECONDS = SEC
    for i in range(0, int(MAX_RECORD_SECONDS * RATE / CHUNK)):
        data = stream.read(CHUNK)
        frames.append(data)
    
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

############################################

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    #pinSW = 14
    #GPIO.setup(pinSW, GPIO.IN)
    GPIO.setup(14, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(18, GPIO.IN)
    GPIO.setup(23, GPIO.IN)

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
    CHUNK =  8192 #chinese small device 1-in 1-out
    #CHUNK = 32000 #logicool webcam C270
    #CHUNK = 10000 #chinese too small usb mic device 1-in
    filename = "file.wav"        
    stateSW = 0
    SEC = 10

    #print("waiting registration for recording...")
    #result = clf.connect(rdwr={"on-connect":connected})
    #print("scaned")
    #print(result)
    #id = str(result.idm).encode("hex")
    #print(id)
    #id_rec = id
    #sleep(3)
    id_rec = "01010214c2156c0a"
    
    print("waiting registration for playing...")
    result = clf.connect(rdwr={"on-connect":connected})
    print("scaned")
    print(result)
    id = str(result.idm).encode("hex")
    print(id)
    id_play = id
    sleep(3)


    
    try:
        while True:
            print("waiting...")
            result = clf.connect(rdwr={"on-connect":connected})
            id = str(result.idm).encode("hex")
            stateSW1 = GPIO.input(14)
            stateSW2 = GPIO.input(15)
            stateSW3 = GPIO.input(18)
            stateSW4 = GPIO.input(23)
            print(str(stateSW1) + " " + str(stateSW2)+ " " +str(stateSW3)+ " " +str(stateSW4) )
            
            if stateSW1 == 1:
               filename = "page1.wav"
            elif stateSW2 == 1:
                 filename = "page2.wav"
            elif stateSW3 == 1:
                 filename = "page3.wav"
            else:
                filename = "page4.wav"
            sleep(1)
            if id == id_rec:
                recording(filename, FORMAT, CHANNELS, RATE, CHUNK, SEC)                
            elif id == id_play:
                subprocess.call("aplay "+filename, shell=True)
                
                
                        
            print( "state=" + str(stateSW) + "  count=" + str(countSW) + " (" + str(shortPushCount) + "," + str(longPushCount) + ")  " + mode)
            sleep(deltaSec)
    except KeyboardInterrupt:
        pass
    
