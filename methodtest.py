import aubio
import numpy as num
import pyaudio
import sys


class pyaubio():
    def __init__(self):
        self.BUFFER_SIZE = 2048
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paFloat32
        self.METHOD = "default"
        self.SAMPLE_RATE = 44100
        self.HOP_SIZE = self.BUFFER_SIZE // 2
        self.PERIOD_SIZE_IN_FRAME = self.HOP_SIZE
        self.current_color = ""

    def main(self, args):
        # Initiating PyAudio object.
        pA = pyaudio.PyAudio()
        # Open the microphone stream.
        mic = pA.open(format=self.FORMAT, channels=self.CHANNELS,
                      rate=self.SAMPLE_RATE, input=True,
                      frames_per_buffer=self.PERIOD_SIZE_IN_FRAME)

        # Initiating Aubio's pitch detection object.
        pDetection = aubio.pitch(self.METHOD, self.BUFFER_SIZE,
                                 self.HOP_SIZE, self.SAMPLE_RATE)
        # Set unit.
        pDetection.set_unit("Hz")
        # Frequency under -40 dB will considered
        # as a silence.
        pDetection.set_silence(-40)

        while True:
            # Update microphone stream
            data = mic.read(self.PERIOD_SIZE_IN_FRAME)
            # Translate to aubio
            samples = num.fromstring(data,
                                     dtype=aubio.float_type)
            # Find pitch from samples
            pitch = pDetection(samples)[0]
            # Get volume from samples
            volume = num.sum(samples ** 2) / len(samples)
            # Format volume for 6 digit float
            self.current_color = self.pitch_detection(pitch)

            # Finally print the pitch and the volume.
            print(str(pitch) + " " + str(volume) + " " + (str(self.current_color)))

    def pitch_detection(self, pitch):
        colordict = {
            (14.0, 16.75): "GREEN",  # C0
            (16.76, 18.0): "CYAN2",  # C#0
            (18.1, 18.90): "ALICEBLUE",  # D0
            (18.91, 19.90): "BLUE2",  # D#0
            (19.91, 21.75): "PURPLE1",  # E0
            (21.76, 22.47): "PURPLE",  # F0
            (22.48, 23.80): "BROWN",  # F#0
            (23.81, 25.23): "BROWN2",  # G0
            (25.24, 26.73): "ORANGERED1",  # G#0
            (26.74, 28.31): "ORANGE",  # A0
            (28.32, 30.00): "YELLOW2",  # A#0
            (30.01, 31.78): "LIMEGREEN",  # B0
            (31.79, 33.67): "GREEN",  # C1
            (33.68, 35.67): "CYAN2",  # C#1
            (35.68, 37.80): "ALICEBLUE",  # D1
            (37.81, 40.03): "BLUE2",  # D#1
            (40.04, 42.42): "PURPLE1",  # E1
            (42.43, 44.94): "PURPLE",  # F1
            (44.95, 47.61): "BROWN",  # F#1
            (47.62, 50.44): "BROWN2",  # G1
            (50.45, 53.44): "ORANGERED1",  # G#1
            (53.45, 56.62): "ORANGE",  # A1
            (56.63, 59.99): "YELLOW2",  # A#1
            (60.00, 63.56): "LIMEGREEN",  # B1
            (63.58, 67.34): "GREEN",  # C2
            (67.36, 71.34): "CYAN2",  # C#2
            (71.36, 75.60): "ALICEBLUE",  # D2
            (75.62, 80.06): "BLUE2",  # D#2
            (80.06, 84.84): "PURPLE1",  # E2
            (84.86, 89.88): "PURPLE",  # F2
            (89.90, 95.22): "BROWN",  # F#2
            (95.24, 100.88): "BROWN2",  # G2
            (100.90, 106.88): "ORANGERED1",  # G#2
            (106.90, 113.24): "ORANGE",  # A2
            (113.26, 119.98): "YELLOW2",  # A#2
            (120.00, 127.12): "LIMEGREEN",  # B2
            (127.16, 134.68): "GREEN",  # C3
            (134.72, 142.68): "CYAN2",  # C#3
            (142.72, 151.20): "ALICEBLUE",  # D3
            (151.24, 160.12): "BLUE2",  # D#3
            (160.16, 169.68): "PURPLE1",  # E3
            (169.72, 179.76): "PURPLE",  # F3
            (179.80, 190.44): "BROWN",  # F#3
            (190.48, 201.76): "BROWN2",  # G3
            (201.80, 213.76): "ORANGERED1",  # G#3
            (213.80, 226.48): "ORANGE",  # A3
            (226.52, 239.96): "YELLOW2",  # A#3
            (240.00, 254.24): "LIMEGREEN",  # B3
            (254.32, 269.36): "GREEN",  # C4
            (269.42, 285.36): "CYAN2",  # C#4
            (285.44, 302.40): "ALICEBLUE",  # D4
            (302.48, 320.24): "BLUE2",  # D#4
            (320.32, 339.36): "PURPLE1",  # E4
            (339.44, 359.52): "PURPLE",  # F4
            (359.60, 380.88): "BROWN",  # F#4
            (380.96, 403.52): "BROWN2",  # G4
            (403.60, 427.52): "ORANGERED1",  # G#4
            (427.60, 452.96): "ORANGE",  # A4
            (453.04, 479.92): "YELLOW2",  # A#4
            (480.00, 508.48): "LIMEGREEN",  # B4
            (508.64, 538.72): "GREEN",  # C5
            (538.88, 580.72): "CYAN2",  # C#5
            (580.88, 604.80): "ALICEBLUE",  # D5
            (604.96, 640.48): "BLUE2",  # D#5
            (640.54, 678.72): "PURPLE1",  # E5
            (678.88, 719.04): "PURPLE",  # F5
            (719.20, 761.76): "BROWN",  # F#5
            (761.90, 807.04): "BROWN2",  # G5
            (807.20, 855.04): "ORANGERED1",  # G#5
            (855.20, 905.92): "ORANGE",  # A5
            (906.08, 959.84): "YELLOW2",  # A#5
            (960.00, 1016.96): "LIMEGREEN",  # B5
            (1017.28, 1077.44): "GREEN",  # C6
            (1077.76, 1161.44): "CYAN2",  # C#6
            (1161.76, 1209.60): "ALICEBLUE",  # D6
            (1209.92, 1280.96): "BLUE2",  # D#6
            (1281.08, 1357.44): "PURPLE1",  # E6
            (1357.76, 1438.08): "PURPLE",  # F6
            (1438.40, 1523.52): "BROWN",  # F#6
            (1523.84, 1614.08): "BROWN2",  # G6
            (1614.40, 1710.08): "ORANGERED1",  # G#6
            (1710.40, 1811.84): "ORANGE",  # A6
            (1812.16, 1919.68): "YELLOW2",  # A#6
            (1920.00, 2033.92): "LIMEGREEN",  # B6
            (2034.56, 2154.88): "GREEN",  # C7
            (2155.52, 2322.88): "CYAN2",  # C#7
            (2323.52, 2419.20): "ALICEBLUE",  # D7
            (2419.84, 2561.92): "BLUE2",  # D#7
            (2562.16, 2714.88): "PURPLE1",  # E7
            (2715.52, 2876.16): "PURPLE",  # F7
            (2876.80, 3037.04): "BROWN",  # F#7
            (3037.68, 3228.16): "BROWN2",  # G7
            (3228.80, 3420.16): "ORANGERED1",  # G#7
            (3420.80, 3623.68): "ORANGE",  # A7
            (3624.32, 3839.36): "YELLOW2",  # A#7
            (3840.00, 4067.84): "LIMEGREEN",  # B7
            (4069.12, 4309.76): "GREEN",  # C8
            (4311.04, 4645.76): "CYAN2",  # C#8
            (4647.04, 4838.40): "ALICEBLUE",  # D8
            (4839.68, 5123.84): "BLUE2",  # D#8
            (5052.32, 5429.76): "PURPLE1",  # E8
            (5431.04, 5752.32): "PURPLE",  # F8
            (5753.60, 6074.08): "BROWN",  # F#8
            (6075.36, 6456.32): "BROWN2",  # G8
            (6457.60, 6840.32): "ORANGERED1",  # G#8
            (6841.60, 7247.36): "ORANGE",  # A8
            (7248.64, 7678.72): "YELLOW2",  # A#8
            (7680.00, 8135.68): "LIMEGREEN",  # B8
        }

        for index, key in enumerate(colordict):
            if pitch > key[0] and pitch < key[1]:
                return colordict[key]
            self.current_color = colordict[key]
            if pitch < key[0]:
                return None

    def getcc(self):
        return self.current_color

    def getBufferSize(self):
        return self.BUFFER_SIZE

    def getChannels(self):
        return self.CHANNELS

    def getFormat(self):
        return self.FORMAT

    def getMethod(self):
        return self.METHOD

    def getSampleRate(self):
        return self.SAMPLE_RATE

    def getHopSize(self):
        return self.HOP_SIZE

    def getPeriodSizeInFrame(self):
        return self.PERIOD_SIZE_IN_FRAME


if __name__ == "__main__":
    p2c = pyaubio()
    p2c.main(sys.argv)
