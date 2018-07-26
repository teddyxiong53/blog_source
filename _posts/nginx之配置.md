---
title: nginx之配置
date: 2018-01-16 16:51:57
tags:
	- nginx

---



把nginx配置时碰到的疑问记录下来。

先列一个简单的default配置。主要针对这个分析。

```
server {
	listen 80 default_server;
	listen [::]:80 ipv6only=on default_server;

	root /var/www/html;

	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
		try_files $uri $uri/ =404;
	}

}
```



## default_server代表什么？

因为一个conf文件里，可以配置多个server，如果都匹配不上，就交给配置了default_server的server进行处理。



## server_name为一个下划线代表什么？

下划线没有特别含义，表示一个无效值，server_name后面正常的应该是跟一个域名的。

nginx里的虚拟主机是通过http请求里的host值来找到对应的虚拟主机的。如果找不到呢？那就是交给default_server来处理。

写ip没有意义（这里要跟的是一个host name），可以写一个下划线(_)，或者完全不写server_name

## nginx配置调试方法

改完后，用nginx -t测试一下。

我发现这种方式没有用。

