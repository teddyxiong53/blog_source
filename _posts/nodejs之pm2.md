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



参考资料

1、

