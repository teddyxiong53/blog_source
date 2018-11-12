---
title: 反向代理之ngrok
date: 2018-11-12 22:48:28
tags:
	- 网络

---



进入https://ngrok.com网络，注册账号。

我就用github账号来注册。

然后下载工具，我就先用windows的试一下。

就是一个可执行程序，不用安装的。

执行命令，得到： C:\Users\Administrator/.ngrok2/ngrok.yml这个文件。

文件里也就是把授权码放进去了而已。

我本地把wamp启动了。

然后执行命令：

```
./ngrok.exe http 80
```

得到打印输出如下：

```
ngrok by @inconshreveable                                                                                                                                                                                                     (Ctrl+C to quit)

Session Status                online
Account                       teddyxiong53 (Plan: Free)
Version                       2.2.8
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://0cbe99aa.ngrok.io -> localhost:80
Forwarding                    https://0cbe99aa.ngrok.io -> localhost:80

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

我访问http://0cbe99aa.ngrok.io这个地址，跟直接访问localhost是一样的效果。

当前用的是免费的，每次重启ngrok，都会随机重新生成域名。如果要固定，需要付费。



这个也有解决方法，就是自己在vps上搭建ngrok服务就好了。



# 参考资料

1、ngrok使用教程

https://blog.csdn.net/liu_005/article/details/79557818

2、VPS自搭建Ngrok内网穿透服务

https://www.jianshu.com/p/d35962b0dba4