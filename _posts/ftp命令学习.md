---
title: ftp命令学习
date: 2018-01-18 11:16:06
tags:
	- ftp

---



windows上搭建一个ftp服务器，linux端要从这个服务器上下载东西下来。怎么操作？

1、在windows上搭建ftp服务器。本来打算弄个简单的绿色的，但是试了几个都不太好，还是选择使用serv-U。配置域win7_ftp_server。配置用户和密码。

2、linux端命令行进行连接。

```
$ ftp
> open 192.168.190.1
然后根据提示输入用户名和密码。连接成功。
> ls 
可以查看目录下有什么文件。
> get 1.txt
下载文件。
> put 2.txt
上传文件。
> bye
退出。
```

