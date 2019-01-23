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



#一些配置项

##sendfile

现在的web服务器都提供sendfile的选项来提高服务器的性能。

那么什么是sendfile？这个选项又是如何影响性能的呢？

这个是Linux2.0以后推出的一个系统调用。

```
#include <sys/sendfile.h>
ssize_t sendfile(int out_fd, int in_fd, off_t *offset, size_t count);
```

主要是避免多次拷贝。

##tcp_nopush

这个是在使用sendfile的时候，才可能触发的一个选项。

tcp_nopush和tcp_nodelay是相反的作用。

就是用来避免小包导致网络拥塞的。



nginx的配置文件以block为单位进行组织，每个block就是一对大括号。

nginx的配置文件主要分为4个部分：

```
main：全局配置
server：主机配置
upstream：上游服务器配置，主要为反向代理、负载均衡相关。
location：url配置特定位置。
```

层次关系是这样：

```
main
	events
	http
		server
			location
			
```



一个完整的例子。

```
user www-data; # 指定nginx worker进程的用户
worker_process 2; # 跟cpu核心数一样。
pid /run/nginx.pid;
worker_rlimit_nofile 65535; #指定单进程最多打开的文件个数，跟系统设定一致
events {
    user epoll;
    worker_connections 65535;
}

http {
    include mime.types;
    default_type application/octec-stream; #指定默认类型为二进制流，
    # 实际效果是：在文件类型未知时，访问对应的url，浏览器是弹出下载窗口
    log_format main 'xxx'; #设置日志格式
    client_max_body_size 20m; # 客户端请求的最大的单个文件大小。
    client_header_buffer_size 16k; 指定客户端请求头的headerbuffer大小。

    sendfile on; #打开高效传输模式
    tcp_nopush on;
    tcp_nodelay on;

    keepalive_timeout 65; #

    gzip on; #开启gzip压缩，实时压缩输出数据流
    server_tokens off; #隐藏nginx版本号。

    server {
        listen 8080;
        server_name xx.com;
        charset utf-8;
        access-log logs/host.access.log main; # 指令访问日志的位置



        location / {
            index index.html;
            root /var/www/html;

        }
        location /down {
            autoindex on; #打开浏览网站文件的功能。
        }
        location ~(jsp|\?) {
            # 指定url里包含js或者?的全部转发到指定服务器端口进行处理。
            proxy_pass http://192.168.0.1:80;
        }
    }
}
```

一般server部分，就单独写到外面。

然后include到主配置文件。



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

5、Full Example Configuration

https://www.nginx.com/resources/wiki/start/topics/examples/full/

6、本博客 Nginx 配置之完整篇

https://imququ.com/post/my-nginx-conf.html

7、nginx sendfile tcp_nopush tcp_nodelay参数解释

https://blog.csdn.net/zmj_88888888/article/details/9169227

8、理解nginx的配置

http://me.52fhy.com/php_dev_environment/09 理解nginx配置.html

9、Nginx配置文件实例整理

https://www.linuxidc.com/Linux/2017-02/140364.htm