---
title: windows之powershell
date: 2024-05-04 12:20:49
tags:
	- windows

---

--

[UNIX](https://zh.wikipedia.org/wiki/UNIX)系统一直有着功能强大的壳程序（[shell](https://zh.wikipedia.org/wiki/殼層)），

Windows PowerShell的诞生就是要提供功能相当于UNIX系统的命令行壳程序（例如：[sh](https://zh.wikipedia.org/wiki/Bourne_shell)、[bash](https://zh.wikipedia.org/wiki/Bash)或[csh](https://zh.wikipedia.org/wiki/C_Shell)），

同时也内置脚本语言以及辅助脚本程序的工具。

- 一致性的设计让所有工具和系统资料的使用语法、命名原则都相同。
- 脚本语言简单易学，而且能支持现有的脚本程序和命令行工具。
- 内含129种称为cmdlet的标准工具，可用来处理常见的系统管理工作。
- 具备完整的扩展，独立软件商或开发者都能很容易的自行扩展。
- 进程间数据传递内容具有强类型特征。
- PowerShell Core可以自动检测字符编码，自动识别Linux和Windows下的换行符，跨平台运行。





如果以前经常使用一些别的工具进行开发，

可能会有一些可执行文件、Perl脚本、批处理文件等，

如果不想放弃这些，可以使用PowerShell直接运行它们。



如果文件名字或路径中有空格，需要用（'）引号将命令扩起来，同时在前面加上符号（&），这种叫做调用操作：

要运行当前目录下的命令，而且命令名字或路径带有空格，需要同时加上符号（&）和（'）：



get-command获取所有的命令

若要查看一个命令的作用，可以使用Get-Help命令。

例子如下，还可以指定参数-Detailed、-Full、-Examples。

![image-20240504122738532](images/random_name/windows之powershell/image-20240504122738532.png)



由于PowerShell可以使用.NET Framework中的对象，

因此要想查看一个对象的属性和方法，

可以使用Get-Member命令。



有时候可能需要从批处理文件、定时任务或者其它非PowerShell程序调用PowerShell脚本，

语法：PowerShell “& ‘full path of the script’ arguments”。

如下例子是从CMD调用PowerShell。



PowerShell提供了两个变量可以检测最后执行的命令是否成功：$lastExitCode和$?。

$lastExitCode：数字型变量，返回最后脚本或应用程序执行返回的退出码或出错级别：



如果想计算一个命令执行时间，可以使用Measure-Command命令



PowerShell一些内置命令都有别名，方便记忆和输入，可以用Get-Help命令查看别名，如下Get-Children的命令有三个别名：gci、ls和dir，输入任意一个都可以列举当前目录。



如果想把得到的结果输出到文件中，可以使用Out-File命令或者重定向操作符将命令输出的结果保存在文件中：

我们可以使用 `Get-Alias` 命令来获取 PowerShell 内置的命令和别名对应关系表：



### 对象：PowerShell 的核心特征

如果你熟悉了 Unix 类系统下的终端相比，看到这里可能觉得 PowerShell 只是换了换语法。

然而，PowerShell 与 Bash 等环境有一个本质不同：**处理的不是「文本」则是「对象」。**

如果你对编程有一定了解，那么这种差异带来的优势无需多解释。

如果对这个概念比较陌生，可以认为 PowerShell 中输出的任何结果都是「一体多面」的，可以像魔方一样展示出更多侧面，或者灵活变形；

这为组合命令、过滤和处理命令输出结果带来了很大便利。

例如，一个最简单的命令

```code-line
echo "Hello World"
```

在 Bash 中只是打印出「Hello World」这串字符。如果想知道它的长度，或者做切割、查找替换等进一步处理，就必须依赖其他命令（或者依赖于 shell 所提供的特定语法）。

但在 PowerShell 下，同一行命令得到的就是一个字符串「对象」，它本身就记录了自己的长度，只要通过

```code-line
"Hello World".Length
```

# 参考资料

1、

https://www.cnblogs.com/lavender000/p/6935589.html

2、

https://sspai.com/prime/story/powershell-primer-01

3、

https://sspai.com/prime/story/powershell-primer-02