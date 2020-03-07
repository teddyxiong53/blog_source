---
title: ffprobe（1）
date: 2020-03-04 11:25:28
tags:
	- 音视频

---

1

ffprobe主要是用来查看多媒体文件的信息。

```
ffprobe -show_packets 1.aac
```

```
ffprobe -show_data 1.mp4
```

```
ffprobe -show_format 1.mp4
```

```
ffprobe -show_frames 1.mp4
```

```
ffprobe -show_streams 1.mp4
```

指定输出的格式：可以是xml、json、ini、csv。

```
ffprobe -of json -show_streams 1.mp4
```

这样来查看rtmp的，来确认数据是否正常。

```
ffprobe rtmp://172.16.4.205:1935/alive/test
```

查看alsa的信息。

```
ffprobe -f alsa default
```







参考资料

1、ffprobe常用命令

https://www.jianshu.com/p/e14bc2551cfd

2、[总结]FFMPEG命令行工具之ffprobe详解

https://blog.csdn.net/ice_ly000/article/details/87870446