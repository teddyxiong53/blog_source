---
title: Linux移植Android的property机制
date: 2022-09-04 16:11:33
tags:
	- Linux

---

--

Android系统（本文以Android 4.4为准）的属性（Property）机制有点儿类似Windows系统的[注册表](https://so.csdn.net/so/search?q=注册表&spm=1001.2101.3001.7020)，

其中的每个属性被组织成简单的键值对（key/value）供外界使用。

 我们可以通过在[adb](https://so.csdn.net/so/search?q=adb&spm=1001.2101.3001.7020) shell里敲入getprop命令来获取当前系统的所有属性内容，

而且，我们还可以敲入类似“getprop 属性名”的命令来获取特定属性的值。

另外，设置属性值的方法也很简单，只需敲入“setprop 属性名 新值”命令即可。

 说白了，Property机制的运作机理可以汇总成以下几句话：
1） 系统一启动就会从**若干属性脚本**文件中加载属性内容；
2） 系统中的所有属性（key/value）会**存入同一块共享内存**中；
3） 系统中的各个进程会将这块**共享内存映射到自己的内存空间**，这样就可以直接读取属性内容了；
4） ==系统中只有一个实体可以设置、修改属性值，它就是属性服务==（Property Service）；
5） 不同进程只可以通过socket方式，向**属性服务**发出修改属性值的请求，而**不能直接修改**属性值；
6） 共享内存中的键值内容会以一种**字典树的形式进行组织**。



![img](../images/random_name/20150911211431534)



我们可以看到，在init进程的main()函数里，

辗转打开了一个内存文件`“/dev/__properties__”`，

并把它设定为128KB大小，

接着调用mmap()将这块内存映射到init进程空间了。

这个内存的首地址被记录在`__system_property_area__`全局变量里，

以后每添加或修改一个属性，

都会基于这个`__system_property_area__`变量来计算位置。



主要的属性文件

```
l  /system/build.prop 
l  /system/default.prop（该文件不一定存在） 
l  /data/local.prop 
l  /data/property目录里的若干脚本
```

# yodaos里的property使用

开机时的property service是在S78property_service启动。



# 参考资料

1、

https://blog.csdn.net/stoic163/article/details/88815430

2、

https://www.cnblogs.com/lzlltmf/p/5906720.html