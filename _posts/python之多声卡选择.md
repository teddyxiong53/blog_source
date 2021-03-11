---
title: python之多声卡选择
date: 2021-03-10 13:22:51
tags:
	- python

---

--

用sounddevice这个库。

遍历电脑上的声卡设备。

```
import sounddevice
print(sounddevice.query_devices())
```



插入usb音箱之前

```
   0 Microsoft 声音映射器 - Input, MME (2 in, 0 out)
>  1 立体声混音 (Realtek High Defini, MME (2 in, 0 out)
   2 Microsoft 声音映射器 - Output, MME (0 in, 2 out)
<  3 Realtek Digital Output (Realtek, MME (0 in, 2 out)
   4 主声音捕获驱动程序, Windows DirectSound (2 in, 0 out)
   5 立体声混音 (Realtek High Definition Audio), Windows DirectSound (2 in, 0 out)
   6 主声音驱动程序, Windows DirectSound (0 in, 2 out)
   7 Realtek Digital Output (Realtek High Definition Audio), Windows DirectSound (0 in, 2 out)
   8 Realtek Digital Output (Realtek High Definition Audio), Windows WASAPI (0 in, 2 out)
   9 立体声混音 (Realtek High Definition Audio), Windows WASAPI (2 in, 0 out)
  10 Speakers (Realtek HD Audio output), Windows WDM-KS (0 in, 8 out)
  11 线路输入 (Realtek HD Audio Line input), Windows WDM-KS (2 in, 0 out)
  12 麦克风 (Realtek HD Audio Mic input), Windows WDM-KS (2 in, 0 out)
  13 SPDIF Out (Realtek HDA SPDIF Out), Windows WDM-KS (0 in, 2 out)
  14 立体声混音 (Realtek HD Audio Stereo input), Windows WDM-KS (2 in, 0 out)
```

带> 的表示默认的输入设备。

带<表示默认的输出设备。

插入usb音箱后，再执行

```
   0 Microsoft 声音映射器 - Input, MME (2 in, 0 out)
>  1 麦克风 (Vmeet200), MME (2 in, 0 out)
   2 立体声混音 (Realtek High Defini, MME (2 in, 0 out)
   3 Microsoft 声音映射器 - Output, MME (0 in, 2 out)
<  4 扬声器 (Vmeet200), MME (0 in, 2 out)
   5 Realtek Digital Output (Realtek, MME (0 in, 2 out)
   6 主声音捕获驱动程序, Windows DirectSound (2 in, 0 out)
   7 麦克风 (Vmeet200), Windows DirectSound (2 in, 0 out)
   8 立体声混音 (Realtek High Definition Audio), Windows DirectSound (2 in, 0 out)
   9 主声音驱动程序, Windows DirectSound (0 in, 2 out)
  10 扬声器 (Vmeet200), Windows DirectSound (0 in, 2 out)
  11 Realtek Digital Output (Realtek High Definition Audio), Windows DirectSound (0 in, 2 out)
  12 Realtek Digital Output (Realtek High Definition Audio), Windows WASAPI (0 in, 2 out)
  13 扬声器 (Vmeet200), Windows WASAPI (0 in, 2 out)
  14 麦克风 (Vmeet200), Windows WASAPI (1 in, 0 out)
  15 立体声混音 (Realtek High Definition Audio), Windows WASAPI (2 in, 0 out)
  16 Speakers (Realtek HD Audio output), Windows WDM-KS (0 in, 8 out)
  17 线路输入 (Realtek HD Audio Line input), Windows WDM-KS (2 in, 0 out)
  18 麦克风 (Realtek HD Audio Mic input), Windows WDM-KS (2 in, 0 out)
  19 SPDIF Out (Realtek HDA SPDIF Out), Windows WDM-KS (0 in, 2 out)
  20 立体声混音 (Realtek HD Audio Stereo input), Windows WDM-KS (2 in, 0 out)
  21 扬声器 (Vmeet200), Windows WDM-KS (0 in, 2 out)
  22 麦克风 (Vmeet200), Windows WDM-KS (1 in, 0 out)
```

可以看到输入输出默认都切换到usb音箱上了。

现在需要让默认的输出设备，还是电脑自带的（通过耳机线连接来播放）

应该怎么操作？

还有说可以在pyaudio接口指定index的。



```
import pyaudio

pa = pyaudio.PyAudio()
res = pa.get_default_host_api_info()
print(res)
```

这个的输出

```
{'index': 0, 'structVersion': 1, 'type': 2, 'name': 'MME', 'deviceCount': 6, 'defaultInputDevice': 1, 'defaultOutputDevice': 4}
```

pyaudio认为是有6个设备，默认输入设备是1，默认输出设备是4

这个跟上面sounddevice看到的是一样的。

把pyaudio所有的设备信息打印出来看看。

```
import pyaudio

pa = pyaudio.PyAudio()
count = pa.get_device_count()
for i in range(count):
    res = pa.get_device_info_by_index(i)
    print("{}:{}".format(i, res))
```

输出：

```
0:{'index': 0, 'structVersion': 2, 'name': 'Microsoft ÉùÒôÓ³ÉäÆ÷ - Input', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
1:{'index': 1, 'structVersion': 2, 'name': 'Âó¿Ë·ç (Vmeet200)', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
2:{'index': 2, 'structVersion': 2, 'name': 'Á¢ÌåÉù»ìÒô (Realtek High Defini', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
3:{'index': 3, 'structVersion': 2, 'name': 'Microsoft ÉùÒôÓ³ÉäÆ÷ - Output', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
4:{'index': 4, 'structVersion': 2, 'name': 'ÑïÉùÆ÷ (Vmeet200)', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
5:{'index': 5, 'structVersion': 2, 'name': 'Realtek Digital Output (Realtek', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
```

把输出设备罗列出来。

没有专门的接口。

```
output_device_index – Index of Output Device to use. Unspecified (or None) uses the default device. Ignored if output is False.
```

我觉得默认的输出声卡，应该是在没有插入usb时的最后一个设备。

不管什么情况下，都取index最大的那个，就一定是系统自带的那个声卡？



参考资料

1、

https://stackoverflow.com/questions/36894315/how-to-select-a-specific-input-device-with-pyaudio

2、pyaudio文档

https://people.csail.mit.edu/hubert/pyaudio/docs/#class-stream