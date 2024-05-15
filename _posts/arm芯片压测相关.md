---
title: arm芯片压测相关
date: 2024-05-13 14:05:11
tags:
	- 芯片
---

--

# buildroot里的压测工具

在 Buildroot 中，除了 `stress-ng` 之外，还有一些其他的工具可以用于芯片压测。这些工具可以测试系统在不同方面的性能，例如 CPU、内存、IO 等。以下是一些常见的工具：

1. **`sysbench`**: 这是一个通用的跨平台性能测试工具，可以测试 CPU、内存、IO 和数据库等方面的性能。它可以模拟多种工作负载，包括 CPU 计算、内存操作、文件 IO 和数据库查询等。在 Buildroot 中，你可以使用 `sysbench` 进行综合性能测试。

2. **`fio`**: 这是一个专门用于测试磁盘性能的工具，可以模拟多种磁盘 IO 负载，包括顺序读写、随机读写、混合读写等。在 Buildroot 中，你可以使用 `fio` 测试系统的磁盘性能。

3. **`iperf`**: 这是一个用于测试网络性能的工具，可以测量网络带宽、延迟和数据包丢失率等指标。在 Buildroot 中，你可以使用 `iperf` 测试系统的网络性能。

4. **`memtester`**: 这是一个用于测试内存稳定性的工具，可以通过模拟内存压力来检测系统的内存是否存在问题。在 Buildroot 中，你可以使用 `memtester` 测试系统的内存稳定性。

这些工具可以通过 Buildroot 的包管理系统进行安装，你可以根据需要选择并安装相应的工具，然后使用它们来测试系统的性能。

# cpuburn-arm

这个是纯汇编的，2018年就不再维护了。

https://github.com/ssvb/cpuburn-arm

# stress

这个看起来维护也不积极了。有了新的stress-ng。

# stress-ng

`stress-ng` 是一个功能更加强大和灵活的压力测试工具，它可以测试系统的 CPU、内存、IO、磁盘等各个方面的性能。下面是一些常用的 `stress-ng` 用法示例：

1. **测试 CPU**:

```bash
stress-ng --cpu 4 --timeout 60s
```

这个命令将在系统上启动 4 个 CPU 负载线程，并持续运行 60 秒。

2. **测试内存**:

```bash
stress-ng --vm 2 --vm-bytes 1G --timeout 60s
```

这个命令将使用两个进程来进行内存测试，每个进程都会分配 1GB 的内存，并持续运行 60 秒。

3. **测试磁盘IO**:

```bash
stress-ng --io 4 --timeout 60s
```

这个命令将在系统上启动 4 个磁盘 IO 负载线程，并持续运行 60 秒。

4. **测试网络IO**:

```bash
stress-ng --sock 2 --timeout 60s
```

这个命令将在系统上启动 2 个网络 IO 负载线程，并持续运行 60 秒。

5. **混合测试**:

```bash
stress-ng --cpu 4 --vm 2 --vm-bytes 1G --io 4 --sock 2 --timeout 60s
```

这个命令将同时进行 CPU、内存、IO 和网络的压力测试，持续运行 60 秒。

你可以根据需要调整参数，比如 `--cpu` 后面的数字表示 CPU 负载的线程数，`--timeout` 后面的时间表示测试的持续时间。你还可以通过 `man stress-ng` 命令查看 `stress-ng` 的更多用法和选项。