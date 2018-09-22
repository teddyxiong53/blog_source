---
title: Makefile经验
date: 2017-02-22 23:16:30
tags:
	- Makefile
---
# 1. 创建文件夹或者删除文件夹的函数
```
CreateDir = $(shell [ -d $1 ] || mkdir -p $1 || echo "$1 exists")
RemoveDir = $(shell [ -d $1 ] && rm -rf $1 || echo "rm $1 failed ")

dummy := $(call CreateDir, $(DIR1_NAME))
dummy += $(call CreateDir, $(DIR2_NAME))
```

# 2. 编译加快速度 

make的时候带-j选项，例如`make -j128`。-j后面的数字，取多少，取决于你的电脑的cpu核心数量。如果不知道可以这样`make -j$(nproc)`。或者指定多一些，也没有关系。

# 3. Makefile的执行步骤

1. 读入所有的Makefile。
2. 读入被include的其他Makefile。
3. 初始化文件中的变量。
4. 推导隐含规则，并分析所有规则。
5. 为所有的目标文件创建依赖关系链。
6. 根据依赖关系，决定哪些目标需要重新生成。
7. 执行命令。

1到5步为第一阶段，6到7步为第二阶段。

在第一阶段，如果变量被使用了，那么make就会把它展开在使用的位置，但是不会完全展开，会延迟展开。

# 4. 文件查找

在大的工程里，源文件很多，我们一般是把这些源文件放在不同的目录下，当make需要去找文件的依赖关系的时候，

可以用vpath关键字。

# 5. 多目标

多个目标，它们依赖的文件都是一样的，而且生成的命令大体一样，我们就可以把它们合并起来。

这里可利用$@这个自动化变量了。

# 6. 静态模式

静态模式可以更容易地定义多目标的规则，可以让我们的规则变得更加有弹性和灵活。

语法规则是：

```
targets: target pattern: prereq patterns
	command
```

举一个常用的例子就是：

```
objs := foo.o bar.o
$(objs): %.o :%.c
	$(CC) -c $(CFLAGS) $< -o $@
```

# 7. 自动生成依赖

在实际项目中，文件的依赖关系是非常多的，不可能一个个地去写。

我们先看一个简单例子。

一个只包含了stdio.h的test.c文件。它的依赖关系是这样的。

```
teddy@teddy-ubuntu:~/test/make$ gcc -M test.c  
test.o: test.c /usr/include/stdc-predef.h /usr/include/stdio.h \
 /usr/include/features.h /usr/include/i386-linux-gnu/sys/cdefs.h \
 /usr/include/i386-linux-gnu/bits/wordsize.h \
 /usr/include/i386-linux-gnu/gnu/stubs.h \
 /usr/include/i386-linux-gnu/gnu/stubs-32.h \
 /usr/lib/gcc/i686-linux-gnu/5/include/stddef.h \
 /usr/include/i386-linux-gnu/bits/types.h \
 /usr/include/i386-linux-gnu/bits/typesizes.h /usr/include/libio.h \
 /usr/include/_G_config.h /usr/include/wchar.h \
 /usr/lib/gcc/i686-linux-gnu/5/include/stdarg.h \
 /usr/include/i386-linux-gnu/bits/stdio_lim.h \
 /usr/include/i386-linux-gnu/bits/sys_errlist.h
```

如果排除掉系统头文件，则是这样的：

```
teddy@teddy-ubuntu:~/test/make$ gcc -MM test.c 
test.o: test.c
```

可见编译器的这个功能可以为我们生成依赖关系，我们如何用起来呢？

一般我们会把这个结果输出到后缀名为.d的文件中，叫做依赖文件。

一般的写法是这样的：

```
%.d :%.c
	@set -e; rm -f $@; \
	gcc -M $(CPPFLAGS) $< > $@.$$$$;\
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$
```

`$$$$`这个得到的是进程号，是为了保证名字的唯一性和临时性。

sed这一行的目标是把：

```
test.o: test.c test.h
```

转换成：

```
test.o test.d : test.c test.h
```

接下来我们要做的就是把这些自动生成的规则放入到我们的主Makefile里。例如这样：

```
SRCS = foo.c bar.c
include $(SRCS:.c=.d)
```

# 8. 嵌套执行Makefile

假如我们有一个子目录subdir，里面有个Makefile。我们可以这样执行：

```
subsystem:
	cd subdir && make
```

等价于：

```
subsystem:
	make -C subdir
```

我们把这个Makefile叫总控Makefile，总控Makefile的变量可以传递到下级的Makefile中，但是不会覆盖下层Makefile里定义的变量。除非指定了`-e`参数。

如果你想要把变量传递给下级的Makefile，那么在总控Makefile里加上：

```
export VAR_NAME
```

如果你要把所有的变量传递到下层，那么只要写一个export，后面什么都不跟，就可以了。

有两个变量是一定会传递到下层Makefile的，无法控制的。一个是SHELL，一个是MAKEFLAGS。

这2个是系统级的变量。

# 9. 定义命令宏

看例子：

```
define myfunc
echo "xxx"
echo "yyy"
endef
```

使用就是这样：

```
all:
	$(myfunc)
```

# 10. 变量的注意事项

MAKELEVEL这个变量，是在哪个目录执行make，改目录的MAKELEVEL就是0，切一次目录，MAKELEVEL的值就加1 。

可以这样用：

```
ifeq ($(MAKELEVEL),0)
$(warnig compile in current dir)
endif
```

下面看变量的高级用法。

## 10.1 变量值的替换

语法格式是：`OBJS:= $(SRCS:%.c=%.o)`。



# 11. make的运行

make命令有3个退出码，分别是0、1、2。

0代表成功。

1代表任意的错误。

2代表用`make -q`来查询是否需要更新，而实际没有任意文件需要更新时，返回2 。



# 12. Makefile的调试

```
make -n
等价于
make --just-print
只是打印语句，不会真的执行。
```

```
make --debug=level
level可能的取值有：
a：表示all。
b：把basic的信息。
i：把隐含规则输出来看。
v：verbose信息。
```



# 其他

@D @F的用途是什么？

目标的目录和目标的文件名。

