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

`click` 是一个功能强大的 Python 库，用于构建命令行接口。以下是 `click` 的主要 API 及其功能简介：

### 1. **基础装饰器**

- **`@click.command()`**：用于定义一个命令。
  
  ```python
  @click.command()
  def hello():
      click.echo("Hello, World!")
  ```

- **`@click.group()`**：用于定义一个命令组，可以将多个命令组织在一起。

  ```python
  @click.group()
  def cli():
      pass
  ```

### 2. **命令参数和选项**

- **`@click.argument()`**：定义命令的参数。

  ```python
  @click.command()
  @click.argument('name')
  def greet(name):
      click.echo(f"Hello, {name}!")
  ```

- **`@click.option()`**：定义命令的选项，支持默认值和类型。

  ```python
  @click.command()
  @click.option('--count', default=1, help='Number of greetings.')
  def hello(count):
      for _ in range(count):
          click.echo("Hello!")
  ```

### 3. **输出功能**

- **`click.echo()`**：用于输出文本，支持更好的格式化和错误流。

- **`click.pause()`**：暂停程序，等待用户输入。

### 4. **输入功能**

- **`click.prompt()`**：提示用户输入，并可以指定类型。

  ```python
  name = click.prompt("Please enter your name", type=str)
  ```

- **`click.confirm()`**：提示用户确认（是/否）。

  ```python
  if click.confirm("Do you want to continue?", default=True):
      click.echo("Continuing...")
  ```

### 5. **错误处理**

- **`click.BadParameter`**：用于抛出参数错误。

- **`click.ClickException`**：用于抛出一般的点击异常。

### 6. **上下文管理**

- **`@click.pass_context`**：允许在命令之间传递上下文。

  ```python
  @click.group()
  @click.pass_context
  def cli(ctx):
      ctx.ensure_object(dict)
  ```

### 7. **自定义帮助信息**

- **`help` 参数**：可以在命令和选项中添加帮助信息，自动生成命令行帮助。

### 8. **多命令支持**

- **嵌套命令**：可以使用 `@click.group()` 嵌套多个命令。

  ```python
  @cli.group()
  def user():
      pass
  
  @user.command()
  def create():
      click.echo("User created!")
  ```

### 9. **命令的别名**

- **`@click.command(name='alias')`**：可以为命令定义别名。

### 示例

以下是一个简单的 `click` 示例，展示了以上 API 的用法：

```python
import click

@click.group()
def cli():
    """这是一个示例CLI工具"""
    pass

@cli.command()
@click.argument('name')
@click.option('--count', default=1, help='Number of greetings.')
def greet(name, count):
    """向指定的人问好"""
    for _ in range(count):
        click.echo(f"你好，{name}！")

if __name__ == '__main__':
    cli()
```

### 总结

`click` 提供了丰富的 API，帮助开发者快速构建功能强大且用户友好的命令行应用程序。通过这些装饰器和功能，用户可以轻松定义命令、选项、参数并处理输入输出。

# argument和option的区别

在 `click` 中，`argument`（参数）和 `option`（选项）都是用于接收用户输入的方式，但它们之间有一些重要的区别：

### 1. **定义方式**

- **Argument (`@click.argument`)**：
  - 通常是必需的，不需要前缀。
  - 在命令行中位置固定，依赖于位置顺序。

  ```python
  @click.command()
  @click.argument('name')
  def greet(name):
      click.echo(f"Hello, {name}!")
  ```

  - 例如：`python script.py Alice`，`Alice` 是一个参数。

- **Option (`@click.option`)**：
  - 通常是可选的，使用前缀（如 `--` 或 `-`）。
  - 可以指定默认值和帮助信息。

  ```python
  @click.command()
  @click.option('--count', default=1, help='Number of greetings.')
  def hello(count):
      for _ in range(count):
          click.echo("Hello!")
  ```

  - 例如：`python script.py --count 3`，`3` 是一个选项值。

### 2. **使用方式**

- **Argument**：
  - 通过位置进行传递，用户必须按照顺序提供。
  - 可以没有默认值。

- **Option**：
  - 通过命令行选项进行传递，用户可以随意选择是否提供。
  - 可以有默认值和帮助文本。

### 3. **示例对比**

#### Argument 示例

```python
@click.command()
@click.argument('filename')
def read_file(filename):
    click.echo(f"Reading file: {filename}")
```

命令行调用：

```bash
python script.py myfile.txt
```

#### Option 示例

```python
@click.command()
@click.option('--verbose', is_flag=True, help='Enable verbose output.')
def hello(verbose):
    if verbose:
        click.echo("Verbose mode is on.")
    click.echo("Hello, World!")
```

命令行调用：

```bash
python script.py --verbose
```

### 4. **总结**

- **Argument**：位置固定，通常是必需的，适用于那些直接作为命令输入的值。
- **Option**：灵活可选，使用前缀，适用于可选的配置或参数。

通过这两种方式，`click` 提供了灵活性，以满足不同命令行输入的需求。

# Pass_context

```
import click

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = 'aaa'

@cli.command()
@click.pass_context
def show_config(ctx):
    click.echo(f'config shared: {ctx.obj["config"]}')

@cli.command()
@click.pass_context
def set_config(ctx):
    new_config = click.prompt('input your config')
    ctx.obj['config'] = new_config
    click.echo(f'config set to {ctx.obj["config"]}')

cli()
```

# **result_callback**



# 参考资料

1、命令行神器 Click

https://funhacks.net/2016/12/20/click/