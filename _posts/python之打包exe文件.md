---
title: python之打包exe文件
date: 2019-09-27 13:33:48
tags:
	- python

---

--

最近用Python写了个工具，需要外发给别人使用，所以打包成exe文件会比较方便。

现在研究一下怎么进行打包。

网上看到说有这三种方式：

```
1、cx-freeze。
	简单。
	注意cx后面那个-不能省略。
2、pyinstaller。
	只支持python2.7。
3、py2exe。
	python3支持还不够好。
说明：
后面发现其实3个都是支持python3的。而且只有pyinstaller可以用起来。而且简单。
```

# 结论是：用pyinstaller





# pyinstaller

试一下pyinstaller。这个效果可以。

安装：

```
pip install pyinstaller
```

运行：

```
pyinstaller.exe -F main.py
```

这个在当前目录下生成了一个main.exe文件。

可以正常运行。路径里有中文也没有关系。

## 运行有个黑色的窗口

就是类似控制台的东西，用来输出stdout内容的。

这个对用户有困扰。

去掉也很简单。这样生成就好了。加上-w参数。

```
pyinstaller.exe -F -w main.py
```

另外，我还是希望看到print打印的输出内容。

对于wxpython。可以指定把stdout重定向到文件。





参考资料

1、python打包exe的方法

https://blog.csdn.net/appke846/article/details/80758925

2、在python3.6环境下使用cxfreeze打包程序

https://blog.csdn.net/tangg555/article/details/79648921

3、python程序在命令行执行提示ModuleNotFoundError: No module named 'XXX' 解决方法

https://www.cnblogs.com/dreamyu/p/7889959.html