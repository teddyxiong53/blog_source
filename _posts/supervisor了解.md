---
title: supervisor了解
date: 2019-11-02 10:55:49
tags:
	- Linux

---



supervisor是一个进程管理工具。

它实现进程管理的方式是：把被管理进程作为自己的子进程来管理。

所以需要在配置文件里，加入我们希望被管理的进程的可执行文件路径。

安装：

```
sudo apt-get install supervisor
```

配置文件在 /etc/supervisor/supervisord.conf 

这个文件我们不需要改。

如果需要增加进程被supervisor管理，在/etc/supervisor/conf.d目录下，新增xx.conf文件。

内容如下：

```
; xx config

[program:xx]
command = python /path/xx.py
directory = /path
user = www-data
startsecs = 3

redirect_stderr = true
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
stdout_logfile = /path/xx.log
```

然后重启supervisor。

```
sudo /etc/init.d/supervisor restart
```

主要命令：

```
# 查看状态
sudo supervisorctl status 
# 启动
sudo supervisorctl start xx
# 停止
sudo supervisorctl stop xx
```



参考资料

1、Supervisor的作用与配置

https://www.jianshu.com/p/0226b7c59ae2