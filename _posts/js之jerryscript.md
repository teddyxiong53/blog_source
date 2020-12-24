---
title: js之jerryscript
date: 2018-12-27 11:52:27
tags:
	- js
---



直接从这里下载。

https://github.com/jerryscript-project/jerryscript

看readme就够了。

编译：

```
python ./tools/build.py
```

编译很快。

运行：

```
./build/bin/jerryr ./test.js
```

下面的doc目录下，有markdown的文档。

tests目录下，有测试脚本。

基本的是这样的。

```
print("hello jerry");
```



简单看了一下，这个对我来说没有什么吸引力，暂时不关注了。

这样编译，方便用gdb进行调试跟踪代码的运行。

```
python2 tools/build.py --debug  --all-in-one ON --logging ON   --line-info ON --jerry-debugger ON  --jerry-cmdline ON  --jerry-port-default ON 
```



# 在rt-thread上使用

现在在rt-thread上使用起来了。

所以仔细研究一下这个。也作为深入学习js的一个材料。

jerryscript的主要特性：

1、对ES5的完整兼容。

2、对低内存的大量优化。

3、完全用C99编写。

4、对预编译的js字节码文件的的snapshot支持。

5、有成熟的C语言API，容易嵌入到你的程序里。

采用的apache2协议进行开源的。可以商用。



jerryscript的开发环境，官网推荐Ubuntu18.04。他们就是在这个上面进行开发。



jerryscript\tests\jerry 这个目录下有一下测试例子。可以看看。

