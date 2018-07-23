---
title: OpenStack（1）安装环境
date: 2018-07-21 22:22:49
tags:
	- 云计算
typora-root-url: ..\
---



Fuel是一个集成的安装环境。可以帮我们降低安装OpenStack的难度。

https://software.mirantis.com/releases/#supported

看这里最后一个版本是9.0的，我们下载对应的iso文件。有2.7G。



需要virtual box版本5.0.12以上。



在virtual box里新建一个叫fuel_master的虚拟机，硬盘给80G。

给我的pc添加3张host only的网卡。

地址依次是：

10.20.0.1

172.16.0.1

192.168.4.1

不要添加nat的网卡，这样会导致异常退出的。

然后用下载的iso文件，进行安装。

安装过程要十几分钟。

但是我这个又出现了内存地址为0的错误。

我把电脑重启一次。再安装很快就好了。

用户名和密码是root和r00tme。

fuel_master的ip地址是10.20.0.2 。

访问一下：http://10.20.0.2:8000/

不行。

在xshell里建一个隧道。

从127.0.0.1:8000到10.20.0.2:8000的隧道。

然后我们访问http://127.0.0.1:8000

我的不通。

这个操作很简单。为什么我的不行呢？

现在ssh连接是没有问题的。

我的防火墙都是关闭的。

删掉重新安装一次看看。在新建的过程中，我想到可能是eth0的类型要修改看看。

之前我在fuel 9.0 setup这里，直接选择了F8 退出。选择我选择设置一下。其实没改。保存继续。

这个保存有点慢。

这次安装花了很久。我知道前面为什么不行了。因为虽然系统安装了，但是需要的软件没有安装完成就出错退出。

很慢很慢。我看到好像是需要外网，就把网卡3改成了nat。然后就又出现了内存错误。

我把网卡4弄成nat的。再开机看看。

不能上网，是因为我的virtual  box没有添加一个全局的nat。

安装虽然慢。但是终于还是安装好了。

我安装的fuel9.0版本，不需要做隧道。可以直接访问。



新建一个OpenStack环境，取名为demo。

参数都保持默认，我的当前这个是基于Ubuntu的了。不像之前的那样是基于centos的。

![](/images/OpenStack（1）-支持的OS.png)



新建一个虚拟机，叫fuel_controller。

设置方法，参考fuel_master的。

新建虚拟机fuel_compute。

新建的2个虚拟机都不用安装系统。

发现在网页上有这样的提示。

```
WARNING: Failed to build the bootstrap image, see /var/log/fuel-bootstrap-image-build.log for details. Perhaps your Internet connection is broken. Please fix the problem and run `fuel-bootstrap build --activate`. While you don't activate any bootstrap - new nodes cannot be discovered and added to cluster. For more information please visit http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-install-guide/bootstrap/bootstrap_troubleshoot.html
```



我发现virtualboxnat模式，pc上看不到对应的网卡。这一点跟VMware不同。

我现在用virtualbox新建一个alpine虚拟机。看看如何才能弄上网。

经过这些操作是可以的：

1、设置为桥接模式。

2、命令行执行：

```
ifconfig eth0 192.168.0.205 netmask 255.255.255.0
route add default gw 192.168.0.1
```

现在可以ping通114.114.114.114 ，但是不能ping通baidu.com。

3、设置dns。

在/etc/resolv.conf里加入

```
nameserver 192.168.0.1
```

4、重启网卡。

```
/etc/init.d/networking restart
```

虽然提示出错，找不到/etc/network/interfaces文件。但是现在可以ping通百度了。



现在在fuel_master上进行操作，看看能不能连上网。

网卡总是找不到。

算了。不折腾virtualbox的了。



# 参考资料

1、主要参考这篇文章。

https://www.cnblogs.com/dongdongwq/p/5627532.html



https://www.jb51.net/article/95254.htm

安装Mirantis OpenStack Fuel 9.0

https://blog.csdn.net/wiborgite/article/details/52948154

虚拟环境下使用Fuel安装部署OpenStack

https://wenku.baidu.com/view/ca809ac7581b6bd97e19ea3c.html