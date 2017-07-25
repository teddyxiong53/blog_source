---
title: Linux命令之开关机
date: 2017-07-24 22:57:08
tags:

	- Linux命令

---

Linux开关机相关的命令，有下面这5个：reboot、shutdown、poweroff、halt、init。

reboot和poweroff

一些典型用法如下：

# 1.  shutdown

```
# 马上关机，这个h表示halt的含义
$ shutdown -h now 
# 马上重启
$ shutdown -r now
```

# 2. halt

```
# 关机
$ halt -p
# 关机但是不留下关机记录
$ halt -d
# 只写关机记录，但是不关机
$ halt -w

```

# 3. init

```
# 关机
$ init 0
# 重启
$ init 6
```



其实，poweroff和halt、reboot就是同一个程序。你可以用diff程序比较一下这2个程序，可以到是一样的。但是执行他们的时候，他们表现看起来是不一样的。为什么会这样呢？

这里就涉及到Linux里一种常见的玩法。就是把代码逻辑大体相同的程序融合成一个文件，然后在代码里，根据argv[0]来判断处理。

