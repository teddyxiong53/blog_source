---
title: Linux之tmpfs的shm
date: 2018-03-07 13:36:33
tags:
	- Linux

---



# 跟ramdisk比较

/dev/shm跟ramdisk不同。shm是一个tmpfs。

而ramdisk是一个块设备，对于的设备是/dev/ram0这样的。你需要把mkfs /dev/ram0才能用。



# tmpfs的优点

1、动态文件系统的大小。

2、速度快。



# 修改shm大小

默认是内存大小的一半，而且默认的inode数量不多，我们可以用mount来重新挂载。

```
mount -o size=1500M -o nr_inodes=1000000 -o noatime,nodiratime -o remount /dev/shm
```

这个改动只是临时的，如果想要永久改动。

在/etc/fstab里加上。

```
tmpfs /dev/shm tmpfs defaults,size=1.5G 0 0 
```

# 应用

我看树莓派上默认/tmp目录，是磁盘上的，并不是tmpfs的。

可以用/dev/shm来做。

```
mkdir /dev/shm/tmp
chmod 1777 /dev/shm/tmp
mount -bind /dev/shm/tmp /tmp
```

查看shm的大小。

```
pi@raspberrypi:/tmp$ df -h /dev/shm
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           463M     0  463M   0% /dev/shm
```

# 简介

`/dev/shm` 是一个特殊的虚拟文件系统（tmpfs），

通常用于共享内存（Shared Memory）操作。

它的主要作用是==允许不同的进程在内存中共享数据，而不需要将数据写入磁盘。==

这对于某些应用程序来说，可以提高性能并减少磁盘I/O。

在 `/dev/shm` 下创建的文件和目录实际上都位于内存中，而不是硬盘上。

这意味着数据可以更快地在不同进程之间传递，因为不需要实际的磁盘读写操作。

共享内存对于一些需要高效的进程间通信（Inter-Process Communication，IPC）的应用程序非常有用，比如数据库管理系统、图形处理程序和多线程应用程序。

==不同进程可以通过共享内存区域在内存中共享数据，而无需复制大量数据或使用其他 IPC 机制。==

要使用 `/dev/shm`，你可以在该目录下创建文件或目录，然后让不同的进程通过文件共享数据。

请注意，`/dev/shm` 的大小通常受到系统内存的限制，因此如果需要大量共享内存，你可能需要调整系统内存设置。

# C语言示例代码

以下是一个简单的C语言示例代码，演示如何使用共享内存在两个进程之间共享数据。这个示例使用了Linux的System V共享内存机制，需要使用`shmget()`、`shmat()`、`shmdt()`和`shmctl()`等函数。确保在编译时使用 `-lrt` 标志链接Realtime库。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define SHM_KEY 12345 // 共享内存的键值
#define SHM_SIZE 100  // 共享内存的大小

int main() {
    int shmid;
    char *shm_ptr;

    // 创建共享内存
    shmid = shmget(SHM_KEY, SHM_SIZE, IPC_CREAT | 0666);
    if (shmid == -1) {
        perror("shmget");
        exit(1);
    }

    // 将共享内存附加到当前进程的地址空间
    shm_ptr = shmat(shmid, NULL, 0);
    if (shm_ptr == (char *) -1) {
        perror("shmat");
        exit(1);
    }

    // 写入数据到共享内存
    strcpy(shm_ptr, "Hello, shared memory!");

    // 分离共享内存
    shmdt(shm_ptr);

    // 在另一个进程中读取共享内存中的数据
    // 你可以编写另一个C程序来演示读取共享内存中的数据

    // 删除共享内存
    shmctl(shmid, IPC_RMID, NULL);

    return 0;
}
```

请注意，上述示例中，一个进程将字符串写入共享内存，然后将共享内存分离，并最终删除共享内存。另一个进程可以使用相同的 `shmid` 来附加到共享内存，并读取其中的数据。

共享内存是一种强大的IPC机制，但需要小心处理，以确保数据的一致性和安全性。在实际应用中，你可能需要添加更多的同步机制来协调不同进程之间的访问。