---
title: docker之用docker方式搭建gitlab
date: 2019-05-20 10:57:11
tags:
	- docker

---



网上看了搭建gitlab的过程，需要安装的东西不少。

使用docker，就可以省去很多麻烦。

试一下。

下载镜像。

```
sudo docker pull gitlab/gitlab-ce:latest
```

运行：

```
sudo docker run --detach \
    --hostname 0.0.0.0 \
    --publish 443:443 --publish 80:80 \
    --name gitlab \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:latest
```

运行后，却不能访问。

查看日志：

```
sudo docker logs -f -t --tail 10 gitlab
```

是因为启动要一段时间，过两分钟就可以访问了。

的确挺强大的。

还集成了web IDE。



参考资料

1、

https://www.jianshu.com/p/24959481340e