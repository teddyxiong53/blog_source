---
title: docker之学习（二）基本命令
date: 2018-01-22 10:50:59
tags:
	- docker

---



退出容器的方式：输入exit或者Ctrl+D。或者另外开一个shell窗口，输入docker stop hello。hello是指运行的某个容器的名字。

# pull

命令格式：

```
docker pull <镜像名字>:<标签>
```

举例：

```
ubuntu:lastest
ubuntu:12.04
teddyxiong53/ubuntu:12.04
```

非官方的镜像名字需要带上用户名。

# run

举例：

```
docker run -i -t --name hello ubuntu /bin/bash
```

-i：以interactive方式运行。

-t：打开tty。

--name：指定容器的名字。可以不指定，那docker就会根据镜像的名字来指定。

用exit退出上面运行的Ubuntu的shell。

用`docker ps -a`。（如果不加-a选项，就看不到未运行的容器）。

```
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS                      PORTS                                                                           NAMES
a9bb29f99328        ubuntu                     "/bin/bash"              52 seconds ago      Exited (0) 46 seconds ago                                                                                   hello
```

指定名字的好处是，你可以用名字来指定运行某个镜像。

# start

```
docker start hello
```

hello是上面我们指定名字的那个容器。

hello还可以用容器id来替代。

restart用法一样。

# attach

其实，我看上面start的效果，不是我想要的。

```
docker attach hello
```

这个才是把shell运行起来的效果。

不过，我试了一下，docker运行的Ubuntu退出后，直接attach是不行的，要先start。

# exec

要演示这个命令，需要开两个shell窗口。

一个shell窗口把hello这个容器运行起来。

另外一个shell窗口里输入：

```
docker exec hello echo "hello world"
```

exec的作用就是在容器外面使用docker容器来执行命令。

# rm和rmi

rm是删除容器。

rmi是删除镜像。

举例：

```
docker rm hello
docker rmi ubuntu:12.04
```

# 常用命令

To clear containers:

> ```
> docker rm -f $(docker ps -a -q)
> ```

To clear images:

> ```
> docker rmi -f $(docker images -a -q)
> ```

To clear volumes:

> ```
> docker volume rm $(docker volume ls -q)
> ```

To clear networks:

> ```
> docker network rm $(docker network ls | tail -n+2 | awk '{if($2 !~ /bridge|none|host/){ print $1 }}')
> ```



- Container是在原先的Image之上新加的一层，称作Container layer，这一层是可读可写的（Image是只读的）。
- Image跟Container的职责区别：Image负责APP的存储和分发，Container负责运行APP。 

参考资料

1、

https://github.com/moby/moby/issues/23371