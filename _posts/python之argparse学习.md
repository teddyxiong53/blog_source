---
title: python之argparse学习
date: 2017-01-05 20:16:41
tags:
	- python
---
# 简单使用

写复杂一点的命令行程序，就需要进行参数的输入和解析。argparse就是一个进行参数解析的库。

先从一个最简单的例子出发来看看。
```
#!/usr/bin/env python
import  argparse
parser = argparse.ArgumentParser()
parser.parse_args()
```
运行效果是这样的：
```
teddy@teddy-ubuntu:~/test/py-test$ ./test.py -h
usage: test.py [-h]

optional arguments:
  -h, --help  show this help message and exit
```

默认都是带了一个`-h`参数的。
现在我们加一个参数进来，代码改成下面这样：
```
#!/usr/bin/env python
import  argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help='echo anything you input')
args = parser.parse_args()
print args.echo
```
运行效果如下：
```
teddy@teddy-ubuntu:~/test/py-test$ ./test.py 
usage: test.py [-h] echo
test.py: error: too few arguments
teddy@teddy-ubuntu:~/test/py-test$ ./test.py aa 
aa
teddy@teddy-ubuntu:~/test/py-test$ ./test.py aa bb cc
usage: test.py [-h] echo
test.py: error: unrecognized arguments: bb cc
teddy@teddy-ubuntu:~/test/py-test$ ./test.py -h
usage: test.py [-h] echo

positional arguments:
  echo        echo anything you input

optional arguments:
```
从上面看，echo这个叫做positional arguments。而`-h`叫做optional arguments。
我们根据shell脚本里的参数来理解一下。以`ls -l ./`。`-l`这个就是选项参数，`./`就是位置参数。



下面看一个完整一点的例子。

```
#!/usr/bin/env python
import sys, argparse

def main(argv):
	p = argparse.ArgumentParser(description='this is a argparse demo')
	p.add_argument('xxx', type=str, nargs='*', help='xxx ')
	p.add_argument('-a', '--aaa', action='store', default=None, help='aa help')
	p.add_argument('-b', '--bbb')
	global args
	args = p.parse_args(argv[1:])
	xxx = args.xxx
	print xxx
	print args
if __name__ == '__main__':
	argv = sys.argv
	main(argv)
```
运行效果：
```
teddy@teddy-ubuntu:~/test/py-test$ ./test.py -a xx yy
['yy']
Namespace(aaa='xx', xxx=['yy'])
```

# 使用总结





# ArgumentParser类

我们先看一些构造函数原型：

```
class argparse.ArgumentParser([description][, epilog][, prog][, usage][, add_help][, argument_default][, parents][, prefix_chars][, conflict_handler][, formatter_class]) 
```

所有参数都可选的，可以不带参数。

description：描述信息。在帮助信息最开始。

epilog：收场白。在帮助信息最后显示。

prog：程序的名字，默认是sys.argv[0]。

usage：这个一般我们不指定，用默认生成的。

add_help：是否添加一个默认的`-h`参数，默认是True的。

argument_default：默认是None。

总结：

一般只填写description。

举例：

```
import argparse

parser = argparse.ArgumentParser(description="help desc")
parser.print_help()
```

输出：

```
C:\Python27\python.exe D:/work/pycharm/py_test/test.py
usage: test.py [-h]

help desc

optional arguments:
  -h, --help  show this help message and exit

Process finished with exit code 0
```

# add_argument函数

原型：

```
ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest]) 
```

name or flags：名字或者一个选项list。例如：`foo或者-f或者--foo`。

action：action类型。

nargs：

const：被action和nargs需要的常量值。



action是我们要看看的。

action的可选值有：store（默认），store_const，store_true，store_false，



