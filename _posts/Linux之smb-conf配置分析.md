---
title: Linux之smb.conf配置分析
date: 2018-01-30 11:21:43
tags:
	- Linux
	- samba

---



一直没有把smb.conf里的配置项目梳理一遍。碰到问题解决起来总是棘手。所以现在梳理一遍。

我的windows系统的情况：

1、计算机名。hostpc。

2、计算机全名。hostpc。

3、计算机描述。hostpc。

4、工作组。XHL_WORK。



#[global]

samba服务器的全局设置，对整个服务器有效。

1、workgroup。

既然我的物理机器的工作组是XHL_WORK。那么我就可以把workgroup设置为这个值。

2、server string。

设置samba server的注释信息。

3、hosts allow。

后面跟ip地址，表示允许哪些机器连接到这里。多个ip用空格隔开。

4、guest account。

不设置的话，默认是以nobody登陆的。所以不用输入密码。

可以设置为：guest account = teddy。以teddy的身份登陆。

5、日志相关的。

```
logfile
max log size
```

6、security。

取值有4种：

```
1、share。不要用户名和密码。
2、user。要用户名和密码。本服务器自己来验证。
3、server。指定一条服务器来验证。
4、domain。指定域服务器来做验证。
```

我们选择user就好了。

其他的都可以不关注。

#[homes]

这个是使用者登陆进来看到的就是自己的home目录的情况。

```
[homes]
	comment = this is my home dir
	browseable = yes
	writeable = yes
	valid users = %S
	create mask = 0777 
    directory mask = 0777
```

我把smb.conf文件整理如下：

```
#======================= Global Settings =======================

[global]
    workgroup = XHL_WORK
    server string = this is ubuntu samba server
    hosts allow = 192.168.190.1
    guest account = teddy
    log file = /var/log/samba/log.%m
    max log size = 1000
    security = user


#======================= Share Definitions =======================

[homes]
   comment = this is my home dir
   browseable = yes
   read only = no
   create mask = 0777
   directory mask = 0777
   valid users = %S
```

重启samba服务。

然后windows上进行远程硬盘映射。可能需要重启一下windows。

然后映射\\192.168.190.130\homes就可以了。



我在树莓派上这样配置。

```
#======================= Global Settings =======================

[global]
    workgroup = XHL_WORK
    server string = this is ubuntu samba server
    log file = /var/log/samba/log.%m
    max log size = 1000



#======================= Share Definitions =======================

[homes]
   comment = this is my home dir
   browseable = yes
   read only = no
   create mask = 0777
   directory mask = 0777
   valid users = %S
   
[share]
    path = /
    available = yes
    browsable = yes
    public = yes
    writeable = yes
```

开始一直报用户密码不对。后面发现是因为我没有`sudo smbpasswd -a pi`导致的。

我的家庭网络的工作组是XHL_WORK。所有计算设备都加入到这个组里。

所以windows映射盘的时候，需要在填写用户名的时候，加上：

```
XHL_WORK\teddy
```

这样来登陆才行。

