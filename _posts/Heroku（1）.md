---
title: Heroku（1）
date: 2018-07-20 23:01:58
tags:
	- 网络

---



看Flask，看到有人提到Heroku这个东西，了解一下。

Heroku是Salesforce旗下的云服务商。提供各种云服务，包括服务器、数据库、监控、计算等。

也提供了免费版本。虽然有时长和宕机的限制。但是对于我们个人使用也够用的。

Heroku是做Ruby的PAAS起家的。是最早的云平台之一。现在支持多种语言。

PaaS平台有：GAE、国内的SAE。

PaaS和vps的区别：

PaaS不需要你配置服务器。不需要安装数据库，也不需要去管负载均衡。平台会帮你打理一切。

你只需要专注自己的业务，把应用的逻辑写好。然后发布就好了。

数据库方面，如果你需要mysql，你可以从平台得到一个mysql地址，用户名和密码，就可以使用了。

如果你的应用流量增大了，你可以到PaaS的管理界面上，增加实例就可以了。



官网：https://www.heroku.com/

要翻墙才能上。

先注册。用qq邮箱看看。提示了这个。

```
The domain qq.com has been blocked.
```

还是换成gmail吧。



https://devcenter.heroku.com/articles/heroku-cli

这里下载CLI工具。命令行工具。

安装完成后，在cmd窗口里输入heroku，就可以看看到帮助信息了。

然后ping一下heroku.com，可以ping通的。

可以看到heroku的服务器就是在亚马逊的AWS上的。所以是很稳定可靠的。

```
teddy@teddy-ubuntu:~$ ping heroku.com
PING heroku.com (50.19.85.156) 56(84) bytes of data.
64 bytes from ec2-50-19-85-156.compute-1.amazonaws.com (50.19.85.156): icmp_seq=1 ttl=128 time=235 ms
64 bytes from ec2-50-19-85-156.compute-1.amazonaws.com (50.19.85.156): icmp_seq=2 ttl=128 time=234 ms
64 bytes from ec2-50-19-85-156.compute-1.amazonaws.com (50.19.85.156): icmp_seq=3 ttl=128 time=233 ms
```

前面我担心我的linux虚拟机里没有翻墙，不能访问这个网站，既然现在看到是可以的。

那么我就尽量在linux下来做。

安装工具：

```
curl https://cli-assets.heroku.com/install.sh | sh
```

这里就开始不能正常了。尽管我让虚拟机通过pc来代理ssr。还是速度太慢。



然后输入heroku login。输入email和密码。密码是你注册heroku时写的密码。是要比较复杂的那种。

密码错了会提示这个：

```
Password: ***********
 »   Error: Invalid credentials provided.
 »
 »   Error ID: unauthorized
```

我现在登录成功了。



为什么使用云平台？

1、不要自己租域名，不用租服务器。不用备案，不要手动配置各种软件。

2、免费。

云平台有什么缺点？

1、流量限制，性能相对差一些。但是个人网站是够用的。需要扩展可以花点钱。

2、用的是二级域名，要使用自己的域名的话，使用alias设置别名。

为什么用国外的云平台？

1、国内的文档不完善，限制多。

为什么使用heroku？

对Python支持好。



heroku的部署是基于git的。

heroku官方提供了一个Django部署的文档。

https://devcenter.heroku.com/articles/django

创建虚拟环境。

我尽量在mingw里做。这里操作比较顺手。

```
Administrator@hostpc MINGW64 /d/work/heroku/hellodjango
$ virtualenv venv --distribute
New python executable in D:\work\heroku\hellodjango\venv\Scripts\python.exe
Installing setuptools, pip, wheel...done.
```



```
Administrator@hostpc MINGW64 /d/work/heroku/hellodjango/venv
$ ls
Include/  Lib/  Scripts/  tcl/
```

在Scripts目录下，有可执行文件。

但是这个虚拟环境不能在mingw下激活。所以我只能又回到cmd下面。

这样就激活了venv了。

```
d:\work\heroku\hellodjango\venv\Scripts
λ activate.bat

(venv) d:\work\heroku\hellodjango\venv\Scripts
λ
```

在venv下，安装东西：

```
pip install Django psycopg2 gunicorn dj-database-url
```





# 参考资料

1、Heroku 教程：使用 Heroku 快速搭建站点

https://segmentfault.com/a/1190000014699439?utm_source=tag-newest

2、线上部署：heroku

http://wiki.jikexueyuan.com/project/node-lessons/heroku.html

3、详细描述一次最新Heroku部署python web项目的完整过程

https://blog.csdn.net/daixin_me/article/details/53995845

4、Heroku实战入门（一）初识heroku

https://www.cnblogs.com/numbbbbb/archive/2013/04/30/3051740.html