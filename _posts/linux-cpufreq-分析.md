---
title: linux cpufreq 分析
date: 2016-11-08 20:59:30
tags:
	- linux
	- cpufreq
---


现在cpu的主频都很高，但是计算机并不需要总是工作在最高频率，

这样比较耗电而且发热严重，

那么就需要os提供一种机制，可以根据实际需要来动态调整cpu的频率。

这个机制就是cpufreq系统。

linux源代码下面的文档是`Document/cpufreq/cpufreq`目录下。

我们先看看一些系统信息，建立感性认识。

所有与cpufreq有关的sysfs接口都在`/sys/devices/system/cpu`目录下。

```
teddy@teddy-ubuntu:/sys/devices/system/cpu$ ls -l
总用量 0
drwxr-xr-x 6 root root    0 11月  6 21:09 cpu0
drwxr-xr-x 6 root root    0 11月  6 21:09 cpu1
drwxr-xr-x 6 root root    0 11月  6 21:09 cpu2
drwxr-xr-x 6 root root    0 11月  6 21:09 cpu3
drwxr-xr-x 2 root root    0 11月  8 21:12 cpuidle
-r--r--r-- 1 root root 4096 11月  8 21:12 isolated
-r--r--r-- 1 root root 4096 11月  8 21:12 kernel_max
drwxr-xr-x 2 root root    0 11月  8 21:12 microcode
-r--r--r-- 1 root root 4096 11月  8 21:12 modalias
-r--r--r-- 1 root root 4096 11月  8 21:12 offline
-r--r--r-- 1 root root 4096 11月  6 21:09 online
-r--r--r-- 1 root root 4096 11月  8 21:12 possible
drwxr-xr-x 2 root root    0 11月  8 21:12 power
-r--r--r-- 1 root root 4096 11月  6 21:10 present
-rw-r--r-- 1 root root 4096 11月  6 21:09 uevent
```

cpu0到cpu3对应我的电脑的4个cpu核心。
online表示目前在工作的cpu核心的编号，offline表示目前被关闭的cpu，present则表示当前电脑主板上已经安装的cpu。从下面的输出可以看出，我的主板可以安装64个cpu，但是实际上只安装了4个。

```
teddy@teddy-ubuntu:/sys/devices/system/cpu$ cat online 
0-3
teddy@teddy-ubuntu:/sys/devices/system/cpu$ cat offline
4-7,8-63
teddy@teddy-ubuntu:/sys/devices/system/cpu$ cat present 
0-3
```

cpu的硬件特性决定了cpu的最高和最低工作频率。

我们再在这个范围里定出一个软件的调节范围。

可见，在系统的启动阶段，经由initcall机制，cpufreq_core_init被调用，由它来完成核心部分的初始化工作。



cpufreq是一个动态调整cpu频率的模块，系统启动时生成一个文件夹

/sys/devices/system/cpu/cpu0/cpufreq/，

里面有几个文件，

其中

scaling_min_freq代表最低频率，

scaling_max_freq代表最高频率，

scaling_governor代表cpu频率调整模式，用它来控制CPU频率

```
affected_cpus                   
cpuinfo_cur_freq                
cpuinfo_max_freq                
cpuinfo_min_freq                
cpuinfo_transition_latency      
related_cpus                    
scaling_available_frequencies   
scaling_available_governors     
scaling_cur_freq                
scaling_driver                  
scaling_governor                
scaling_max_freq                
scaling_min_freq                
scaling_setspeed                
stats                           
```



scaling_governor的可能取值：

```
performance 
powersave
Userspace
ondemand 
conservative 
```



参考资料

1、

https://blog.csdn.net/zhenwenxian/article/details/6196943