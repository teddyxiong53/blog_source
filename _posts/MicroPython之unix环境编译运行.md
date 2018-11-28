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



```
teddy@teddy-ubuntu:~/work/micropython/micropython/ports/unix$ ./micropython -m pystone
Pystone(1.2) time for 50000 passes = 0.357
This machine benchmarks at 140056 pystones/second
```

