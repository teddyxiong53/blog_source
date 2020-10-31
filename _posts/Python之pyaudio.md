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

# 主要类分析

文件在：

```
/usr/lib/python2.7/dist-packages/pyaudio.py
```

文件大概1000行。

属于pyaudio的东西有：

主要的类有2个：

1、PyAudio。

2、Stream。

主要方法有：

1、获取版本号的。

```
import pyaudio,os,sys
print pyaudio.get_portaudio_version()
print pyaudio.get_portaudio_version_text()
```

运行：

```
1899
PortAudio V19-devel (built Aug 11 2015 07:04:06)
```

采样格式有：

paFloat32

paUint8

paInt32

错误码有：

paNoError

paNotInitialized

回调函数的返回值有：

paContinue

paComplete

paAbort。

代码：

```
import pyaudio,os,sys
print pyaudio.get_sample_size(pyaudio.paInt8)
print pyaudio.get_sample_size(pyaudio.paFloat32)
```

运行：

```
teddy@teddy-ThinkPad-SL410:~/work/test/audio$ python test.py 
1
4
```



## PyAudio

提供了方法：

1、init和terminate

2、open和close一个stream。

3、查询host api。

4、查询audio devices。

我在我的笔记本上一个个接口来测试一下。

### get_default_host_api_info

代码：

```
import pyaudio,os,sys
pa = pyaudio.PyAudio()
print pa.get_default_host_api_info()
```

运行：

```
{'index': 0L, 'name': u'ALSA', 'defaultOutputDevice': 10L, 'type': 8L, 'deviceCount': 11L, 'defaultInputDevice': 10L, 'structVersion': 1L}
```

### get_default_input_device_info

代码：

```
import pyaudio,os,sys
pa = pyaudio.PyAudio()
print pa.get_default_input_device_info()
```



运行：

```
{'defaultSampleRate': 44100.0, 'defaultLowOutputLatency': 0.008707482993197279, 'defaultLowInputLatency': 0.008707482993197279, 'maxInputChannels': 32L, 'structVersion': 2L, 'hostApi': 0L, 'index': 10L, 'defaultHighOutputLatency': 0.034829931972789115, 'maxOutputChannels': 32L, 'name': u'default', 'defaultHighInputLatency': 0.034829931972789115}
```

### get_default_output_device_info

代码：

```
import pyaudio,os,sys
pa = pyaudio.PyAudio()
print pa.get_default_output_device_info()
```



运行：

```
{'defaultSampleRate': 44100.0, 'defaultLowOutputLatency': 0.008707482993197279, 'defaultLowInputLatency': 0.008707482993197279, 'maxInputChannels': 32L, 'structVersion': 2L, 'hostApi': 0L, 'index': 10L, 'defaultHighOutputLatency': 0.034829931972789115, 'maxOutputChannels': 32L, 'name': u'default', 'defaultHighInputLatency': 0.034829931972789115}
```



###get_host_api_count

代码：

```
import pyaudio,os,sys

pa = pyaudio.PyAudio()

print pa.get_host_api_count()
```

运行情况：

```
teddy@teddy-ThinkPad-SL410:~/work/test/audio$ python test.py 
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
2
```

我当前的默认录音设备是外部的一个usb摄像头。

可以看到是2个

### get_device_info_by_index

代码：

```
import pyaudio,os,sys

pa = pyaudio.PyAudio()

for i in range(pa.get_host_api_count()):
	print pa.get_device_info_by_index(i)
```

运行：

```
{'defaultSampleRate': 44100.0, 'defaultLowOutputLatency': 0.005804988662131519, 'defaultLowInputLatency': 0.005804988662131519, 'maxInputChannels': 2L, 'structVersion': 2L, 'hostApi': 0L, 'index': 0, 'defaultHighOutputLatency': 0.034829931972789115, 'maxOutputChannels': 2L, 'name': u'HDA Intel: ALC269 Analog (hw:0,0)', 'defaultHighInputLatency': 0.034829931972789115}
{'defaultSampleRate': 44100.0, 'defaultLowOutputLatency': 0.005804988662131519, 'defaultLowInputLatency': -1.0, 'maxInputChannels': 0L, 'structVersion': 2L, 'hostApi': 0L, 'index': 1, 'defaultHighOutputLatency': 0.034829931972789115, 'maxOutputChannels': 8L, 'name': u'HDA ATI HDMI: 0 (hw:1,3)', 'defaultHighInputLatency': -1.0}
```

## Stream类

PyAudio的open方法，返回的就是一个Stream对象。



# windows下安装

windows下安装，还不是一件容易的事情。

因为需要编译。

用pipwin来安装反而是比较快的。

```
pip install pipwin
pipwin install pyaudio
```



# 参考资料

1、PyAudio 官网

http://people.csail.mit.edu/hubert/pyaudio/

http://people.csail.mit.edu/hubert/pyaudio/docs/