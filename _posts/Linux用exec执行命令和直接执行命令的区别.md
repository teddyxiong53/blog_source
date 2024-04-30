---
title: Linux用exec执行命令和直接执行命令的区别
date: 2023-06-02 15:53:11
tags:
	- Linux
---

--

# exec和eval来执行命令，跟直接执行命令有什么区别

在Linux命令行中，`exec`和`eval`都是用来执行命令的工具，但它们的作用和用法有所不同。

1. `exec`命令是用来替换当前进程的shell，它会在当前shell进程中执行指定的命令，然后结束当前进程。这意味着一旦`exec`命令执行成功，当前shell进程将被新的进程替换，之后的任何命令都不会被执行。这种方式通常用于执行一些需要替换当前shell环境的命令，比如启动一个新的shell或者执行一个新的程序。

2. `eval`命令是用来将参数作为shell命令进行解释和执行。它会将参数作为一个shell脚本进行解释执行，所以可以用来动态执行一些命令或者表达式。`eval`命令通常用于处理一些需要动态生成命令的场景，比如通过变量来构造命令。

直接执行命令则是在当前shell环境中执行指定的命令，不会替换当前进程，也不会动态解释参数。它执行完命令后，控制权回到当前shell环境，继续执行后续的命令。

总的来说，`exec`用于替换当前shell环境，`eval`用于动态解释和执行参数，而直接执行命令则是在当前shell环境中执行指定的命令。

# exec举例说明

当涉及需要替换当前shell环境或者修改进程的输入输出时，`exec`命令可以派上用场。下面是一些例子：

1. **启动新的shell进程**：

```bash
#!/bin/bash
echo "Before exec"
exec bash  # 启动一个新的bash shell进程，替换当前的shell
echo "After exec"  # 这行命令不会执行，因为上一行的exec已经替换了当前进程
```

在这个例子中，`exec bash`替换了当前的shell进程，因此`echo "After exec"`这行命令不会执行。

2. **重定向标准输入/输出/错误**：

```bash
#!/bin/bash
exec > output.log  # 将标准输出重定向到output.log文件
echo "This will be written to output.log"
exec 2> error.log  # 将标准错误重定向到error.log文件
echo "This will be written to error.log" >&2
```

在这个例子中，`exec > output.log`将标准输出重定向到output.log文件，`exec 2> error.log`将标准错误重定向到error.log文件。

3. **替换当前进程的环境**：

```bash
#!/bin/bash
echo "Before exec, current directory is $(pwd)"
exec cd /tmp  # 切换当前工作目录到/tmp
echo "After exec, current directory is $(pwd)"  # 这行命令不会执行，因为上一行的exec已经替换了当前进程
```

在这个例子中，`exec cd /tmp`替换了当前进程的工作目录为`/tmp`，因此`echo "After exec, current directory is $(pwd)"`这行命令不会执行，而当前目录已经改变为`/tmp`。