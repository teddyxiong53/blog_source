---
title: Linux之cgroup学习
date: 2017-06-06 22:21:51
tags:
	- Linux
	- cgroup

---



# 什么是cgroup

cgroup是Control group的缩写。是linux内核提供的用来限制、记录、隔离进程组的资源的机制。

2007年，在linux2.6.24引入。它并不是一个全新的东西，它是把进程管理从cpuset中玻璃出来。

作者是来自谷歌的Paul Menage。

cgroup提供了一个cgroup的虚拟文件系统。这个文件系统是作为用户接口。用户可以通过这个文件系统来进行分组管理和子系统设置。我们必须挂载这个虚拟文件系统，才能使用cgroup。

更cgroup起类似作用的还有古老的ulimit。

我们看看系统里的情况：

```
vm-alpine-0:/proc/1# mount | grep cgroup
cgroup_root on /sys/fs/cgroup type tmpfs (rw,nosuid,nodev,noexec,relatime,size=10240k,mode=755)
openrc on /sys/fs/cgroup/openrc type cgroup (rw,nosuid,nodev,noexec,relatime,release_agent=/lib/rc/sh/cgroup-release-agent.sh,name=openrc)
cpu on /sys/fs/cgroup/cpu type cgroup (rw,nosuid,nodev,noexec,relatime,cpu)
cpuacct on /sys/fs/cgroup/cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,cpuacct)
blkio on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,blkio)
devices on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,devices)
freezer on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,freezer)
net_cls on /sys/fs/cgroup/net_cls type cgroup (rw,nosuid,nodev,noexec,relatime,net_cls)
net_prio on /sys/fs/cgroup/net_prio type cgroup (rw,nosuid,nodev,noexec,relatime,net_prio)
pids on /sys/fs/cgroup/pids type cgroup (rw,nosuid,nodev,noexec,relatime,pids)
```



```
vm-alpine-0:/proc/1# cat /proc/cgroups 
#subsys_name    hierarchy       num_cgroups     enabled
cpu     2       1       1
cpuacct 3       1       1
blkio   4       1       1
devices 5       1       1
freezer 6       1       1
net_cls 7       1       1
net_prio        8       1       1
pids    9       1       1
```

```
vm-alpine-0:/proc/1# cat cgroup 
9:pids:/
8:net_prio:/
7:net_cls:/
6:freezer:/
5:devices:/
4:blkio:/
3:cpuacct:/
2:cpu:/
1:name=openrc:/
```

在/sys/fs/cgroup下也有信息。

```
vm-alpine-0:/sys/fs/cgroup# ls
blkio     cpu       cpuacct   devices   freezer   net_cls   net_prio  openrc    pids
```

```
vm-alpine-0:/sys/fs/cgroup/cpu# tree
.
├── cgroup.clone_children
├── cgroup.procs
├── cgroup.sane_behavior
├── cpu.rt_period_us
├── cpu.rt_runtime_us
├── cpu.shares
├── notify_on_release
├── release_agent
└── tasks
```



# cgroup可以做什么

1、限制资源使用。例如限制mem use max。

2、优先级控制。

3、审计。

4、控制进程。

在实际操作中，系统管理员会做些什么？

1、隔离一个进程集合。例如nginx的所有进程。

2、为这组进程分配足够的内存。

3、限制访问某些设备。

我们可以自己新建一个cgroup，然后挂载。

```
vm-alpine-0:~/work/test# mkdir cgroup
vm-alpine-0:~/work/test# cd cgroup/
vm-alpine-0:~/work/test/cgroup# cd ..
vm-alpine-0:~/work/test# mount -t tmpfs cgroup_root ./cgroup/
vm-alpine-0:~/work/test# mount
...
cgroup_root on /root/work/test/cgroup type tmpfs (rw,relatime)
vm-alpine-0:~/work/test# mkdir -p cgroup/cpuset
vm-alpine-0:~/work/test# mount -t cgroup -ocpuset cpuset ./cgroup/cpuset
vm-alpine-0:~/work/test# 

```



# 示例

## CPU限制

写一个deadloop.c文件。如下：

```
void main()
{
  int i=0; 
  for(;;) i++;
}
```

编译运行，这个程序肯定会把CPU占用100%的。top看看，是接近100%的。

```
CPU: 100% usr   0% sys   0% nic   0% idle   0% io   0% irq   0% sirq
Load average: 0.11 0.06 0.02 2/190 4041
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
 4040  4031 root     R      708   0%   0  91% ./deadloop
```



我们在/sys/fs/cgroup目录下新建一个xhl的文件。然后系统会自动在下面产生一些文件。

```
vm-alpine-0:/sys/fs/cgroup/cpu# tree
.
├── cgroup.clone_children
├── cgroup.procs
├── cgroup.sane_behavior
├── cpu.rt_period_us
├── cpu.rt_runtime_us
├── cpu.shares
├── notify_on_release
├── release_agent
├── tasks
└── xhl
    ├── cgroup.clone_children
    ├── cgroup.procs
    ├── cpu.rt_period_us
    ├── cpu.rt_runtime_us
    ├── cpu.shares
    ├── notify_on_release
    └── tasks
```

我们找到deadloop的pid：

```
vm-alpine-0:~/work/test/cgroup# ps ax | grep deadloop
 4040 root       0:52 ./deadloop
 4043 root       0:00 grep deadloop
```

是4040。我的这个系统好像跟网上描述的都不太相同。

按道理应该有一个cpu.cfg_quota_us的文件的。用来配置cpu时间配额。

然后把4040 echo到tasks里，这样就可以把CPU的占用限制下来了。



# 内核相关代码

cgroup 在 Linux 内核中的实现涉及多个关键组件和模块。下面是一些与 cgroup 相关的主要内核代码：

1. cgroup 核心代码：cgroup 核心代码包含在内核的 cgroup 子系统中。该代码位于 `kernel/cgroup/` 目录下，包括与 cgroup 生命周期管理、cgroup 层次结构、资源控制和统计等相关的文件。

2. cgroup 文件系统：cgroup 使用了一种特殊的文件系统，称为 cgroup 文件系统。文件系统的实现代码位于 `fs/cgroup/` 目录下，包括与 cgroup 目录和文件的创建、读写、删除等相关的文件。

3. cgroup 控制器（Controller）：cgroup 控制器是用于管理和控制特定资源的模块。每个控制器负责管理一种或多种资源，例如 CPU、内存、磁盘I/O、网络等。每个控制器都有相应的内核代码，位于 `kernel/cgroup/` 目录下的子目录中，例如 `cpu/`、`memory/`、`blkio/`、`net_cls/` 等。

4. cgroup 调度器：cgroup 调度器是用于根据资源限制和控制策略，对 cgroup 中的进程进行调度和分配资源的模块。调度器相关的代码位于 `kernel/sched/` 目录下，包括与调度器算法、策略和实现相关的文件。

5. 进程管理和关联：cgroup 在内核中与进程管理和调度紧密相关。相关代码位于 `kernel/` 目录下的进程管理相关子目录中，例如 `kernel/fork.c`、`kernel/exit.c` 等。这些代码负责将进程与 cgroup 进行关联、跟踪进程的 cgroup 归属以及进行资源限制和控制。

这只是一些与 cgroup 相关的主要内核代码，涉及的代码文件还有很多，具体的代码路径和文件取决于所使用的内核版本和配置。可以通过查看 Linux 内核源代码来深入了解 cgroup 的内核实现细节。