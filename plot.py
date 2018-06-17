import pyaudio
import numpy as np
import pylab
import time
import aubio


BUFFER_SIZE = 2048
RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second
HOP_SIZE = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME = HOP_SIZE
METHOD = "default"
FORMAT = pyaudio.paFloat32


def soundplot(stream):
    t1 = time.time()
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    pylab.plot(data)
    pylab.title(i)
    pylab.grid()
    pylab.axis([0,len(data),-2**16/2,2**16/2])
    pylab.savefig("03.png",dpi=50)
    pylab.close('all')
    print("took %.02f ms"%((time.time()-t1)*1000))


if __name__=="__main__":
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                    frames_per_buffer=CHUNK)

# Detecting pitch
    pitch_detect = aubio.pitch(METHOD, BUFFER_SIZE,
                               HOP_SIZE, RATE)

    pitch_detect.set_unit("Hz")

    pitch_detect.set_silence(-40)

    while True:
        data = stream.read(PERIOD_SIZE_IN_FRAME)
        samples = np.fromstring(data,
                                dtype=aubio.float_type)
        pitch = pitch_detect(samples)[0]
        volume = np.sum(samples**2)/len(samples)
        volume = "{:6f}".format(volume)
        print(str(pitch) + " " + str(volume))
        for i in range(int(20*RATE/CHUNK)):  # do this for 10 seconds
            soundplot(stream)
        stream.stop_stream()
        stream.close()
        p.terminate()


