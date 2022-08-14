---
title: openwrt（十七）问题解决
date: 2018-04-15 11:56:55
tags:
	- openwrt

---



### openwrt显示未开启或者未连接无线？

我的树莓派一直放在，今天发现不知道为什么自动挂了。重新上电，发现没有wifi热点出来。

luci显示未开启或者未连接无线。

我重启，删除接口重新添加，还是不行。

我刷成最新的openwrt，因为我当前的还是lede的。

我到官网上看，树莓派3B的最新的镜像是：

http://downloads.lede-project.org/releases/17.01.4/targets/brcm2708/bcm2710/lede-17.01.4-brcm2708-bcm2710-rpi-3-ext4-sdcard.img.gz

我当前的版本是：lede-17.02.0-rc1-brcm2708-bcm2710-rpi-3-ext4-sdcard-angelina-ace-201760714.img。

我当前这个版本似乎还新一点。不过我还是下载官方的看看。我也不记得我这个版本是哪里来的了。

不过这个版本解压后，只有290M。

我之前的那个有1个G。

先烧录看看。这个分配的空间更加小。

```
root@LEDE:/# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root               252.0M     10.0M    236.9M   4% /
tmpfs                    60.7M     52.0K     60.6M   0% /tmp
tmpfs                   512.0K         0    512.0K   0% /dev
```

配置文件也更少。

界面是英文的。

不过我觉得界面更加合理了。

我只需要修改/etc/config/network里的lan，改成192.168.0.100，因为我的树莓派连接到我的主路由器的。

/etc/init.d/network restart重启网络。

然后ssh连接正常。luci界面开启wifi，手机连接正常。上网正常。

界面设计是Bootstrap风格。标签都在顶栏。我感觉比在侧边好。

反应速度也快了很多。

还是需要把软件源替换一下。

opkg update，提示这个。

```
wget: SSL support not available, please install one of the libustream-ssl-* libraries as well as the ca-bundle and ca-certificates packages.
```

我到这个目录下，下载libustream-openssl的ipk包文件。上传到openwrt里安装。

https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base/

然后发现winscp连接不上去。还需要安装vsftpd和opkg install vsftpd openssh-sftp-server。

我先找到当前如何进行文件上传的方法。

这个肯定是要板端的一个server。

tftp服务器，默认也没有。

ftp服务器，没有。

web服务器，有，但是没有上传接口。

走客户端的思路。

ftp命令，没有，也就不能从pc上下载文件了。

python都没有带。

简单。我用U盘拷贝上去不就好了嘛。

```
root@LEDE:/mnt# opkg install 
libopenssl_1.0.2o-1_arm_cortex-a53_neon-vfpv4.ipk                       zlib_1.2.11-1_arm_cortex-a53_neon-vfpv4.ipk
libustream-openssl_2016-07-02-ec80adaa-4_arm_cortex-a53_neon-vfpv4.ipk
```

先把这3个安装了。https的访问问题就可以解决。

现在是无法ping通外网。ping 114.114.114.114也不行。那就是跟dns没有关系。

但是我手机通过openwrt联网是ok的。

是我没有添加默认网关导致的。

```
root@LEDE:/mnt# route add default gw 192.168.0.1
```

这样就好了。

现在ping 114.114.114.114是好的了。但是ping www.sina.com还是不行。

那这个就是跟dns有关系了。

我到luci的网络，接口，lan里修改，增加自定义dns为114.114.114.114 。

现在就可以ping通新浪了。

我执行opkg update。还是出错。

```
Collected errors:
 * opkg_download: Failed to download https://downloads.openwrt.org/releases/17.01.4/targets/brcm2708/bcm2710/packages//Packages.gz, wget returned 5.
 * opkg_download: Failed to download https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base/Packages.gz, wget returned 5.
```

我手动wget下载一个文件看看。提示ssl证书错误。

```
root@LEDE:~# wget https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base/Packages.gz
Downloading 'https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base/Packages.gz'
Connecting to 148.251.78.235:443
Connection error: Invalid SSL certificate
root@LEDE:~# 
```

我查了一下，好像说是时间不对导致的。我的时间当前确实是不对的。

改时间。

```
root@LEDE:~# date -s "2018-04-15 13:05:00"
Sun Apr 15 13:05:00 UTC 2018
root@LEDE:~# date
Sun Apr 15 13:05:03 UTC 2018
```

再试，还是不行。

https://wiki.openwrt.org/doc/howto/wget-ssl-certs

参考这篇文章看看。

鉴于后面的操作，可能大量需要从pc上传文件到openwrt，U盘拷贝太麻烦。

我还是优先把winscp的传输搭建好。

安装这2个就可以：

```
vsftpd-tls_3.0.3-2_arm_cortex-a53_neon-vfpv4.ipk
openssh-sftp-server_7.4p1-1_arm_cortex-a53_neon-vfpv4.ipk 
```



1、更新ssl。

```
mkdir -p /etc/ssl/certs
```

2、在/etc/profile里增加：

```
export SSL_CERT_DIR=/etc/ssl/certs
```

3、执行生效。

```
source /etc/profile
```

4、

```
opkg install ca-certificates
```

我发现downloads.openwrt.org可以用http来访问。

我改一下distfeeds.conf文件，这样暂时就绕过去了。可以进行联网安装。

不至于让问题死锁。

5、安装wget。

```
root@LEDE:/etc/opkg# opkg install wget
root@LEDE:/etc/opkg# which wget
/usr/bin/wget
root@LEDE:/etc/opkg# ls /usr/bin/wget -l
lrwxrwxrwx    1 root     root             8 Apr 15 05:29 /usr/bin/wget -> wget-ssl
root@LEDE:/etc/opkg# 
```

算了。暂时不继续做了。后续如果碰到问题再继续解决ssl的问题吧。



# 参考资料

1、SSR for OpenWRT 客户端、服务端发布【2017-02-08 增加LEDE、潘多拉IPK】

http://www.right.com.cn/forum/thread-204802-1-1.html







