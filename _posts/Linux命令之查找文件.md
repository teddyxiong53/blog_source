---
title: Linux命令之查找文件
date: 2017-09-21 22:16:58
tags:
	- Linux命令

---



# 1. find

find是最基础也是最常用的，但是Linux其实还有其他的命令可用。



# 2. locate

locate相当于`find -name`。但是又不一样。它不搜索具体的目录，而是搜索一个数据库，数据库是/var/lib/locatedb。这个数据库含有本地所有文件信息，Linux会自动创建这个数据库，并且每天更新一次。

我在我的树莓派上运行了一下，是这样。

```
pi@raspberrypi:~$ locate mosquitto*
locate: warning: database `/var/cache/locate/locatedb' is more than 8 days old (actual age is 47.3 days)
pi@raspberrypi:~$ 
```

需要手动触发一次数据库更新：`sudo updatedb`。

再试。

```
pi@raspberrypi:~$ locate xhl
/home/pi/work/linux_src/linux-rpi-4.4.y/arch/arm/boot/dts/kirkwood-lsxhl.dts
pi@raspberrypi:~$ 
```

# 3. whereis

whereis只能搜索程序。

```
pi@raspberrypi:~$ whereis sh
sh: /bin/sh.distrib /bin/sh /usr/share/man/man1/sh.1.gz
pi@raspberrypi:~$ 
```



# 4. which

只能搜索PATH路径下的可执行程序，而且只返回第一个结果。



# 5. type

看结果就知道是什么意思了。

相当于把名字的具体内容输出给你看。

```
sh is /bin/sh
pi@raspberrypi:~$ type grep
grep is aliased to `grep --color=auto'
pi@raspberrypi:~$ 
```

