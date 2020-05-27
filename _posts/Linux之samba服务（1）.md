---
title: Linux之samba服务（1）
date: 2020-05-25 10:20:08
tags:
	- Linux

---

1

现在需要让板端支持samba文件的播放。

所以需要对samba进行一个深入的认识。

# samba和SMB关系

samba是一个软件的名字。

SMB是一个协议的名字。

samba是unix下对SMB协议实现的一个软件。

SMB协议是Server MessageBlock的意思。服务器信息块。



Samba 是一个自由的开源软件套件，用于实现 Windows 操作系统与 Linux/Unix 系统之间的无缝连接及共享资源。

samba还能实现活动目录和域控制器的功能。



我的Ubuntu笔记本上，目前安装了samba服务器功能，可以让外部正常访问文件。

在shell里，输入samba，再按tab键，可以看到系统提示了下面的命令。

```
samba             samba_dnsupdate   samba_kcc         samba-regedit     samba_spnupdate   samba-tool        samba_upgradedns 
```

这些命令分别有什么作用？

samba

从man信息看到：

```
samba - Server to provide AD and SMB/CIFS services to clients
```

是要给服务软件，给客户端提供AD和SMB服务的。

This program is part of the samba(7) suite.

所以我们`man 7 samba`看看有些什么。



samba suite

samba suite是一组软件，用来提供AD和SMB服务的。

samba也用nmbd实现了NetBIOS协议。

```
samba
	是一个daemon程序，提供AD和文件、打印服务给smb client。对应的配置文件是smb.conf。
	默认并没有启动这个。
smbd
	提供文件和打印服务。对应的配置文件也是smb.conf。
nmbd
	提供NetBios名字服务和浏览支持。配置文件也是smb.conf。
winbindd
	用来集成授权服务和user database。
smbclient
	实现一个类似ftp的客户端。这个用来访问其他机器提供的samba服务。
samba-tool
	主要的管理工具。
testparm
	这个是用来检查smb.conf里的配置是否合法。
smbstatus
	看看当前连接到smbd的连接情况。
nmblookup
	允许netbios名字查询。
smbpasswd
	修改samba用户密码。
smbcacls
	这个是设置ACL，访问控制列表的。
smbtree
	这个是samba client的一部分。
	apt install smbclient
	相当于windows下的网络发现。可以罗列出局域网里提供的samba访问的列表。
smbtar
	这个可以备份samba服务器上的文件。
smbspool	
	是一个打印辅助工具。
smbcontrol
	用来控制smbd、nmbd这些进程的。
rpcclient
	这个是执行rpc命令的工具。
pdbedit
	这个是用来维护user database的工具。
findsmb
	这个是用来局域网里的smb server。
	但是这个在Ubuntu上搜索不到。
net
	这个命令是用来提供类似windows下的net命令功能的。
wbinfo
	用来存取winbindd的信息的。
	
```



一些操作

首先，我想看本机上已经有的samb用户有哪些。这个怎么查看？用pdbedit来看。

```
root@thinkpad:~# pdbedit -L
teddy:1000:teddy
```

当前我只有一个用户。

增加用户和删除用户，都是用是smbpasswd来做。

但是要注意，这里操作的用户，都要是本机上存在的用户。

例如本机上有teddy这个用户，你才能把他添加到smb用户。

例如xxx这个用户，本来就是不存在的，你就不能把他添加到smb用户。



# samba4

我在buildroot里打开mpd的samba支持。

则自动选配了samba4。

samba依赖了python，是用python做了哪些事情呢？

1、编译系统是用python写的。

2、70个用C语言写的python模块。主要是给AD用的。

3、一些测试是用python写的。

4、单元测试是用python写的。



# arch wiki总结

这个wiki写得非常好。

/etc/samba/smb.conf这个配网文件默认没有，需要我们手动创建。



# smbclient使用

我先在我的两台Ubuntu机器上进行测试。

一台是台式机上的虚拟机，一台是笔记本。

2台机器上都搭建了samba服务的。

我在笔记本上进行操作。ip地址前面那2个斜杠可以没有。

```
smbclient -L //172.16.2.121 -U hlxiong@123456
```

得到的情况如下：

```
Domain=[WORKGROUP] OS=[Windows 6.1] Server=[Samba 4.3.11-Ubuntu]

        Sharename       Type      Comment
        ---------       ----      -------
        homes           Disk      this is my home dir
        share           Disk      
        IPC$            IPC       IPC Service (this is ubuntu samba server)
        hlxiong         Disk      this is my home dir
Domain=[WORKGROUP] OS=[Windows 6.1] Server=[Samba 4.3.11-Ubuntu]

        Server               Comment
        ---------            -------
        HLXIONG-VIRTUAL      this is ubuntu samba server
        PC-20180606DKDX      

        Workgroup            Master
        ---------            -------
        WORKGROUP   
```

这一步是需要的，因为需要查看目标上有哪些目录是可以访问的。

然后就可以这样登陆上去操作了。

```
smbclient  //172.16.2.121/homes -U hlxiong@123456
```



从samba4开始，samba可以作为AD和DC来运行。

如果你在生产环境使用samba，建议运行2个以上的DC来做备份。

怎样设置一个samba作为第一个DC，来构建一个新的AD forest。





参考资料

1、samba文件共享以及用法（访问控制）

https://blog.csdn.net/weixin_43275140/article/details/84577175

2、linux及samba用户的查看与删除

https://blog.csdn.net/qq_32693119/article/details/80016272

3、Samba 系列（一）：在 Ubuntu 系统上使用 Samba4 来创建活动目录架构

https://linux.cn/article-8065-1.html

4、Samba 4.11 发布，更好的可扩展性与默认禁用SMB1

https://www.linuxidc.com/Linux/2019-09/160723.htm

5、Samba 4.10 发布，完全支持Python 3

https://www.linuxidc.com/Linux/2019-03/157614.htm	

6、

https://www.samba.org/samba/docs/

https://sambaxp.org/fileadmin/user_upload/sambaxp2019-slides/power_sambaxp2019_python_samba.pdf

https://www.samba.org/~jelmer/samba4-python.pdf

7、

https://wiki.archlinux.org/index.php/samba

8、Samba客户端配置

https://yq.aliyun.com/articles/175133