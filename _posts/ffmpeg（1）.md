---
title: ffmpeg（1）
date: 2018-08-11 15:11:40
tags:
	- 视频

---

1

ffmpeg是包括：

1、录制。

2、转换。

3、音视频编解码。

是一个完整的开源解决方案。

支持40多种编码，90多种解码。

包括：

```
libavformat
	音视频文件的封装和解封装。
libavdevice
	对输入输出设备的支持。
libavcodec
	编解码。
libavutil
	工具函数。
libswscale
	缩放。
libpostproc
	后期效果处理。
libavresample
	重采样。
libswresample
	
```



AVPacket：解码前的数据，例如AAC、H264数据。

AVFrame：解码后的数据，例如RGB、pcm数据。



下载代码，编译。

```
git clone https://git.ffmpeg.org/ffmpeg.git
```



```
./configure 
```

提示：

```
nasm/yasm not found or too old. Use --disable-x86asm for a crippled build.
```

安装nasm就好了。







# 参考资料

1、FFMpeg框架代码阅读

https://www.cnblogs.com/azraelly/archive/2012/12/30/2840133.html

2、FFmpeg源代码结构图

https://www.cnblogs.com/x_wukong/p/4864863.html

3、多媒体文件格式探测⑨

https://www.cnblogs.com/tocy/p/media_container_9-probe-utility.html