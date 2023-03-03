---
title: Linux之samba服务（1）
date: 2020-05-25 10:20:08
tags:
	- Linux

---



现在需要让板端支持samba文件的播放。

所以需要对samba进行一个深入的认识。

smb协议是微软和intel在1987年制定的一个协议。

是一个开放的协议。可以支持扩展。这就导致协议到现在变得非常复杂。

后来微软又把smb升级为cifs。Common Internet FileSystem。加入了更多的特性。

smb是在netbios基础上进行实现的。

netbios是在tcp层之上的。

当安装TCP/IP协议时，NetBIOS 也被Windows作为默认设置载入，我们的计算机也具有了NetBIOS本身的开放性。某些别有用心的人就利用这个功能来攻击服务器，使管理员不能放心使用文件和打印机共享。

![image-20200527203915417](../images/random_name/image-20200527203915417.png)



在netbios出现后，微软就基于netbios实现了一个网络文件/打印服务系统。

这个系统基于netbios设定了一套文件共享协议。

微软称之为smb协议。

后来这个协议被微软用来做lan manager和Windows NT服务器系统里。

而微软的普通电脑系统里，都包含客户端。

所以这个协议在局域网系统里影响非常大。

随着Internet的流行，微软希望把这一套系统推广到internet上。

就升级成了CIFS。

为了让Windows和unix系统更好地互相通信。最好的办法就是在unix里安装smb的协议软件。

这样Windows电脑这边，什么都不用改，就可以把unix当做Windows服务器一样来使用了。

smb协议带有非常浓厚的微软的色彩。



在smb协议里，计算机为了访问网络资源，就需要了解网络上的资源的列表。

这个机制，就做浏览（browse）。

在smb协议里，经常使用广播的方式。

但是如果每次都使用广播的方式来了解网络里的资源的情况。会导致大量的数据包。

因此，最好在网络里维护一个网络资源列表。

只有必要的时候，才重新查找资源。

但是没有必要每台计算机都维护一份资源列表。

在一个网络里，只需要几台计算机维护就好了。

这些特殊的计算机，被称为browser。

browser并不是认为指定的，而是计算机之间协商推举产生的。

多个browser里，一个是主browser，其余为备份browser。



这是由于系统的默认配置
Default: guest account = nobody 默认将guest访问，映射到系统nobody用户的访问
和我们设定的
map to guest = Bad User 使用无效密码的用户登录将被拒绝，除非用户名不存在，在这种情况下，它将被视为访客登录并映射到 guest account

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



# 匿名共享

在global下面：

```
[global]
	security = share
[public] # 这个是共享名
	public = yes
	path = /share #绝对路径
```



浏览器打开是这样：

```
\\172.16.2.121
```

然后浏览器帮你转成了

```
file://172.16.2.121
```

这个视频教程讲了匿名访问的，挺好的。

https://www.bilibili.com/video/BV1GW411j7TG?p=3



file://和smb://的区别





samba主要用于在windows和unix之间共享资源。资源包括文件、打印机等等。

NFS主要用于在UNIX/LINUX上。

从配置来看，samba比较复杂，nfs比较简单。

samba能解决win和linux,linux和linux之间的共享，但是SMB协议是MS的，SMB的高级特性是和windows的特性联系紧密的。但NFS更简洁，方便，更原生，兼容性更好。

这个是带密码的smb链接写法。

```
smb://Administrator:P%40ss@msmith1/c/WINDOWS/Desktop/foo.txt
```

这个符合我的需求了。





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

9、SMB协议

https://baike.baidu.com/item/SMB%E5%8D%8F%E8%AE%AE

10、

https://www.jianshu.com/p/15893eece2ee

11、

https://zhidao.baidu.com/question/2121939832608350307.html

12、samba数据源类似file的调用---SmbFile

https://blog.csdn.net/q790006739/article/details/88817473