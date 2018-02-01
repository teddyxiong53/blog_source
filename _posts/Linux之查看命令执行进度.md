---
title: Linux之查看命令执行进度
date: 2018-02-01 10:56:55
tags:
	- Linux

---



Linux里很多命令都没有执行进度提示，这个是很折磨人的。不过有大神已经提供了工具了。

地址在这里：https://github.com/Xfennec/progress.git

```
git clone https://github.com/Xfennec/progress.git
make
make install
```

我使用了一下，感觉体验不太好。对于目录拷贝。

继续找。

看到说pycp可以。

还有用scp的，这样做：

```
scp -r ./ pi@127.0.0.1:/mnt
```

这样做确实是最简单好用的。



