---
title: Python之pip用法深入
date: 2018-06-17 14:45:56
tags:
	- Python

---



平时都用得很简单，都是一个pip install 。

其实pip工具还是有很多值得研究的地方。

我的测试环境还是用我在树莓派上搭建的HA的虚拟Python环境。因为这里比较干净。东西没有那么多。

一个虚拟的环境下，有这么几个文件夹。

```
bin
	python：实际上是指向真实环境的软链接。
	pip：这个是实实在在的文件。
	
include
lib
	site-packages
```

后面加一个点，是要在本目录下搜索setup.py文件。

```
teddy@teddy-ubuntu:~/work/test/python$ pip install .
Directory '.' is not installable. File 'setup.py' not found.
```



我重点关注aiohttp这个库。

# 查看包里的文件

```
(hass) pi@raspberrypi:~/work/hass/hass$ pip show --files aiohttp
Name: aiohttp
Version: 3.2.1
Summary: Async http client/server framework (asyncio)
Home-page: https://github.com/aio-libs/aiohttp/
Author: Nikolay Kim
Author-email: fafhrd91@gmail.com
License: Apache 2
Location: /home/pi/work/hass/hass/lib/python3.6/site-packages
Requires: attrs, chardet, multidict, async-timeout, yarl, idna-ssl
Files:
  aiohttp-3.2.1-py3.6.egg-info/PKG-INFO
  aiohttp-3.2.1-py3.6.egg-info/SOURCES.txt
  aiohttp-3.2.1-py3.6.egg-info/dependency_links.txt
  aiohttp-3.2.1-py3.6.egg-info/requires.txt
  aiohttp-3.2.1-py3.6.egg-info/top_level.txt
  aiohttp/__init__.py
  aiohttp/__pycache__/__init__.cpython-36.pyc
  aiohttp/__pycache__/abc.cpython-36.pyc
  aiohttp/__pycache__/client.cpython-36.pyc
.....

  aiohttp/_cparser.pxd
  aiohttp/_frozenlist.c
  aiohttp/_frozenlist.cpython-36m-arm-linux-gnueabihf.so
  aiohttp/_frozenlist.pyx
  aiohttp/_http_parser.c
```



仔细一看，其实pip也没有太多东西。



# 非root用户进行安装

https://blog.csdn.net/no_giveup/article/details/53699734



pip的版本问题

我当前python27对应的pip版本是10.0.1 。



# 参考资料

1、pip安装使用详解

http://www.ttlsa.com/python/how-to-install-and-use-pip-ttlsa/

2、

https://github.com/sqreen/PyMiniRacer/issues/50