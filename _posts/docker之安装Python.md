---
title: docker之安装Python
date: 2018-08-03 21:36:38
tags:
	- docker
	- Python

---



因为总是碰到各种Python版本问题。另外，我想要加强对docker应用。

所以就通过docker来构建多个Python环境。

# 方法一

直接拉取官方镜像。

```
docker search python
```

```
docker pull python:3.5
```



# 参考资料

1、docker运行python3.6+flask小记

https://www.cnblogs.com/xuanmanstein/p/7630606.html

2、Docker实践：运行Python应用

https://www.cnblogs.com/52fhy/p/5962770.html