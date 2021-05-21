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



# 参考资料

1、

这篇文章很实用。

http://nuclear.mutantstargoat.com/articles/make/