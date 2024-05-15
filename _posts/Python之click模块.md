---
title: Python之click模块
date: 2019-01-15 17:56:59
tags:
	- python
---

--

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

# 简介

当然，以下是关于Python中的`click`模块的简要介绍：

| 模块           | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| **click**      | `click` 是一个用于创建命令行界面（CLI）的Python模块。它可以帮助您快速构建命令行应用程序，提供用户友好的命令行接口。`click`模块的主要目标是简化命令行开发，使得创建CLI应用更加容易和直观。 |
| **命令**       | 在`click`中，命令由装饰器`@click.command()`定义，并且通常是CLI程序的主要功能单元。您可以通过添加参数、选项和回调函数来自定义命令。 |
| **参数和选项** | `click`允许您定义命令所需的参数和选项。参数是命令行中的位置参数，而选项是通过命令行标志传递的附加信息。这些参数和选项可以通过`@click.argument()`和`@click.option()`装饰器进行定义。 |
| **回调函数**   | 每个命令都有一个关联的回调函数，用于定义命令的行为。当用户运行命令时，关联的回调函数将被调用，并执行相应的操作。 |
| **帮助文档**   | `click`自动生成帮助文档，使得您的CLI应用程序能够自动生成并展示命令、参数和选项的使用说明。 |
| **扩展性**     | 通过`click`，您可以轻松地编写自定义命令行界面，并与其他Python库和框架（如Flask、Django等）集成。 |

`click`的设计使得它成为编写CLI应用程序的理想选择，因为它提供了简洁、直观的API，并且易于学习和使用。

# 发展历史

以下是`click`模块的简要发展历史：

| 日期           | 事件                                                         |
| -------------- | ------------------------------------------------------------ |
| **2012年**     | `click`模块由Armin Ronacher创建，并首次发布。Armin Ronacher是Flask框架的作者，他创建`click`是==为了解决在Flask项目中处理命令行任务的需求。== |
| **2013年**     | `click`的第一个稳定版本（版本0.1）发布。该版本包含了基本的命令行功能，并得到了Python社区的关注和支持。 |
| **2014年**     | `click`的版本0.2发布，带来了更多的功能和改进。此时，`click`已经成为Python社区中流行的命令行界面开发工具之一。 |
| **2015年**     | `click`的版本1.0发布，标志着其稳定性和成熟度的进一步提升。此版本中包含了一系列新功能和改进，使得`click`更加强大和灵活。 |
| **2016年至今** | `click`持续得到更新和维护，不断引入新功能、改进和修复。它成为了Python生态系统中广泛使用的命令行界面开发工具之一，并被许多知名项目（如Flask、Pyramid等）采用。 |

自从首次发布以来，`click`一直以其简单、易用和功能丰富而受到开发者的青睐，并且在Python生态系统中扮演着重要的角色。

# 主要api

以下是`click`模块中一些主要的API：

1. **`click.command()`**: 用于装饰命令函数，将其转换为命令行命令。
   
2. **`@click.option()`**: 用于定义命令行选项。可以指定选项的名称、缩写、类型、默认值等。

3. **`@click.argument()`**: 用于定义命令行参数。可以指定参数的名称、类型等。

4. **`click.echo()`**: 输出消息到标准输出。类似于Python的内置函数`print()`，但更加灵活，可以指定输出的文件、颜色等。

5. **`click.prompt()`**: 从用户处获取输入。可以指定提示信息、输入类型、默认值等。

6. **`click.confirm()`**: 获取用户确认输入。可以指定确认信息、默认值等。

7. **`click.secho()`**: 输出带有颜色的消息到标准输出。可以指定消息、颜色等。

8. **`click.group()`**: 创建命令组。用于组织多个相关的命令。

9. **`click.File()`**: 将参数解析为文件对象。用于处理文件路径。

10. **`click.Path()`**: 将参数解析为文件路径。提供了更多的路径处理选项，如绝对路径、可写性检查等。

这些是`click`模块中一些常用的API，您可以使用它们来创建灵活、强大的命令行应用程序。

# 参考资料

1、命令行神器 Click

https://funhacks.net/2016/12/20/click/