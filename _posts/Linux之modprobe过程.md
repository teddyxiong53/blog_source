---
title: Linux之modprobe过程
date: 2018-04-05 21:39:55
tags:
	- Linux

---



我要在mylinuxlab上使用modprobe，是插入usb相关的模块，有依赖关系。

然后是不成功。我希望把mylinuxlab里的这个功能完善一下。

现在的关键是，modprobe的工作过程是怎么样的？

```
/ko # modprobe -c
modprobe: can't change directory to '/lib/modules': No such file or directory
```

首先，是对/lib/modules这个目录有依赖。

我先看看树莓派上的这个目录是怎么样的。

```
pi@raspberrypi:/lib/modules/4.14.24+$ ls -lh
total 1.9M
drwxr-xr-x 11 root root 4.0K Mar  9 23:35 kernel
-rw-r--r--  1 root root 489K Mar  9 23:36 modules.alias
-rw-r--r--  1 root root 506K Mar  9 23:36 modules.alias.bin
-rw-r--r--  1 root root  11K Mar  9 23:35 modules.builtin
-rw-r--r--  1 root root  12K Mar  9 23:36 modules.builtin.bin
-rw-r--r--  1 root root 146K Mar  9 23:36 modules.dep
-rw-r--r--  1 root root 211K Mar  9 23:36 modules.dep.bin
-rw-r--r--  1 root root  302 Mar  9 23:36 modules.devname
-rw-r--r--  1 root root  57K Mar  9 23:35 modules.order
-rw-r--r--  1 root root  327 Mar  9 23:36 modules.softdep
-rw-r--r--  1 root root 215K Mar  9 23:36 modules.symbols
-rw-r--r--  1 root root 264K Mar  9 23:36 modules.symbols.bin
```

内容还比较复杂。

我怎么手动构建这样一个目录内容呢？

这个好像有点麻烦。我暂时不深入了。



modprobe 命令是根据depmod -a的输出/lib/modules/version/modules.dep来加载全部的所需要模块。

删除模块的命令是：modprobe -r filename。

就是insmod和rmmod的替代品。

相比于insmod的优点是，可以自动处理模块的依赖关系。



系统启动后，正常工作的模块都在/proc/modules文件中列出。

使用lsmod命令也可显示相同内容。

在内核中有一个“Automatic kernel module loading"功能被编译到了内核中。

当用户尝试打开某类型的文件时，内核会根据需要尝试加载相应的模块。

/etc/modules.conf或 /etc/modprobe.conf文件是一个自动处理内核模块的控制文件。





modprobe 与 insmod 命令的区别：

insmod 与 modprobe 都是载入 kernel module，不过一般差别于 modprobe 能够处理 module 载入的相依问题。

比方你要载入 a module，

但是 a module 要求系统先载入 b module 时，

直接用 insmod 挂入通常都会出现错误讯息，

不过 modprobe 倒是能够知道先载入 b module 后才载入 a module，如此相依性就会满足。

不过 modprobe 并不是大神，

不会厉害到知道 module 之间的相依性为何，

该程式是读取 /lib/modules/2.6.xx/modules.dep 档案得知相依性的。

而该档案是透过 depmod 程式所建立。







# depmod

Linux**内核模块可以为其它模块提供提供服务**(在代码中使用EXPORT_SYMBOL)，

这种服务被称作”symbols”。

若第二个模块使用了这个symbol，则该模块很明显依赖于第一个模块。

这些依赖关系是非常繁杂的。

depmod读取在/lib/modules/version 目录下的所有模块，

并检查每个模块导出的symbol和需要的symbol，

然后创建一个依赖关系列表。

默认地，该列表写入到/lib/moudules /version目录下的modules.dep文件中。

若命令中的filename有指定的话，则仅检查这些指定的模块(不是很有用)。

若命令中提供了version参数，则会使用version所指定的目录生成依赖，

而不是当前内核的版本(uname -r 返回的)。

modules.dep文件是这个样子。当前我们编译出来的就有了。

不需要depmod来生成。

这个依赖关系，跟Makefile类似，冒号后面表示依赖项。

```
kernel/sound/drivers/snd-aloop.ko:
kernel/amlogic/npu/galcore.ko:
kernel/amlogic/bt/sdio_bt.ko: kernel/amlogic/wifi/aml_sdio.ko
kernel/amlogic/wifi/aml_sdio.ko:
kernel/amlogic/wifi/vlsicomm.ko: kernel/amlogic/wifi/aml_sdio.ko
kernel/drivers/trustzone/optee.ko:
kernel/drivers/trustzone/optee_armtz.ko: kernel/drivers/trustzone/optee.ko
```



depmod指令会自动分析/lib/modules/$(uname -r)目录下的可加载模块，并按照固定的格式填入modules.dep中。

因此，我们可以先将需要加载的ko文件拷贝到对应的目录，再执行depmod指令就ok了。

# modprobe错误解决

```
modprobe: bad line 1: 1 tokens found, 2 needed
```

```
	read_config("/etc/modprobe.conf");
	read_config("/etc/modprobe.d");

```

## modprobe.conf



# 参考资料

1、

https://github.com/linuxkit/linuxkit/issues/1742

2、

https://blog.csdn.net/daocaokafei/article/details/114707070

3、

https://blog.csdn.net/pplogic/article/details/87258414