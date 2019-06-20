---
title: 音频之jack
date: 2019-06-20 16:48:37
tags:
	- 音频
---

1

在Linux的音频架构里，为了混音，一般是有一个音频守护进程。

例如pulseaudio就是这样一个守护进程。

jackd也是一个类似的程序。但是是对于音乐制作这种专业场景的。

当前我的笔记本上，默认运行了pulseaudio。

jackd也是安装了的。如果没有安装，这样安装：

```
sudo apt-get install jackd 
```

还需要安装另外一个软件：

```
sudo apt-get install qjackctl
```

你需要把自己添加到audio这个组。

查看自己当前在哪些组里。

```
$ groups teddy
teddy : teddy adm dialout cdrom sudo dip plugdev lpadmin sambashare
```

并没有在audio这个组里。

加入到这个组。

```
sudo usermod -a -G audio teddy
```

还需要注销一下才能生效。

# 和pulseaudio的共存

当你启动jackd之后，声卡就被jackd独占了。

而你的浏览器等的声音，是靠pulseaudio来工作的。pulseaudio是gnome桌面默认的声音服务器。

需要想办法让jackd跟pulseaudio共存。

```
sudo apt-get install pulseaudio-module-jack
```





参考资料

1、关于linux音频JACK的那些事情……

https://blog.csdn.net/zhang_danf/article/details/25405381

2、漫谈Linux下的音频问题

https://www.cnblogs.com/little-ant/p/4016172.html