---
title: PyCharm使用总结
date: 2018-06-28 19:10:28
tags:
	- Python

---



# 设置Python3和Python2的切换

https://blog.csdn.net/sgfmby1994/article/details/77876873



# 安装scrapy



# pycharm edu版本

这个版本可以下载一些教程。整个界面非常简洁。



# 安装模块

直接在设置里，找到对应的解释器，点击加号，在弹出的搜索窗口输入要安装的模块，点击安装就好了。



# 安装插件

edu版本的，没有terminal，到设置里，搜索plugin，然后搜索terminal就可以找到安装。

升级到2020.2版本默认就有terminal。这样的terminal才能正常使用venv的。



# pycharm的代码提示

python作为一种动态语言，因为没有类型，所以IDE提示是非常不方便的。

pycharm提供了Type Hint的方法。

具体说明在这里：

https://www.jetbrains.com/help/pycharm/type-hinting-in-product.html

使用了typing这个模块。和PEP484的内容。

在python2里，是通过注释来提供类型，在python3里，是通过注解。

```
a = None # type: dict
```

```
a: dict = None
```



参考资料

1、pyCharm中python对象的自动提示问题

https://my.oschina.net/pierrecai/blog/1142711