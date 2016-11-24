---
title: kali linux启动samba服务
date: 2016-10-06 09:10:50
tags: 
	- kali
	- samba
---
多台计算机协同工作的时候，总是需要共享数据，samba服务是很好的选择。
下面是在kali linux上开启samba服务的步骤。

1. 改配置文件。
```
cd /etc/samba
#先保存当前的配置文件
mv smb.conf smb.conf.bak
gedit smb.conf
# 把下面的内容复制粘贴到smb.conf文件里
# 下面这个配置把/root目录用share这个名字进行共享。
[share]
	path = /root
	available = yes
	browsable = yes
	public = yes
	writeable = yes
```

2. 启动samba服务。
```
service smbd start
service nmbd start
```
3. 访问测试。
我的kali当前的ip地址是192.168.0.101，在windows中，地址栏输入：\\\\192.168.0.101。这样就可以打开kali的共享目录了，且可以在windows下对该目录进行读写。

4. 设置开机就启动samba服务。
要加自己的开机启动服务，最好在/etc/rc.loacl文件里添加，这样对系统的启动不会有影响，这也是最简单的方式。rc.local是等待 /etc/init.d的服务都开启后才执行的，所以如果/etc/init.d中的服务未开启完成，rc.local是不会执行的。
linux启动服务的方式有两种：
* 传统的方式是 /etc/init.d 服务名 start
* 实际上还可以这样，service 服务名 start
/etc/init.d下面都是脚本文件。相当于调用了service 服务名 start这样的命令。是一个简单封装。

```
cd /etc
gedit rc.local 
# 把下面的内容加入到rc.local文件里，exit 0之前
# 这条命令相当于同时启动了smbd和nmbd
/ect/init.d/samba start
```





