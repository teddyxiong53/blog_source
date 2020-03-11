---
title: 渗透之lazagne
date: 2020-03-10 09:12:28
tags:
	- 渗透

---

1

lazagne是一个用来查看本地计算机的密码的工具。

目前最新的release版本是2.4.3 ，下载到电脑上，杀毒软件会提示是木马。

代码在这里：

https://github.com/AlessandroZ/LaZagne

使用方法，在cmd窗口里执行。后面可以跟这些参数。

```
chats               Run chats module       
mails               Run mails module       
all                 Run all modules        
git                 Run git module         
svn                 Run svn module         
windows             Run windows module     
wifi                Run wifi module        
maven               Run maven module       
sysadmin            Run sysadmin module    
browsers            Run browsers module    
games               Run games module       
multimedia          Run multimedia module  
memory              Run memory module      
databases           Run databases module   
php                 Run php module         
```

目前在我的机器上测试的情况是：

chats：没有检查出来。

mails：没有检查出来。

git：检查出来gitee和github的，但是gitee的是明文，而github是加密过的。

wifi：可以很容易检查出连接过的wifi的密码。

sysadmin：这个可以检查出在这个电脑上使用ssh连接过的服务器的密码。

browsers：这个很要命。基本上密码都被检查出来了。

all：这个就是把所有的模块都跑一遍。跑这个就够了。所有的密码都出来了。



在我的Linux笔记本上没有检测出任何密码。这个就有点奇怪了。

Linux这么安全？至少wifi密码能找到吧。哦，知道了。是因为需要sudo权限来执行。







这个很可怕。需要研究一下原理。



这些是因为本地保存了明文密码还是什么？

LaZagne项目是一个开源应用程序，用于检索存储在本地计算机上的大量密码。 每个软件使用不同的技术（明文，API，自定义算法，数据库等）存储其密码。 此工具的开发目的是找到这些最常用的软件的密码。



源代码不多，python写的。

我有点后悔直接在我的电脑上跑了这个程序。不知道打包好的那个release包，里面有没有什么问题。如果它把检查出来的密码直接发出去了就比较麻烦了。

事已至此，还是相信这个开发者是有职业道德的。



使用pycharm来调试一下。在windows下。

1、新建一个工程，使用conda下面的python2.7的解释器。

2、把代码的windows目录拷贝到建立的工程目录下。

3、安装依赖。

```
1、cd 到当前工程自己的python解释器目录下。
2、python.exe -m pip install -r requirements.txt
```

4、运行一下lazagne.py，可以跑起来。







参考资料

