---
title: Python之pyaudio
date: 2017-11-22 10:34:07
tags:
	- Python
	- pyaudio

---



看叮当的代码，用到了pyaudio这个东西。了解一下具体实用方法。



# 概述

pyaudio是PortAudio的Python库。



用pyaudio可以进行录像、播放、生成wav文件这些操作。

测试环境：

1、树莓派3

2、usb摄像头带录音功能。

3、外接3.5mm音箱。



主要类有两个，PyAudio和Stream。

## PyAudio类

可以做的事情：

1、初始化和结束PortAudio。

2、open和close Stream。

3、查询可用的PortAudio的API

4、查询可用的PortAudio设备。



# 先看播放

```
#!/usr/bin/python

import pyaudio,wave, sys

CHUNK = 1024
wf = wave.open("./test.wav", "rb") 

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	channels=wf.getnchannels(),
	rate=wf.getframerate(),
	output=True)
data = wf.readframes(CHUNK)
while data != '':
	stream.write(data)
	data = wf.readframes(CHUNK)
stream.stop_stream()
stream.close()
p.terminate()

```

我用arecord录音得到一个5s的文件，用这个脚本测试，正常。

注意上面那个output=True，说明是播放，如果是input=True，那么就是录音了。

# 录音

```
#!/usr/bin/python 

import wave
import pyaudio,sys

CHUNK

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
	channels=2,
	rate=44100,
	input=True,
	frames_per_buffer=1024
	)
	
frames=[]
# record for 5 seconds
SECS=5
for i in range(0, 44100/1024 * SECS):
	data = stream.read(1024)
	frames.append(data)
	
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("./output.wav", 'wb')
wf.setnchannels(2)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b''.join(frames))
wf.close()
```

# 在input和output之间建立连接

效果就是边录变播。

```
#!/usr/bin/python 

import wave
import pyaudio,sys

CHUNK

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
	channels=2,
	rate=44100,
	input=True,//关键是这里，都是True。
	output=True,
	frames_per_buffer=1024
	)
	
frames=[]
# record for 5 seconds
SECS=5
for i in range(0, 44100/1024 * SECS):
	data = stream.read(1024)
	frames.append(data)
	
stream.stop_stream()
stream.close()
p.terminate()

```

# callback版本的播放wav文件

```
#!/usr/bin/python

import pyaudio,wave, sys, time

CHUNK = 1024
wf = wave.open("./test.wav", "rb") 

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
	data = wf.readframes(frame_count)
	return (data, paudio.paContinue)
	
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	channels=wf.getnchannels(),
	rate=wf.getframerate(),
	output=True，
	stream_callback=callback
	)
stream.start_stream()
while stream.is_active():
	time.sleep(1)
	
stream.stop_stream()
stream.close()
wf.close()
p.terminate()

```



# 参考资料

1、PyAudio 官网

http://people.csail.mit.edu/hubert/pyaudio/