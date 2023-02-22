---
title: Python之PikaPython研究
date: 2023-02-13 19:24:17
tags:
	- python

---



以这里生成的lvgl的工程目录来作为阅读材料。

http://pikascript.com/

看官方仓库还是内容多了，不容易甄别。

之前在rt-thread的开发者会议上认识了作者。

看着这个系统逐渐完善起来。

现在觉得有必要系统学习一下。

因为micropython真的很乱。那种写法让我很难阅读和分析。

pika的代码量不大，写法也是比较清晰的。

最长的文件，是pikaVM.c，也只有3000多行。

```
obj_runNativeMethod
	
```



# 搭建docker环境

https://pikadoc.readthedocs.io/zh/latest/get-start_linux.html

下载代码：

```
git clone https://gitee.com/lyon1998/pikapython
cd pikapython/docker 
# build镜像
bash build.sh
# 运行容器
sh run.sh

```

然后要初始化linux port

```
cd port/linux
bash pull-core.sh
bash init.sh
```

运行repl

```
bash run.sh
```



这个对应python里的`__new__`和`__init__`函数。

```
typedef PikaObj* (*NewFun)(Args* args);
typedef PikaObj* (*InitFun)(PikaObj* self, Args* args);
```



```
class_defineMethod

一个普通的方法
typedef void (*Method)(PikaObj* self, Args* args);
```



有不少自动生成的代码。这个是比较关键的点。

生成代码的方案，比用宏定义展开的可读性要更好。

这个是pika跟micropython的重要区别。



很多New_xx命名的函数。这种很重要。



pika在lvgl ubuntu vscode sim下运行

因为我只有这个测试环境。

也比较习惯这个测试环境。看看怎么跑起来。



# 参考资料

1、

