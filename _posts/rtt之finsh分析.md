---
title: rtt之finsh分析
date: 2017-11-06 20:21:04
tags:
	- rtt
	- finsh

---



RT-Thread的finsh模块是一个shell模块，是一个比较复杂的模块。本文是学习记录。

# 1、finsh模式

finsh支持的两种模式：

1、C语言解释器模式。称为c-style。使用时，函数必须带括号。

​	在这种模式下，可以解析执行大部分C语言的表达式。

​	而且可以用类似C语言的函数调用方式访问系统中的函数和全局变量。

​	也可以在命令行上创建变量。

​	这种方式，对于rtos是非常方便的，你可以直接在串口上改变全局变量的值。

2、传统命令行模式。称为msh。（module shell）

# 2、 finsh按键支持

1、支持方向键和退格键。

2、还不是很完善。不支持ctrl+c，不支持delete。



# 3、使用体验

为了有个大概的印象，我先不深入，先对shell进行一个实际使用。看看体验如何。

简单起见，就是用keil工具打开stm32f10x的工程。用模拟的方式运行。

我按一下tab键，就自动打印出了系统当前支持的命令的内容。

```

 \ | /
- RT -     Thread Operating System
 / | \     1.2.1 build Dec 29 2016
 2006 - 2013 Copyright by rt-thread team
finsh>>
finsh>>
--function:
hello_rtt        -- say hello to rtt
hr               -- say hello to rtt alias
led              -- set led[0 - 1] on[1] or off[0].
list_mem         -- list memory usage information
hello            -- say hello world
version          -- show RT-Thread version information
list_thread      -- list thread
list_sem         -- list semaphone in system
list_event       -- list event in system
list_mutex       -- list mutex in system
list_mailbox     -- list mail box in system
list_msgqueue    -- list message queue in system
list_mempool     -- list memory pool in system
list_timer       -- list timer in system
list_device      -- list device in system
list             -- list all symbol in system
--variable:
var              -- a test var
dummy            -- dummy variable for finsh
```



我们用hr这个命令试一下看看：

```

finsh>>
finsh>>hr()
hello, rtt 
        0, 0x00000000
finsh>>hr
        134218411, 0x080002ab

```

可以看到，如果不带括号。则不能正常使用命令。因为系统默认配置，只支持了c-style的命令。没有支持msh的。

我们看看hr这个命令的实现。

对应的代码在application.c里：

```
int var;
int hello_rtt(int a)
{
	rt_kprintf("hello, rtt \n");
	return 0;
}

FINSH_FUNCTION_EXPORT(hello_rtt, say hello to rtt);
FINSH_FUNCTION_EXPORT_ALIAS(hello_rtt, hr, say hello to rtt alias);
FINSH_VAR_EXPORT(var, finsh_type_int, a test var);

```



# 4、 增加命令和变量

## 4.1 c-style方式

1、用宏的方式进行增加。

```
#include <finsh.h>
FINSH_FUNCTION_EXPORT(name, desc)
FINSH_VAR_EXPORT(name, type, desc)
//还可以支持函数的别名，一般是在函数名很长的时候，取一个短名字。
FINSH_FUNCTION_EXPORT_ALIAS(name, alias, desc)
```

2、用函数的方式进行增加。

这个不细讲了。不怎么用。

##4.2 msh方式

msh方式只支持命令，不支持变量。添加只能用宏的方式来添加。

```
#include <finsh.h>
MSH_CMD_EXPORT(cmd, desc);
或者
FINSH_FUNCTION_EXPORT_ALIAS(name, alias, desc)
```

如果命令只想被msh解析，不要被c-style解析。那么就以`__`开头。这部分会被c-style过滤掉的。

# 5、内置命令

我们上面用tab联想处理的命令，就是finsh的内置命令。tab联想等价于list()的输出。

内置命令都很容易明白意思，不一一描述了。

rtt的其他组件会注册一些命令。例如打开dfs模块时，会增加如下命令：

```
mkfs
df 
ls
rm
cat 
copy
mdkir
```

msh的内置命令有：

```
RT-Thread shell commands:
list_timer       - list timer in system
list_device      - list device in system
version          - show RT-Thread version information
list_thread      - list thread
list_sem         - list semaphore in system
list_event       - list event in system
list_mutex       - list mutex in system
list_mailbox     - list mail box in system
list_msgqueue    - list message queue in system
ls               - List information about the FILEs.
cp               - Copy SOURCE to DEST.
mv               - Rename SOURCE to DEST.
cat              - Concatenate FILE(s)
rm               - Remove (unlink) the FILE(s).
cd               - Change the shell working directory.
pwd              - Print the name of the current working directory.
mkdir            - Create the DIRECTORY.
ps               - List threads in the system.
time             - Execute command with time.
free             - Show the memory usage in the system.
exit             - return to RT-Thread shell mode.
help             - RT-Thread shell help.
```



# 6、相关宏配置

默认是这样的。msh没打开。

```
/* SECTION: finsh, a C-Express shell */
#define RT_USING_FINSH
/* Using symbol table */
#define FINSH_USING_SYMTAB
#define FINSH_USING_DESCRIPTION
//#define FINSH_USING_MSH

```

如果打开了`FINSH_USING_MSH`而没有打开`FINSH_USING_MSH_ONLY`，finsh同时支持两种c-style模式与msh模式，但是默认进入c-style模式，执行 `msh()`即可切换到msh模式，在msh模式下执行 `exit`后即退回到c-style模式。



