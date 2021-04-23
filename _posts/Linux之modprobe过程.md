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



modprobe looks in
       the module directory /lib/modules/`uname -r` for all the modules and other files, 

except for the optional configuration files in the /etc/modprobe.d directory (see modprobe.d(5)). 

modprobe will also use module options
       specified on the kernel command line in the form of <module>.<option> and blacklists in the form of modprobe.blacklist=<module>.



# modprobe跟alias关系





# 参考资料

1、

https://github.com/linuxkit/linuxkit/issues/1742

