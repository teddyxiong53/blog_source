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

默认的管理员用户是root，密码是你设置的密码。

然后进入设置，把验证关闭掉。

![image-20210406191312635](../images/random_name/image-20210406191312635.png)

也可以不关闭。

那就不关闭，进入管理界面，可以看到前面的用户的申请信息。

创建2个用户：

hanliang.xiong：1073167306@qq.com

webdev：teddyxiong53@163.com

创建一个group，名字为only4u。

把2个user都加到这个group里。

新建2个project，一个blog。一个web。

用repo来同步。

```
http://10.28.39.10/only4u/web
http://10.28.39.10/only4u/blog
```



参考资料

1、

https://www.jianshu.com/p/24959481340e

2、官网

https://docs.gitlab.com/omnibus/docker/