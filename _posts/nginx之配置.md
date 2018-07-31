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



# nginx配置文件结构

```
#全局块
events {
  #events块
}
http { # http块
  ... # http全局块
  server { # server块
    ... # server全局块
    location { # location块
      
    }
  }
  server {
    
  }
  ... # http全局块
}
```

1、全局块。配置会影响nginx全局的。一般包括：用户组，pid文件路径，log文件路径，include其他文件。

2、events块。最大连接数。

3、http块。里面可以放多个server块。

4、location块。配置请求的路由。



```
在http的server里增加rewrite ^(.*) https://$host$1 permanent;
这样就可以实现80进来的请求，重定向为https了。
```



# location配置详解

```
location = / {
   # 规则A
}
location = /login {
  # 规则B
}
location ^~ /static/ {
  # 规则C
}
location ~ \.(gif|jpg|png|js|css)$ {
  # 规则D
}
location ~* \.png$ {
  # 规则E
}
location !~ \.xhtml$ {
  # 规则F
}
location !~* \.xhtml$ {
  # 规则G 
}
location / {
  # 规则H
}
```

访问根目录/，匹配到规则A。

访问http://localhost/login 将匹配规则B。

访问http://localhost/register 将匹配规则H。（为什么？？）

访问http://localhost/static/a.html 将匹配规则C。



uwsgi_pass



# 参考资料

1、Nginx配置详解

https://www.cnblogs.com/knowledgesea/p/5175711.html

2、SSL证书安装指引

https://www.cnblogs.com/lxwphp/p/8288003.html

3、nginx的location配置详解

这篇文档特别好。

https://www.cnblogs.com/sign-ptk/p/6723048.html

4、跨过Nginx上基于uWSGI部署Django项目的坑

https://www.cnblogs.com/qingspace/p/6838747.html