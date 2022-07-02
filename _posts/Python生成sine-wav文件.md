---
title: Python生成sine-wav文件
date: 2022-03-28 19:17:25
tags:
	- Python

---

--

现在需要生成一个16通道的sine wav文件。

看看Python怎么实现。

```
import numpy as np
from scipy.io import wavfile

fs = 48000
nsamps = fs * 10

A, Csharp, E, G = 440.0, 554.365, 660.0, 783.991

def sine(freqHz):
    tao = 2 * np.pi
    return np.sin( 
        np.linspace(0,  tao * freqHz * nsamps / fs,  nsamps,  endpoint=False)
    )

A7_chord = np.array( [ sine(A), sine(Csharp), sine(E), sine(G) ] ).T

wavfile.write("A7--4channel.wav", fs, A7_chord)
```

这个是生成了4个声调的正弦波。

比我要的还高级一点。不过我不用这么高级的。

我就：16声道，1K Hz的频率，采样率就48K，时长10s。



最后整理成这样。

```
import numpy as np
from scipy.io import wavfile
import sys,os
import math

fs = 48000
t = 120
nsamps = fs * t

freq = 1000.0
if len(sys.argv )< 2:
    print("usage: {} filename".format(sys.argv[0]))
    sys.exit(1)
fn = sys.argv[1]

if not os.path.exists('./output'):
    os.mkdir('./output')
    
def sine(freqHz):
    tao = 2 * np.pi
    return np.sin( 
        np.linspace(0,  tao * freqHz * nsamps / fs,  nsamps,  endpoint=False)
    )
def empty():
    return np.linspace(0, 0, nsamps, endpoint=False)
    
if fn == '16_ch_1KHz_0dB_48kfs_32bit.wav':
    data = np.array( [ sine(freq), sine(freq),sine(freq),sine(freq),sine(freq), sine(freq),sine(freq),sine(freq),sine(freq), sine(freq),sine(freq),sine(freq),sine(freq), sine(freq),sine(freq),sine(freq) ] ).T
if fn == '8ch_1KHz_0dB_48kfs_32bit_L.wav':
    data = np.array( [
        sine(freq),empty(), 
        sine(freq),empty(), 
        sine(freq),empty(), 
        sine(freq),empty(), 
        sine(freq),empty(), 
        sine(freq),empty(), 
        sine(freq),empty(), 
        sine(freq),empty()
    ]).T
    
if fn == '8ch_1KHz_0dB_48kfs_32bit_R.wav':
    data = np.array( [
        empty(), sine(freq),
        empty(), sine(freq),
        empty(), sine(freq),
        empty(), sine(freq),
        empty(), sine(freq),
        empty(), sine(freq),
        empty(), sine(freq),
        empty(),sine(freq),
    ]).T
    

if fn == '16_CH_1KHz_0dB_48kfs_32bit_mute.wav':
    data = np.array( [
        empty(), empty(),
        empty(), empty(),
        empty(), empty(),
        empty(), empty(),
        empty(), empty(),
        empty(), empty(),
        empty(), empty(),
        empty(), empty(),
    ]).T
wavfile.write('/mnt/fileroot/hanliang.xiong/work/image_server/audio_files/speaker_test/'+fn, fs, data.astype(np.int32))

```



参考资料

1、

https://stackoverflow.com/questions/58869822/how-to-create-multichannel-wav-file-in-python

2、

https://scipy.github.io/devdocs/reference/generated/scipy.io.wavfile.write.html#scipy.io.wavfile.write