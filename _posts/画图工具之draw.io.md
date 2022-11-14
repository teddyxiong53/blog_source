---
title: 画图工具之draw.io
date: 2022-11-08 14:41:32
tags:
	- 画图

---

--

之前用过draw.io，还以为是国内某个厂家做的。现在发现是国外的开源项目，在github上有代码。

可以自己进行搭建。

觉得可以把这个作为自己的主力画图工具。

因为官方的网站在国内访问不好。

所以可以自己搭建一个本地的版本。借助docker。只要1分钟就可以搭建好。非常方便。

# docker搭建

```
 docker pull fjudith/draw.io
 docker run -itd --name="draw-io" --restart=always -p 8080:8080 fjudith/draw.io

```

然后就可以通过8080端口访问了。

效果跟官网的是一样的。

# 所有图形种类分析



# 参考资料

1、

https://blog.csdn.net/qq_43719932/article/details/113917496