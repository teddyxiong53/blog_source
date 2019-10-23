---
title: python项目之自动添加标签
date: 2019-10-19 16:27:49
tags:
	- Python

---

1

这个是《python基础教程》（第三版）第20章内容的学习。

主要是使用python杰出的文本处理能力。把纯文本转成html。

原书代码在这里：

https://github.com/teddyxiong53/beginning_python_source_code/tree/master/Chapter20

就是一个类似把markdown文件渲染成html的功能。

先定义一下功能。

```
1、可以处理不同的文本框以及内嵌文本。
2、要可以很容易扩展成其他的渲染格式。例如latex。这个就要求我们设计地扩展性要好。
```

我们需要使用的工具有：

````
1、文件读和文件写。
2、文件内容逐行读取。
3、字符串方法。
4、生成器。
5、re模块。
````

要渲染的内容是：test_input.txt。

在pycharm里新建项目：text_render。

从文本里看，文本块（包括段落、标题、列表项）之间有一个或者多个空行。

```
def lines(file):
    for line in file:
        yield line
    yield '\n'

def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        else:
            yield ''.join(block).strip()
            block = []
```

上面的代码定义了2个生成器。

生成器lines：每次返回一行数据，在文末添加一个空行。

生成器blocks：实现文本块的分解。

新建simple_markup.py。

```
import sys,re
from util import *

print('<html><head><title>...</title><body>')
title = True
with open('./text_input.txt') as f:
    for block in blocks(f):
        # replace *x* to <em>
        block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
        if title:
            print('<h1>')
            print(block)
            print('</h1>')
            title = False #相当于只有第一个block被当成title。
        else:
            print("<p>")
            print(block)
            print("</p>")

print('</body></html>')
```

执行：

```
python simple_markup.py > 1.html
```

上面只做了两件事情：

1、加em标签。

2、加p标签。

使用了re模块的sub方法进行替换。

下面我们进行重构。

列出一些潜在的组件。

```
1、解析器。
	用来读取文本并管理其他类。
2、规则。
	对于每种文本，都制定一条对应的规则。
3、过滤器。
	使用正则表达式来处理内嵌元素。
4、处理程序。
	用来给解析器生成输出。
	本质是渲染器，但是我们不叫渲染器。主要是为了强调它负责处理解析器的输出。
	而不必像HTMLRenderer那样使用标记语言来渲染文本。
	xml的解析方案SAX也使用了类似的处理程序机制。
```

新建handlers.py。

````
class Handler:
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback("start_", name)

    def end(self, name):
        self.callback("end_", name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                match.group(0)
            return result
        return substitution


class HTMLRenderer:
    def start_paragraph(self):
        print('<p>')
    def end_paragraph(self):
        print('</p>')

    def sub_emphasis(self, match):
        return '<em>{}</em>'.format(match.group(1))
````

到这里，处理程序的可扩展性和灵活性都很高了。

我们开始看看文本解析的优化。

新建rules.py文件。





参考资料

1、

