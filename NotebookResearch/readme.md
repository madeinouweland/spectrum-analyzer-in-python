```python
%pip install numpy
%pip install matplotlib
```

```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
samplerate = 44100  # samples per second
rootnote = 880  # A-note, 880Hz
framelength = 512
```


```python
times = np.arange(framelength)
amplitudes = np.sin(2 * np.pi * rootnote * times / samplerate)

plt.plot(times, amplitudes)
plt.show()
```



![png](output_3_0.png)




```python
secondnote = rootnote * 4

signal1 = np.sin(2 * np.pi * rootnote * times / samplerate)
signal2 = np.sin(2 * np.pi * secondnote * times / samplerate) * 0.5  # Half volume
amplitudes = (signal1 + signal2) / 2

plt.plot(times, amplitudes)
plt.show()
```



![png](output_4_0.png)




```python
frequencies = np.fft.fftfreq(framelength, d=1/samplerate)  # Horizontal axis from -samplerate/2 to samplerate/2
freq_amplitudes = np.abs(np.fft.fft(amplitudes))  # Positive Frequency Amplitudes

plt.plot(frequencies, freq_amplitudes)
plt.show()
```



![png](output_5_0.png)




```python
frequencies2 = np.fft.rfftfreq(framelength, d=1/samplerate)  # Horizontal axis from 0 to samplerate/2
freq_amplitudes2 = np.abs(np.fft.rfft(amplitudes))  # Positive Frequency Amplitudes

plt.plot(frequencies2, freq_amplitudes2)
plt.show()
```



![png](output_6_0.png)
