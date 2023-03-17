---
title: scons（一）
date: 2018-01-24 16:56:20
tags:
	- scons

---



因为rt-thread里用了这个工具，为了方便调试，把这个构建工具学习一下。

# 1. scons简介

开源的用Python编写的构建工具。

与make相比，有哪些优势？

1、用Python脚本作为配置文件。

2、对于C和C++，默认就支持进行依赖关系分析。

3、跨平台。

# 2. HelloWorld

新建一个目录，scons-test。下面放hello.c和SConstruct这2个文件。

SConstruct文件里就一行：

```
Program('hello.c')
```

然后执行scons命令，就会进行编译。

Program的位置上可以出现的词：

Program：表示编译出一个可执行程序。

Object：表示编译出一个o文件。

清除：

```
scons -c
```

SConstruct的内容是Python脚本。Program是一个类。

但是跟普通的Python脚本还是不同。

它的行为上类似Makefile。调用顺序。

指定输出文件的名字：

```
Program('hello_exe', "hello.c")
```

编译多个c文件：

```
Program('hello_exe', ['hello.c', 'f1.c', 'f2.c'])
```

用Glob来通配C文件：

```
Program('hello_exe', Glob('*.c'))
```

每个文件名都用引号括起来，比较麻烦。可以这样：

```
src_files = Split("f1.c f2.c")
Program('hello_exe', src_files)
```

其实，可以把参数的名字也带上，这样清晰一点：

```
Program(target = 'hello_exe', source=src_files)
```

上面讨论的都是编译了一个程序的，其实编译多少个都无所谓的。

```
Program('hello1', 'hello1.c')
Program('hello2', 'hello2.c')
```



# 3.编译库

为了方便后面的测试，新建4个文件：

```
$ touch f1.c f2.c f3.c f4.c
$ echo "void f1() {printf(\"%s\\n\", __func__);}" > f1.c
$ echo "void f2() {printf(\"%s\\n\", __func__);}" > f2.c
$ echo "void f3() {printf(\"%s\\n\", __func__);}" > f3.c
$ echo "void f4() {printf(\"%s\\n\", __func__);}" > f4.c
```

新建main.c：

```
void main()
{
    f1();
    f2();
    f3();
    f4();
}
```



SConstruct文件：

```
src_files = Glob("f*.c")
Library("foo", src_files)
```

可以明确指定静态库或者动态库：

StaticLibrary或者SharedLibrary。

链接库：

```
src_files = Glob("*.c")
Library("foo", src_files)
Program("hello", "main.c", LIBS=['foo'], LIBPATH=".")
```







# 4.SConstruct和SConscript关系

SConstruct是主要文件。SConscript相当于函数一样的功能，里面最后面会返回一些对象。

在前面的基础上，继续扩展。增加一个子目录d1，下面放一个d1f1.c的文件。

```
teddy@teddy-ubuntu:~/work/test/scons-test$ mkdir d1
teddy@teddy-ubuntu:~/work/test/scons-test$ cd d1
teddy@teddy-ubuntu:~/work/test/scons-test/d1$ touch d1f1.c
teddy@teddy-ubuntu:~/work/test/scons-test/d1$ echo "void d1f1() {printf(\"%s\\n\", __func__);}" > d1f1.c
teddy@teddy-ubuntu:~/work/test/scons-test/d1$ 
```

现在目录结构是：

```
teddy@teddy-ubuntu:~/work/test/scons-test$ tree
.
├── d1
│   ├── d1f1.c
│   └── SConscript
├── f1.c
├── f2.c
├── f3.c
├── f4.c
├── main.c
└── SConstruct
```

SConstruct内容：

```
src_files = Glob("*.c")
subobj = SConscript(['d1/SConscript'])
obj = subobj + Object(src_files )
Program("hello", list(obj))
```

SConscript内容：

````
obj = Object(Glob("*.c"))
Return("obj")
````



# 5.env 

环境变量用于设置编译过程中用到的各种参数。

把下面的代码加入到SConstruct里，可以打印出来看看。

```
env = Environment()
dict = env.Dictionary()
keys = dict.keys()
keys.sort()
for key in keys:
    print "key: %s, value:%s" % (key, dict[key])
```







SourceSignatures("MD5")

SourceSignatures("timestamp")



Depends(hello, 'some file')：明确指定依赖关系。



Import函数。引入变量用的。

```
Import("env")
```

跟Export对应。这个是导出变量的。



File和Dir的用法

```
import pdb
import SCons
#pdb.set_trace()

env = Environment(CC="gcc",     CCFLAGS="-g")
#env.Program("foo.c")

print Dir(".").path
print Dir(".").abspath
print Dir("#").path
print Dir("#.").path
print File("foo.c").srcnode().path
```

输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/scons$ scons -Q
/home/hlxiong/work/test/scons
/home/hlxiong/work/test/scons
/home/hlxiong/work/test/scons
/home/hlxiong/work/test/scons
foo.c
scons: `.' is up to date.
```

Dir('#')表示源代码的顶层目录。



添加自定义选项。

```
import pdb
import SCons
#pdb.set_trace()

env = Environment(CC="gcc",     CCFLAGS="-g")
#env.Program("foo.c")

AddOption("--copy", dest="copy", action="store_true", 
		default=False,
		help="copy rt-thread dir to local"
	)
print GetOption("copy")
```

你可以这样查看这个添加的内容。

```
scons --help
```

```
Local Options:
  --copy                      copy rt-thread dir to local
```

执行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/scons$ scons --copy -Q
True
scons: `.' is up to date.
```

# 重新学习

现在我对scons的定位变为：自己做开源项目的主要构建工具。

所以对相关的知识点，都要研究透彻。

以awtk的为参考。

尽量不引入面向对象的用法。直接写最简单直观的python脚本。

scons是一个Python写的自动化构建工具，

就比如老牌的cmake，

或者如果经常跟google一些[开源项目](https://so.csdn.net/so/search?q=开源项目&spm=1001.2101.3001.7020)打交道的话，

那肯定知道新近开始流行的gyp（google内部用的构建工具），

scons实现跟它们有类似的功能。

而scons又有区别于其他构建工具的特点，不得不承认，这些特点让我喜欢上了这个工具。

先简单总结下吸引我的几点：

\1. 自动依赖分析

\2. 工具本身由python实现，跨平台

\3. **基于MD5识别构建文件的改变**，并且可以自定义和扩展

\4. 构建文件逻辑用python来写，功能强大，扩展性超强，跨平台

\5. 简单易用（半小时内可以学会如何构建中小规模编译环境）

\6. 官方提供的文档详细易理解（如果看过google的gyp的文档，那叫一个坑爹）



写一个SConstruct文件。

把多个c文件编译成可执行文件

```
Program([Glob('*.c'), Glob('ext/*.c')])
```

生成动态库文件

```
SharedLibrary('ext/extScons.c')
Program(['helloScons.c'], LIBS=['extScons'], LIBPATH='./ext')
```

解释一下，

SharedLibrary()指定把ext/extScons.c编译成动态链接库，

如果想编译为静态链接库则使用StaticLibrary()。

Program方法中，

LIBS指定的是主程序helloScons.c需要使用的动态链接库libextScons.so，

LIBPATH则指定的是libextScons.so的路径。

运行scons后，可以看到ext文件夹下生成了libextScons.so，

主文件夹下生成了可执行程序helloScons。



如果要把编译和链接两个步骤分开呢？没问题，scons提供了Object方法来编译生成.o(windows下为.obj)文件。

```
import os
Object('ext/extScons.c')
Library('ext/extScons.o')
Object('helloScons.c')
Program(['helloScons.o'], LIBS=['extScons'], LIBPATH='./ext')
```



# 相关概念

## 三种环境

scons三种环境变量：

1. 外部环境（External Environment）变量，执行scons命令的shell环境中的变量，可以使用os.environ（一个外部环境变量字典）来获取。
2. 构建环境（Construction Environment）变量，构建环境在scons中表现为Environment对象，在scons中，可以很方便的创建或克隆出不同的构建环境，构建环境变量主要是一些编译过程中用到的配置选项`（$CPPPATH、$CPPFLAGS、$CPPDEFINES等）。可以使用Environment对象访问，例如env[‘CPPPATH’]。`
3. 执行环境（Execution Environment）变量，执行构建命令的环境中的变量，scons的执行环境和外部环境是隔离开的，从而确保不会因为外部环境的一些错误配置发生不好追踪的错误，最大限度保证正确性。（makefile中外部环境会影响执行环境）可以`使用env[‘ENV’]访问，例如env[‘ENV’][‘PATH’]。`

## **SCons环境**

当SCons开始构建工程，它会创建一个自己的环境，

这个环境包括工程依赖关系树，帮助函数，创建者和一些其他的工具。

这个环境一部分在内存中创建，

另外一些存储到磁盘以便下次构建时加速。

这个是SCons的环境，不同于使用Makefile的用户理解的系统环境。



## **系统环境**

是一个类似操作系统的环境容器，

包括PATH,HOME等变量。

通常可以通过os.environ在Python中获取，

因此在SCons也是如此。

SCons没有隐式导入任何系统环境设置(例如编译器选项，工具路径等)，

因为它被设计为行为可预见的跨平台工具。

这也是为什么如果依赖一些系统环境变量，你必须自己通过SCons脚本隐式获取。

## SConstruct

是SCons执行的主脚本名，处理即从它开始。

## **SConscript**

也是SCons执行的脚本，

只不过是放到工程的子目录。

这些文件主要是为了进行分层级的编译，通过放在工程根目录的SConstruct包含。

## **Builder**

是一个SCons对象，

你可以显式调用它在一系列源文件中指定编译依赖目标。

**SCons的威力是依赖关系会自动的被跟踪，**

当源文件更改后，系统会自动探测哪些目标需要重新构建。

## **SCanner**

另外一个SCons对象。

它可以扫描额外依赖的源文件，这些依赖的文件不会被作为Builder的源文件编译。

## **Tool**

是任何扩展Builders，Scanners，和其他有助于SCons环境的外部组件，

SCons通过扫描一些目标位置来寻找工具，这些工具可以是工程特定，也可以通过自己安装来扩展核心功能的。

# 常用函数

## 

#### Import()、Export()函数

Import(vars)

导入其它脚本定义的变量

‘vars’变量名，变量名是字符串，可以是一个变量或一个变量列表

Export(vars)

导出变量，供其它脚本使用

‘vars’变量名，变量名是字符串，可以是一个变量或一个变量列表

#### SConscript()函数

SConscript(scripts, [exports, variant_dir, duplicate])

读取一个或多个sconscript脚本，返回一个node列表，node是指一个编译对象

‘scripts’：指定要加载的sconscript脚本名称与路径

‘exports’：可选参数，导出一个变量，此变量比一般Export()导出的变量有更高优先权

‘variant_dir’：可选参数，指定一个目录，编译动作都在该目录中进行，不影响源码路径

‘duplicate’：可选参数，指定编译目录中是否拷贝源码

#### PresentDir()函数

PresentDir()

获取当前脚本所在路径

#### Glob()函数

Glob(pattern)

返回满足pattern指定条件的Node(编译对象)

‘pattern’：指定匹配条件，支持unix shell的通配符替换。支持当前脚本所在路径进行相对路径索引

#### IsDefined()函数

IsDefined(depend)

判断依赖的宏或宏列表是否被定义，被定义返回True，如果存在未被定义的宏返回False

‘depend’：指定依赖的宏，或宏列表

#### DeleteSrcFile()函数

DeleteSrcFile(src, remove)

将指定的文件从编译列表中移除

‘src’：编译node列表

‘remove’：指定被移除的文件

#### AddCodeGroup()函数

AddCodeGroup(name, src, depend, **parameters)

将编译对象添加到一个代码组中进行编译管理，返回编译对象列表

‘name’：指定代码组名称，如果该名称已经存在，则将添加到已经存在的组中。在keil工程中以该名称呈现一个工作组

‘src’：指定要被添加的编译对象列表

‘depend’：关键字参数，指定创建该组依赖的宏，如果条件宏不满足，则直接返回空列表

‘parameters’：可变关键字参数，指定相应的编译行为，支持的关键字如下：

CPPPATH指定头文件路径，对应gcc的-I

CCFLAGS对应gcc的--include选项

CPPDEFINES定义编译宏，对应gcc的-D

LINKFLAGS定义链接选项

LOCAL_CPPPATH

定义仅对当前组有效的头文件路径选项

# 文件过期的判定方式

scons判断文件过期的方式：

- Decider(‘MD5’)，使用md5比较，优点是比较准确，缺点速度慢，适用于规模较小的项目。
- Decider(‘timestamp-newer’)，使用timestamp比较，优点是速度快，缺点是可能不准确，适用于规模较大的项目。
- Decider(‘MD5-timestamp’)，使用md5和timestamp比较，先使用timestamp检测出疑似过期的文件，然后使用md5进行比较，是上面两种方案的折中。
- 自定义Decider的方式。

# 设置构建目录

使用VariantDir和SConscript设置构建目录：

- 默认的情况下，scons会把编译的结果直接放在源码目录，也就是构建目录就是源码目录。
- 使用VariantDir指定的构建目录只对SConscript所在目录之下的目录有效。
- SConscript中的相对路径是相对于SConscript所在目录的，在设置VariantDir之后，相对路径自动变为相对于VariantDir，所以在SConscript中配置的源代码文件的路径最好是相对路径，这样VariantDir如果变更，不用修改SConscript。

# 源代码分析

从setup.cfg看起。

入口函数是：

```
[options.entry_points]
console_scripts =
    scons = SCons.Script.Main:main
```

SConsOptions.py，文件1000行左右。

这个进行scons命令的选项的解析。

```
有这些类：
SConsValues
SConsOption
SConsOptionGroup
SConsBadOptionError
SConsOptionParser 继承自optparse这个库，但是这个已经过时了，argparse是推荐的。
一个方法：
def Parser
```



​                    

SCons.Node.FS

这个代表了什么？

FS是文件系统的意思。

Node包含了哪些情况？

在内部，SCons 将它所知道的所有文件和目录表示为节点。这些内部对象（不是对象文件）可以以多种方式使用，使您的 SConscript 文件可移植且易于阅读。



SCons.SConf

这个代表了什么？

SCons.Script

# 参考资料

1、scons使用

https://www.cnblogs.com/blueoverflow/p/4913766.html

2、官方手册

https://scons.org/doc/production/HTML/scons-man.html

3、

https://blog.csdn.net/danshiming/article/details/122771064

4、SCons基本概念

http://billowqiu.github.io/2012/07/08/scons%E6%A6%82%E8%A7%88/

5、scons脚本编写

https://os.iot.10086.cn/doc/oneos_cube/scons_script.html

6、SCons常用语法

https://os.iot.10086.cn/doc/oneos_cube/scons_func.html

7、scons学习笔记

https://zhoubo888.com/2020/08/27/scons%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/

8、官方手册

https://scons.org/doc/production/HTML/scons-user.html