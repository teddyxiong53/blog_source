---
title: docker之学习（四）查看docker
date: 2018-01-22 11:39:40
tags:
	- docker

---



# 用history命令查看镜像历史

```
docker history hello:0.1
```

```
teddy@teddy-ubuntu:~/work/test/example$ docker history hello:0.1
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
913bff44f2c0        About an hour ago   /bin/sh -c #(nop)  EXPOSE 443/tcp               0 B                 
f468fdf2d615        About an hour ago   /bin/sh -c #(nop)  EXPOSE 80/tcp                0 B                 
7c70d79f39b9        About an hour ago   /bin/sh -c #(nop)  CMD ["mini_httpd"]           0 B                 
712a52b05681        About an hour ago   /bin/sh -c apt-get install -y mini-httpd        5.65 MB             
627cb8341031        About an hour ago   /bin/sh -c apt-get update                       39.5 MB             
9994a9a8eceb        2 hours ago         /bin/sh -c #(nop)  MAINTAINER teddyxiong53...   0 B                 
7b9b13f7b9c0        7 months ago        /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B                 
<missing>           7 months ago        /bin/sh -c mkdir -p /run/systemd && echo '...   7 B                 
<missing>           7 months ago        /bin/sh -c sed -i 's/^#\s*\(deb.*universe\...   2.76 kB             
<missing>           7 months ago        /bin/sh -c rm -rf /var/lib/apt/lists/*          0 B                 
<missing>           7 months ago        /bin/sh -c set -xe   && echo '#!/bin/sh' >...   745 B               
<missing>           7 months ago        /bin/sh -c #(nop) ADD file:5aff8c59a707833...   118 MB      
```



# 从容器里复制文件

```
docker cp hello-nginx:/etc/nginx/nginx.conf ./
```

# 用commit命令从容器的修改中创建镜像。

```
docker commit -a "teddyxiong53 <1073167306@qq.com>" -m "add hello.txt" hello-nginx hello:02
```

-a：作者信息。

-m：修改信息。

hello-nginx：容器名字。

这个就是创建了hello:0.2版本。

# 用diff命令查看容器里的文件的情况

```
docker diff hello-nginx
```

```
teddy@teddy-ubuntu:~/work/test/example$ docker diff hello-nginx
A /data
```



# 用inspect命令查看镜像和容器的详细信息

```
docker inspect hello-nginx
```

