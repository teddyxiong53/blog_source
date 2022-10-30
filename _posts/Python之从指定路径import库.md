---
title: Python之从指定路径import库
date: 2017-09-24 10:35:02
tags:
	- python

---



学习python的module的写法，写了一个module，但是不知道怎么使用起来。

module1.py文件：

```
#!/usr/bin/python

def func1():
	print "module1 func1"
__all__ = [func1]
```

然后在命令行上进行import。

最简单的做法是这样的：

```
import sys
sys.path.append("./")
import module1

```

查看相关情况是这样的：

```
>>> import module1
>>> help(module1)
Help on module module1:

NAME
    module1

FILE
    /home/pi/work/test/python/module1.py

DATA
    __all__ = [<function func1>]

(END)

>>> dir(module1)
['__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'func1']
```



import的查找路径的顺序是怎样的？

```
标准库
第三方库
当前路径
```



什么是绝对导入？什么是相对导入？

```
绝对导入
import A.B
from A import B
```

```
相对导入
from . import B
from ..A imprt B
```

python2里是默认是相对路径导入。python3默认为绝对路径导入。

有时候，在python2的代码里，会加上这句：

```
from __future__ import absolute_import
```

这个又是为了达到什么目标呢？

是为了禁止隐式相对导入。

对于下面这个目录结构。

```
thing
├── books
│ ├── adventure.py
│ ├── history.py
│ ├── horror.py
│ ├── __init__.py
│ └── lovestory.py
├── furniture
│ ├── armchair.py
│ ├── bench.py ---这个
│ ├── __init__.py
│ ├── screen.py
│ └── stool.py 这个
└── __init__.py
```

如果我们要在stool.py里音乐bench.py。有下面三种方式：

```
import bench # 这个就是隐式相对导入。不推荐。python3废弃了。这种方式只适合用来导入系统路径下的。
from . import bench # 这个是显式相对导入
from furniture import bench # 这个就是绝对导入。
```



import特点，防止重复导致，你import多次，只有第一次有用。

如果你的py文件修改了，希望另外一个脚本里把这个修改体现出来。

例如服务器运行后，不让停止的情况下，重新load某个脚本。

```
from imp import reload
reload(xxx)
```

imp里的reload已经是过时的了。

sys.reload可以用。



这个还有点麻烦。



其实这两个错误的原因归根结底是一样的：

在涉及到相对导入时，

package所对应的文件夹必须正确的被python解释器视作package，

而不是普通文件夹。

否则由于不被视作package，

无法利用package之间的嵌套关系实现python中包的相对导入。

文件夹被python解释器视作package需要满足两个条件：

1、文件夹中必须有`__init__.py`文件，该文件可以为空，但必须存在该文件。

2、不能作为顶层模块来执行该文件夹中的py文件（即不能作为主函数的入口）。



# 最佳实践

https://zhuanlan.zhihu.com/p/78247846

## module

在Python中，一个.py文件就是一个module，即“模块”，**模块的名称是文件名去掉末尾的'.py'**。

一个模块（A）中的变量、函数、类等符号，

被其他模块（B）import之后，可被其他模块（B）引用。

我们写程序代码的时候，就可以把代码分门别类地放在不同的.py文件中，按照各自的层级位置，实现各自的功能。

比如将程序分成`brick.py`、`wall.py`、`house.py`。

- `brick.py`实现砖头制作函数，不同的参数指定砖头规格；
- `wall.py`中`import brick`，调用函数得到不同规格砖头，组装形成墙体；
- `house.py`是主程序，`import wall`后调用函数得到墙体，必要时也可以`import brick`制作特定的砖头，最后统一组装成房子。

Python是“电池内置”型（battery included）语言，

初次安装Python解释器时会一并安装很多基础的模块和包，称为“标准库（standard library）”，

在Python安装路径的`lib`子目录下可看到。

此外，用户可以自行安装其他第三方库，默认会放在`lib/site-packages`子目录下。



有的模块出于运行效率考虑，是被编译进Python解释器的，并不以`.py`文件形式存在，比如常用的`builtins`、`sys`等。

内置的`len()`函数、加减乘除运算等就在`builtins`模块中，使用时甚至不需要我们import，Python解释器在启动时便已import好了，而`sys`模块需要先import才能使用。



## package

自己写的模块应该避免与Python内置模块重名，但不同人编写的模块名称相同怎么办？

为解决名称冲突问题，Python引入按照目录组织模块的方法，创造了package（包）的概念。

包是一个特殊的目录，其下**必须**含有名为`__init__.py`的文件，否则Python会将其当作普通目录而不是包，目录下`__init__.py`文件对应的模块名就是包（目录）名，**文件内容可以为空**。

有了包，只要顶层包名称与其他人不发生冲突，模块名称便不会冲突。

如下目录组织，顶层包为`soud`目录，import成功后，相应模块名称为`sound.example`、`sound.formats.wavread`、`sound.effects.echo`、`sound.filters.vocoder`等，

要引用模块中的变量、函数符号，按照`模块名.符号名`方式使用即可。

```
sound/                          # 顶层包
      __init__.py               # 初始化sound包
      formats/                  # 子包formats
              __init__.py
              wavread.py
              wavwrite.py
              ...
      effects/                  # 子包effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/                  # 子包filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
      example.py
```



为提高代码复用和有效模块化组织，建议使用主程序+包的方式组织项目，其中包内按分层思想放置若干模块，包内模块间使用相对导入（relative import），项目根目录下放置主程序文件。仍以开头建大楼为例，组织如下：

```bash
projectname/              # 项目目录
    #__init__.py          # 也可以变成包，供今后其他项目import
    construct/            # 子包construct用于建造过程
        __init__.py
        brick.py          # 制作砖头
        wall.py           # 制作墙体
        misc.py           # 其他不好归类的功能
        ...
    decoration/           # 子包decoration用于装修装饰过程
        __init__.py
        room.py           # 放间装修装饰
        clean.py          # 清洁
        ...
    doc/                  # 项目文档目录
    buildhouse.py         # 项目主程序，如果较复杂应继续分拆
    README.md             # 项目简介
```

- 在`construct`包下，对`brick`模块都使用`from .brick import (XX, YY, ZZ)`的形式，明确要import的变量、函数、类名称；
- 同时，在`__init__.py`中使用`from .brick import (XX, YY, ZZ)`、`from .wall import (AA, BB, CC)`等把这些**可以对外导出**的符号import一遍，这样`construct`包被`construct`包下模块或主程序`buildhouse.py`导入时，可以简化为`from ..construct import (XX, CC)`、`from construct import (AA, BB, CC, XX, YY, ZZ)`或`import construct`。
- 尽可能地减少在import语句使用 "*" 符号，实在无法避免时，为限制 "*" 符号带来的命名冲突，在`construct/__init__.py`、`decoration/__init__.py`文件中，定义`__all__`变量，明确限定允许被导出的所有符号。
- 主程序运行时，先切换到`projectname`目录下，再执行`python buildhouse.py`，或者直接`python path/to/projectname/buildhouse.py`



# 参考资料

1、ImportError:attempted relative import with no known parent package

https://blog.csdn.net/nigelyq/article/details/78930330

2、Python import搜索的路径顺序

https://blog.csdn.net/csdn912021874/article/details/83017425

3、

https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import