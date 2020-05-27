---
title: Linux之mplayer
date: 2020-05-27 11:37:08
tags:
	- Linux

---

1

大部分视频和音频格式都能通过FFmpeg项目的libavcodec函数库本地支持。对于那些没有开源解码器的格式，MPlayer使用二进制的函数库。它能直接使用Windows的DLL。专有的CSS解析软件和相关格式使MPlayer成为被众多开放源代码播放器所使用的后端。



mplayer是需要占用console的。直接加`&`的方式，会无法运行。

```
[1]+  Stopped (tty output)       mplayer https://applink.dossav.com/nfs/a.mp3 -novideo -channels 2 -srate 48000 -af format=s16le -ao pcm:file=/tmp/snapfifo
```

这样就可以了：

```
mplayer [你的参数] < /dev/null > /dev/null 2>1&
```



参考资料

1、官网

http://www.mplayerhq.hu/design7/news.html

2、关于mplayer如何在后台播放的问题

https://blog.csdn.net/luo964061873/article/details/8119839