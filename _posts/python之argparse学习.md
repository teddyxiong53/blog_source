---
title: python之argparse学习
date: 2017-01-05 20:16:41
tags:
	- python
---

--

argparse是作为optparse的替代品，在Python2.7引入进来的。



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



看一个例子：

```
#!/usr/bin/python 

import argparse

parser = argparse.ArgumentParser(description="test ArgumentParser desc")
parser.add_argument("--no-network-check", action="store_true", help="check help info")

args = parser.parse_args()

print args

```

运行效果：

```
pi@raspberrypi:~/work/test/py-test$ ./test.py 
Namespace(no_network_check=False)
pi@raspberrypi:~/work/test/py-test$ ./test.py --no-network-check
Namespace(no_network_check=True)
pi@raspberrypi:~/work/test/py-test$ 
```

可以看到，参数里的`-`被转成了下划线。

# action有哪些值，代表什么含义

在`argparse`库中，`action`参数用于指定命令行选项的动作。以下是`argparse`中常用的几种`action`值及其含义：

- `'store'`（默认值）：将命令行参数的值存储到对应的属性中。例如，`parser.add_argument("--name")`将命令行参数的值存储到`args.name`属性中。

- `'store_const'`：将指定的常量值存储到属性中。常量值通过`const`参数指定。例如，`parser.add_argument("--verbose", action="store_const", const=True)`将将`True`存储到`args.verbose`属性中。

- `'store_true'`：将`True`存储到属性中。通常用于表示开关选项，如果在命令行中使用了该选项，则将`True`存储到对应的属性中。

- `'store_false'`：将`False`存储到属性中。通常用于表示开关选项，如果在命令行中使用了该选项，则将`False`存储到对应的属性中。

- `'append'`：将多个命令行参数的值追加到列表中。例如，`parser.add_argument("--file", action="append")`将多个`--file`选项的值存储到`args.file`列表中。

- `'append_const'`：将指定的常量值追加到列表中。常量值通过`const`参数指定。

- `'count'`：统计命令行选项出现的次数，并将次数存储到属性中。例如，`parser.add_argument("--verbose", action="count")`将统计`--verbose`选项出现的次数，并将次数存储到`args.verbose`属性中。

- `'help'`：打印帮助信息并退出程序。当用户在命令行中使用帮助选项（如`-h`或`--help`）时，`argparse`会自动执行该动作。

这些是一些常见的`action`值，用于定义选项的行为。通过选择适当的`action`值，你可以根据自己的需求来处理命令行参数，并将其存储到相应的属性中。

# 参数组（Argument Group）

这段代码使用`argparse.ArgumentParser`对象的`add_argument_group`方法创建了一个参数组（Argument Group）。

下面是对该代码的解释：

```python
group = parser.add_argument_group('http arguments', 'Extra arguments when set --http')
```

这行代码创建了一个名为`http arguments`的参数组，并将其赋值给变量`group`。让我们逐个解释参数的含义：

- `'http arguments'`：这是参数组的标题（Title），用于标识参数组的名称或主题。在这个例子中，参数组的标题是`http arguments`。

- `'Extra arguments when set --http'`：这是参数组的描述（Description），用于提供有关参数组的额外信息。在这个例子中，描述是`Extra arguments when set --http`，说明当设置了`--http`选项时，这个参数组包含一些额外的参数。

通过使用参数组，你可以将相关的命令行选项组织在一起，并在帮助信息中以更清晰的方式呈现。参数组可以用于将一组相关的选项分组显示，并提供额外的描述信息，以帮助用户理解这些选项的用途和关系。

在创建参数组后，你可以使用`add_argument`方法向该参数组中添加具体的命令行选项。例如：

```python
group.add_argument("--url", help="URL for HTTP connection")
group.add_argument("--timeout", type=int, help="Timeout value for HTTP requests")
```

以上代码将`--url`和`--timeout`选项添加到名为`http arguments`的参数组中。这样，这些选项将与该参数组相关联，并在帮助信息中以参数组的形式显示出来。