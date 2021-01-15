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



# 突然不能frp ssh访问了

我一直通过frp连接到办公室的Linux机器，但是今天突然就不能访问了。

把办公室linux、服务器都重启了一次，还是一样的。

报错是这样：

```
ssh_exchange_identification: Connection closed by remote host
```

这里说重启服务，还是不行。

另外说可能是连接的客户端太多，我这也没有连接多少。就一个。

https://www.cnblogs.com/cxq20190307/p/10694547.html

还有说要关闭selinux的。

关闭ubuntu的防火墙 
ufw disable

我感觉是跟办公室的linux机器没有关系。

问题可能还是出在服务器上。

我在我的本地linux上安装supervisor，把frpc在本地用这个启动。

现在就正常了。真是奇怪。可能跟这个也没有关系。



# OpenWrt搭建frp

我现在刷的OpenWrt上默认带了frp。而我做微信开发，又有frp的需求。

看看怎么把这个环境弄好弄稳定，一次搞定，后面不要再折腾。

没有公网ip，没办法做到。

frps应该搭建在有公网ip的机器上。一般是一台vps上。



# 0.18.0和0.34.3

我之前是用0.18.0的，这个版本比较老，当前都还没有aarch64的机器。所以没有编译0.18.0的版本。

所以我在树莓派上就找不到对应的执行文件。

我的树莓派4上，安装的是0.34.3版本。这个也是当前的最新版本。

服务端，使用精简的配置文件，里面就两行，指定端口为7000的。

```
[common]
bind_port = 7000
```

客户端，是这样：

```
[common]
server_addr = 服务器公网ip
server_port = 7000

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 6000
```

然后服务端和客户端都启动，

从另外一台电脑，执行：

```
ssh xx@公网ip -oPort=6000
```

xx是本地机器的用户名。

这样就可以从任意位置访问到本地机器的ssh登陆。



## 使用完整的配置

到目前位置，我使用完整配置的，还没有成功过。

完整配置里的东西

```
前面的端口定义没有什么。

这个vhost，如果打开，在我的服务器上是跑不起来的。
#vhost_http_port = 80
#vhost_https_port = 443
主要是应对什么场景呢？不管先。我用不上。
然后是控制面板的端口，7500
以及控制面板的用户名和密码。
然后是token配置。
```

在客户端的full配置里，也有token配置，保持一致就好了。

客户端配置的full版本力量，多了很多常用的应用场景配置。

但是我都用不上。

还是在精简版本的配置文件上，加入自己的需要的配置，这样可控一点，不会引入大量自己不清楚的东西。

## 可行配置

现在服务端

```
[common]
bind_port = 7000
dashboard_port = 7500
dashboard_user = xx
dashboard_pwd = xx
log_file = /home/ubuntu/tools/frp/frps.log
log_level = info

log_max_days = 3

# disable log colors when log_file is console, default is false
disable_log_color = false

authentication_method = token


authenticate_heartbeats = false

authenticate_new_work_conns = false

token = 123

allow_ports = 5000,6000-6010

```

客户端

```
[common]
server_addr = xx
server_port = 7000

token = XX

user = thinkpad

log_file = /home/teddy/tools/frp/frpc.log

log_level = info

log_max_days = 3

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 6000

[pyspider]
type = tcp
local_ip = 127.0.0.1
local_port = 5000
remote_port = 5000
```

现在可以访问控制面板（在7500端口），也可以正常看到统计的数据。

![image-20210113103547949](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210113103547949.png)



现在我的frp就基本正常了。



# OpenWrt的frp客户端配置

是从luci界面配置的。

配置会被写入到/var/etc/frp/frpc.conf文件里。

就配置本地的80端口到6001就可以了。

之前不行，是因为我勾选了proxy-protocol。应该把这个勾选为停用。

相当于在配置里加了这么一个条目。

![image-20210113104915823](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210113104915823.png)

现在可以正常在公网访问到树莓派的管理界面了。



# 我的环境

服务器：运行frps。

笔记本：运行pyspider，暴露22和5000的pyspider端口。

树莓派：作为nas和下载机，把webui对外可访问。还需要把ssh也暴露。因为webui的终端有时候刷不出来。





参考资料

1、使用 FRP 反向代理实现 Windows 远程连接

https://www.cnblogs.com/zhanggaoxing/p/9221705.html

2、frp官方中文文档

https://www.cnblogs.com/sanduzxcvbnm/p/8508741.html

3、阿里云服务器实现 frp 内网穿透

https://blog.csdn.net/cao0507/article/details/82758288

4、

https://blog.csdn.net/ocaihong123/article/details/80522220

5、IT男的VPS系列教程 篇一：内网穿透（Frp）-拯救没有公网IP的你

https://post.smzdm.com/p/566063/