---
title: Linux之switch_root
date: 2023-03-13 13:37:33
tags:
	- Linux

---



# switch_root 命令  

除了基于initramfs的系统（如第四节的mini linux），

通常initramfs都是为安装最终的根文件系统做准备工作，

它的最后一步需要安装最终的根文件系统，

然后切换到新根文件系统上去。



以往 的基于ramdisk 的initrd 使用pivot_root命令切换到新的根文件系统，

然后卸载ramdisk。

**但是initramfs是rootfs，**

**而rootfs既不能 pivot_root，也不能umount。**



为了从initramfs中切换到新根文件系统，需要作如下处理： 

（1）删除rootfs的全部内容，释放空间 
find -xdev / -exec rm '{}' ';' 

（2）安装新的根文件系统，并切换 
cd /newmount; mount --move . /; chroot . 

（3）把stdin/stdout/stderr 附加到新的/dev/console，然后执行新文件系统的init程序 



上述步骤比较麻烦，而且要解决一个重要的问题：

第一步删除rootfs的所有内容也删除了所有的命令，

那么后续如何再使用这些命令完成其他步骤？

busybox的解决方案是，

提供了switch_root命令，完成全部的处理过程，使用起来非常方便。 

switch_root命令的格式是：

```
switch_root [-c /dev/console] NEW_ROOT NEW_INIT [ARGUMENTS_TO_INIT]  
```

其中NEW_ROOT是实际的根文件系统的挂载目录，

执行switch_root命令前需要挂载到系统中；

NEW_INIT是实际根文件系统的init程序的路径，一般是/sbin/init；

 -c /dev/console是可选参数，用于重定向实际的根文件系统的设备文件，一般情况我们不会使用；

而 ARGUMENTS_TO_INIT则是传递给实际的根文件系统的init程序的参数，也是可选的。  



需要特别注意的是：switch_root命令必须由PID=1的进程调用，也就是必须由initramfs的init程序直接调用，不能由init派生的其他进程调用，否则会出错，提示： 

switch_root: not rootfs  

也是同样的原因，init脚本调用switch_root命令必须用exec命令调用，否则也会出错，提示： 

switch_root: not rootfs 

# pivot_root命令

`pivot_root` 命令是一个用于更改 Linux 系统根文件系统的工具，它是基于 `pivot_root` 系统调用实现的。

命令的基本语法如下：

```bash
pivot_root new_root put_old
```

其中，`new_root` 是新的根文件系统的路径，`put_old` 是原始根文件系统的路径。

使用 `pivot_root` 命令时需要注意以下几点：

1. 需要以超级用户（root）权限运行该命令。
2. 命令会将当前进程的根文件系统更改为新的文件系统，并将原始的根文件系统放置在指定的目录中。
3. 在切换根文件系统之前，需要确保新的根文件系统和原始根文件系统都是有效的、可用的。
4. 切换根文件系统可能涉及到一些细节和注意事项，如更新挂载点、重新打开文件句柄等，需要在使用前仔细了解相关文档和用法。

需要注意的是，`pivot_root` 命令在大部分现代 Linux 发行版中不再常用，而是通过更高级的初始化系统（如 systemd）来进行根文件系统的切换和管理。

# pivot_root和switch_root区别

我看我们的脚本里还有这个。

那么这个的执行是在switch_root之后。

```
./etc/overlaymount:3:        pivot_root $1 $1$2 && {
```

这一层是为了其他的用途。

为了实现overlay。

```
do_overlay_mount() { #<overlay dir>
        mkdir -p $1/upper $1/work
        fopivot $1/upper $1/work /rom 1
}
```

```
do_overlay_mount /data/overlay
```



`pivot_root` 和 `switch_root` 是两个 Linux 命令，

用于切换根文件系统（root filesystem）。

它们的主要区别如下：

1. **目的**：
   
   - `pivot_root` 命令的主要目的是将当前进程的根文件系统更改为指定目录，并将原来的根文件系统移动到新的根文件系统下的指定目录。**这样可以实现对根文件系统的切换，同时保留原始根文件系统的挂载点。**
- `switch_root` 命令的主要目的是将当前进程的根文件系统更改为指定目录，并启动新的 init 进程作为新的根文件系统的第一个进程。**这样可以完全切换到新的根文件系统，同时结束原始根文件系统的进程。**
   
2. **使用方式**：
   - `pivot_root` 命令的语法如下：
     
     ```
     pivot_root new_root put_old
     ```
     其中，`new_root` 是要切换到的新根文件系统的路径，`put_old` 是原始根文件系统在新根文件系统中的目录。
   - `switch_root` 命令的语法如下：
     
     ```
     switch_root new_root init
    ```
     其中，`new_root` 是要切换到的新根文件系统的路径，`init` 是要启动的新 init 进程的路径。
   
3. **行为差异**：
   - `pivot_root` 命令将原始根文件系统移动到新的根文件系统下的指定目录，但不会启动新的 init 进程。**原始根文件系统的挂载点将保留，并继续存在于新的根文件系统中。**
   - `switch_root` 命令将当前进程的根文件系统更改为指定目录，并启动新的 init 进程。新的 init 进程成为系统的第一个进程，并负责初始化系统环境、挂载文件系统以及启动其他进程。**原始根文件系统的进程将结束。**

综上所述，`pivot_root` 和 `switch_root` 在切换根文件系统时有不同的行为和目的。选择使用哪个命令取决于您的具体需求和场景。

# switch_root实现代码分析

`switch_root` 命令的实现通常是在 Linux 系统的启动阶段的 initrd（initial ramdisk）或初始化脚本中完成的。

下面是一个简单的 `switch_root` 实现的伪代码示例：

```bash
# 定义新根文件系统的路径和新 init 程序的路径
new_root="/path/to/new_root"
new_init="/path/to/new_init"

# 挂载新根文件系统
mount -o move /proc $new_root/proc
mount -o move /sys $new_root/sys
mount -o move /dev $new_root/dev

# 切换根文件系统和启动新 init 进程
exec chroot $new_root $new_init
```

上述示例代码的执行过程如下：

1. 定义了新根文件系统的路径 `new_root` 和新 init 程序的路径 `new_init`，您需要将其替换为实际的路径。

2. 使用 `mount` 命令将当前系统中的 `/proc`、`/sys` 和 `/dev` 挂载点移动到新根文件系统的对应位置。这是为了确保新根文件系统内部可以访问这些关键目录。

3. 使用 `chroot` 命令切换到新根文件系统，并执行新 init 程序。`chroot` 命令将改变当前进程的根文件系统为指定目录 `new_root`，并在该目录下执行指定的命令 `new_init`，成为新的 init 进程。

通过以上步骤，`switch_root` 实现了根文件系统的切换和启动新 init 进程的操作。在实际系统中，还需要处理一些额外的细节，例如卸载旧根文件系统、重新挂载文件系统等，以确保切换的正确性和稳定性。具体实现可能因系统和启动流程的不同而有所差异，但上述示例提供了一个基本的框架和思路。

# 参考资料

1、

https://blog.csdn.net/lbaihao/article/details/51839481