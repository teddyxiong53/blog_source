---
title: Makefile（一）
date: 2018-04-12 20:49:02
tags:
	- Makefile

---



这个系列是我重新学习Makefile的记录。重点在把之前不清楚的概念理清。



# 变量

Makefile里自带的变量分为3种：

1、环境变量。PATH这种。

2、内置变量。CURDIR这种。

3、自动变量。$>这种。

## 查看内置变量

Makefile这样写。

```
$(warning CURDIR=$(CURDIR) )
$(warning MAKEFILES=$(MAKEFILES) )
$(warning MAKEFILES_LIST=$(MAKEFILES_LIST) )
$(warning VPATH=$(VPATH) )
$(warning SHELL=$(SHELL) )
$(warning MAKESHELL=$(MAKESHELL) )
$(warning MAKE=$(MAKE) )
$(warning MAKELEVEL=$(MAKELEVEL) )
$(warning MAKEFLAGS=$(MAKEFLAGS) )
$(warning MAKECMDGOALS$(MAKECMDGOALS) )
$(warning SUFFIXES=$(SUFFIXES) )
```

输出：

```
teddy@teddy-ubuntu:~/work/test/make$ make
Makefile:6: CURDIR=/home/teddy/work/test/make 
Makefile:7: MAKEFILES= 
Makefile:8: MAKEFILES_LIST= 
Makefile:9: VPATH= 
Makefile:10: SHELL=/bin/sh 
Makefile:11: MAKESHELL= 
Makefile:12: MAKE=make 
Makefile:13: MAKELEVEL=0 
Makefile:14: MAKEFLAGS= 
Makefile:15: MAKECMDGOALS 
Makefile:16: SUFFIXES=.out .a .ln .o .c .cc .C .cpp .p .f .F .m .r .y .l .ym .yl .s .S .mod .sym .def .h .info .dvi .tex .texinfo .texi .txinfo .w .ch .web .sh .elc .el 
make: *** No targets.  Stop.
```

## 自动变量

在模式规则中，不能出现具体的文件名，否则模式规则就失去了意义。

这就需要借助自动变量来做。

自动变量的构成规则：

1、都是以$开头。

2、后面可以有的符号是：

```
7种基本的。
@
%
*
<
^
?
+
组合的，都是小括号加D和F。D代表目录。F代表文件。上面7种基本的跟括号和D组合，总共得到14种。
$(@D)
所以总共是21种。
7种基本的，14种组合。
```



```
$@
表示目标文件。
```

```
$%
只要当目标是一个静态库（.a）文件的时候，才有用。表示里面的o文件。
如果目标不是静态库文件，表示空的。
```

```
$*
在规则模式下，代表了目标模式里%所代表的部分。
对于构造相关文件名很有用。
```

```
$<
依赖文件名。
```

```
$^
规则所有依赖文件列表，用空格隔开。
如果目标是静态库文件，它代表的就是所有的o文件。
会自动去掉重复的项。
```

```
$+
跟$^类似，不同的在于会保留重复的项。这个特点在链接时交叉引用有用。
```

```
$?
所有比目标文件要新的依赖文件列表。
```

# 函数

## 文本处理函数

字符串替换。subst（这个就是一个完整单词了，没有缩写）。

```
$(subst :,$(space),$(PATH))
这个就是把PATH环境变量里的冒号替换为空格。space是自己定义的。
```



## eval函数

eval是一个比较特殊的函数。

使用它可以在Makefile里构造一个可变的依赖关系链。

函数eval对它的参数进行展开，展开的结果作为Makefile的一部分。

eval函数没有返回值。

eval函数在执行时，会对它的参数进行两次展开。

第一次展开：是由函数本身完成的。

第二次展开：是函数的结构作为Makefile的内容，被make解析展开。

理解这两次展开，对于学会使用eval非常重要。



# 一个最小且实用的Makefile

只有一个代码目录

```
src = $(wildcard *.c)
obj = $(src:.c=.o)

LDFLAGS = -lGL -lglut -lpng -lz -lm

myprog: $(obj)
    $(CC) -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
    rm -f $(obj) myprog
```

多个代码目录

```
csrc = $(wildcard src/*.c) \
       $(wildcard src/engine/*.c) \
       $(wildcard src/audio/*.c)
ccsrc = $(wildcard src/*.cc) \
        $(wildcard src/engine/*.cc) \
        $(wildcard src/audio/*.cc)
obj = $(csrc:.c=.o) $(ccsrc:.cc=.o)

LDFLAGS = -lGL -lglut -lpng -lz -lm

mygame: $(obj)
    $(CXX) -o $@ $^ $(LDFLAGS)
```



# 技巧

定义宏。和使用宏。

```
define mymacro
	@dir="$(1)"; ls $(1)/*
endef

all:
	$(call mymacro, "src")
```

foreach用法。

```
all:
	$(foreach s, "aa bb cc", echo $(s))
```





```
declare test='ywnz.com'    #定义并初始化shell变量
```

# VPATH变量和vpath关键字

在一些大的工程中，有大量的源文件，

我们通常的做法是把这许多的源文件分类，并存放在不同的目录中。

所以，当 make 需要去找寻文件的依赖关系时，你可以在文件前加上路径，



但最好的方法是把一个路径告诉 make，让 make 在自动去找。



Makefile 文件中的特殊变量 VPATH 就是完成这个功能的，

如果没有指明这个变量，make 只会在当前的目录中去找寻依赖文件和目标文件。

如果定义了这个变量，那么，make 就会在当前目录找不到的情况下，到所指定的目录中去找寻文件了。

```
VPATH = src:../headers
```



上面的定义指定两个目录，“src”和“../headers”，make 会按照这个顺序进行搜索。

目录由“冒号”分隔。（当然，当前目录永远是最高优先搜索的地方）



另一个设置文件搜索路径的方法是使用 make 的“vpath”关键字（注意，它是全小写的），

这不是变量，这是一个 make 的关键字，

这和上面提到的那个 VPATH 变量很类似，

但是它更为灵活。

它可以指定不同的文件在不同的搜索目录中。

这是一个很灵活的功能。



# 定义一个空格的方法

```
empty:=
space:= $(empty) $(empty)
```

```
merge=$(subst $(space),,$(1))
```



# 防止重复包含一个mk文件

```
ifneq ($(this_filname),1)
this_filename=1
...
endif
```

# origin函数

这个函数是作用是返回变量的定义的位置。

可能的返回值有：

```
undefined
default
environment
file
command line
override
automatic
```

# shell返回

它的作用跟反引号的是一样的。

# make的参数

```
-b,-m
	这2个参数是忽略跟其他版本的make的兼容性。
-B
	相当于完全重新构建。
-C
	切换到指定目录编译。
--debug=xx
	xx取值：
	a：all，所有调试信息。
	b：basic，基本调试信息。
	v：verbose。
	i：输出隐式规则。
	j：job，输出执行命令的详细信息。
	m：输出make过程中处理Makefile文件的过程。
-d
	等价于--debug=a
-e
	明确指定环境变量。
-f
	指定makefile的名字。
-i
	忽略执行中的所有错误。
-I
	搜索makefile的路径。
	
-j
	并发执行的个数。
-k
	keep-going。出错也不停止。
-l
	load，表示make执行的最大负载。
-n
	等价于--just-print，只是打印解析过程。
	
-p
	输出makefile中所有数据。包括所有的规则和变量。
-q
	不运行命令，也不输出。
	
```



# 参考资料

1、

这篇文章很实用。

http://nuclear.mutantstargoat.com/articles/make/