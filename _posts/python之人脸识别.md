---
title: python之人脸识别
date: 2019-10-17 17:05:54
tags:
	- python

---

1

dlib是一个c++写的工具库，包含了机器学习算法和和工具，用来创建复杂的软件。

在工业和学术界得到了广泛应用，包括机器人、嵌入式设备、手机、

http://dlib.net/

dlib的python包，在windows上，直接用pip安装是不行的。

从这里下载编译好的版本。

https://pypi.org/simple/dlib/

下载的包不大，才1M多。

我下载的是这个：dlib-18.17.100-cp35-none-win_amd64.whl

安装：

```
pip install dlib-18.17.100-cp35-none-win_amd64.whl
```

报了错：

```
dlib-18.17.100-cp35-none-win_amd64.whl is not a supported wheel on this platform.
```

这个是因为python的版本不严格相等导致的。

whl文件是python3.5的。我安装的python是3.7的。

但是官网也没有编译3.7版本的。

所以只能自己编译。

先安装cmake。从https://cmake.org/download/ 下载cmake的安装包。





参考资料

1、python三步实现人脸识别

https://www.cnblogs.com/jyxbk/p/7677877.html

2、使用dlib库进行人脸识别

https://blog.csdn.net/qiumokucao/article/details/81610628

3、python dlib ubuntu 人脸识别2 使用mmod_human_face_detector进行人脸检测

https://blog.csdn.net/lan_liang/article/details/84713699