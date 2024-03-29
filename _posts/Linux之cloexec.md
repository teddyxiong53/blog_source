---
title: Linux之cloexec
date: 2019-01-10 14:17:51
tags:
	- Linux
---

--

什么是cloexec？

是close on execute的缩写。

应对的是这样的场景：

==在exec启动新进程后，子进程仍然可以操作父进程里的fd。==

==很多时候，我们不希望这样。==

所以就希望在exec的时候，子进程关闭掉这些fd。

要达到目的，有两种方法：

1、O_CLOEXEC。在open的时候，就传入这个标志。这个是Linux2.6之后才执行的。

2、F_CLOEXEC。专门用fcntl函数来给fd进行操作。



`O_CLOEXEC` 是文件描述符标志（File Descriptor Flag），用于在打开文件时控制文件描述符的关闭行为。

这个标志通常与 `open` 系统调用一起使用。

当你使用 `O_CLOEXEC` 标志来打开文件时，

表示你要求在子进程中关闭这个文件描述符，

以确保不会出现资源泄漏的问题。

这对于编写多进程或多线程的应用程序非常有用，

因为它可以避免在不需要的情况下继承不必要的文件描述符。

使用 `O_CLOEXEC` 标志的 `open` 调用如下：

```c
int fd = open("example.txt", O_RDONLY | O_CLOEXEC);
```

在这个示例中，打开文件 "example.txt" 并使用 `O_CLOEXEC` 标志来创建文件描述符 `fd`。

当 `fd` 被用于创建子进程时，子进程将自动关闭这个文件描述符，以防止资源泄漏。

需要注意的是，==`O_CLOEXEC` 标志的行为仅在使用 `exec` 系列系统调用创建新进程时才会生效，这是因为在 `exec` 过程中会关闭所有文件描述符。==

在其他情况下（如 `fork` 创建子进程），文件描述符不会自动关闭。

因此，`O_CLOEXEC` 主要用于确保在执行 `exec` 后不再需要的文件描述符会被关闭。



