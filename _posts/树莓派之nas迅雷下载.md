---
title: 树莓派之nas迅雷下载
date: 2019-01-14 17:17:59
tags:
	- 树莓派
---



用aria来做。

安装aria和apache。

```
sudo apt-get install aria2 apache2
```

然后修改apache的权限。

sudo visudo，在最后面加上这个。

```
www-data ALL=(ALL) NOPASSWD: ALL
```

新建aria的配置文件。

```
mkdir ~/.aria2
touch ~/.aria2/aria2.session
touch ~/.aria2/aria2.conf
```

aria2.conf内容这样写：

```
dir=/home/pi/hard_disk/download
disable-ipv6=true
enable-rpc=true
rpc-allow-origin-all=true
rp-listen-all=true
continue=true
input-file=/home/pi/.aria2/aria2.session
save-session=/home/pi/.aria2/aria2.session
max-concurrent-downloads=3
```

然后下载管理界面。

在/var/www/html目录下。

```
git clone http://github.com/wzhy90/yaaw
```

然后打开电脑的浏览器，访问：

http://192.168.0.7/yaaw/

就可以看到管理界面。



注册一个免费的ngrok。在这里。可以访问内网里的树莓派。

https://www.ngrok.cc/user.html

参考资料

1、

https://segmentfault.com/a/1190000014248533

2、树莓派做下载机，Aria2！

这个好，主要参考这篇。

http://shumeipai.nxez.com/2014/07/01/raspberry-pi-do-download-machine-aria2.html