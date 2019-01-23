---
title: nodejs之部署方法
date: 2019-01-23 11:15:55
tags:
	- nodejs

---



安装基本工具：

```
npm i pm2 webpack vue-cli -g
```

pm2是用来管理nodejs进程的工具。pm是Process Manager的意思。

```
# 启动进程
pm2 start app.js
# 启动4个进程进行负载均衡
pm2 start api.js -i 4
# 监控进程
pm2 monitor
# 让pm2随着服务器启动而启动
pm2 startup
```

官网是https://pm2.io

# 简单版本

这个做法不需要依赖太多的外部的东西。

1、安装nginx。

2、保持nginx的默认配置不变。

3、在/etc/nginx/conf.d下面新建一个test-8081.conf文件。

内容如下：

```
upstream hello {
    server 0.0.0.0:8081;
}

server {
    listen 80;
    server_name hello.nginx;
    location / {
        proxy_set_header Host  $http_host;
        proxy_set_header X-Real-IP  $remote_addr;
        proxy_set_header X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_set_header X-Nginx-proxy true;
        proxy_pass http://hello;
        proxy_redirect off;
    }
}
```

这个配置是表示把对80端口的访问转到8081端口。

4、测试一下配置是否是好的。

```
sudo nginx -t
```

然后重启nginx。

5、写一个hello.js，随便哪个目录。

```
const http = require('http')
http.createServer(function(req,res) {
        res.writeHead(200,{'Content-Type':'text/plain'})
        res.end('hello world')
        }).listen(8081)

console.log('server test')
```

6、运行node hello.js。如果不允许这个，就提示502错误。

访问127.0.0.1，就可以看到hello world了。

# 改进版本

用pm2来启动hello.js。

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ pm2 start hello.js 

[PM2] Starting /home/hlxiong/work/test/node/hello.js in fork_mode (1 instance)
[PM2] Done.
┌──────────┬────┬─────────┬──────┬───────┬────────┬─────────┬────────┬─────┬───────────┬─────────┬──────────┐
│ App name │ id │ version │ mode │ pid   │ status │ restart │ uptime │ cpu │ mem       │ user    │ watching │
├──────────┼────┼─────────┼──────┼───────┼────────┼─────────┼────────┼─────┼───────────┼─────────┼──────────┤
│ hello    │ 0  │ N/A     │ fork │ 31268 │ online │ 0       │ 0s     │ 0%  │ 27.3 MB   │ hlxiong │ di
```

可以用pm2 list查看。

可以用pm2 log查看日志。

用pm2 stop hello停止。

用pm2 delete hello来删除这个任务。





参考资料

1、

https://segmentfault.com/a/1190000010098126