---
title: python（1）
date: 2024-03-18 19:22:17
tags:
	- python

---

--

# 快速查阅python标准库文档

用linux下面的pydoc命令。

举例：

```
pydoc os.walk
```

# python发展历史

Python的发展历史可以追溯到上世纪80年代末和90年代初。以下是Python的主要发展历程：

1. **起源：**
   Python的创始人是Guido van Rossum（吉多·范罗苏姆），他在1989年圣诞节期间开始开发Python。最初的目标是设计一种易于阅读和使用的编程语言，具有简洁、清晰的语法，同时又能够支持大型项目的开发。

2. **Python 1.x系列：**
   Python的第一个正式版本是在1991年发布的Python 0.9.0版。1994年发布了Python 1.0版，这是Python的第一个稳定版本。随后的1.x系列版本陆续发布，不断改进语言的功能和性能。

3. **Python 2.x系列：**
   在Python 1.x系列之后，Python 2.x系列成为主流版本。Python 2.0于2000年发布，带来了一些重要的改进，如增加了内置的垃圾回收器。2.x系列一直持续到2010年代初期，期间发布了许多更新版本，其中最知名的是2.7版，成为了长期支持版本（Long-Term Support，LTS）。

4. **Python 3.x系列：**
   Python 3.x系列的开发是为了解决Python 2.x系列中的一些设计缺陷和不一致性。Python 3.0于2008年发布，引入了许多不兼容的语言变化，以改进Python的一致性、简洁性和可用性。尽管在初期遇到了一些用户和库的迁移问题，但随着时间的推移，Python 3逐渐成为了主流版本。Python 2.x系列于2020年正式停止维护。

5. **社区与生态系统的发展：**
   Python的成功不仅仅源自语言本身，还得益于庞大的开发者社区和丰富的生态系统。Python社区积极活跃，提供了大量的第三方库和框架，涵盖了几乎所有领域，从网络开发到科学计算，再到人工智能和机器学习。

6. **持续发展：**
   Python持续保持着活跃的开发和更新，每年都会发布几个小版本，同时也会有较长时间的版本周期来充分测试和准备下一个大版本。截至2022年，Python的最新稳定版本是Python 3.10。Python的发展仍在不断进行，面向未来，社区持续努力改进语言本身和相关的工具与库，以适应不断变化的需求和技术趋势。

# python的doc怎么编写

编写Python的文档（doc）是非常重要的，它可以帮助其他开发者理解你的代码、库或项目的功能、用法和设计理念。Python社区通常采用以下几种方式来编写文档：

1. **Docstrings：**
   在Python中，可以使用docstrings来为函数、类、模块等提供文档。Docstrings是位于代码块顶部的字符串文本，用于描述代码的用途、参数、返回值等信息。通常采用三引号（'''或"""）包围，可以是单行或多行文本。使用标准的docstring格式可以使得文档更易读，并且可以通过特定工具自动生成文档。

   ```python
   def example_function(arg1, arg2):
       """
       这是一个示例函数的docstring。

       参数：
       arg1 (int): 第一个参数的描述
       arg2 (str): 第二个参数的描述

       返回值：
       bool: 返回值的描述
       """
       # 函数体代码...
   ```

2. **Sphinx：**
   Sphinx是一个流行的文档生成工具，广泛用于Python项目。它可以根据代码中的docstrings自动生成详细的文档网站或文档文件。Sphinx支持使用reStructuredText（reST）或Markdown等格式编写文档，可以生成HTML、PDF等多种格式的文档输出。

3. **reStructuredText（reST）：**
   reStructuredText是一种轻量级标记语言，被广泛用于编写Python项目的文档。它支持丰富的标记语法，可以方便地表达文档的结构、链接、代码示例等内容。Sphinx的默认格式就是reST，因此在编写Sphinx文档时会使用reST语法。

4. **Markdown：**
   虽然Sphinx默认使用reST格式，但也支持使用Markdown编写文档，通过相应的插件可以让Sphinx支持Markdown格式的文档。对于一些习惯使用Markdown的开发者来说，这样可以更加方便地编写文档。

5. **文档的内容：**
   无论采用何种格式，好的文档应该包含以下内容：
   - 项目简介：描述项目的目的和功能。
   - 安装说明：如何安装项目或依赖。
   - 使用说明：如何使用项目的各个功能，通常包括代码示例。
   - API文档：详细描述函数、类、模块等的接口和用法。
   - 配置说明：如何配置项目或库的参数。
   - 贡献指南：如何贡献代码或报告问题。

编写Python文档时，遵循一致的格式和规范，并确保文档内容准确、清晰易懂，可以帮助提高项目的可维护性和用户体验。

## reST文档写在python代码文件里的举例说明

当你在Python代码文件中编写reStructuredText（reST）文档时，通常是利用docstrings来写入文档内容。以下是一个简单的示例，展示了如何在Python代码文件中编写reST文档：

```python
def greet(name):
    """
    这个函数用于向指定的人打招呼。

    :param name: str，要打招呼的人的名字。
    :return: str，包含问候语的字符串。
    """
    return f"Hello, {name}!"

def add(a, b):
    """
    这个函数用于计算两个数的和。

    :param a: int，第一个加数。
    :param b: int，第二个加数。
    :return: int，两个数的和。
    """
    return a + b

if __name__ == "__main__":
    # 使用示例
    print(greet("Alice"))
    print(add(2, 3))
```

在上面的示例中：

- 函数`greet`和`add`都有相应的docstrings，用于描述函数的作用、参数和返回值。
- 使用了reST的标记语法，如`:param`用于描述函数参数，`:return`用于描述返回值。
- 在每个函数的顶部，使用了多行字符串形式的docstrings。

通过这种方式，你可以在Python代码文件中编写详细的文档，使得其他开发者可以轻松理解你的代码的作用和用法。

## :param :return这些是保留关键字吗？

在Python中，`:param`和`:return`并不是保留关键字，

它们只是一种约定俗成的写法，

用于在docstrings中描述函数的参数和返回值。

这种写法通常被文档生成工具（如Sphinx）所支持，并且它们并不会影响代码的执行或语法解析。

在docstrings中，`:param`用于描述函数的参数，`:return`用于描述函数的返回值，这样可以使得文档更加清晰明了。

但是，这些写法并不是Python语言本身的一部分，它们只是一种约定俗成的规范，开发者可以根据需要自由选择其他的写法或格式来编写文档。

总之，`:param`和`:return`等类似写法只是一种方便的约定，用于编写更具结构化和易读性的文档，而不会直接影响到Python代码的运行或解析。

## 还有哪些约定

除了`:param`和`:return`之外，Python的docstrings中常见的约定还包括：

1. **`:rtype:`：**
   用于描述函数的返回值类型。例如 `:rtype: int` 表示返回值类型为整数。

2. **`:raises:`或`:except:`：**
   用于描述函数可能抛出的异常或错误。例如 `:raises ValueError: 如果参数无效，则引发 ValueError 异常`。

3. **`:type:`：**
   用于描述函数参数的类型。例如 `:type arg1: int` 表示参数 arg1 的类型为整数。

4. **`:param type arg: description`：**
   类似于 `:param arg: description`，但是在这种情况下还包括参数的类型信息。

5. **`:keyword:`：**
   用于描述函数的关键字参数。

6. **`:example:`或`:Example:`：**
   用于提供函数或代码示例。

7. **`:note:`或`:Note:`：**
   用于提供额外的注释或说明。

8. **`:seealso:`或`:See Also:`：**
   用于提供相关链接或参考资料。

这些约定都是为了让文档更加清晰、结构化，以及易于理解。在编写docstrings时，可以根据需要选择适合的约定来描述函数、类、模块等的各种信息。

## 这个约定有什么文档进行描述吗

这些约定通常是由Python社区的文档编写指南和标准所规定的，其中最重要的文档是PEP（Python Enhancement Proposal，Python增强提案）。以下是与docstrings相关的一些PEP：

1. **PEP 257 - Docstring Conventions：**
   这个PEP定义了Python的docstring约定，包括docstring的格式、风格和用法。它提供了一些通用的建议，帮助开发者编写清晰、规范的文档字符串。

2. **PEP 287 - reStructuredText Docstring Format：**
   这个PEP介绍了使用reStructuredText格式编写docstring的方法。它指导开发者如何使用reST语法来编写结构化的文档字符串，以及如何在文档生成工具（如Sphinx）中使用它们。

3. **PEP 484 - Type Hints：**
   这个PEP介绍了Python的类型提示语法，它并不直接与docstrings有关，但是可以与docstrings一起使用，用于描述函数的参数和返回值的类型信息。

虽然这些PEP中并没有直接列出所有可能的docstring约定，但它们提供了一些通用的指导原则，帮助开发者编写清晰、一致的文档字符串。此外，Python官方文档和Sphinx文档也提供了关于docstring编写的详细指南和示例。

## PEP 287 内容罗列

PEP 287 提出了将 reStructuredText 作为 Python docstrings 的标准格式的建议，以下是其主要内容的概述：

1. **背景和动机：**
   PEP 287 引入了 reStructuredText 作为 Python docstrings 的标准格式的提案。其目的是通过使用一种通用的、易于阅读和编辑的标记语言来编写文档字符串，从而提高 Python 代码的可读性、可维护性和文档生成效率。

2. **reStructuredText 格式：**
   PEP 287 介绍了 reStructuredText 的基本语法和常用结构，包括标题、段落、列表、链接、引用等。这些功能使得开发者可以以一种结构化和清晰的方式编写文档字符串。

3. **文档字符串示例：**
   PEP 287 提供了一些使用 reStructuredText 编写的文档字符串示例，涵盖了函数、类、模块等不同类型的文档。这些示例展示了如何描述函数参数、返回值、异常、示例代码等内容，并且符合标准的 reStructuredText 格式。

4. **Sphinx 集成：**
   PEP 287 讨论了如何利用 Sphinx 文档生成工具来自动生成基于 reStructuredText 格式的文档。Sphinx 提供了强大的文档生成功能，可以根据代码中的文档字符串自动生成详细的 API 文档和用户手册。

5. **最佳实践和建议：**
   PEP 287 提供了一些关于如何编写清晰、一致的文档字符串的最佳实践和建议。例如，建议使用适当的标题和结构来组织文档、使用代码示例来说明使用方法等。

总之，PEP 287 为 Python 的文档字符串提供了一种标准的、结构化的格式，即 reStructuredText，以提高代码的可读性和文档生成效率。



# Python 文档字符串风格指南

如果你对 Python 文档字符串（Docstring）的概念不是很清楚，可以参考以下材料：

- [PEP 257](https://www.python.org/dev/peps/pep-0257) - 文档字符串约定（Docstring Conventions）
- [PEP 287](https://www.python.org/dev/peps/pep-0287) - reStructuredText 风格文档字符串格式
- [PEP 484](https://www.python.org/dev/peps/pep-0484) - 类型提示（Type Hints）
- [Google Python Style guides](https://google.github.io/styleguide/pyguide.html#381-docstrings) - Google 风格文档字符串格式



https://www.megengine.org.cn/doc/stable/en/development/docs/python-docstring-style-guide.html