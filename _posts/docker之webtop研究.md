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

