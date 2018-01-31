---
title: Linux之cloud-lab（三）kernel调试
date: 2018-01-30 22:56:25
tags:
	- Linux系统

---



看kernel代码，还是用gdb调试着看会比较好。

1、配置内核。把CONFIG_DEBUG_INFO打开。重新编译内核。

2、make boot DEBUG=1，然后当前的命令行窗口会卡住。

3、我们另外开一个命令行窗口。输入：

```
arm-linux-gnueabi-gdb /labs/linux-lab/output/arm/linux-v4.6.7-vexpress-a9/vmlinux
```

这个会读取当前目录下的.gdbinit文件。当前目录是/labs/linux-lab。

这个gdbinit做了这些事情：

```
1、sleep两秒。不知道为什么要来这么一下。
2、在start_kernel那里下个断点。
3、在timer_init那里下断点。
4、在do_fork下断点。
5、target remote :1234
6、输入了几次c，
```

这个对我来说，不是很妥当。

我只需要再start_kernel那里停住就好了。后面我手动走。

改一下。只留这些。

```
python import time; print "\nWaiting for 2 secs..."; time.sleep(2)
python print "\nExecuting gdb commands in local .gdbinit ..."

python print "\n(gdb) break start_kernel"
break start_kernel

python import time; time.sleep(1)
python print "\n(gdb) target remote :1234"
target remote :1234
```

启动调试，出错。

