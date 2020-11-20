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

密码长度有要求，我只能用最复杂的那个密码。

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



国内类似heroku的平台有哪些？

bmob.com，名字叫比目。

rainbond.com。名字叫云帮。



heroku从2007年开始运营。平台的灵活性高，支持多种编程语言。

如果要把应用部署到heroku上，需要使用git来推送到heroku的git服务器上。由这个git服务器来完成安装和升级操作。

heroku使用名为dyno的计算单元来衡量使用量。并作为收费的依据。

最常用的dyno类型是web dyno。表示一个web服务器实例。

如果想要增加处理请求的能力，可以部署多个web dyno。每个dyno运行一个实例。

另外一种dyno是worker dyno。用于执行后台作业或者其他辅助任务。

heroku提供了大量的插件和扩展，可用于数据库、email和其他服务。

下面我们看看把flasky部署到heroku的步骤。

1、注册heroku账户。有免费套餐，非常适合用来做实验。

2、安装heroku cli。

```
安装好之后，执行
heroku login
输入你的email和密码。
```

3、把你的ssh公钥上传到heroku。这样才能用git push。正常情况下，heroku login会自动上传你的ssh公钥。

4、创建应用。

```
heroku create xhl-flasky
对应的域名是：xhl-flasky.herokuapp.com
```

毫无疑问，你的应用名字必须是唯一的。

在创建应用的过程中，heroku会为你的应用创建一个git仓库。对应的地址是：

https://git.heroku.com/xhl-flasky.git

必须设置FLASK_APP环境变量才能使用flask命令。

```
heroku config:set FLASK_APP=flasky.py
```

5、配置数据库。

heroku以扩展形式支持postgres数据库。heroku的免费套餐包含一个小型数据库，最多能存1万条记录。

执行下面的命令，为应用绑定一个postgres数据库。

```
heroku addons:create heroku-postgresql:hobby-dev
```

6、配置日志。

heroku把应用写入到stdout和stderror的输出看做日志。

```
heroku config:set FLASK_CONFIG=heroku
heroku config:set SECRET_KEY=xxx
```

7、配置email。

heroku没有提供smtp服务器。

所以我们需要配置一个外部服务器，发送量不大的时候，我们可以用自己的一个邮箱就行了。

还是为了安全，通过环境变量的方式来设置。

```
heroku config:set MAIL_USERNAME=xx@xx.com
heroku config:set MAIL_PASSWORD=xxx
```

8、使用flask-sslify开开启https。

前面我们看到，我们的应用的域名其实是heroku的二级域名。

所以我们的https用的证书其实是heroku的证书。

因此，为了安全，我们只需要拦截发给http的请求，重定向到https。这个就是flask-sslify完成的工作。

9、运行web生产服务器。

heroku要求应用自己启动web生产服务器，并在PORT环境变量设置的端口号上监听请求。

flask自带的web开发服务器，不适合在这种情况下使用。因为它不是为生产环境设计的。

生产服务器有2个常用的：uwsgi和gunicorn。

10、服务器上运行。

```
heroku run flask deploy
```

创建并配置好数据库表之后，重启应用。使用更新后的数据库。

```
heroku restart
```

查看日志：

```
heroku logs
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

5、《Flask web开发》第17章。