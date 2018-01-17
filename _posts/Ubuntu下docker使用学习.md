---
title: Ubuntu下docker使用学习
date: 2017-06-12 20:32:24
tags:

	- ubuntu

	- docker

---

docker是一个开源的应用容器引擎，用Go语言开发，基于Apache2.0协议进行开源。

docker主要是给开发者用来把自己的应用打包到一个可以移植的容器里，然后可以放在任意的Linux机器上运行。容器采用的是沙箱机制，开销非常低。

常见的应用场景有：

* web应用的自动化打包和发布。
* 自动化测试和持续集成、发布。
* 在服务器环境中部署和调整数据库或者其他的后台应用。

docker的官网是：https://www.docker.com

github地址是：[https://github.com/docker/docker](https://github.com/docker/docker)

为了方便运行，可以把身份切换为root用户再进行下面的操作。

官网的教程在这：https://docs.docker.com/get-started/

# 1. docker的安装

docker到目前有2个版本：社区版本和企业版本。企业版本比社区版本功能要多一些。



发现一个较好的国内的加速的安装方式。

```
curl -sSL https://get.daocloud.io/docker | sh
```

这个就是下载了一个脚本然后执行，执行后就是安装启动了docker。

配置docker加速器。

网址在这里：https://www.daocloud.io/mirror#accelerator-doc

按照提示操作就是了。

# 2. 运行helloworld

前面docker安装好了，也配置好加速器了。下载看看helloworld的运行。

```
teddy@teddy-ubuntu:~$ sudo docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
78445dd45222: Pull complete 
Digest: sha256:c5515758d4c5e1e838e9cd307f6c6a0d620b5e07e6f927b07d05f6d12a1ac8d7
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

上面的处理过程是：先在本地找helloworld这个镜像，如果没有找到，那么就到网上去下载，得益于我们配置的加速器，这个过程很快就完成了。我试了在没有配置加速器的时候，下载失败了。

按照上面的提示信息，我们可以试一下运行：

```
sudo docker run -it ubuntu bash
```

还是感谢DaoCloud的加速器，这个过程变得很快，让人体验感觉很好。

```
teddy@teddy-ubuntu:~$ docker run -it ubuntu bash
docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.29/containers/create: dial unix /var/run/docker.sock: connect: permission denied.
See 'docker run --help'.
teddy@teddy-ubuntu:~$ sudo docker run -it ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
bd97b43c27e3: Pull complete 
6960dc1aba18: Pull complete 
2b61829b0db5: Pull complete 
1f88dc826b14: Pull complete 
73b3859b1e43: Pull complete 
Digest: sha256:ea1d854d38be82f54d39efe2c67000bed1b03348bcc2f3dc094f260855dff368
Status: Downloaded newer image for ubuntu:latest
root@63124cb53c9f:/# 
root@63124cb53c9f:/# 
root@63124cb53c9f:/# 

```

这样我们就进入到一个Ubuntu的环境，这个就类似一个虚拟机了。

输入exit就可以退出这个docker。

# 3. docker的命令分析

我们输入docker，然后按tab键，就可以看到docker的命令有哪些。我们一个个试一下。

images是列出当前我们按照的镜像。

```
teddy@teddy-ubuntu:~$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              7b9b13f7b9c0        10 days ago         118MB
hello-world         latest              48b5124b2768        5 months ago        1.84kB
teddy@teddy-ubuntu:~$ 

```

info：

```
root@teddy-ubuntu:/home/teddy# docker info
Containers: 2
 Running: 0
 Paused: 0
 Stopped: 2
Images: 2
Server Version: 17.05.0-ce
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 10
 Dirperm1 Supported: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins: 
 Volume: local
 Network: bridge host macvlan null overlay
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Init Binary: docker-init
containerd version: 9048e5e50717ea4497b757314bad98ea3763c145
runc version: 9c2d8d184e5da67c95d601382adf14862e4f2228
init version: 949e6fa
Security Options:
 apparmor
 seccomp
  Profile: default
Kernel Version: 4.4.0-31-generic
Operating System: Ubuntu 16.04.1 LTS
OSType: linux
Architecture: x86_64
CPUs: 4
Total Memory: 7.78GiB
Name: teddy-ubuntu
ID: 4V4F:6X5P:4CJ4:VEGQ:72CQ:HAXA:H23U:2VYK:OBWB:E6AS:HDAZ:HKEL
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
Experimental: false
Insecure Registries:
 127.0.0.0/8
Registry Mirrors:
 http://e2e3221a.m.daocloud.io/
Live Restore Enabled: false

WARNING: No swap limit support
root@teddy-ubuntu:/home/teddy# 
```



# 4. 搜索可用的镜像

用docker search keyword的方式，就可以搜索到你想要的镜像。

例如：`docker search ubuntu`。

下载一个镜像。

```
docker pull ubuntu
```



















































Docker之所以这么吸引人，除了它的新颖的技术外，围绕官方Registry（Docker Hub）的生态圈也是相当吸引人眼球的地方。

在Docker Hub上你可以很轻松下载到大量已经容器化的应用镜像，即拉即用。

而且你还可以在Docker Hub中绑定你的代码托管系统（目前支持Github和Bitbucket）配置自动生成镜像功能，这样Docker Hub会在你代码更新时自动生成对应的Docker镜像，是不是很方便？

