import pyaudio
import wave

def rec_wav(CHUNK):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=0,
                        frames_per_buffer=CHUNK)
    print ("recording...")

    print( int(RECORD_SECONDS * RATE / CHUNK) )
    frames = []
    for i in range(0, int(RECORD_SECONDS * RATE / CHUNK)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


if __name__ == "__main__":
    #CHUNK =  8192 #chinese small device 1-in 1-out
    #CHUNK = 32000 #logicool webcam C270
    CHUNK = 10000 #chinese too small usb mic device 1-in 
    rec_wav(CHUNK)

    
