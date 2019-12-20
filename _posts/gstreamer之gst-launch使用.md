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



```
gst-launch-1.0 videotestsrc ! xvimagesink
```

xvimagesink

渲染视频帧到一个本地显示，用XVideo插件。

管道元件之间，用感叹号进行连接。之所以使用感叹号，因为它看起来跟管道符比较像。

还可以这样：

```
gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink
```

效果跟上面是一样的。都是弹出一个小窗口，播放彩色条纹。

可以通过property=value的方式，进行属性设置，多个属性之间用空格隔开。

```
gst-launch-1.0 videotestsrc pattern=11 ! videoconvert ! autovideosink
```

这个是显示一个同心圆的画面。

要知道某个element的属性有哪些，可以用gst-inspect-1.0 xx来查看。



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