---
title: 树莓派之fswebcam
date: 2017-08-02 22:35:01
tags:

	- 树莓派

	- fswebcam

---

先看看帮助信息。梳理出其中有用的部分。

1、fswebcam只能用来拍照，不能产生持续的码流，也就是不能录像。

2、一般的用途是：定时抓拍，然后把图片上传到云端，这样来做一个简单的监控。

`-c`选项可以用一下，这样配置文件改起来比较方便。

新建一个fswebcam.conf文件。内容如下：

```
device /dev/video0
input 0
loop 15
skip 20
background
resolution 640x480
set brightness=60%
set contrast=13%
jpeg 95
save ./xxx.jpg
palette MJPEG
```

上面这份配置文件拍不出照片，但是可以作为一个格式的样板。

以daemon模式运行后，要杀死进程，用`killall fswebcam`来做。

默认情况下，照片下面会带一行banner，是个时间戳。

常用的命令如下：

1、指定拍照的名字，以时间命名。

```
 fswebcam -d /dev/video0  ./`date "+%Y-%m-%d_%H-%M-%S"`.jpg
```







