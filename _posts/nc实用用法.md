---
title: netcat常用命令
date: 2016-11-05 21:43:01
tags:
	- netcat
---
netcat，也简写为nc，是linux下的网络工具，被称为网络工具里的瑞士军刀。短小精悍，二进制文件只有30KB，但是功能却很强大。
nc是Linux下用来实现任意的tcp和udp端口连接和监听的工具。可以用来做端口扫描。
从名字上看，netcat是一个网络相关的cat，cat是把文件内容输出到命令行的，netcat的字母含义就是把网络上其他主机的文件输出到本地命令行。经常被当成攻击工具来用。
一般用途包括：
* 简单的tcp代理。
* 基于shell脚本的http client和server。
* 网络后台测试。
* socks或者http代理。

下面是基本用法。是从man信息里总结出来的。

# 1. 建立简单的client/server模型
```
# 在本机上监听8811端口
nc -l 8811
# 另外开一个shell窗口，输入下面的命令
# 连接到8811端口
nc 127.0.0.1 8811
```
现在你在第二个shell窗口输入"XXX"，回车。可以看到第一个shell窗口把"XXX"回显出来了。

这个可以是一个简单的QQ的雏形。

# 2. 端口扫描
nc的端口扫描功能效率远不及nmap。
```
# 扫描这个主机的135端口
nc -vv 192.168.19.1 135
```




```
teddy@teddy-ubuntu:~$ nc -z -v -n -w 2 127.0.0.1 20-23
nc: connect to 127.0.0.1 port 20 (tcp) failed: Connection refused
nc: connect to 127.0.0.1 port 21 (tcp) failed: Connection refused
Connection to 127.0.0.1 22 port [tcp/*] succeeded!
nc: connect to 127.0.0.1 port 23 (tcp) failed: Connection refused
```

上面可以看到机器的22号端口是打开的。可以用下面的命令来获取Banner信息。

```
teddy@teddy-ubuntu:~$ nc -v 127.0.0.1 22
Connection to 127.0.0.1 22 port [tcp/ssh] succeeded!
SSH-2.0-OpenSSH_6.9p1 Ubuntu-2ubuntu0.2

Protocol mismatch.
teddy@teddy-ubuntu:~$ 
```



# 3. 传输文件

相对于scp命令，nc命令不需要经过认证。

这个可以是黑客利器。

假如我们入侵了一台Linux服务器，服务器上有nc工具。我们在该服务器上执行下面的命令，准备发送文件：

```
nc -v -l 12345 < server_info.txt
```

然后在我们自己的机器上，执行下面的语句，就可以把文件取下来。我现在是用一台机器进行模拟的。

```
nc -v -n 127.0.0.1 12345 > get_server_info.txt
```

如果是传输文件夹怎么办呢？用tar来压缩再传。可以利用管道，不生成文件，直接把压缩结果进行发送。











