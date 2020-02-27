---
title: ffmpeg之ffserver用法
date: 2020-02-25 09:47:40
tags:
	- 视频

---

1

ffserver可以用来做流媒体服务器。

最简单的用法，就是直接ffserver，不带任何参数。

默认使用配置文件/etc/ffserver.conf。

调试时，可以加上-d选项。表示debug。

步骤1：启动ffserver。

视频的参数设置，是用v4l-ctl --all查看出来的。

需要修改/etc/ffserver.conf，因为里面默认是把视频的帧率配置为3fps的。如果以这个来启动，会报错。提示不支持这个帧率。修改为30fps。

```
ffserver -d
```



步骤2：启动视频采集和声音采集。推送到一个http目标地址上。

```
ffmpeg \
	-f v4l2 -s 320x240 -r 30 -i /dev/video0 \
	-f alsa -ac 2 -i hw:0 \
	http://localhost:8090/feed1.ffm
```



步骤3：点播播放地址.

```
ffplay http://localhost:8090/test1.mpg
```

虽然没有报错，但是没有效果出来。

我需要把步骤2的ffmpeg进程停掉，才能在ffplay这边看到界面。





参考资料

1、

https://trac.ffmpeg.org/wiki/ffserver