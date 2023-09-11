---
title: systemV IPC介绍
date: 2023-07-29 10:58:12
tags:
	- ipc
---
--



# System V IPC 介绍

System V IPC（Inter-Process Communication）是一组用于进程间通信的API，是Unix-like系统中最早的进程间通信机制之一。System V IPC提供了三种进程间通信方式：共享内存（shared memory）、消息队列（message queue）和信号量（semaphore）。

共享内存是一种将内存区域映射到多个进程地址空间的机制，多个进程可以通过共享内存进行数据交换，从而达到高效的通信目的。

消息队列是一种通过消息传递的方式进行通信的机制，进程通过消息队列发送和接收消息，从而实现进程间通信。

信号量是一种计数器，它用于同步和互斥多个进程对共享资源的访问。多个进程可以使用信号量来协调对共享资源的访问，从而避免数据竞争和死锁等问题。

System V IPC提供了一组API，用于创建、访问和删除共享内存、消息队列和信号量等系统对象。这些API包括：

- `shmget`：用于创建或获取共享内存区域。
- `shmat`：用于将共享内存区域附加到进程的地址空间中。
- `shmdt`：用于将共享内存区域从进程的地址空间中分离。
- `shmctl`：用于控制共享内存区域的状态。
- `msgget`：用于创建或获取消息队列。
- `msgsnd`：用于向消息队列发送消息。
- `msgrcv`：用于从消息队列接收消息。
- `msgctl`：用于控制消息队列的状态。
- `semget`：用于创建或获取一个信号量集。
- `semop`：用于执行信号量操作。
- `semctl`：用于控制信号量集的状态。

由于System V IPC提供了高效的进程间通信机制，因此它在Unix-like系统中得到了广泛的应用，特别是在高性能计算、嵌入式系统和实时系统等领域。

# 发展历史

System V IPC（Inter-Process Communication）是Unix-like系统中最早的进程间通信机制之一，它的历史可以追溯到1980年代早期。下面是System V IPC的发展历史：

- 1983年，AT&T发布了System V操作系统，其中包含了一组新的进程间通信机制，即System V IPC。System V IPC包括了共享内存、消息队列和信号量等机制，这些机制被广泛应用于Unix-like系统中。
- 1984年，POSIX（Portable Operating System Interface）标准委员会成立，开始制定一个跨平台的操作系统接口标准。在POSIX标准中，System V IPC被作为标准的进程间通信机制之一，并得到了广泛的应用。
- 1990年代，随着计算机硬件和软件技术的不断发展，新的进程间通信机制得到了广泛的应用，例如网络套接字（socket）、Remote Procedure Call（RPC）和Distributed Computing Environment（DCE）等技术。这些技术提供了更加灵活和高效的进程间通信方式，逐渐取代了System V IPC成为主流的进程间通信机制。
- 目前，System V IPC仍然是Unix-like系统中常用的进程间通信机制之一，特别是在高性能计算、嵌入式系统和实时系统等领域。同时，由于System V IPC的接口和语义不够简洁和直观，一些新的进程间通信机制，如POSIX消息队列、文件映射和UNIX域套接字等，也逐渐得到了广泛的应用。