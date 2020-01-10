---
title: gstreamer之gst-launch使用
date: 2018-11-12 11:43:19
tags:
	- 视频
---



可以不用任何C代码，用命令行工具，就可以建立一个pipeline。

工具有：

1、gst-launch。在命令行快速建立一个pipeline。

2、gst-inspect。用来查询各个插件Element的详细信息。

3、gst-discoverer



# gst-launch

可以让你在写c代码之前，快速验证一下pipeline的可行性。

只能建立简单的pipeline。

这个只能用来调试，不能用在正式的代码里。

从最简单的开始。

**管道元件之间，用感叹号进行连接。之所以使用感叹号，因为它看起来跟管道符比较像。**

显示笔记本的摄像头数据。

```
gst-launch-1.0 v4l2src ! xvimagesink
```

xvimagesink和ximagesink的不同：

ximagesink只支持rgb，不支持yuv。

所以还是用xvimagesink比较好。

设置一下参数，我的笔记本会失败。因为不支持帧率设置。去掉framerate=15/1就可以了。

```
gst-launch-1.0 v4l2src ! video/x-raw,format=YUY2,width=640,height=480,framerate=15/1 ! queue2 ! videorate ! videoscale ! videoconvert ! xvimagesink
```

**queue2插件**

简单的数据队列。属于core element。在libgstcoreelements.so文件里。

有src和sink。可接收的数据类型都是any的。

**videorate插件**

这个是通过操作时间戳来达到目的的。

对应的文件是libgstvideorate.so。属于base插件。

可以接收的能力（输出的能力也是一样的）

```
video/x-raw
video/x-bayer
image/jpge
image/png
```

**videoconvert**

这个是进行color space转化的。



可以给元件命名。规则是name=xx

后面使用的时候，在xx后面跟一个点号就可以了。

```
gst-launch-1.0 videotestsrc ! videoconvert ! tee name=t ! queue ! autovideosink t. ! queue ! autovideosink
```

这个的效果是产生2个一样的窗口，都是播放彩色条纹。

```
gst-launch-1.0 souphttpsrc location=https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm ! matroskademux name=d d.video_00 ! matroskamux ! filesink location=sintel_video.mkv
```

```
gst-launch-1.0 souphttpsrc location=https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm ! matroskademux name=d d.audio_00 ! vorbisparse ! matroskamux ! filesink location=sintel_audio.mka
```

播放一个mp3文件

```
 gst-launch-1.0 filesrc location="1.mp3" ! decodebin ! alsasink
```



参考资料

1、GStreamer基础教程10——GStreamer工具

https://blog.csdn.net/sakulafly/article/details/21455637

2、Read and write raw PCM using GStreamer

https://blog.csdn.net/brandon2015/article/details/50457900

3、xvimagesink

https://gstreamer.freedesktop.org/documentation/xvimagesink/index.html?gi-language=c

4、常见gstreamer pipeline 命令

https://blog.csdn.net/songwater/article/details/34800017

5‘、使用 GStreamer 进行多用途的多媒体处理

https://www.ibm.com/developerworks/cn/aix/library/au-gstreamer.html