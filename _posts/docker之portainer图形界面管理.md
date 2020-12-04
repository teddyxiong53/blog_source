---
title: docker之portainer图形界面管理
date: 2020-12-01 17:05:30
tags:
	- docker
---

1

安装：

```
docker pull docker.io/portainer/portainer
```

如果仅有一个docker宿主机，则可使用单机版运行，Portainer单机版运行十分简单，只需要一条语句即可启动容器，来管理该机器上的docker镜像、容器等数据。

```
sudo docker run -d -p 9000:9000 \
--restart=always \
-v /var/run/docker.sock:/var/run/docker.sock \
--name prtainer-test \
docker.io/portainer/portainer
```



参考资料

1、Docker使用Portainer搭建可视化界面

https://www.cnblogs.com/ExMan/p/11657069.html