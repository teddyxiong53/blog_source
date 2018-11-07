---
title: windows远程连接Ubuntu桌面
date: 2018-11-06 09:25:30
tags:
	- windows

---



```
#安装xrdp 
sudo apt-get install xrdp 
#安装vnc4server 
sudo apt-get install vnc4server tightvncserver
#安装xubuntu-desktop 
sudo apt-get install xubuntu-desktop 
#向xsession中写入xfce4-session 
echo “xfce4-session” >~/.xsession 
#开启xrdp服务 
sudo service xrdp restart
```

然后用windows的远程桌面就可以访问了。

这种方式连不上去。

还是用vnc来连接吧。



因为要关闭Ubuntu上的加密。但是我的电脑的dconf-editor没法用。

算了。



参考资料

1、xrdp完美实现Windows远程访问Ubuntu 16.04

https://www.cnblogs.com/xuliangxing/p/7560723.html

2、

https://www.cnblogs.com/xuliangxing/p/7642650.html

3、

https://blog.csdn.net/c80486/article/details/8545492

4、

https://askubuntu.com/questions/755020/gsettings-change-privacy-settings-via-command-line