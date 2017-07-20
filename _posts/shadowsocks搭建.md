---
title: shadowsocks搭建
date: 2017-06-29 22:12:30
tags:

	- 翻墙

---

都说现在shadowsocks是很好的翻墙方式。那么必须学习一下。

shadowsocks的优点：

* 耗电很低。
* 支持开机自启动，断网没有影响。
* 可以使用自己的服务器。
* 支持区分国内外流量。
* 无需root

翻墙的感觉会达到无缝的感觉。

搭建ss需要一个vps。vps是Virtual Private Server的缩写。就相当于你买了一台服务器，放在国外，你可以随时通过你自己的这台服务器访问墙外的世界。

有三家vps商家可以选择：

DigitalOcean。30块一个月。有点贵。

搬瓦工BandWagon。以考虑。可以支付宝支付。就选择这个了。

看看选择哪种主机呢？

就选择中国直连特惠主机，只有洛杉矶节点。

内存512M、硬盘10G、流量1000GB每月。

```
Basic VPS - Self-managed - SPECIAL 10G KVM PROMO V3 - LOS ANGELES - CHINA DIRECT ROUTE
SSD: 10 GB RAID-10
RAM: 512 MB
CPU: 1x Intel Xeon
Transfer: 1000 GB/mo
Link speed: 1 Gigabit
```

搬瓦工各节点测试IP：

Los Angeles：   104.194.78.3

Florida：       74.121.150.3

Phoenix：       198.35.46.2（可在控制面板里切换到这个机房）

我只能ping同洛杉矶那个。



买好账号后，打开

[https://bwh1.net/clientarea.php?action=products](https://bwh1.net/clientarea.php?action=products)

这个网址。登陆。



由于搬瓦工VPS后台控制面板集成了一键安装Shadowsocks服务，所以特别适合第一次尝试搭建Shadowsocks服务器的新手，很简单便捷。

但是我后面测试过，默认的这个效果并不太好。所以还是自己手动来搭建。

# 1. 在vps上安装操作系统

因为我比较习惯Ubuntu的，所以我选择Ubuntu，版本尽量选择新一些的。

我选择了Ubuntu16.04的64位版本。

安装还是很快的，大概1到2分钟就好了。

你安装的时候，网页会提示你root密码和访问端口。安装后之后，就可以用SecureCRT来进行连接了。



# 2. 安装shadowsocks

依次执行下面的3条命令：

```
apt-get update
apt-get install python-pip
pip install shadowsocks
```

我执行`apt-get update`的时候，碰到错误：`Could not get lock /var/lib/dpkg/lock - open (11: Resource temporarily unava`。稍为等1分钟就自动好了，应该是后台在做某些操作。

安装完之后，你要在/etc/目录下新建一个shadowsocks.json的配置文件（默认没有这个文件）。

把里面的内容编写如下。你需要把port和password改为自己要设置的值。

```
{
        "port_password":{
                "port1":"password1",
                "port2":"password2"
        },
        "method":"chacha20",
        "timeout":600
}
```

启动服务：

```
sudo ssserver -c /etc/shadowsocks.json -d start 
```

会出现错误提示，说libsodium找不到。因为新的加密算法需要这个库的支持。

依次执行下面的命令，安装这个库。

```
下载源代码文件
wget https://github.com/jedisct1/libsodium/releases/download/1.0.11/libsodium-1.0.11.tar.gz
解压后编译
tar xf libsodium-1.0.11.tar.gz && cd libsodium-1.0.11
./configure && make -j2 && make install
ldconfig
```

如要停止服务：

```
sudo ssserver -d stop
```









