---
title: cpp之popl库分析
date: 2020-04-30 11:53:08
tags:
	- cpp

---

1

涉及的知识点：

```
模板函数
完美转发
异常
字符串操作
```



代码：https://github.com/badaix/popl

popl是一个c++写的命令行参数解析器。

支持跟getopt类似的参数风格。

涉及到一个概念：groff。

什么是groff？是gnu troff的缩写。

那么什么又是troff呢？是typesetter roff的缩写。是格式排版的意思。



所以首先要讨论roff这个东西。

groff是roff排版系统目前最常用的实现。

其他的实现还有：troff、nroffdiroff等。

roff历史悠久，现在使用还很广泛。

man手册、很多软件书籍、标准文档都是用roff来写的。

如果你想要快速学会groff，可以从模仿man手册的内容开始。



roff系统由预处理器、排版程序、后处理器组成。

这种架构大量使用管道机制。



# 最简单例子

```
#include "popl.hpp"
#include <iostream>

int main(int argc, char **argv)
{
    popl::OptionParser op("my option parser");
    auto helpSwitch = op.add<popl::Switch>("h", "help", "this is the help");
    op.parse(argc, argv);
    if(helpSwitch->is_set()) {
        std::cout << op << std::endl;
        exit(0);
    }
    return 0;
}
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test -h
my option parser:
  -h, --help        this is the help
```

可以得到使用的步骤如下：

```
1、创建一个OptionParser实例op。
2、往op里add一些选项，
3、op.parse，解析参数。
4、看参数是否有。进行相关操作。
```

上面的-h选项，就是一个开关类型的选项。要么有，要么没有，选项后面不带参数值。

分析popl.hpp里对上面代码的实现。

```
OptionParser
	构造函数：
		只有一个。接收一个string参数，作为描述。可以没有，没有则默认为空字符串。
	add方法
	parse
		有2个版本，
		一个是只接收一个参数，是ini文件名字。
		一个是把main函数的argc和argv参数传递进去。
		
```

Option选项可以有三种：

Value：这个就是参数的选项。例如-p 8080

Switch：这个就是不带参数的选项。例如：-h。Switch是Value的子类。

Implicit：这个是可以带参数，也可以不带参数的。

表现在代码上，就是下面3个类都是Option的子类。



所以，首先需要把Option这个类分析透，这个是一切讨论的起点。

一个Option，就对应一个选项。例如-h。-p 8080。这个都各对应了一个Option对象。

下面以-p 8080为例进行分析。

```
op.add<popl.Value>("p", "port", "specify the port");
```

OptionParser的add函数，把参数都转发给了Value的构造函数。

```
std::shared_ptr<T> option = std::make_shared<T>(std::forward<Ts>(params)...);
```



把值存到指定的变量里。

```
op.add<Value<size_t>>("p", "port", "server port", 1704, &port);
```



参考资料

1、GNU troff (groff) — a GNU project

https://www.gnu.org/software/groff/

2、Groff排版概览

https://www.chungkwong.cc/groff.html