---
title: 代理之frp
date: 2019-11-12 14:12:49
tags:
	- 代理

---

1

看hachina的内容的时候，发现使用了frp。了解一下。

frp是反向代理工具。是Fast Reverse Proxy的缩写。

frp目前处于开发阶段，协议随时可能变，所以客户端和服务端要版本匹配。

代码在这里：https://github.com/fatedier/frp

这里有提供免费的服务。

https://www.frp.fun/

我刚好有一台阿里云的服务器，可以搭建一下反向代理。

frp当前最主流的版本是哪个？

在hachina的镜像里集成的是0.18.0。我就用这个版本吧。

从这里可以看到发布版本。最新的是0.29.1的了。

https://github.com/fatedier/frp/releases

在这个发布版本里，特别声明了和之前的版本不兼容。

https://github.com/fatedier/frp/releases/tag/v0.18.0

解压后是这样：

```
├── frpc 客户端
├── frpc_full.ini 客户端配置完整版本。
├── frpc.ini 客户端配置
├── frps  服务端
├── frps_full.ini
├── frps.ini 服务端配置
└── LICENSE
```

配置文件使用精简版本就可以了。

服务器运行：

```
./frps -c ./frps.ini 
```

客户端需要修改一个配置，就是server_addr，修改成你的云服务器的公网ip。

客户端运行：

```
./frpc -c ./frpc.ini
```

客户端包了超时的错误。

```
login to server failed: dial tcp
```

可能有区别的地方就是防火墙相关的配置，

然后因为阿里云的安全服务限制，只有几个端口是默认打开的，所以要自己登陆阿里云服务器后台更改端口限制。

放开端口限制后，就可以连上了。

现在该怎么测试呢？



访问一下云服务的7500端口，看配置，这个应该是dashboard的端口。

但是不行，应该用frps_full.ini来启动服务器才行。

现在就可以访问dashboard了。

但是还是用精简版本的配置文件吧。我不需要dashboard。

现在从另外一台电脑，输入：

```
ssh -oPort=6000 hlxiong@x.x.x.x
```

x.x.x.x是我的阿里云服务器端的地址。这样就可以登陆到我的本地机器了。



接下来就是让frps在服务器上能够一直运行。

就用supervisor来做吧。

```
root@xhl-ecs:/etc/supervisor/conf.d# vi frp.conf
[program:frp]
command=/root/work/frp_0.18.0_linux_amd64/frps -c /root/work/frp_0.18.0_linux_amd64/frps.ini
autostart = true
```

然后把supervisor重启一下就可以了。

```
service supervisor restart
```



参考资料

1、使用 FRP 反向代理实现 Windows 远程连接

https://www.cnblogs.com/zhanggaoxing/p/9221705.html

2、frp官方中文文档

https://www.cnblogs.com/sanduzxcvbnm/p/8508741.html

3、阿里云服务器实现 frp 内网穿透

https://blog.csdn.net/cao0507/article/details/82758288

4、

https://blog.csdn.net/ocaihong123/article/details/80522220