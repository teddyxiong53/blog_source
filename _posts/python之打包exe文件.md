---
title: python之打包exe文件
date: 2019-09-27 13:33:48
tags:
	- python

---

1

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



# cx-freeze

结论：不能用。

所以看看cx-freeze怎么做。

安装：

```
pip install cx-freeze
```

查看版本：

```
C:\Python37\Scripts>python cxfreeze --version
cxfreeze 6.0b1
```

先看一个HelloWorld。

新建hello.py。

```
print("hello")
```

执行命令：

```
python cxfreeze d:/tmp/hello.py --target-dir d:/tmp/hello_output 
```

打包后大概10M。

```
$ ls
hello.exe*  lib/  python37.dll*
```

多个文件怎么打包呢？

只需要打包入口的就行了，其余的可以被自动包含进来。

另外写一个hello2.py文件。导出一个myprint函数给hello.py用。

只打包hello.py，可以正常运行。

但是我打包我的程序，却不能正常运行，提示这个：

```
  File "C:\Python37\lib\site-packages\urllib3\packages\six.py", line 82, in _import_module
    __import__(name)
ModuleNotFoundError: No module named 'queue
```



在网上看到说使用一个--init-script。这个并没有什么用。

这个后面跟的就是要转换的脚本文件。

可以把整个过程梳理得更加好用一点。

在c:\python37\scripts目录下，新建一个cxfreeze.bat文件。写入下面的内容：

```
@echo off
c:/python37/python.exe c:/python37/scripts/cxfreeze %*
```

这个是为了解决不能在任意路径下使用cxfreeze的问题。

然后在我的目录下执行：

```
cxfreeze.bat --init-script=D:\work\中国移动\语料采\code\wakeup_collect_single\client\main.py  main.py
```

在D:\work\中国移动\语料采\code\wakeup_collect_single\client目录下会生成dist目录。

打包的东西就在下面。

但是现在还是一样的错误，说queue模块找不到。但是实际上是有的。

我换到没有中文路径的目录下看看。还是一样的错误。

网上找了一下，跟打包没有关系，是跟引入模块有关系。

需要自己添加到指定路径。

找了一下，没有找到解决的办法，放弃了。

# py2exe

不行。

试一下py2exe。

```
pip install py2exe
```

可以运行。

执行：

```
build_exe.exe -b 2 main.py
```

这个会提示：

```
IndexError: tuple index out of range
```

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



参考资料

1、python打包exe的方法

https://blog.csdn.net/appke846/article/details/80758925

2、在python3.6环境下使用cxfreeze打包程序

https://blog.csdn.net/tangg555/article/details/79648921

3、python程序在命令行执行提示ModuleNotFoundError: No module named 'XXX' 解决方法

https://www.cnblogs.com/dreamyu/p/7889959.html