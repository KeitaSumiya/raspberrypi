#https://people.csail.mit.edu/hubert/pyaudio/docs/
#https://docs.python.org/2/library/wave.html
#https://github.com/jackaudio/jack2/issues/226

import pyaudio
import wave
import time

wf = wave.open('file.wav', 'rb')

wavLengthSec = float(wf.getnframes()) / float(wf.getframerate())
halfPauseNum = int( 10.0 * (wavLengthSec / 2.0) )
print(wavLengthSec)
print(halfPauseNum)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
count = 0
while stream.is_active():
    count += 1
    if( count == halfPauseNum):
        stream.stop_stream()
        break
        
    time.sleep(0.1)

print(count)

# count down
print('pausing: 3')
time.sleep(1)
print('pausing: 2')
time.sleep(1)
print('pausing: 1')
time.sleep(1)

stream.start_stream()

while stream.is_active():
    count += 1
    time.sleep(0.1)

print(count)

stream.stop_stream()

# count down
print('pausing: 3')
time.sleep(1)
print('pausing: 2')
time.sleep(1)
print('pausing: 1')
time.sleep(1)

wf.rewind()
stream.start_stream()
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()

wf.close()

# close PyAudio (7)
p.terminate()
