---
title: docker之学习（八）使用docker构建服务
date: 2018-01-22 16:58:16
tags:
	- docker

---



我们构建一个使用Jekyll框架的网站。包含这2个镜像：

1、一个镜像安装了Jekyll。

2、一个镜像安装了Apache，来让Jekyll可以运行起来。

工作流程是这样的：

1、创建上面的2个镜像。只需要做一次。

2、从Jekyll镜像创建一个容器。存放通过Volume挂载的网站源代码。

3、从Apache镜像创建一个容器。

4、网站需要更新的时候，清理并重复上面的步骤。

这个例子，可以看做是创建一个多主机站点的最简单的方法。

#创建镜像

1、新建一个jekyll目录。下面放一个Dockerfile。

```
FROM ubuntu:14.04
MAINTAINER teddyxiong53 <1073167306@qq.com>

RUN apt-get  update && \
apt-get -y install ruby ruby-dev make nodejs
RUN gem install --no-rdoc --no-ri jekyll -v 2.5.3

VOLUME /data
VOLUME /var/www/html
WORKDIR /data

ENTRYPOINT [ "jekyll", "build", "--destination=/var/www/html" ]
```

经常会在apt-get update的时候出错。网上找了下，说把update跟install拼在同一行就好了。我试了，还是不行。

有说加上这个：`sudo apt-get update -o Acquire-by-hash=yes`。试一下。不行。

有说这样：

```
sudo apt-get clean  
sudo apt-get update --fix-missing  
```

也不行。

试一下这个：

```
RUN apt-get update -o Debug::Acquire::http=true
```

还是不行。

我换成Ubuntu:latest看看。

还是出错。换成Ubuntu:16.04的看看。

还是出错。我仔细看了下，是安装ruby的时候出错的。

我换成Debian系统的看看。

要想其他的方法来进行解决。

我先把Ubuntu启动。然后在里面进行apt-get update操作。把ruby安装好。

然后基于这个镜像进行操作。

```
#1. 进入到Ubuntu的docker内部
docker run -i -t ubuntu --name ubuntu_jekyll 
#2. 另外开一个shell窗口，把我的主机的/etc/apt/sources.list拷贝到docker的Ubuntu里。
#按道理是可以直接在docker里的Ubuntu进行编辑的，但是里面连vi工具都没有。所以就这样拷贝了。
docker cp /etc/apt/sources.list container_id:/etc/apt/sources.list
#3. 需要把我修改后的Ubuntu保存成我的本地镜像。xxx是通过docker ps找到的容器名字保存出来的。
docker commit xxxx teddyxiong53/ubuntu 
```

现在把Dockerfile的FROM改成：

```
FROM teddyxiong53/ubuntu
```

再进行build。现在就顺利多了。

最后的Dockerfile是这样：

```
FROM teddyxiong53/ubuntu
MAINTAINER teddyxiong53 <1073167306@qq.com>



RUN apt-get update --fix-missing  
RUN apt-get -y install gcc 
RUN apt-get -y install ruby 
RUN apt-get -y install ruby-dev
RUN apt-get -y install  make
RUN apt-get -y install  nodejs

RUN gem install --no-rdoc --no-ri jekyll -v 2.5.3

VOLUME /data
VOLUME /var/www/html
WORKDIR /data

ENTRYPOINT [ "jekyll", "build", "--destination=/var/www/html" ]
```



2、在跟Jekyll同一层目录，新建一个apache目录。也放一个Dockerfile。

```
FROM teddyxiong53/ubuntu
MAINTAINER teddyxiong53 <1073167306@qq.com>
RUN apt-get clean
RUN apt-get update --fix-missing
RUN apt-get install -y apache2

VOLUME [ "/var/www/html" ]
WORKDIR /var/www/html

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2

RUN mkdir -p $APACHE_LOCK_DIR $APACHE_LOG_DIR $APACHE_RUN_DIR

EXPOSE 80

ENTRYPOINT [  "/usr/sbin/apache2" ]

CMD [  "-D", "FOREGROUND" ]
```

现在查看一下：

```
teddy@teddy-ubuntu:~/work/docker/apache$ docker images
REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
apache                     latest              59074e0bd420        12 seconds ago      268 MB
jekyll                     latest              d41f0ce4069d        3 minutes ago       394 MB
```

# 创建容器

这个例子是根据《第一本docker书》的内容在做的。

先把示例网站的内容下载下来。

```
wget https://codeland.github.com/jamtur01/james_blog/zip/master
```

解压放好。现在创建Jekyll容器。

```
teddy@teddy-ubuntu:~/work/docker$ docker run -v /home/teddy/work/docker/website/james_blog-master:/data/ --name myblog jekyll
Configuration file: /data/_config.yml
            Source: /data
       Destination: /var/www/html
      Generating... 
                    done.
 Auto-regeneration: disabled. Use --watch to enable.
```

这样，这个容器就已经在后台运行了。

现在创建Apache容器。

```
teddy@teddy-ubuntu:~/work/docker$ docker run -d -P --volumes-from myblog apache
431e54500974c16c22b11f07de7c525bfa7ec834419ec31925d3a549f10d285b
teddy@teddy-ubuntu:~/work/docker$ 
```

查到apache的容器id，然后：

```
teddy@teddy-ubuntu:~/work/docker$ docker port 431e54500974 80
0.0.0.0:32768
teddy@teddy-ubuntu:~/work/docker$ 
```



然后我们在一台电脑上访问：http://192.168.190.130:32768/

就可以得到目标界面了。

到这里，这个环境就搭建好了。

