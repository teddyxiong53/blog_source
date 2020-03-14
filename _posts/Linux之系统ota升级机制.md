---
title: Linux之系统升级机制
date: 2018-07-25 10:10:28
tags:
	- Linux

---



更新嵌入式设备最佳的方式是对整个镜像进行更新。

对于Linux，这个问题转化为对分区的更新。

所以分区要仔细考虑。

bootloader分区。尽量避免更新这个。

内核分区。除非有安全问题，否则不更新。

rootfs。一般是只读的。

用户分区。最需要更新的。



有两种可能的镜像更新：

1、对称。

```
有2个bootloader分区。2个kernel分区。2个rootfs分区。2个用户分区。
可以在更新过程中取消。
```

2、非对称。

```

```



基于镜像的更新软件有：

1、swupdate。

2、RAUC。



嵌入式设备位置分散、数量庞大、部署地点情况复杂。

因此对这些设备进行升级，肯定是无法采取单个、本地升级。太费时费力。

看看怎么进行远程批量自动升级。

最好可以通过web界面实时查看升级的情况。



一个参考的分区

````
|2M   |8M      | 100M   |16M    |2M    |
----------------------------------------
|uboot| kernel | rootfs | backup| info |
````

分区作用：

```
backup：
	存放要备份的东西，以便升级完成后，从这里再拷贝到新的文件系统里。
info：
	固化信息分区。
	存放版本号，设备类型、设备id等。
```



#板端的升级管理程序

功能：

```
1、管理版本信息。
2、post设备信息给服务端。
3、从服务端下载升级包。
4、校验、管理升级包。
5、启动升级执行程序。
```



```
1、开机运行，作为守护进程。
2、第一次运行，读取版本信息，存放到info分区里。
3、每隔一段时间上传版本号给服务端，服务端看看是否需要更新（这个让客户端主动，减轻服务端的压力）
4、如果有新版本，给客户端返回镜像下载地址和升级命令。
```

# 升级执行程序

功能：

```
1、解压升级包。
2、备份文件。
3、格式化内核、文件系统分区。
	格式化分区，不影响系统正常运行？
	我觉得把应用单独放一个分区，根文件系统不用升级。
	内核被覆盖，不影响运行。
4、加载升级包里的文件到内核、文件系统分区。
5、重启系统。
6、拷贝备份文件到文件系统里。
```





升级方案需要

```
1、可以更新app，也需要可以更新内核和其他基础组件。
2、要可以避免变砖。
3、应该是原子的。要么成功，要么失败。不能存在第三种状态。这样就有不确定的风险。
4、必须有验证签名机制。
5、ota应该是通过安全通道。
```

怎么做升级方案？

不要自己写，用成熟的开源方案。

有这些：

```
1、swupdate。
2、rauc。
3、mender。
4、ostree、libostree。
5、swupd。
```



为什么不采用桌面系统的包管理的方式进行更新？

因为不是原子的。会带来不可控的东西。

所以只能通过镜像的方式进行更新。



recovery的是ramfs，

**基于recovery的，比ab系统会省空间。**

Android直到N版本才引入ab系统的。之前也是基于recovery的。

**基于recovery的叫单拷贝方式。基于ab系统的叫双拷贝方式。**

单拷贝的分区情况：

```
|bootloader|recovery |normal| data|
```



单拷贝方式的缺点：

```
1、在更新期间，你什么也做不了。
2、没法回退。
```

单拷贝的优点：

```
1、空间会少占用一点。
2、经过多年考验，可靠。
```



双拷贝的分区

```
|bootloader| system a| system b| data |
```

双拷贝的优点：

```
1、升级用户可以没有感知。可以在后台升级。用户下次重启时切换到系统。
2、可以做回退。
```



还有增量升级法。





# 参考资料

1、嵌入式 Linux 软件更新机制及架构汇总

https://www.aliyun.com/jiaocheng/121425.html

2、IoT固/软件更新及开源选项

https://blog.csdn.net/wireless_com/article/details/79548091

3、【IoT】如何实现 ESP32 固件的 OTA 在线升级更新

https://blog.csdn.net/liwei16611/article/details/81051909

4、可在线OTA升级的嵌入式系统设计方案

https://blog.csdn.net/zhou_chenz/article/details/54917622

5、基于Flask搭建Android应用OTA升级服务

https://blog.csdn.net/zjt19870816/article/details/80917529

6、嵌入式定制常用的实时Linux改造方案

https://blog.csdn.net/qq_34003774/article/details/80591716

7、260亿物联网终端，或将使OTA升级独成一个产业

http://www.sohu.com/a/214389286_472880

8、OTA升级如何实现？全解共享单车OTA升级过程

https://www.sohu.com/a/231352656_100093632

9、【迷你强的物联网】起始篇-简介与MQTT服务器【从零开始搭建自己的物联网系统】

https://blog.csdn.net/relijin/article/details/73274739

10、Updating Embedded Linux Devices: Update strategies

https://mkrak.org/2018/01/10/updating-embedded-linux-devices-part1/

11、

https://elinux.org/images/3/31/Comparison_of_Linux_Software_Update_Technologies.pdf

12、可在线OTA升级的嵌入式系统设计方案

https://blog.csdn.net/zhou_chenz/article/details/54917622