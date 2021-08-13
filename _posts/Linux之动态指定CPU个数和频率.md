---
title: Linux之动态指定CPU个数和频率
date: 2021-08-03 11:32:33
tags:
	- Linux

---

--

现在要切换CPU的核心数和频率来做测试。看看怎么来做。

查看CPU情况。

```
# lscpu 
Architecture:        aarch64
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
Thread(s) per core:  1
Core(s) per socket:  4
Socket(s):           1
Vendor ID:           ARM
Model:               4
Model name:          Cortex-A53
Stepping:            r0p4
BogoMIPS:            48.00
Flags:               fp asimd evtstrm aes pmull sha1 sha2 crc32
```

靠操作/sys/devices/system/cpu 这个目录下的文件来做。

关闭cpu3,

```
# echo 0 > /sys/devices/system/cpu/cpu3/online
# grep "processor" /proc/cpuinfo
```

的确有用。

在关闭CPU1看看。

```
# echo 0 > /sys/devices/system/cpu/cpu1/online
# grep "processor" /proc/cpuinfo
processor       : 0
processor       : 2
```

我全部关闭看看。

```
# echo 0 > /sys/devices/system/cpu/cpu2/online
sh: write error: Device or resource busy
```

至少要有一个在。

然后看看怎么调节频率。

也是在sysfs里操作。

内核文档里提到这个目录：

/sys/devices/system/cpu/cpu0/cpufreq/ 

但是我当前的板端没有cpufreq这个目录。



参考资料

1、

https://www.cyberciti.biz/faq/debian-rhel-centos-redhat-suse-hotplug-cpu/

2、

https://stackoverflow.com/questions/2271272/how-can-i-change-cpu-frequency-manually-using-sysfs-cpufreq-subsystem

3、kernel文档cpu-freq部分