---
title: ssr之sslocal代码分析
date: 2019-01-03 09:52:59
tags:
	- ssr

---



把sslocal的代码看一下。

我就看2.8.2的。因为Ubuntu默认安装的就是这个。

看setup.py里。

```
    entry_points="""
    [console_scripts]
    sslocal = shadowsocks.local:main
    ssserver = shadowsocks.server:main
    """,
```



还是通过写的方式来读。

先新建一个ssr目录。在这个下面写。

下面新建shadowsocks目录。新建local.py。从头部开始写，可以看到依赖了shell.py。

新建shell.py。shell.py依赖了common.py。

common.py没有依赖自己写的文件了，算是底层的一个工具文件。

好，就从common.py开始写。

每个文件开始都从future模块引入了几个新的特性。

```
ord是根据字符求ascii码。
chr的根据int值得到字符。
```

```
def compat_chr(d):
    if bytes == str: #在python2里是True，在python3里是False
        return _chr(d)
    return bytes([d])
```

