---
title: docker之镜像导出
date: 2021-06-22 19:20:33
tags:
	- docker

---

--

现在有个jd脚本的容器，因为docker hub已经被删库了，我想要把容器在其他机器运行。

这个就只能通过把镜像导出到其他机器来运行了。

有两套机制：

export/import机制：通过操作容器。

save/load机制：通过操作镜像文件。



export/import机制

```
# 查看本地的容器
docker ps -a
# 导出容器，xxx是容器的id。
docker export xxx > xxx.tar 
# 到目标机器上
docker import - new_xxx < xxx.tar
# 查看镜像，可以看到有一个名字为new_xxx的镜像了。
docker images
```

save/load机制

```
# 查看本地镜像
docker images
# 保存镜像
docker save xxx > xxx.tar
# 在另外一台机器上，载入镜像
docker load < xxx.tar
```



两种机制对比：

1、文件大小不同。export方式导出的文件要小一些。

2、是否可以对镜像重命名。import可以指定镜像名字。load不能对镜像重命名。

3、是否可以把多个镜像打包到一个文件里。export方式不支持，save方式支持。

4、是否包含镜像历史。export方式会丢失镜像的历史提交。

5、应用场景。export方式，主要是用来做基础镜像如何分发。



结论：

我用export方式就好了。



参考资料

1、

https://www.hangge.com/blog/cache/detail_2411.html

