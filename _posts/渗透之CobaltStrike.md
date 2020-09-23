---
title: 渗透之CobaltStrike
date: 2020-09-23 17:10:30
tags:
	- 渗透

---

1

[Cobalt Strike](https://www.cobaltstrike.com/): C/S架构的商业渗透软件，适合多人进行团队协作，可模拟APT做模拟对抗，进行内网渗透

New Cobalt Strike licenses cost $3,500 per user for a one year license. License renewals cost $2,500 per user, per year. Request a quote to begin the purchase process.

是商业收费软件。

简称CS。在业内非常有名。



Cobalt Strike是一款超级好用的渗透测试工具，拥有多种协议主机上线方式，

集成了提权，凭据导出，端口转发，socket代理，office攻击，文件捆绑，钓鱼等多种功能。

同时，Cobalt Strike还可以调用Mimikatz等其他知名工具，因此广受技术大佬的喜爱。

学会使用这款“神器”可以在我们渗透的过程中起到事半功倍的作用

这个工具的社区版是大家熟知的Armitage(一个MSF的图形化界面工具)，而Cobalt Strike大家可以理解其为Armitage的商业版。



早期版本Cobalt Srtike依赖Metasploit框架，

而现在Cobalt Strike已经不再使用MSF而是作为单独的平台使用，

它分为客户端(Client)与服务端(Teamserver)，

服务端是一个，客户端可以有多个，团队可进行分布式协团操作。



Armitage 这个工具，从github上看，代码都是5年前更新的。说明这个项目不活跃了。

这个是官网介绍。

https://www.offensive-security.com/metasploit-unleashed/armitage/

Armitage是java写的基于metasploit的工具。

Ubuntu不能apt-get直接安装。

到官网下载安装包。

http://www.fastandeasyhacking.com/

解压后，把路径加入到PATH里。

还需要配置一个环境变量。

```
export MSF_DATABASE_CONFIG=/home/teddy/.msf4/database.yml
export PATH=$PATH:/home/teddy/armitage
```

然后执行armitage启动。弹窗提示登陆，直接默认选项登陆就好了。

可以顺利了打开图形界面。

可以点击菜单：hosts-- add hosts。我们就添加一台计算机。

然后就出现一台计算机的图标。我们可以在上面右键选择scan。就可以进行扫描。



参考资料

1、Cobalt Strike系列教程第一章：简介与安装

https://zhuanlan.zhihu.com/p/93718885

2、ubuntu下安裝armitage

https://cloud.tencent.com/developer/article/1197998