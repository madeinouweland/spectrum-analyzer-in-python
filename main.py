import pyglet
import time
import wave
import pyaudio
import array
import numpy as np

class Renderer(pyglet.window.Window):
    bands = np.logspace(2, 4, num=8)
    frames_per_buffer = 512

    def __init__(self) -> None:
        super().__init__(1200, 800)
        self.batch = pyglet.graphics.Batch()
        self.bars = []
        self.labels = []

        bar_width = self.width / len(self.bands)
        xx = 0
        for band in self.bands:
            xx += bar_width * .05
            self.bars.append(pyglet.shapes.Rectangle(xx, 0, bar_width * .9, 0, color=(255, 125, 30), batch=self.batch))
            self.labels.append(pyglet.text.Label(str(int(band)), x=xx+bar_width/2, y=self.height - 20, anchor_x="center", batch=self.batch))
            xx += bar_width * .95

    def start(self, file: wave.Wave_read) -> None:
        # Generate a list of frequencies that will be analyzed by the fourier transform.
        self.frequencies = np.fft.rfftfreq(self.frames_per_buffer, d=1/file.getframerate())

        def callback(in_data, frame_count: int, time_info, status) -> tuple:
            """Process a number (frame_count) of samples."""
            data = file.readframes(frame_count)  # Read data from the wave file.
            array_of_ints = array.array("h", data)  # Convert byte pairs to floats.
            left_channel = array_of_ints[::2]  # Only take the left channel from the data by skipping every other value.
            self.freq_amplitudes = np.abs(np.fft.rfft(left_channel)) / 2000
            return (data, pyaudio.paContinue)  # Return data and always continue.

        audio = pyaudio.PyAudio()
        format = audio.get_format_from_width(file.getsampwidth())
        stream = audio.open(format=format, channels=file.getnchannels(), frames_per_buffer=self.frames_per_buffer, rate=file.getframerate(), output=True, stream_callback=callback)

        last_time = time.perf_counter()
        while stream.is_active():
            elapsed_time = time.perf_counter() - last_time
            if elapsed_time > 1 / 60:  # Update frequency = 60 times per second.
                last_time = time.perf_counter()
                self.dispatch_events()  # Needed to show the window.
                self.on_update()
                self.on_draw()
                self.flip()

    def on_update(self) -> None:
        # Create a list of zeroes. Each frequency band starts with zero. Bands are the columns you see on the screen.
        band_bucket = np.zeros(len(self.bands))
        for index in range(len(self.bands)):
            start_freq = self.bands[index]
            end_freq = start_freq * 2
            for freq_index in range(len(self.freq_amplitudes)):
                # Put the highest frequency amplitude from the fourier in a matching a band frequency.
                if self.frequencies[freq_index] > start_freq and self.frequencies[freq_index] < end_freq:
                    if self.freq_amplitudes[freq_index] > band_bucket[index]:
                        band_bucket[index] = self.freq_amplitudes[freq_index]
            if band_bucket[index] > self.bars[index].height:
                self.bars[index].height = band_bucket[index]
            else:
                self.bars[index].height /= 1.11

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

with wave.open("TestSong.wav", "rb") as file:
    # Inspect structural info from wave file.
    print("sample_width", file.getsampwidth(), "bytes")
    print("channels", file.getnchannels())
    print("framerate", file.getframerate(), "Herz")
    renderer = Renderer()
    renderer.start(file)
