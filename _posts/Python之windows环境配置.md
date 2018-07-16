---
title: Python之windows环境配置
date: 2018-06-28 19:16:34
tags:
	- Python

---



为了逼迫自己向Python3转，我现在在windows上安装了Python3的版本。

把默认的Python配置配置为Python3的。

修改PATH的路径就好了。

这样验证就好了。

```
C:\Users\Administrator
λ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

我现在学习爬虫的。

```
pip install beautifulsoup4
```

这个安装没有问题。因为按照Python3.7的，默认就勾选了pip工具了。



# windows下多个Python环境共存配置

1、在环境变量里加入2个的。

```
C:\python27;C:\Python27\Scripts;C:\python37;C:\Python37\Scripts;
```

2、当前之所以不能共存，是因为有同名的可执行文件。

主要是pip和Python这2个exe文件。

我都拷贝一个为pip2和python2这样的名字文件。



用脚本来做。思路就是改文件名。



# 参考资料

1、windows下通过cmd切换python2和python3版本

https://blog.csdn.net/fxjzzyo/article/details/77070868