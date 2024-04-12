---
title: Linux之flock命令
date: 2024-04-07 11:13:17
tags:
	- Linux

---

--

`flock` 是一个命令行工具，用于在 Shell 脚本中对文件进行加锁，以确保只有一个进程可以访问该文件。它的基本用法如下：

```
flock [OPTION] LOCKFILE COMMAND
```

其中，`LOCKFILE` 是用来指定锁定文件的路径，`COMMAND` 是需要加锁的命令或者脚本。`flock` 命令会尝试获取 `LOCKFILE` 上的排他锁，如果获取成功，则执行 `COMMAND`，执行完后释放锁；如果获取失败，则会一直等待直到获取到锁为止。

以下是一些常用的选项：

- `-n`：非阻塞模式，如果无法获取锁，则立即返回，而不是等待。
- `-x`：排他锁模式，其他进程无法同时获得相同的锁。
- `-s`：共享锁模式，其他进程可以获取相同的锁。

下面是一个示例，演示了如何使用 `flock` 来确保只有一个进程可以访问某个文件：

```bash
#!/bin/bash

# 指定锁文件路径
LOCKFILE="/tmp/my_lock_file.lock"

# 使用 flock 加锁，并执行命令
flock -x "$LOCKFILE" \
    echo "This command is protected by flock and can only be executed by one process at a time."
```

在这个示例中，`flock` 命令尝试获取名为 `/tmp/my_lock_file.lock` 的排他锁，然后执行 `echo` 命令。如果多个进程同时运行这个脚本，只有一个进程能够成功获取锁，其他进程会等待直到锁被释放。