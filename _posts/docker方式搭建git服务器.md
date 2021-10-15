---
title: docker方式搭建git服务器
date: 2019-05-20 15:51:11
tags:
	- docker
---





# gogs方式

gogs官网在这里：https://gogs.io/

```
sudo docker pull gogs/gogs
```



```
sudo mkdir -p /var/gogs
```

```
sudo docker run -d --name=mygogs -p 10022:22 -p 10080:3000 -v /var/gogs:/data gogs/gogs
```

通过localhost:10080进行访问。

第一次访问，会需要你配置数据库。

选择sqlite3。这样就免去配置数据库的麻烦。



参考资料

1、使用Docker搭建git服务Gogs

https://www.jianshu.com/p/4e43bda3e1f2