---
title: pycparser研究
date: 2023-09-29 09:11:11
tags:
	- 编程语言
---

--

# 简介

代码在这里：

https://github.com/eliben/pycparser

pycparser是一个用于解析C语言代码的Python库。

它提供了一种简单而灵活的方法来分析和操作C语言代码的抽象语法树（Abstract Syntax Tree，AST）。

pycparser的主要功能是将C语言代码解析为AST，并提供了一组工具和函数来遍历和操作AST。

它可以处理包含复杂语法结构的C代码，

包括条件语句、循环语句、函数定义等。

使用pycparser，你可以编写Python程序来分析C代码的结构、查找特定的语法模式、提取变量和函数声明等信息，

以及进行其他与C代码相关的静态分析任务。

它还可以用于构建自定义的C代码分析工具和编译器前端。

pycparser基于PLY（Python Lex-Yacc）工具，

这是一个用于构建词法分析器和语法分析器的Python工具集。

它使用C语言的语法规则作为输入，生成对应的AST。

总结一下，pycparser是一个功能强大的Python库，用于解析和操作C语言代码的AST。

它为开发者提供了一种方便的方式来进行C代码分析和处理，无论是用于静态分析、代码转换还是构建自定义工具。

# 一般用途

pycparser在以下几个方面具有广泛的用途：

1. 静态代码分析：pycparser可以用于静态分析C语言代码，识别代码中的语法错误、潜在的问题和不符合规范的代码模式。你可以使用pycparser**构建自定义的静态代码分析工具**，例如检测未初始化变量、查找内存泄漏、检查函数调用规则等。

2. 代码转换和重构：通过解析C代码为AST，pycparser使得对代码进行**转换和重构变得更加容易**。你可以使用pycparser修改AST并重新生成相应的C代码，实现代码的自动转换、代码风格的一致性修改、代码重构等操作。

3. 编译器前端开发：如果你需要开发一个C语言编译器或编译器前端，pycparser可以帮助你构建基础的语法分析器。它提供了一个方便的接口来解析C代码为AST，并可以进一步进行语义分析、类型检查等编译器前端的任务。

4. 代码生成和模板扩展：**通过解析C代码为AST，你可以使用pycparser生成其他编程语言的代码，或者在C代码的基础上进行模板扩展。**这对于将C代码转换为其他语言、生成代码框架或进行代码生成任务非常有用。

需要注意的是，pycparser是一个基于文本的解析器，它只能解析合法的C代码。如果你的代码包含了非标准的C扩展或特定编译器的特性，可能需要进行适当的调整或扩展。



- C代码混淆器
- 各种c编译器的前端
- 静态分析工具
- 自动化单元测试生成工具
- 为c语言添加新扩展

pycparser是用*纯python*编写的，除了python解释器外无需其他依赖。

pycparser的目标是完全支持C99标准(ISO/IEC 9899)，也支持部分C11的特性。



- pycparser无需其他依赖，它唯一使用的非标准库是PLY，但PLY已集成到了`pycparser/ply`中，当前PLY版本是3.10，PLY主页为http://www.dabeaz.com/ply/

# 运行示例

直接把代码下载下来，运行各个示例程序即可。

## dump_ast.py

```
λ python examples\dump_ast.py
FileAST:
  FuncDef:
    Decl: foo, [], [], [], []
      FuncDecl:
        TypeDecl: foo, [], None
          IdentifierType: ['int']
    Compound:
  FuncDef:
    Decl: main, [], [], [], []
      FuncDecl:
        TypeDecl: main, [], None
          IdentifierType: ['int']
    Compound:
      FuncCall:
        ID: foo
      Return:
        Constant: int, 0
```

这个是分析的basic.c这个文件。

```
int foo() {}

int main() {
  foo();
  return 0;
}
```

# cffi

pycparser最著名的一个应用就是cffi。

用来解析c函数的声明来生成ffi接口。

# 源码解读

Pycparser非常容易上手，需重点阅读`examples`目录和`c_ast.py`文件


重要文件介绍

`_c_ast.cfg和c_ast.py`提供了C99的语法和实现，如_c_ast.cfg对IF语句的描述:
`If: [cond*, iftrue*, iffalse*]`
表示If节点由三个子节点构成，分别是condition、iftrue、iffalse，同BNF范式的描述

c_ast.py中对If节点定义

```
class If(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.iftrue is not None: nodelist.append(("iftrue", self.iftrue))
        if self.iffalse is not None: nodelist.append(("iffalse", self.iffalse))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.iftrue is not None:
            yield self.iftrue
        if self.iffalse is not None:
            yield self.iffalse

    attr_names = ()
```

发现`__init__`方法除了三个子节点，还多了一个coord节点，

该节点是用来表示源码中节点的位置信息的，比如代码行号等。

观察children方法，用nodelist管理子节点，

每一个子节点用tuple表示，

如条件语句用("cond",self.cond)表示，

self.cond才是真实的条件节点，"cond"是该节点的TAG。

## func_calls.py

这个是生成调用关系图的example。



# pycparser的ast

`pycparser` 是一个用于解析 C 语言代码的 Python 库，它可以将 C 代码解析为抽象语法树（Abstract Syntax Tree，AST）的形式。AST 是一种树状结构，用于表示程序源代码的语法结构。

在 `pycparser` 中，AST 是由一系列 Python 对象组成的树状结构，每个对象表示 C 代码的一个语法结构（如函数、语句、表达式等）。这些对象定义在 `pycparser.c_ast` 模块中。

以下是 `pycparser` 中常见的 AST 对象类型：

- `FileAST`：表示整个 C 文件的 AST 根节点。
- `FuncDef`：表示函数定义。
- `Decl`：表示声明语句。
- `Typename`：表示类型名称。
- `ID`：表示标识符（变量名、函数名等）。
- `Constant`：表示常量（整数、浮点数、字符串等）。
- `UnaryOp`：表示一元操作符表达式。
- `BinaryOp`：表示二元操作符表达式。
- `If`：表示 if 语句。
- `For`：表示 for 循环语句。
- `While`：表示 while 循环语句。
- `Assignment`：表示赋值语句。

通过解析 C 代码并构建 AST，你可以使用 `pycparser` 提供的 API 对代码进行分析、修改和生成。你可以遍历 AST，访问各个节点的属性和子节点，以获取源代码的结构信息，并进行相应的操作。

以下是一个简单的示例，演示如何使用 `pycparser` 解析 C 代码并遍历 AST：

```python
from pycparser import parse_file, c_ast

# 解析 C 代码文件，生成 AST
ast = parse_file('example.c')

# 遍历 AST
def traverse(node):
    print(node.__class__.__name__)  # 打印节点类型

    # 遍历子节点
    for child in node.children():
        traverse(child)

# 从根节点开始遍历 AST
traverse(ast)
```

上述示例中，`parse_file` 函数用于解析指定的 C 代码文件，返回整个文件的 AST 根节点。`traverse` 函数用于遍历 AST，打印每个节点的类型，并递归遍历其子节点。

通过了解 `pycparser` 的 AST 对象和相关操作，你可以更好地理解和利用 `pycparser` 库来处理和分析 C 代码。

# 生成c代码

使用 `pycparser` 库来生成 C 代码，你可以构建相应的 AST，然后将 AST 转换回 C 代码的字符串表示。

下面是一个简单的示例，演示如何使用 `pycparser` 生成一些简单的 C 代码：

```python
from pycparser import c_ast, c_generator

# 创建一个新的 C 文件的 AST
ast = c_ast.FileAST([])

# 创建一个函数定义
func_def = c_ast.FuncDef(
    decl=c_ast.Decl(
        name='foo',
        type=c_ast.FuncDecl(
            args=c_ast.ParamList(params=[]),
            type=c_ast.TypeDecl(declname='void')
        )
    ),
    body=c_ast.Compound(
        block_items=[
            c_ast.Return(expr=None)
        ]
    )
)

# 将函数定义添加到 AST 的外部定义列表中
ast.ext.append(func_def)

# 生成 C 代码字符串
generator = c_generator.CGenerator()
code = generator.visit(ast)

# 打印生成的 C 代码
print(code)
```

上述示例中，首先创建了一个空的 `FileAST` 对象作为 AST 的根节点。然后创建了一个函数定义 `FuncDef`，其中包含了函数名、函数类型和函数体。在这个示例中，函数名为 "foo"，无参数且返回类型为 `void`，函数体中只包含一个 `Return` 语句。

接下来，将函数定义添加到 AST 的外部定义列表中，通过 `ast.ext.append(func_def)` 完成。

最后，使用 `CGenerator` 对象将 AST 转换为 C 代码的字符串表示。`CGenerator` 的 `visit` 方法会遍历 AST 并生成相应的 C 代码字符串。

通过打印 `code` 变量，你可以看到生成的 C 代码字符串。

你可以根据需要使用 `pycparser` 提供的 AST 对象构建更复杂的 C 代码结构，并通过 `CGenerator` 将 AST 转换为对应的 C 代码字符串。

# 网上找到的示例



https://snyk.io/advisor/python/pycparser/example



# ply教程

PLY 包含两个独立的模块：lex.py 和 yacc.py，都定义在 ply 包下。

lex.py 模块用来将输入字符通过一系列的正则表达式分解成标记序列，

yacc.py 通过一些上下文无关的文法来识别编程语言语法。

yacc.py 使用 LR 解析法，并使用 LALR(1)算法（默认）或者 SLR 算法生成分析表。

这两个工具是为了一起工作的。

lex.py 通过向外部提供token()方法作为接口，

方法每次会从输入中返回下一个有效的标记。

yacc.py 将会不断的调用这个方法来获取标记并匹配语法规则。

yacc.py 的功能通常是生成抽象语法树(AST)，

不过，这完全取决于用户，如果需要，yacc.py 可以直接用来完成简单的翻译。

就像相应的 unix 工具，yacc.py 提供了大多数你期望的特性，

其中包括：

丰富的错误检查、语法验证、支持空产生式、错误的标记、通过优先级规则解决二义性。

事实上，传统 yacc 能够做到的 PLY 都应该支持。



yacc.py 与 Unix 下的 yacc 的主要不同之处在于，

yacc.py 没有包含一个独立的代码生成器，

而是在 PLY 中依赖反射来构建词法分析器和语法解析器。

不像传统的 lex/yacc 工具需要一个独立的输入文件，

并将之转化成一个源文件，

Python 程序必须是一个可直接可用的程序，

这意味着不能有额外的源文件和特殊的创建步骤（像是那种执行 yacc 命令来生成 Python 代码）。

又由于生成分析表开销较大，PLY 会缓存生成的分析表，并将它们保存在独立的文件中，除非源文件有变化，会重新生成分析表，否则将从缓存中直接读取。



由于 PLY 是作为教学工具来开发的，

你会发现它对于标记和语法规则是相当严谨的，

这一定程度上是为了帮助新手用户找出常见的编程错误。

不过，高级用户也会发现这有助于处理真实编程语言的复杂语法。

还需要注意的是，PLY 没有提供太多花哨的东西（例如，自动构建抽象语法树和遍历树），我也不认为它是个分析框架。

相反，你会发现它是一个用 Python 实现的，基本的，但能够完全胜任的 lex/yacc。

本文的假设你多少熟悉分析理论、语法制导的翻译、基于其他编程语言使用过类似 lex 和 yacc 的编译器构建工具。

如果你对这些东西不熟悉，你可能需要先去一些书籍中学习一些基础，

比如：Aho, Sethi 和 Ullman 的《Compilers: Principles, Techniques, and Tools》（《编译原理》），和 O’Reilly’ 出版的J ohn Levine 的《lex and yacc》。

事实上，《lex and yacc》和 PLY 使用的概念几乎相同。





参考资料

1、

https://xiazemin.github.io/python/2020/07/08/ply.html

# 参考资料

1、C语言源码分析库Pycparser介绍

**https://blog.csdn.net/WaterDemo22/article/details/98965725**

2、Python-C语言语法解析：pycparser模块

https://blog.csdn.net/u011079613/article/details/122462729