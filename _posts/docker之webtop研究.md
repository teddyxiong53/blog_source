---
title: docker之webtop研究
date: 2024-04-25 14:26:17
tags:
	- docker

---

--

webtop是一个很方便的方式，可以让你在浏览器里访问远程访问权的桌面。

这篇介绍就很好了。参考这个做就行。

https://blog.csdn.net/wbsu2004/article/details/120519093



```
docker run -d \
  --name=webtop \
  --privileged `#optional` \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Shanghai \
  -e SUBFOLDER=/ `#optional` \
  -p 3000:3000 \
  -v /home/teddy/work/webtop-config:/config \
  --shm-size="1gb" `#optional` \
  --restart unless-stopped \
  linuxserver/webtop
  
```

执行完在浏览器打开3000端口的地址就直接可以访问了。

打开浏览器，访问中文网站，可以看到中文都是显示乱码的。

执行下面的命令来安装中文字体。

在docker的shell里执行。方便粘贴命令。

进入docker的shell：

```
docker exec -it --user root linuxserver-webtop /bin/bash
```



```
# 安装 wget
apk --no-cache add ca-certificates wget 

# 安装公钥 
wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub 

#下载字体
wget https://github.com/Fangyh09/font-ttf/raw/master/simsun.ttc

# 创建文件夹 
mkdir /usr/share/fonts/win

# 移动字库
mv simsun.ttc /usr/share/fonts/win

# 扫描字体目录并生成字体信息的缓存
fc-cache -vf

# 查看系统内所有中文字体及字体文件的路径
fc-list :lang=zh
```

官网：

https://docs.linuxserver.io/images/docker-webtop/



# linuxserver.io 介绍

LinuxServer.io是一个由全球范围内的爱好者组成的团队，

==他们致力于构建和维护最大的Docker镜像集合。==

这个团队的核心原则是自由和开源软件的理念。

他们的主要目标是提供易于使用和精简的Docker镜像，并附有清晰、简洁的文档。

LinuxServer.io的镜像==建立于一个独特定制的基础镜像之上，==

使用s6-overlay使得每个基础镜像都具有高度的可扩展性，

可以配置几乎任何应用程序。

这种标准化不仅提供了统一性，

还通过共享基础层节省了用户的带宽和存储空间。

==他们的构建流程经过完全重新设计，==

现在可以为用户提供快速有效的镜像更新。

当上游应用程序或应用程序依赖项更新时，他们的镜像将自动重新构建，确保镜像保持尽可能的最新。

他们新的标签系统也使用户能够更清楚地了解特定构建封装的应用程序版本。

LinuxServer.io认为，一流的镜像应该配备一流的文档。

他们提供的所有镜像都附有清晰、详尽的设置指南，

可以在GitHub或他们的专用文档空间中找到。

此外，他们的博客还提供了更多指南和观点文章。

对于使用他们镜像的用户，LinuxServer.io通过Discord服务器和Discourse论坛提供第一手支持。

无论是LinuxServer的新手还是老手，总会有团队或社区成员随时准备帮助解决任何问题。

总的来说，LinuxServer.io是一个专注于提供高质量Docker镜像和文档的社区，致力于帮助用户轻松地使用Docker来部署各种服务。