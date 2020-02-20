---
title: linphone学习（1）
date: 2020-02-20 13:45:51
tags:
	- 音频

---

1

搭建sip服务器

在基于sip协议进行voip通话时，手续需要搭建sip服务器。

opensips

从官网下载LTS版本。

2.4版本是一个LTS版本。网上不少的文章都是基于这个来讲解的。



https://opensips.org/pub/opensips/2.4.7/

需要的依赖：

```
sudo apt-get install libncurses5-dev libncursesw5-dev libxml2-dev
```

安装mysql支持。安装时，提示设置root的密码。设置为最简单的那个。

```
 sudo apt-get install libmysqlclient-dev   mysql-client mysql-server
```

执行make menuconfig。

改动2个点就可以了：

```
1、需要打开db_mysql
2、指定prefix为/usr/local/opensips
```

menuconfig的结果，保存在Makefile.conf文件里。

参考官方文档进行编译：

https://www.opensips.org/Documentation/Install-CompileAndInstall-2-4

编译安装：

```
make all -j4
sudo make install
```

安装后的目录情况：

```
root@teddy-ThinkPad-SL410:/usr/local/opensips# tree
.
├── etc
│   └── opensips
│       ├── opensips.cfg
│       ├── opensipsctlrc
│       └── osipsconsolerc
├── lib64
│   └── opensips
│       ├── modules
│       └── opensipsctl
│           ├── opensipsctl.base
│           ├── opensipsctl.ctlbase
│           ├── opensipsctl.fifo
│           ├── opensipsctl.sqlbase
│           ├── opensipsctl.unixsock
│           └── opensipsdbctl.base
├── sbin
│   ├── opensips
│   ├── opensipsctl
│   ├── opensipsdbctl
│   ├── opensipsunix
│   ├── osipsconfig
│   └── osipsconsole
└── share
```

修改/usr/local/opensips/etc/opensips/opensipsctlrc

主要目的是配置mysql的。还有配置ip地址。

然后是修改opensips.cfg文件。

这个最好是重新生成一个。

代码目录下执行menuconfig，选择生成配置脚本。

然后把得到的cfg文件，拷贝到/usr目录下去，替换默认的opensips.cfg。

在这个基础上进行修改。

改完后，执行命令检查一下配置：

```
opensips -C
```

创建数据库。

```
opensipsdbctl create
```

启动服务：

```
opensipsctl start
```

添加账号。

```
opensipsctl add 1000 1000
opensipsctl add 2000 2000 
```

我把台式机Ubuntu作为服务器，笔记本和手机作为2个通话设备。可以正常进行通话。



Ubuntu下安装linphone。

```
sudo apt-get install linphone
```





参考资料

1、【SIP】opensips 服务器搭建测试 2016-02-25 09:09:38

https://blog.csdn.net/jhope/article/details/53129122?utm_source=distribute.pc_relevant.none-task

2、

https://blog.csdn.net/qq_38631503/article/details/80005454