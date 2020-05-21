---
title: Python之click模块
date: 2019-01-15 17:56:59
tags:
	- python
---



click是一个第三方模块。

作用相当于python内置的argparse。

但是好用很多。

click的使用有2个步骤：

```
1、使用@click.command装饰一个函数。使之成为命令行接口。
2、使用@click.option修饰，使之成为命令行选项。
```

代码如下：

```
import click

@click.command()
@click.option("--param", default=default_value, help="param desc info")
def func(param):
    pass
```

一个基本例子。

```
import click
@click.command()
@click.option("--count", default=1, help="number of greetings")
@click.option("--name", prompt="your name", help="the person to greet")
def hello(count, name):
    for x in range(count):
        click.echo("hello %s" % name)

hello()
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python test.py --help
Usage: test.py [OPTIONS]

Options:
  --count INTEGER  number of greetings
  --name TEXT      the person to greet
  --help           Show this message and exit.
```



参考资料

1、命令行神器 Click

https://funhacks.net/2016/12/20/click/