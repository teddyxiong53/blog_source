---
title: supervisor了解
date: 2019-11-02 10:55:49
tags:
	- Linux

---

--

# 新建配置

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

# 增加配置

现在我的supervisor正常在运行，我新增了一个conf文件。

frps.conf

执行提示错误：

```
ubuntu@VM-0-17-ubuntu:/etc/supervisor/conf.d$ sudo supervisorctl reread
frps: available
ubuntu@VM-0-17-ubuntu:/etc/supervisor/conf.d$ sudo supervisorctl start frps
frps: ERROR (no such process)
```

我执行update

```
ubuntu@VM-0-17-ubuntu:/etc/supervisor/conf.d$ sudo supervisorctl update
frps: added process group
```

这样frps被自动启动了。

reload是重启supervisord。

update是刷新配置文件。

# 支持python virtualenv

因为我的pyspider的安装在virtualenv里的，又需要开机启动运行。

其实很简单，就是用绝对路径来指定python就好了。

不行，会找不到对应的模块。

可以采用`bash`脚本，脚本里面`source virtualenv`和启动服务，然后`supervisor`去调那个`bash`脚本的方式来管理进程。

```
teddy@thinkpad:~/work/pyspider$ cat start_pyspider.sh 
#!/bin/sh
TOP=/home/teddy/work/pyspider
source $TOP/.venv/bin/activate
pyspider -c $TOP/config.json > /dev/null 2>&1 &
```



# 问题

unix:///var/run/supervisor.sock no such file



# 参考资料

1、Supervisor的作用与配置

https://www.jianshu.com/p/0226b7c59ae2

2、

https://stackoverflow.com/questions/55561601/why-supervisorctl-error-no-such-process

3、supervisor + virtualenv + gunicron

https://www.jianshu.com/p/40caabd91827

