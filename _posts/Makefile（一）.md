---
title: Makefile（一）
date: 2018-04-12 20:49:02
tags:
	- Makefile

---



这个系列是我重新学习Makefile的记录。重点在把之前不清楚的概念理清。

# 发展历史

Makefile是一种用于构建和编译软件项目的工具，它的发展历史可以追溯到20世纪70年代。以下是Makefile的主要发展历史：

1. 1977年：Makefile的起源
   Makefile的概念最早由Stuart Feldman于1977年在贝尔实验室的第七版Unix操作系统中引入。它的目的是自动化代码编译和构建过程。Makefile通过定义规则和依赖关系来描述如何构建一个项目，以及如何在源代码发生更改时进行增量构建。

2. 1980年代：GNU Make
   在1980年代初，Richard Stallman创建了GNU项目，为了实现GNU软件的自动构建，他开发了GNU Make工具。GNU Make是Makefile语法的标准化实现，广泛用于GNU项目和许多其他开源项目。GNU Make引入了许多改进和扩展，使Makefile更加强大和灵活。

3. 1990年代：Makefile的广泛应用
   在1990年代，Makefile变得更加广泛应用于软件开发领域，不仅用于C和C++项目，还用于其他编程语言的项目。许多编程环境和集成开发工具（IDE）开始支持Makefile，使其更容易使用。

4. 2000年代：自动化工具的兴起
   随着时间的推移，自动化构建工具（如Apache Ant、Apache Maven、CMake等）在某些情况下开始取代传统的Makefile。这些工具提供了更多功能和更容易使用的配置方式，特别适用于复杂的项目。

5. 当代：Makefile的继续演进
   尽管有更多现代化的构建工具可供选择，但Makefile仍然在许多项目中得到广泛使用。它们特别适合小型项目和一些特定的应用场景。同时，Makefile仍在不断演进，社区继续开发新的工具和技术来改进Makefile的功能和性能。

总的来说，Makefile作为一种构建工具，经历了几十年的发展和演进，仍然在软件开发中发挥着重要的作用，并在不同的环境和项目中继续使用。

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

Makefile提供了一些内置变量，这些变量包含了有关Makefile执行环境的信息，可以在Makefile规则中使用。以下是一些常见的内置变量：

1. `CC`：C编译器的名称，默认是`cc`。你可以覆盖它以指定使用的特定编译器。

2. `CFLAGS`：C编译器的编译选项。你可以设置这个变量来包含编译选项，如优化级别、警告级别等。

3. `LDFLAGS`：链接器的选项。你可以在这里指定链接时需要的标志，如库路径和库文件。

4. `LDLIBS`：链接时需要的库文件。你可以在这里列出需要链接的库文件的名称。

5. `RM`：删除命令的名称，默认是`rm`。你可以在这里指定删除文件的命令。

6. `MAKE`：Make命令的名称，默认是`make`。这是Makefile自身的递归调用时使用的命令。

7. `SHELL`：Shell的名称，默认是`/bin/sh`。你可以更改Shell的名称，以便在规则的命令中使用不同的Shell。

8. `PWD`：当前工作目录的路径。这个变量包含Makefile执行时的当前目录。

9. `MAKEFILE_LIST`：包含当前Makefile以及所有被包含的Makefile的列表。

这些内置变量在Makefile中可以用于自定义构建规则，编译选项和其他任务。你可以根据项目的需要设置这些变量，以简化Makefile的维护和配置。

例如，你可以在Makefile中使用`CC`和`CFLAGS`来指定编译器和编译选项：

```make
CC = gcc
CFLAGS = -O2 -Wall

myprogram: main.c function1.c function2.c
    $(CC) $(CFLAGS) -o $@ $^
```

这里，`$(CC)`和`$(CFLAGS)`分别引用了`CC`和`CFLAGS`变量的值，用于设置编译器和编译选项。这使得Makefile更加灵活，可以轻松适应不同的编译需求。

### VPATH

`VPATH` 是一个特殊的Makefile变量，

==它用于指定Make命令在哪些目录中搜索依赖文件。==

`VPATH` 变量对于将源文件和依赖文件分布在不同目录的项目非常有用。

通常，Make会在当前目录中查找依赖文件，

但通过设置 `VPATH` 变量，你可以告诉Make去其他目录中查找依赖文件。

`VPATH` 变量可以包含一个或多个目录的路径，这些目录是Make用于查找依赖文件的候选目录。你可以将这些目录用冒号分隔开，就像环境变量 `PATH` 一样。

以下是一个示例 Makefile，其中使用 `VPATH` 变量：

```make
VPATH = src:include

myprogram: main.c function1.c function2.c
    gcc -o $@ $^

main.c: main.h
function1.c: function1.h
function2.c: function2.h

%.c: %.h
    @echo "$< has changed. Rebuilding $@."

.PHONY: clean
clean:
    rm myprogram
```

在这个示例中，`VPATH` 包含了 `src` 和 `include` 两个目录，

Make 会在这两个目录中查找依赖文件。

例如，`main.c` 和 `function1.c` 的依赖文件 `main.h` 和 `function1.h` 分别位于 `include` 目录中，但是 Make 仍然能够正确地找到它们。

==通过使用 `VPATH` 变量，你可以更灵活地组织项目的源代码和头文件，使 Make 能够自动查找依赖文件，而不需要在规则中指定完整的路径。这有助于简化 Makefile，并使其更易于维护。==

### MAKELEVEL

==`MAKELEVEL` 是一个内置变量，用于指示当前的Make命令递归调用的层级。==

当Make命令在一个Makefile中嵌套调用另一个Makefile时，`MAKELEVEL` 变量会告诉你当前的递归层级。它的值从0开始，表示最外层的Makefile，==每次递归调用时加1。==

这个变量对于了解Make命令的递归调用层级非常有用，可以用于控制某些操作或执行特定的命令，以适应递归调用的不同需求。例如，你可以使用 `MAKELEVEL` 变量来执行不同的操作或命令，具体取决于递归调用的层级。

以下是一个示例，演示如何在Makefile中使用 `MAKELEVEL` 变量：

```make
ifeq ($(MAKELEVEL),0)
# 当MAKELEVEL为0时执行的操作
all: myprogram

myprogram: main.c
    gcc -o myprogram main.c
else
# 当MAKELEVEL不为0时执行的操作
all:
    @echo "This is a recursive call at level $(MAKELEVEL)."
endif

.PHONY: clean
clean:
    rm myprogram
```

在这个示例中，当 `MAKELEVEL` 为0时，执行构建 `myprogram` 的操作，否则在递归调用时输出一个消息，指示当前的递归层级。这可以帮助你根据递归调用的层级执行不同的操作，从而实现更灵活的Makefile。

### MAKEFLAGS

`MAKEFLAGS` 是一个内置变量，==它包含了Make命令的选项和标志。==

这些选项和标志通常是从命令行传递给Make命令的，包括构建目标、Makefile 文件、并行执行选项等。

`MAKEFLAGS` 的值是一个字符串，它包含了从命令行传递给Make命令的选项和标志。你可以使用它来获取在Make命令启动时设置的选项，以便在Makefile中做一些特殊的操作或条件检查。

以下是一个示例，演示如何使用 `MAKEFLAGS` 变量：

```make
ifeq (,$(findstring --no-print-directory,$(MAKEFLAGS)))
# 如果命令行中未使用--no-print-directory选项
$(info Make is not running with --no-print-directory)
else
# 如果命令行中使用了--no-print-directory选项
$(info Make is running with --no-print-directory)
endif

all: myprogram

myprogram: main.c
    gcc -o myprogram main.c

.PHONY: clean
clean:
    rm myprogram
```

在这个示例中，通过检查 `MAKEFLAGS` 变量中是否包含 `--no-print-directory` 选项，你可以确定Make是否在不显示进入和退出子目录的信息时运行。这可以帮助你在Makefile中根据Make命令的选项执行不同的操作。

`MAKEFLAGS` 变量是一个有用的工具，可以用于根据命令行选项和标志的不同设置调整Makefile中的行为。

### SUFFIXES

`SUFFIXES` 是一个特殊的Makefile变量，

==它用于定义文件后缀（或扩展名）的规则。==

通过设置 `SUFFIXES` 变量，你可以告诉Make如何处理不同扩展名的文件，并建立它们之间的依赖关系。

这对于自定义构建规则非常有用，特别是当处理不常见的文件类型时。

`SUFFIXES` 变量通常包含一组文件后缀，用空格分隔开。例如：

```make
.SUFFIXES: .c .o .cpp .h
```

在上述示例中，`.SUFFIXES` 被设置为 `.c .o .cpp .h`，表示在Makefile中定义了文件后缀为 `.c`、`.o`、`.cpp` 和 `.h`。

通常，`.c` 对应C源文件，`.o` 对应目标文件，`.cpp` 对应C++源文件，`.h` 对应头文件。

==一旦设置了 `SUFFIXES`，你可以定义规则来处理这些后缀。==例如：

```make
.c.o:
    $(CC) $(CFLAGS) -c $< -o $@

.cpp.o:
    $(CXX) $(CXXFLAGS) -c $< -o $@
```

在这个示例中，定义了两个规则，第一个规则用于将 `.c` 文件编译成 `.o` 文件，第二个规则用于将 `.cpp` 文件编译成 `.o` 文件。 `$<` 代表依赖文件（源文件），`$@` 代表目标文件。

通过设置 `SUFFIXES` 和定义相关规则，你可以自定义处理不同文件类型的构建过程，使Makefile更具灵活性。这在处理多种文件类型的项目中尤为有用。

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

## 常用的处理函数

在Makefile中，你可以使用一些内置的函数来处理文本、字符串和文件路径等。这些函数可以帮助你在Makefile规则中执行各种操作。以下是一些常用的Makefile处理函数：

1. `$(wildcard pattern)`：查找匹配通配符模式的文件，并返回一个文件列表。例如，`$(wildcard *.c)` 可以用于查找当前目录下的所有C源文件。

2. `$(addprefix prefix, names)`：将指定的前缀添加到名称列表中的每个名称。例如，`$(addprefix obj_, file1 file2)` 可以将前缀"obj_"添加到每个文件名。

3. `$(addsuffix suffix, names)`：将指定的后缀添加到名称列表中的每个名称。例如，`$(addsuffix .o, file1 file2)` 可以将后缀".o"添加到每个文件名。

4. `$(subst from, to, text)`：将文本中的字符串 `from` 替换为字符串 `to`。例如，`$(subst old, new, This is old text.)` 将返回 "This is new text."

5. `$(patsubst pattern, replacement, text)`：使用通配符模式进行替换，将 `pattern` 匹配的部分替换为 `replacement`。例如，`$(patsubst %.c, %.o, file1.c file2.c)` 可以用于将C源文件的扩展名替换为目标文件的扩展名。

6. `$(notdir names)`：从文件路径中提取文件名部分，删除目录路径。例如，`$(notdir dir/file.c)` 返回 "file.c"。

7. `$(dir names)`：从文件路径中提取目录路径，删除文件名部分。例如，`$(dir dir/file.c)` 返回 "dir/"。

8. `$(basename names)`：从文件路径中提取不带扩展名的文件名部分。例如，`$(basename dir/file.c)` 返回 "dir/file"。

9. `$(shell command)`：执行shell命令并返回结果。这可用于执行外部命令，如获取文件列表或检查文件的存在性。

10. `$(foreach var, list, text)`：对列表中的每个元素执行一些操作，用于生成文本。例如，`$(foreach file, $(wildcard *.c), $(file:.c=.o))` 可以将C源文件列表转换为目标文件列表。

这些函数可以在Makefile中帮助你执行各种文本和路径操作，以自动化构建过程、生成文件列表、修改文件名等等。根据你的具体需求，你可以选择适当的函数来简化Makefile规则的编写。

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





`==eval` 函数是Makefile中的一个高级函数，==

==它用于动态生成Makefile规则和变量。==

通过 `eval` 函数，你可以在Makefile中执行任意的Makefile代码，使其具有更大的灵活性。

 `eval` 函数通常用于复杂的自动生成规则、条件语句、循环以及更高级的自定义构建过程。

`eval` 函数的基本语法如下：

```make
$(eval variable := value)
```

其中 `variable` 是你要定义或修改的Makefile变量的名称，而 `value` 是你要赋给该变量的值。这个值通常包含Makefile代码，用于生成规则或变量。

以下是一个示例，演示如何在Makefile中使用 `eval` 函数来动态生成规则：

```make
define generate_rule
$(1): $(2)
    @echo Building $$@
    gcc -o $$@ $(2)
endef

# 使用eval函数生成规则
$(eval $(call generate_rule, myprogram, main.c function1.c function2.c))
```

在这个示例中，`generate_rule` 是一个自定义的Makefile函数，它使用 `eval` 函数生成规则。然后，`$(call generate_rule, myprogram, main.c function1.c function2.c)` 调用该函数，生成一个构建 `myprogram` 的规则，该规则依赖于 `main.c function1.c function2.c`。通过 `eval` 函数，你可以根据不同的输入参数生成不同的规则。

`eval` 函数的强大之处在于，它允许你在Makefile中编写可重用的代码块，以根据需要生成不同的规则和变量，从而更容易处理复杂的构建要求。但要小心使用它，因为过度使用 `eval` 函数可能会导致Makefile难以理解和维护。



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

# VPATH变量和vpath指令

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

==这和上面提到的那个 VPATH 变量很类似，==

==但是它更为灵活。==

它可以指定不同的文件在不同的搜索目录中。

这是一个很灵活的功能。

## vpath指令

`vpath` 不是Makefile的关键字，而是一个Makefile指令，用于指定Make在哪些目录中查找文件依赖关系。`vpath` 指令非常有用，特别是在处理大型项目，需要将源文件和头文件分布在不同目录中时。

`vpath` 指令的基本语法如下：

```make
vpath pattern directories
```

- `pattern` 是一个通配符模式，用于匹配文件名或路径。
- `directories` 是一个包含目录路径的列表，用空格分隔。

`vpath` 指令告诉Make，在构建目标时，可以在 `directories` 中列出的目录中查找与 `pattern` 匹配的文件依赖。这意味着你可以将依赖文件放置在不同的目录中，而不需要在规则中指定完整的路径。

以下是一个示例，演示如何使用 `vpath` 指令：

```make
vpath %.c src
vpath %.h include

myprogram: main.c function1.c function2.c
    gcc -o $@ $^

main.c: main.h
function1.c: function1.h
function2.c: function2.h
```

在这个示例中，`vpath` 指令设置了文件匹配模式 `%.c` 和 `%.h`，并指定了相应的目录 `src` 和 `include`。

这意味着Make会在这些目录中查找 `.c` 文件和 `.h` 文件的依赖。虽然 `main.c`、`function1.c` 等文件没有包含完整的路径信息，但由于 `vpath` 指令的设置，Make仍然能够找到它们。

`vpath` 指令非常有用，可以帮助你更灵活地组织源文件和头文件，同时保持Makefile的可维护性。这在处理大型项目或跨多个目录的项目中尤为有用。

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

# 隐含规则

## 隐含规则有哪些

隐含规则（Implicit Rules）是Make工具内置的一组规则，用于自动推导和执行构建操作，而无需在Makefile中显式定义这些规则。

这些规则通常用于根据文件的扩展名或文件类型来推断如何编译或构建目标文件。

以下是一些常见的隐含规则及其用途：

1. **C/C++编译规则**：根据文件扩展名（如`.c`或`.cpp`）自动执行C或C++编译。例如，`main.c`将自动编译为`main.o`。

2. **汇编规则**：根据汇编文件的扩展名（如`.s`或`.asm`）自动执行汇编操作。

3. **目标文件生成规则**：根据`.o`文件的依赖关系自动构建可执行文件，库文件或其他目标文件。

4. **归档（Archive）规则**：自动创建静态库（`.a`文件）。

5. **链接规则**：根据可执行文件的依赖关系自动执行链接操作。

6. **Yacc和Lex规则**：自动执行Yacc和Lex文件的编译和生成。

7. **扩展名转换规则**：用于将一个文件扩展名转换为另一个扩展名，例如，从`.y`生成`.c`。

8. **文件复制规则**：复制文件，如从源代码目录到构建目录。

这些隐含规则使Make工具能够自动识别文件类型并执行相应的构建操作，从而减少了在Makefile中编写大量的规则的需求。如果你需要进一步自定义构建过程，可以在Makefile中显式定义自己的规则，覆盖或补充隐含规则。隐含规则的定义通常包含在Make工具的内部规则数据库中。

## 怎样禁用所有的隐含规则

要禁用所有的隐含规则，你可以在Makefile中设置一个特殊的变量 `.SUFFIXES` 为空，这将导致Make工具不再使用任何隐含规则。以下是如何在Makefile中禁用所有隐含规则的示例：

```make
.SUFFIXES:
```

==将 `.SUFFIXES` 设置为空即可禁用所有隐含规则。==

这会告诉Make工具不再关心文件扩展名，不会自动推断如何编译或构建文件。这对于完全控制构建过程，并避免隐含规则的干扰非常有用。

需要注意的是，禁用隐含规则后，你需要显式定义所有构建规则，包括编译、链接、汇编等操作。这可能会导致Makefile变得更加复杂，但也提供了更高的灵活性和控制权，尤其适用于复杂的项目。

# 查看make的递归嵌套层次

```
# 用于跟踪嵌套层数的变量
CURRENT_DEPTH := 0

# 递归目标
recursive_target:
	@$(eval CURRENT_DEPTH=$(shell echo $$(($(CURRENT_DEPTH) + 1))))
	@echo "当前嵌套层数为 $(CURRENT_DEPTH)"
	@$(MAKE) recursive_target_inner
	@$(eval CURRENT_DEPTH=$(shell echo $$(($(CURRENT_DEPTH) - 1))))
	@echo "当前嵌套层数为 $(CURRENT_DEPTH)"

recursive_target_inner:
	@echo "这是递归目标内部"
```



# 参考资料

1、

这篇文章很实用。

http://nuclear.mutantstargoat.com/articles/make/