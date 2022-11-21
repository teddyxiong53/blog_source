---
title: Python虚拟机
date: 2022-11-17 17:46:33
tags:
	- python

---

--

# 字节码



https://geek-docs.com/python/python-examples/python-is-a-glimpse-into-the-bytecode.html



# 解释器

在解释器接手之前。python会执行：词法分析，语法分析， 编译。

然后将python的源代码生成 `code object`， 这里面就是python解释器可以识别的指令，然后解释器去解释(运行) 其中的指令。



另外Python的解释器是一个栈堆机器， 

其底层使用的逻辑是用栈表示的，

而我们普通的电脑底层是寄存器机器，使用的是数据存放在内存地址



解释器的定位

我们其实可以类比于c语言的过程，

两者的源代码，先要形成底层机器可以识别的语言，

这个`code object`就相当于汇编， 

而c编译为了可执行文件运行在机器上，就相当于`code object`运行在了我们的解释器上，



其实个人感觉还是比较类似的过程，只不过解释器实现了一个类似虚拟机的的功能，也有点像java了，两者都是解释型语言。

同样的java虚拟机也是一个堆栈机器。



stack 栈机器

我们的解释器是一个堆栈机器。而计算机是一个寄存器机器。

寄存器机器使用内存地址等保存数据， 运行时主要是使用寄存器去访问和操作各种地址、数据，

**堆栈机器的操作都是对栈的操作**，而数据储存的问题上，pyhton就是在`code object`的结构中



# 参考资料

1、

https://zhuanlan.zhihu.com/p/45101508

2、

https://bbs.pediy.com/thread-258353.htm