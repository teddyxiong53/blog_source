---
title: Python之pyaudio
date: 2017-11-22 10:34:07
tags:
	- Python
	- pyaudio

---



看叮当的代码，用到了pyaudio这个东西。了解一下具体实用方法。



# 概述

用pyaudio可以进行录像、播放、生成wav文件这些操作。

测试环境：

1、树莓派3

2、usb摄像头带录音功能。

3、外接3.5mm音箱。

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

