# audio.py
# Record .WAV file at 16kHz/16-bit
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import pyaudio, sys, threading, wave


class KeyboardPoller(threading.Thread):
    def run(self):
        global key_pressed

        if sys.stdin.read(1) == 'K': # Enter
            key_pressed = True
        else :
            key_pressed = False

        data_ready.set()


class AudioRecord(object):
    def __init__(self, chunk=1024, _format=pyaudio.paInt16, channels=1, fs=16000):
        self.chunk = chunk
        self.format = _format
        self.channels = channels
        self.fs = fs
        self.p = pyaudio.PyAudio()


    def record(self):
        self.frames = list()
        output_file = raw_input('Output file name: ') + '.wav'
        poller = KeyboardPoller()
        poller.start()

        print '--- Recording ---'

        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  input=True,
                                  frames_per_buffer=self.chunk
                                 )

        while not data_ready.isSet() :
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

        if key_pressed:
            pass

        print '--- Stopped Recording ---'

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.write_wav(output_file)


    def write_wav(self, output_file):
        wf = wave.open('wavs/training/{0}'.format(output_file), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()


if __name__ == "__main__" :
    data_ready = threading.Event()
    a = AudioRecord()
    a.record()
