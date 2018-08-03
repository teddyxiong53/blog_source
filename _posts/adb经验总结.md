---
title: adb经验总结
date: 2018-07-18 19:10:28
tags:
	- Linux

---



开发中，会用到adb。把碰到的问题和解决方法记录下来。



## adb乱码问题解决

https://www.cnblogs.com/xilifeng/archive/2013/03/15/2961456.html



## 在bat文件里使用adb

test.bat内容：

```
adb shell < cmd.txt
```

在cmd.txt里写入需要执行的命令。

## Windows下adb shell使用有问题

有这些问题：

1、vi不能用。

2、adb shell里不能tab补全。

下载这个adb专用的putty就可以了。

https://github.com/sztupy/adbputty/downloads

hostname那里填写：transport-usb 。连接类型选择：adb。

这样就可以正常使用了。

## 后台有程序运行，无法exit

exit提示

```
/data/doss # exit
You have stopped jobs.
```

只需要把后台的杀掉就好了。

```
/data/doss # kill %1
[1]+  Terminated                 tail -f wakeup.log
```



