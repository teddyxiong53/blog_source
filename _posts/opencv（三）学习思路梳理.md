---
title: opencv（三）学习思路梳理
date: 2018-04-08 11:27:44
tags:
	- opencv

---



目前已经把opencv跑起来了。现在要理一下思路，看看怎么开展学习。

opencv经历了版本1，版本2，版本3 。

现在最新版本是3.4.1的。新版本的问题是，没有太多资料可以参考。

那么现在要弄清楚一个问题，就是版本1/2/3之间有哪些大的改动，阅读基于版本1和版本2的书籍，是否可以很顺利地进行实验验证。

1.x的太古老，我们可以不考虑了。

2.x使用应该是比较多的，很多书籍都是基于这个来讲解的。

# 3.x的改进

1、硬件加速、移动开发的支持。

2、采用了内核加插件的架构模式，主题上更加容易扩展。

3、支持了windows是vs工具最新吧。

4、得益于谷歌编程之夏的贡献，opencv的基础得到了很多的更新。

5、社区的贡献。

6、在Intel芯片上的性能提升。

7、直接集成了cuda模块。

8、配置上更加方便了。把lib文件都集成到一个里。用起来方便。



其实看到这里，还不是很清楚，我就基于2.x的文档，在3.4.1的版本上进行实验，摸着石头过河吧。



主要学习基于这份教程：

http://www.opencv.org.cn/opencvdoc/2.3.2/html/doc/tutorials/tutorials.html



# 参考资料

1、OpenCV3.0 3.1版本的改进

https://blog.csdn.net/wangyaninglm/article/details/50461054

2、

https://github.com/opencv/opencv/wiki/ChangeLog