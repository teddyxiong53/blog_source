---
title: windows远程连接Ubuntu桌面
date: 2018-11-06 09:25:30
tags:
	- windows

---

1

Ubuntu上安装服务：

```
sudo apt install xfce4 xfce4-goodies tightvncserver
```

输入下面的命令启动服务。

```
vncserver
```

从5900开始，每增加一个连接，端口号加1。注意看输出的提示。

netstat -ant也可以查看，端口号很重要 。

我现在的是5902的。

然后需要把端口号加入到防火墙的白名单里。

```
iptables -I INPUT -p tcp --dport 5902 -j ACCEPT 
```

然后windows上打开mstsc（就是远程桌面），输入Ubuntu的ip地址和用户名。

然后选择vnc-any。输入端口号这些。

连接。

我现在是可以连接上来，但是是一篇空白。

看看~/.vnc/目录下的日志。

```
/home/teddy/.vnc/xstartup: 行 13: gnome-session-fallback: 未找到命令
```



参考资料

1、ubuntu配置vnc服务

https://www.cnblogs.com/young233/p/10847531.html