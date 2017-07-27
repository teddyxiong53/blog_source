---
title: Ubuntu之source.list写法
date: 2017-07-28 00:41:32
tags:

	- Ubuntu

---

安装了Ubuntu的第一件事情往往就是该source.list了。那么这个文件的写法格式要求是怎样的呢？

我现在以我的树莓派上的配置为例来讲解。

```
pi@raspberrypi:~/work/test/python$ cat /etc/apt/sources.list
deb http://mirrors.aliyun.com/raspbian/raspbian jessie main contrib non-free rpi
deb-src http://mirrors.aliyun.com/raspbian/raspbian jessie main contrib non-free rpi
```

我这个是很简单的。只有两行，一行是deb，代表软件的位置，一行是deb-src，代表源码的位置。都是指向了阿里云的镜像，这样国内下载软件就比较快。后面的内容是一样的。



`http://mirrors.aliyun.com/raspbian/raspbian`这个链接，用浏览器打开，可以看到下面有个dists目录和pool目录。



