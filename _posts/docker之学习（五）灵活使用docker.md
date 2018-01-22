---
title: docker之学习（五）灵活使用docker
date: 2018-01-22 11:52:01
tags:
	- docker

---



# 1. 搭建docker私有仓库

docker命令默认使用的docker仓库是docker hub。

docker注册服务器也是一个docker镜像。先下载。

```
docker pull registry:latest
```

运行：

```
docker run -d -p 5000:5000 --name hello-registry \
-v /tmp/registry:/tmp/registry \
registry
```

现在我们把之前创建的hello:0.1镜像上传到私有仓库。

```
docker tag hello:0.1 localhost:5000/hello:0.1
docker push localhost:5000/hello:0.1
```

这样，我们在另外一台电脑上可以连接到我们这个私有仓库进行下载。

````
docker pull 192.168.190.130:5000/hello:0.1
````

远程删除镜像：

```
docker rmi 192.168.190.180:5000/hello:0.1
```

还可以用亚马逊的云服务来存储自己的私有镜像。



# 2.连接docker容器

以web应用为例，虽然我们可以把web server、数据库都安装在一个镜像里，但是更多的做法是放到不同的镜像里。那么就需要让两个镜像进行连接通信才行。应该怎么做呢？

举例说明如下。

我们先下载一个MongoDB的数据库镜像。

```
docker run --name db -d mongo
```

直接run，如果没有，会先自动下载的。

接下来，我们创建web容器。并且和db容器连接起来。

```
docker run --name web -d -p 80:80 --link db:db nginx
```

`--link <容器名字>:<别名>`

link这个选项有个限制，就是只限于在同一个服务器上的多个容器。

如果对于分布在不同的服务器上的容器，应怎样进行连接呢？

可以借助于一个叫Ambassador的容器来做。具体不看先。



# 3. 创建docker基础镜像

通过Dockerfile创建镜像的时候，是基于docker hub上的官方镜像来做的。

现在我们想要看看怎样创建自己的私有基础镜像。

##Ubuntu基础镜像

我们看看怎么创建Ubuntu基础镜像。

1、安装debootstrap工具。

```
sudo apt-get install debootstrap
```

从帮助信息里看，这个工具的作用是：

```
debootstrap - Bootstrap a basic Debian system
```

de代表的就是Debian系统。

现在我们下载Ubuntu14.04的二进制文件。14.04的代号是trusty。

```
sudo deboootstrap trusty trusty
```

`deboootstrap <代号> <目录>`

然后用import命令来创建基础镜像。

```
sudo tar -C trusty -c . | sudo docker import - trusty
```

命令的前半部分是用来创建一个压缩包文件。

`import <url或者-> <镜像名字>:<标签> `

如果是通过管道接受数据，就是用`-`。url的例子是这样的：

```
docker import http://xxx.com/trusty.tgz trusty
```

然后我们可以用这个镜像来run了。



## 创建空的基础镜像

用/dev/null来作为数据来源：

```
tar cv --files-from /dev/null | sudo docker import - xhl_docker_img
```

这样我们就创建了一个空的基础镜像了。

怎么用呢？

我们先写一个hello.c，并且在主机上编译好。

```
#include <stdio.h>

int main()
{
    printf("hello docker empty image\n");
    return 0;
}

```

编译为静态的可执行文件。

```
gcc hello.c -static -o hello
```

然后我们在当前目录新建一个Dockerfile。内容如下：

```
FROM xhl_docker_img
ADD ./hello /hello
CMD ["/hello"]
```

然后我们创建这个镜像。

```
docker build --tag hello-img:0.1
```

然后运行：

```
docker run --rm hello-img:0.1
```

`--rm`表示的是，如果有同名的容器，先删除掉。



