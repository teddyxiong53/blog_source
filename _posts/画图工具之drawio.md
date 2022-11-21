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

# 资源收集

这个示范看起来不错。有很多技巧可以学习。

画图也是一门艺术创作。

https://www.bilibili.com/video/BV1Qz4y1d7C1



# 直接vscode里安装插件

搜索drawio找插件，安装好。

新建一个文件，后缀名为drawio。

例如：test.drawio。然后在vscode里打开，就直接可以进行画图了。

这个应该是最简单实用的方式了。



# docker搭建

```
 docker pull fjudith/draw.io
 docker run -itd --name="draw-io" --restart=always -p 8080:8080 fjudith/draw.io

```

然后就可以通过8080端口访问了。

效果跟官网的是一样的。

# 所有图形种类分析



# 设置

默认是使用了压缩模式。

这样保存下来的drawio文件，实际上是一个压缩后的xml文件，阅读理解起来不直观。

可以改成非压缩的。

点击files-- properties，就可以看到选项。



# 怎样画一个饼图

搜索pie，可以找到饼图。但是不能调节各个部分的个数和比例。



# 参考资料

1、

https://blog.csdn.net/qq_43719932/article/details/113917496