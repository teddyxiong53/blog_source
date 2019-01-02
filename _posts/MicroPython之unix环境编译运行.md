---
title: MicroPython之unix环境编译运行
date: 2018-11-28 21:54:23
tags:
	- MicroPython

---



```
cd ports/unix
make
```

会报错。

网上找了下，说要安装这个。

```
sudo apt-get install python-cffi
```

安装了，还是报错。

在安装这个。

```
sudo apt-get install libffi-dev
```

还是不行，看readme的，是需要用git命令操作一下，我还是git clone下来处理吧。

执行：

```
git submodule update --init
```

这个是会下载其他的几个开源项目的代码。

然后在ports/unix下面编译就可以了。

我现在比较关注的upip的使用。

```
./micropython -m upip install micropython-pystone
```

```
teddy@teddy-ubuntu:~/work/micropython/micropython/ports/unix$ ./micropython -m upip install micropython-pystone
Installing to: /home/teddy/.micropython/lib/
Warning: pypi.org SSL certificate is not validated
Installing micropython-pystone 3.4.2-2 from https://files.pythonhosted.org/packages/13/00/8f7c7ab316e8850ea3273956e1370d008cfd36697dec2492388d3b000335/micropython-pystone-3.4.2-2.tar.gz
```

测试模块：

```
teddy@teddy-ubuntu:~/work/micropython/micropython/ports/unix$ ./micropython -m pystone
Pystone(1.2) time for 50000 passes = 0.357
This machine benchmarks at 140056 pystones/second
```



下载的文件放在~/.micropython/lib目录下，就是一个pystone.py。

```
>>> import pystone
>>> dir(pystone)
['__class__', '__file__', '__name__', 'clock', 'main', 'LOOPS', '__version__', 'Ident1', 'Ident2', 'Ident3', 'Ident4', 'Ident5', 'Record', 'TRUE', 'FALSE', 'pystones', 'Proc0', 'IntGlob', 'BoolGlob', 'Char1Glob', 'Char2Glob', 'Array1Glob', 'Array2Glob', 'PtrGlb', 'PtrGlbNext', 'Proc5', 'Proc4', 'Func2', 'Proc7', 'Proc8', 'Proc1', 'Func1', 'Proc6', 'Proc2', 'Proc3', 'Func3']
>>> print pystone.__file__
Traceback (most recent call last):
  File "<stdin>", line 1
SyntaxError: invalid syntax
>>> print(pystone.__file__)
/home/hlxiong/.micropython/lib/pystone.py
>>> 
```



upip的代码在这里，我们看一下。

https://github.com/micropython/micropython-lib/tree/master/upip



查看帮助信息。

```
hlxiong@hlxiong-VirtualBox:~/work/study/micropython-github/micropython/ports/unix$ ./micropython -m upip -h
upip - Simple PyPI package manager for MicroPython
Usage: micropython -m upip install [-p <path>] <package>... | -r <requirements.txt>
import upip; upip.install(package_or_list, [<path>])

If <path> is not given, packages will be installed into sys.path[1]
(can be set from MICROPYPATH environment variable, if current system
supports that).
Current value of sys.path[1]: /home/hlxiong/.micropython/lib

Note: only MicroPython packages (usually, named micropython-*) are supported
for installation, upip does not support arbitrary code in setup.py.
```



我现在有个疑问，upip，是micropython默认带了吗？不然怎么直接就看以用呢？

搜索一下。在这里。

```
./ports/unix/modules/upip.py
```

而且这个目录下，就只有upip的。这个就算是随mp一起的基本工具。

就如此pip对于python一样。

另外，还有库是用C语言的写，例如usocket的。

```
./ports/unix/modusocket.c
```

用C语言写的模块还有：一共9个。

```
modffi.c  
modjni.c  
modmachine.c 
modos.c 
modtermios.c
modtime.c 
moduos_vfs.c 
moduselect.c
modusocket.c
```

还有一些库是在extmod目录下。例如ssl的。

```
./micropython/extmod/modussl_mbedtls.c
```



pypi是python package index的缩写。

upip下载，是解析一个json文件。url是这么拼出来的。

以下载包pystone为例。

```
https://pypi.org/pypi/micropyton-pystone/json
```

这个url上就是一个json文件。

这个只有2个版本，一个是3.4.2-1，一个是3.4.2-2 。默认是下载3.4.2-2的。

对应的地址是：

```
"url": "https://files.pythonhosted.org/packages/13/00/8f7c7ab316e8850ea3273956e1370d008cfd36697dec2492388d3b000335/micropython-pystone-3.4.2-2.tar.gz"
```





