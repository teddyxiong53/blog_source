---
title: 音频之portaudio代码分析
date: 2021-10-14 10:24:33
tags:
	- 音频

---

--

alsa接口来写，还是比较繁琐。所以还是研究一下portaudio，把这个库研究透彻。

官网：

http://www.portaudio.com/

pa_stable_v190600_20161030

V19 版本

执行configure：

```
Configuration summary:

  Target ...................... x86_64-unknown-linux-gnu
  C++ bindings ................ no  为了编译c++的接口。
  Debug output ................ no  

  ALSA ........................ yes
  ASIHPI ...................... no

  OSS ......................... yes
  JACK ........................ yes
```

使用回调技术来编写portaudio应用的步骤

1、写一个回调函数，给portaudio在需要处理音频的时候调用。

2、初始化pa库，打开一个stream，做audio io操作。

3、start stream

4、在回调函数里，需要对音频数据进行读写操作。

5、如果你在回调函数里返回1，那么就会触发stop stream。你可以可以另外调用stop函数。

6、关闭stream。

除了这种回调方式外，V19还支持阻塞方式。

下面看看怎么用回调的方式来播放锯齿波，对应的代码是paex_saw.c。

需要包含头文件：

```
#include "portaudio.h"
```

这个头文件里的内容：

```
大概1200行。
枚举
	错误码：0表示支持，错误从-10000开始。
结构体

函数
	初始化：Pa_Initialize
	结束：Pa_Terminate
	
```

hostapi是什么？

应该是指底层的支持的库，因为有个枚举PaHostApiTypeId

包括了：

```
    paOSS=7,
    paALSA=8,
```

以paex_saw.c为例进行分析

PaStream结构体

```
这个实际不是结构体。
typedef void PaStream;
都是指针方式来用，相当于void *指针。
```

```
//1、初始化
Pa_Initialize();
//2、打开stream
Pa_OpenDefaultStream
//3、start stream
Pa_StartStream
//4、等待一下
Pa_Sleep
//5、停止stream
Pa_StopStream
//6、关闭stream
Pa_CloseStream
//7、结束pa
Pa_Terminate
```

src/hostapi/alsa/pa_linux_alsa.c分析

大概4600行代码。



注册stream结束时的回调

```
Pa_SetStreamFinishedCallback( stream, &StreamFinished );
```



pyaudio



参考资料

1、官网教程

http://files.portaudio.com/docs/v19-doxydocs/writing_a_callback.html