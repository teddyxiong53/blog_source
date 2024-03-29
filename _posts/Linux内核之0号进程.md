---
title: Linux内核之0号进程
date: 2019-12-05 09:47:28
tags:
	- Linux
---

--

Linux 里有3个特殊的进程：

idle进程（pid=0）

init进程（pid=1）

kthreadd（pid=2）

# idle进程

idle进程又系统自动创建，运行在内核态。

idle进程是唯一一个没有通过fork或者kthread创建的进程。

完成系统加载后，变成进程调度、交换。



0号进程的前世是init_task，今生是idle。



在smp系统上，每个核心有独立的运行队列。每个运行队列上有一个idle进程。



init_task是内核中所有的进程、线程的task_struct的雏形。

# Linux的0号进程介绍

在 Linux 内核中，0 号进程（PID 0）是一个特殊的进程，也称为"swapper" 或 "idle" 进程。

它在系统引导时由内核创建，具有以下特点：

1. **初始进程**：0 号进程是系统中的第一个用户态进程，其 PID 为 0。它是系统中第一个在用户空间运行的进程，通常会在内核启动时自动创建。这个进程不对应任何实际的可执行程序。

2. **空闲进程**：0 号进程通常被视为"空闲进程"，因为它没有实际的工作任务，仅用于在没有其他进程可执行时运行。

3. **切换到用户态**：0 号进程在内核启动期间负责完成从内核态到用户态的切换。一旦内核初始化完成，0 号进程会切换到用户态，而内核将继续运行其他用户空间进程。

4. **死循环**：一旦 0 号进程切换到用户态，它会进入一个无限循环，等待执行任何其他用户进程。当系统中没有其他用户进程运行时，0 号进程就会在空闲状态下循环运行。

5. **系统空闲时间**：**0 号进程的主要作用之一是测量系统的空闲时间。**内核可以使用 0 号进程来跟踪系统空闲时间，以便在某些情况下执行节电操作或其他管理任务。

6. **PID 0 的特殊性**：在 Linux 中，0 号进程具有特殊的意义，因为它是第一个用户态进程，但也因为其特殊性，不能被终止或杀死。它只会在系统关闭时才会被结束。

总之，0 号进程是 Linux 内核启动时创建的一个特殊进程，主要负责完成内核到用户态的切换，等待其他用户进程的执行。它在测量系统空闲时间和保持系统运行方面具有重要作用。这个进程的存在确保了系统可以在引导后切换到用户态并接受用户任务的执行。

# 参考资料

1、linux的 0号进程 和 1 号进程

https://www.cnblogs.com/alantu2018/p/8526970.html