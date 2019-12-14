---
title: 音频之tinyalsa代码分析
date: 2019-12-13 16:25:25
tags:
	- 音频

---

1

tinyalsa的代码量不大，可以读一下。

看顶层Makefile。

```
all:
	$(MAKE) -C src
	$(MAKE) -C utils
	$(MAKE) -C doxygen
	$(MAKE) -C examples
```

主要代码在src目录，工具的代码在utils目录。

还有例子。

```
install include/tinyalsa/pcm.h $(DESTDIR)$(INCDIR)/
	install include/tinyalsa/mixer.h $(DESTDIR)$(INCDIR)/
	install include/tinyalsa/asoundlib.h $(DESTDIR)$(INCDIR)/
	install include/tinyalsa/version.h $(DESTDIR)$(INCDIR)/
```

主要的头文件，就是4个。

pcm.h

mixer.h

asoundlib.h

version.h

utils目录下有5个文件，对应了4个工具：

```

```

我们先看tinycap。

从名字看，这个工具就是用来录音的。

基本用法

```
tinycap xx.wav
```

可以带的参数有：

```
-D card -d device -c channels -r rate -b bits -p period_size -n n_periods -t time_in_sec
```

card和device都是0这样的数字描述的。

录音测试一下

```
/userdata # tinycap 1.wav                  
Capturing sample: 2 ch, 48000 hz, 16 bit   
^CCaptured 151576 frames                   
```

默认是双通道，48K，16bit。

录音正常。

看看代码。

```
tinycap -- 
```

表示把录音数据输出到stdout。打印出来全是乱码。不知道这个什么场景下需要使用。

主要就是capture_sample这个函数里在工作。这个函数是阻塞的。

```
capture_sample
	pcm_open(0, 0,)//传递设备的硬件号进行，还有配置信息。
		这样打开/dev/snd/pcmC%uD%u%c设备的。
		然后是调用alsa-lib的函数。进行设置。
	while (capturing) {
        frames_read = pcm_readi(pcm, buffer, pcm_get_buffer_size(pcm));
        靠这里持续录音。
    sigint，把capturing设置为0。这样来跳出循环。
```

整体逻辑还是比较简单的。

但是对pcm相关函数的使用，跟我们一般的用法不相同。

```
是打开/dev/snd/pcmC%uD%u%c 这样的设备节点。
我之前看到的代码，都是打开"default"或者"hw:0，0"这样的。
操作上，都是使用了ioctl来操作fd的。包括读取音频数据。
```

