---
title: docker之学习（三）创建docker镜像
date: 2018-01-22 11:10:32
tags:
	- docker

---



创建docker镜像的基础是编写Dockerfile。

先看一个例子。

#写Dockerfile

新建一个example目录。在里面新建一个Dockerfile。内容如下：

```
FROM ubuntu:latest
MAINTAINER teddyxiong53 <1073167306@qq.com>
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y nginx
RUN echo "\daemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx

VOLUME ["/data", "/etc/nginx/site-enabled", "/var/lib/nginx"]

WORKDIR /etc/nginx

CMD ["nginx"]
EXPOSE 80
EXPOSE 443

```

解释：

1、FROM。指定基于的基础镜像。

2、MAINTAINER。指定维护者信息。

3、RUN。运行shell脚本或者命令。因为创建镜像过程中不能接收用户输入，所以ap-get install要指定y，来避免那个手动输入的确认过程。

4、CMD。容器启动时执行的命令。

5、EXPOSE。与主机相连的端口号。

因为这个脚本在执行过程中，update非常慢，而且两次都失败了。报错：

```
E: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
The command '/bin/sh -c apt-get install -y nginx' returned a non-zero code: 100
```

不打算安装nginx了。改为下面这样：

```
FROM ubuntu:latest
MAINTAINER teddyxiong53 <1073167306@qq.com>
RUN apt-get update
RUN apt-get install -y mini-httpd

CMD ["mini_httpd"]
EXPOSE 80
EXPOSE 443

```

我选择使用mini_httpd这个。



# 用build命令创建镜像

执行命令：

```
docker build --tag hello:0.1 .
```

注意最后那个点号，表示的是Dockerfile所在路径。0.1是指定标签。如果不指定，就是latest。

然后用docker images查看。

运行：

```
docker run --name hello-nginx -d -p 80:80 -v /root/data:/data hello:0.1
```

`-p 80:80`：表示把容器的80端口和主机的80端口对接起来。这样我们访问http://主机ip:80就是访问容器里的80端口了。

`-v /root/data /data`：表示把主机的/root/data连接到容器的/data目录。

创建过程打印：

```
teddy@teddy-ubuntu:~/work/test/example$ docker build --tag hello:0.1 .
Sending build context to Docker daemon 2.048 kB
Step 1/7 : FROM ubuntu:latest
 ---> 7b9b13f7b9c0
Step 2/7 : MAINTAINER teddyxiong53 <1073167306@qq.com>
 ---> Using cache
 ---> 9994a9a8eceb
Step 3/7 : RUN apt-get update
 ---> Using cache
 ---> 627cb8341031
Step 4/7 : RUN apt-get install -y mini-httpd
 ---> Running in d65bb53f33dd
Reading package lists...
Building dependency tree...
Reading state information...
....省略部分打印
Processing triggers for systemd (229-4ubuntu17) ...
 ---> 712a52b05681
Removing intermediate container d65bb53f33dd
Step 5/7 : CMD mini_httpd
 ---> Running in 6bf669c0e4e6
 ---> 7c70d79f39b9
Removing intermediate container 6bf669c0e4e6
Step 6/7 : EXPOSE 80
 ---> Running in c3e3f9175bc4
 ---> f468fdf2d615
Removing intermediate container c3e3f9175bc4
Step 7/7 : EXPOSE 443
 ---> Running in 801f105c44a5
 ---> 913bff44f2c0
Removing intermediate container 801f105c44a5
Successfully built 913bff44f2c0
```

# 什么是docker镜像

1、docker镜像是由文件系统叠加而成的。

2、最低端是一个引导文件系统，叫做bootfs。

3、第二层是rootfs。rootfs里放的就是Ubuntu系统。

4、镜像可以叠加。最底层的叫基础镜像。

