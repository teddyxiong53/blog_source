---
title: nodejs之pm2
date: 2021-12-04 18:22:11
tags:
	- nodejs

---

--

https://github.com/jackhutu/jackblog-api-express/blob/master/process.json

pm2启动可以指定一个process.json文件来指定一些特性。

```
{
  "apps": [
    {
      "name"              : "jackblog-api",
      "script"            : "./server/app.js",
      "log_date_format"   : "YYYY-MM-DD HH:mm Z",
      "out_file"          : "./logs/pm2-out.log",
      "error_file"        : "./logs/pm2-err.log",
      "pid_file"          : "./logs/jackblog-api.pid",
      "ignoreWatch"       : ["[\\/\\\\]\\./", "node_modules"],
      "watch"             : "false",
      "exec_mode"         : "fork_mode", //cluster_mode
      "env": {
        "NODE_ENV"        : "production"
      }
    }
  ]
}
```

# 什么是pm2

pm2是一个daemon进程的管理器。

帮你管理和keepalive你的进程。

通过npm来安装。

```
npm i -g pm2
```

# 基本使用

启动一个nodejs脚本

```
pm2 start app.js
```

启动一个shell脚本

```
pm2 start test.sh
```

启动一个python脚本

```
pm2 start test.py --watch
```

启动一个可执行文件

```
pm2 start test -- --port 1234
```

## 命令行常用的选项

## 常用的子命令

```
pm2 start/stop/restart xx
pm2 delete xx

如果xx==all，那么表示把所有的都操作一下。

pm2 ls
ls有ps、status这2个alias。作用一样。


pm2 logs  查看日志

pm2 monit  这个在命令行显示一个dashboard

pm2 plus 这个是启动一个web的dashboard。这个执行时，会询问你是否有pm2.io的账号，如果没有，就在命令上进行注册操作。
		这个操作还比较流畅。
		这个是连接到官方网站的。
		我之前其实已经把我的qinglong wechat的连接上去了。上面有统计数据。
		
```

# 文件目录分析

相关文件的都是在`~/.pm2`目录下。

有这些文件：

```
pm2.log
	这个是pm2工具本身的日志。
logs
	这个是相关的App的运行日志目录里。
```

# 用json文件来管理多个进程

```
[{
    "name"      : "echo",
    "script"    : "./examples/echo.js",
    "max"       : "10",
    "instances" : "max",
    "args"      : "-d 1"
},{
    "name"      : "api",
    "script"    : "./examples/child.js",
    "instances" : "4"
},{
    "name"      : "bus",
    "script"    : "./examples/echokill.js"
}]
```

然后pm2 start test.json就可以统一管理上面的多个进程。



# 以0.4.10版本来分析代码

pm2是对nodejs的cluster模块的封装。

它可以自动监听进程状态、重启进程、停止不稳定的进程（避免无限循环重启）

利用pm2，可以在不锈钢代码的情况下，实现负载均衡集群。

lib目录下的God.js和Satan.js是主要的逻辑。



Satan.js提供了程序的退出、杀死等方法，因此它是魔鬼；God.js 负责维护进程的正常运行，当有异常退出时能保证重启，所以它是上帝



# 参考资料

1、官方文档

https://pm2.keymetrics.io/docs/usage/quick-start/

2、源代码分析

https://www.jianshu.com/p/ac843b516fda

3、

https://tsejx.github.io/node-guidebook/server-application/pm2/