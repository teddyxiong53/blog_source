---
title: OpenStack（1）安装环境
date: 2018-07-21 22:22:49
tags:
	- 云计算

---



Fuel是一个集成的安装环境。可以帮我们降低安装OpenStack的难度。

https://software.mirantis.com/releases/#supported

看这里最后一个版本是9.0的，我们下载对应的iso文件。有2.7G。



需要virtual box版本5.0.12以上。



在virtual box里新建一个叫fuel_master的虚拟机，硬盘给80G。

添加3张host only的网卡。

地址依次是：10.20.0.1

172.16.0.1

192.168.4.1

不要添加nat的网卡，这样会导致异常退出的。

然后用下载的iso文件，进行安装。

安装过程要十几分钟。

但是我这个又出现了内存地址为0的错误。







# 参考资料

1、

https://www.cnblogs.com/dongdongwq/p/5627532.html



https://www.jb51.net/article/95254.htm

安装Mirantis OpenStack Fuel 9.0

https://blog.csdn.net/wiborgite/article/details/52948154

虚拟环境下使用Fuel安装部署OpenStack

https://wenku.baidu.com/view/ca809ac7581b6bd97e19ea3c.html