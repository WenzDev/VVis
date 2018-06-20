import aubio
import numpy as num
import pyaudio
import sys

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE = 2048
CHANNELS = 1
FORMAT = pyaudio.paFloat32
METHOD = "default"
SAMPLE_RATE = 44100
HOP_SIZE = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME = HOP_SIZE
index = 0

def main(args):

    # Initiating PyAudio object.
    pA = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pA.open(format=FORMAT, channels=CHANNELS,
                  rate=SAMPLE_RATE, input=True,
                  frames_per_buffer=PERIOD_SIZE_IN_FRAME)

    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
                             HOP_SIZE, SAMPLE_RATE)
    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-40)

    # Infinite loop!
    while True:

        # Always listening to the microphone.
        data = mic.read(PERIOD_SIZE_IN_FRAME)
        # Convert into number that Aubio understand.
        samples = num.fromstring(data,
                                 dtype=aubio.float_type)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]
        # Compute the energy (volume)
        # of the current frame.
        volume = num.sum(samples**2)/len(samples)
        # Format the volume output so it only
        # displays at most six numbers behind 0.
        volume = "{:6f}".format(volume)

        answer = pitch_detection(samples)

        # Finally print the pitch and the volume.
        print(str(pitch) + " " + str(volume) + (str(answer)))


def pitch_detection(samples):
    colordict = {
        (0.0, 13.99): "Red",
        (14.00, 250.00): "Blue",
    }

    for index, key in enumerate(colordict, start=0):
        if samples > colordict[key][0] and samples < colordict[key][1]:
            return key
        return "Not Found"


if __name__ == "__main__":
    main(sys.argv)
