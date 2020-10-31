---
title: python之subprocess和multiprocessing比较
date: 2019-10-19 15:11:25
tags:
	- python

---

1

# subprocess

subprocess模块允许你spawn新的进程。连接它们的0、1、2的fd。

获取它们的返回值。

这个模块的主要设计目的是用来取代：

```
os.system
os.spawn*
```

主要的接口有：

```
run
	这个是3.5新增的。
	举例：
	subprocess.run(['ls', './']) 
call
	subprocess.call(['ls', './']) 
check_call
	subprocess.check_call(['ls', './']) 
	这个的不同在于在命令出错的时候，会抛出异常。
	
```

```
import subprocess
child = subprocess.Popen(['ping', '-n', '4', 'www.baidu.com' ])
child.wait() # 等待子进程。
print("end of parent ")
```



subprocess对已的pep324。文档在2003年提出的。

在这个文档里，说明了设计这个模块的动机：

1、不合适的启动进程的函数，会导致风险。

2、让python更好地替换掉难用的shell脚本。

当前python有很多的函数用来做进程创建。让开发者难以选择。

subprocess相当于之前的其他模块，做了这些事情：

```
1、一个统一的模块。
2、跨进程的异常。父进程可以检测到子进程的异常。
3、提供了一个hook，可以在fork跟exec之间来执行。这个一般用来修改uid。
4、不会隐式调用/bin/sh
5、所有fd的重定向的组合都支持。
6、支持连接多个子进程。相当于管道。
7、统一的换行符支持。
```

设计

```
1、subprocess基于popen2这个函数。
```

# multiprocessing

multiprocessing设计的目的是进行多进程操作的。

目的是提高并发能力。



参考资料

1、python subprocess 和 multiprocess选择以及我遇到的坑

https://www.cnblogs.com/pengyusong/p/6113148.html

2、python subprocess模块使用总结

https://www.cnblogs.com/lincappu/p/8270709.html