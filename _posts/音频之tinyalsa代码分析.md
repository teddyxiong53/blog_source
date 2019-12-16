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

utils目录下有5个文件，对应了5个工具：

```
tinycap.c  
tinymix.c  
tinypcminfo.c  
tinyplay.c  
tinywavinfo.c
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
alsa-lib就是调用了ioctl的。

snd_pcm_writei()-->snd_pcm_hw_writei(alsa-lib-1.1.3/src/pcm/pcm_hw.c)-->ioctl(fd, SNDRV_PCM_IOCTL_WRITEI_FRAMES, &xferi)调进内核
```



# tinyalsa跟alsa-lib的关系

tinyalsa借用了alsa-lib的一些头文件，主要是一些结构体和宏定义，没有链接alsa-lib的库。



# tinyplay

```
/ # tinyplay                                                        
usage: tinyplay file.wav [options]                                  
options:                                                            
-D | --card   <card number>    The device to receive the audio      
-d | --device <device number>  The card to receive the audio        
-p | --period-size <size>      The size of the PCM's period         
-n | --period-count <count>    The number of PCM periods            
-i | --file-type <file-type >  The type of file to read (raw or wav)
-c | --channels <count>        The amount of channels per frame     
-r | --rate <rate>             The amount of frames per second      
-b | --bits <bit-count>        The number of bits in one sample     
-M | --mmap                    Use memory mapped IO to play audio   
```

基本测试：

```
tinycap 1.wav
# 录音3秒，按ctrl+c停掉。
# 不带任何参数播放。
tinyplay 1.wav 
```



# tinypcminfo

```
/userdata # tinypcminfo                      
Info for card 0, device 0:                   
                                             
PCM out:                                     
      Access:   0x000009                     
   Format[0]:   0x000444                     
   Format[1]:   00000000                     
 Format Name:   S16_LE, S24_LE, S32_LE       
   Subformat:   0x000001                     
        Rate:   min=8000Hz      max=192000Hz 
    Channels:   min=2           max=2        
 Sample bits:   min=16          max=32       
 Period size:   min=32          max=65536    
Period count:   min=2           max=4096     
                                             
PCM in:                                      
      Access:   0x000009                     
   Format[0]:   0x000444                     
   Format[1]:   00000000                     
 Format Name:   S16_LE, S24_LE, S32_LE       
   Subformat:   0x000001                     
        Rate:   min=8000Hz      max=192000Hz 
    Channels:   min=2           max=8        
 Sample bits:   min=16          max=32       
 Period size:   min=8           max=65536    
Period count:   min=2           max=16384    
```

# tinywavinfo

这个是查看wav文件的信息。

# tinymix

```
/userdata # tinymix --help                                                 
usage: tinymix [options] <command>                                         
options:                                                                   
        -h, --help        : prints this help message and exists            
        -v, --version     : prints this version of tinymix and exists      
        -D, --card NUMBER : specifies the card number of the mixer         
commands:                                                                  
        get NAME|ID       : prints the values of a control                 
        set NAME|ID VALUE : sets the value of a control                    
        controls          : lists controls of the mixer                    
        contents          : lists controls of the mixer and their contents 
```



总的代码量其实不大。



参考资料

1、alsa-lib应用层接口分析

https://blog.csdn.net/yuhuqiao/article/details/82785234