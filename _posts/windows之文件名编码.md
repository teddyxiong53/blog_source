---
title: windows之文件名编码
date: 2019-03-27 17:07:32
tags:
	- windows

---





在cygwin下面，一个C语言程序，打开中文名字的文件，提示文件找不到，但是文件是存在的。

我觉得应该就是编码问题。

windows中文版的路径名是gbk编码？

用这种方法：

```
1、使用C语言的函数设置为中文运行环境
setlocale(LC_ALL,"Chinese-simplified");
```

还是不行。

```
字符串有中文怎么不用_wfopen？
fopen只支持ASCII文件名
```

但是_wfopen这个在Linux下 是不支持的。



找到解决方法了。

就是把源文件用utf-8编码。



参考资料

1、专治Cygwin中文路径的不识别文件的水土不服

https://blog.csdn.net/freesonhp/article/details/42106159

2、Cygwin 各种情况下中文乱码--终极解决方案

按照这个操作了，不行。

https://www.cnblogs.com/yshl-dragon/p/3631056.html

3、windows和Linux路径及编码差异

https://blog.csdn.net/lisidapao/article/details/80890948

4、C/C++中读取中文路径文件的方法

https://blog.csdn.net/sibo626/article/details/6931040

5、

https://stackoverflow.com/questions/396567/is-there-a-standard-way-to-do-an-fopen-with-a-unicode-string-file-path