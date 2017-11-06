---
title: rtt之finsh代码分析
date: 2017-11-06 21:15:53
tags:
	- rtt
	- finsh

---



rtt支持多种编译工具链。从简单角度考虑，我选择GNU工具的情况进行分析。

# 入口处

按照从外到内的顺序分析。

入口文件**shell.c和shell.h**。

shell.c里一个重要函数finsh_system_init，shell.h里一个重要结构体finsh_shell。

**finsh_system_init**

```
1、finsh_system_function_init
2、finsh_system_var_init
3、shell结构体全局变量初始化。
4、shell结构体的rx_sem初始化。
5、启动finsh_thread线程。
```

**finsh_shell**

```
1、接收的sem。
2、输入状态。分3种：等待正常键、等待特殊键、等待功能键。
3、回显模式。默认开的。
4、当前历史命令索引。
5、历史命令总数。
6、历史命令数组。
7、finsh_parser。用来解析c-style的命令的。
8、当前输入内容数组。
9、当前行尾的位置。
10、当前光标位置。
11、设备。
```

我们顺着上面的往下走。出现了2个新的东西，一个是finsh_thread，一个是finsh_parser结构体。

**finsh_thread**

```
1、finsh_init(&shell->parser);
2、while(1)
{
	1、等待字符输入。
	while(读到一个字符)
	{
    	//一个方向键，会产生连续3个键值。依次是0x1b 0x5b 0x41
    	finsh_run_line
	}
}
```

这里引出一个重要函数**finsh_init**。

finsh_init

```
1、finsh_parser_init
2、finsh_node_init
3、finsh_var_init
4、finsh_error_init
5、finsh_heap_init
上面这些初始化都很简单，就是memset。
```



**finsh_parser**在**finsh.h**里。

finsh_parser是c-style解析的入口结构体，非常重要。

finsh_parser内容简洁，就3个成员。

```
1、当前解析的字符串。
2、struct finsh_token token;
3、struct finsh_node *root;
```

从这里又引出2个重要结构体。都在finsh.h里。

**finsh_token**：

```
1、char eof
2、replay 从含义上看是回放的意思，用得较多。后面再分析用途。
3、position。
4、char current_token
5、一个union。value。可能是char、int、long类型。
6、string[128]
7、char *line。

```

**finsh_node**：

```
1、char node_type
2、char data_type
3、idtype
4、一个union。value。可能是char、short、int、long、void *
5、一个union。id。可能是finsh_var、finsh_sysvar、finsh_syscall
6、兄弟节点、子节点指针。

```

从上面又可以看到3个新的结构体**finsh_var、finsh_sysvar、finsh_syscall**。

finsh_sysvar、finsh_syscall是都在finsh.h里，内容简单，都差不多。finsh_var不一样。当我可以暂时忽略这个结构体。

# 简单总结 

到这里，我们涉及了2个重要头文件。shell.h和finsh.h。

shell.h：可以认为就是定义了finsh_shell结构体。

finsh.h：可以认为就是定义了finsh_parser结构体。



# 继续前进

前面我对finsh_thread_entry函数有所忽略。现在继续看里面的函数。

涉及到的主要函数有：

1、shell_handle_history

2、shell_auto_complete

3、shell_push_history

4、msh_exec：这个是msh的情况。

5、finsh_run_line：这个是c-style的情况。

现在就一个个分析这5个函数。

## shell_handle_history

以shell开头的函数都在shell.c里。

这个函数实际上就两行。但是值得分析。

```
    rt_kprintf("\033[2K\r");
    rt_kprintf("%s%s", FINSH_PROMPT, shell->line);
```

`"\033[2K\r"`这个表示了什么操作？

表示的是清空当前行的内容。这就是在你当前行已经输入了几个字符后，你按一下up键，自动把你的输入清空，然后把上一条命令的内容给你显示出来。

## shell_auto_complete

我们当前分析还是先集中在c-style的。

这个就是调用了list_prefix函数。这个函数较复杂，但是用途很明确。先不管。

## shell_push_history

不分析。

## finsh_run_line

函数内容：

```
1、finsh_parser_run
2、finsh_compiler_run
3、finsh_vm_run
```

先暂时学到这里。

