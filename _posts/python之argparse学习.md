---
title: python之argparse学习
date: 2017-01-05 20:16:41
tags:
	- python
---
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


