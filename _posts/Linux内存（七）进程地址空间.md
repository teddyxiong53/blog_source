---
title: Linux内存（七）进程地址空间
date: 2018-04-03 15:01:23
tags:
	- Linux内核

---



本文是对《Linux内核设计与实现》第15章的总结。

# 地址空间

每个进程都有一个32位的平坦地址空间。

“平坦”这个术语是指地址空间是一个独立的连续空间。

有些os提供了段地址空间。但是现在的os基本上都是实用了平台地址空间的。

进程的内存空间里一般有这些对象：

1、text段。

2、data段。

3、bss段。

4、进程的用户栈。

5、动态库。

6、mmap。

7、shm。

8、匿名的内存映射，例如malloc的内存。

每一个对象对应一个vma结构体。所有的vma结构体用一个mm_struct来统一管理。

一个mm_struct跟一个task_struct对应。

## 内存描述符

mm_struct。

结构体的内容如下：

```
1、struct vm_area_struct *mmap。//内存区域链表。
2、struct rb_root mm_rb//vma的红黑树，提高搜索速度，复杂度是O(logN)
3、struct vm_area_struct *mmap_cache。//最近使用的内存区域。
4、ulong free_area_cache。//地址空间的第一个空洞。hole。
5、pgd_t *pgd。//页全局目录。
6、atomic_t mm_users//
7、atomic_t mm_count //
8、struct rw_semaphore mmap_sem //
9、spinlock_t page_table_lock //页表锁。
10、struct list_head mm_list //所有的mm_struct形成的链表。
11、ulong start_code，end_code，start_data，end_data。
12、ulong start_brk，brk
13、start_stack
14、arg_start，arg_end
15、env_start，env_end。
16、ulong  rss。 //所分配的物理页。
17、ulong total_vm。//全部页面数目。
18、ulong locked_vm。//锁住的page数目。
19、ulong saved_auxv[] 保存的auxv
20、cpumask_t cpu_vm_mask;//lazy TLB交换掩码。
21、mm_context_t context//CPU架构相关的特殊数据。
22、ulong flags //
23、int core_waiters //coredump等待线程。
24、struct core_state *core_state。
25、spinlock_t ioctx_lock  //异步io链表锁。
26、struct list_head ioctx_list //异步io链表。
```

## 分配mm_struct

task_struct里的mm这个成员就是自己的mm_struct。

是在fork的时候，用copy_mm函数来赋值父进程的mm_struct。

是通过fork.c里的allocate_mm从mm_cachep这个slab里分配得到的。

如果希望子进程和父进程共享地址空间，那么就在clone的时候，传递CLONE_VM标志。

是否共享地址空间，是linux上进程和线程的唯一区别。

## 撤销mm_struct

在进程退出的时候，exit.c里的exit_mm函数被调用。

## mm_struct与内核线程

内核线程没有地址空间，所以对应的task_struct的mm成员是NULL 。

这也是内核线程的真正含义，他们没有用户上下文。

省掉了地址空间再好不过了。因为内核线程不需要访问任何用户空间的内存。

即使如此，内核线程还是需要使用页表的。

为了避免内核线程为mm_struct何page table浪费内存，也为了避免不必要的地址空间切换，内核线程直接使用前一个进程的mm_struct。

当一个进程被调度的时候，这个进程的mm所指向的地址空间被装载到内存，task_struct的active_mm会被更新。

当一个内核线程被调度的时候，内核发现它的mm是NULL，就会保留前一个进程的地址空间，然后把内核线程的active_mm更新。指向前一个进程的mm_struct。

# vm_area_struct

虚拟内存区域。

是指地址空间连续的一个独立内存范围。

每个vma是一个管理单位，它具有相同的属性，例如读写执行。

你可以用pmap来查看一个进程的地址空间。

这个是我在mylinuxlab里查看的init进程的情况。可以看到arm的是从0x10000这个地方开始，不同于x86的0x08048000 。

```
~ # pmap -x 1
1: init
Address   Kbytes     PSS   Dirty    Swap  Mode  Mapping
00010000    1376     257       0       0  r-xp  /bin/busybox
00177000      12      12      12       0  rw-p  /bin/busybox
0017a000     144      32      32       0  rw-p  [heap]
7e9d7000     132       8       8       0  rw-p  [stack]
7ef10000       4       0       0       0  r-xp  [sigpage]
7ef11000       4       0       0       0  r--p  [vvar]
7ef12000       4       1       0       0  r-xp  [vdso]
ffff0000       4       0       0       0  r-xp  [vectors]
```

在proc下面看到的类似。

```
/proc/1 # cat maps
00010000-00168000 r-xp 00000000 b3:00 12290      /bin/busybox
00177000-0017a000 rw-p 00157000 b3:00 12290      /bin/busybox
0017a000-0019e000 rw-p 00000000 00:00 0          [heap]
7e9d7000-7e9f8000 rw-p 00000000 00:00 0          [stack]
7ef10000-7ef11000 r-xp 00000000 00:00 0          [sigpage]
7ef11000-7ef12000 r--p 00000000 00:00 0          [vvar]
7ef12000-7ef13000 r-xp 00000000 00:00 0          [vdso]
ffff0000-ffff1000 r-xp 00000000 00:00 0          [vectors]
```

# 页表



# 切换进程时，如何切换页表？

Linux进程切换的核心函数是context_switch。

这个函数简化后，就是这样：

```
swtich_mm()
switch_to()
```

switch_mm就是切换页表。

对于arm架构，是把CP15的C2寄存器指向对应进程的页表的位置。

对于x86架构，是CR3寄存器。

# 为什么要用多级页表？

页表本质是一个映射表。

最直接的想法，就是每一个页对应一个条目。

对应x86的32位，4KB的页，这样导致页表就要占用1M的空间。太大了。

对于64位，问题就更加严重了。



# pagemap proc

在Documentation/vm/pagemap.txt里。

在2.6.25版本以后，pagemap就是一个新的用户接口，用来在用户态查看page table。

有4个组件是相关的。

1、/proc/pid/pagemap

用来查看物理页框和虚拟页的对应关系。

```
/proc/1 # hexdump pagemap 
0000000 0000 0000 0000 0000 0000 0000 0000 0000
*
0000080 094e 0006 0000 a000 f7ec 0009 0000 a000
0000090 f7ed 0009 0000 a000 800e 0006 0000 a000
00000a0 0000 0000 0000 0000 0000 0000 0000 0000
*
0000100 0000 0000 0000 0000 0946 0006 0000 a000
0000110 0947 0006 0000 a000 0008 0006 0000 a000
```



2、/proc/kpagecount。

```
/proc/1 # hexdump /proc/kpagecount 
0000000 0000 0000 0000 0000 0000 0000 0000 0000
*
^C
/proc/1 # hexdump /proc/kpageflags 
0000000 0000 0010 0000 0000 0000 0010 0000 0000
*
^C
```

3、/proc/kpageflags。

4、/proc/kpagecgroup。



# 参考资料

1、ARM-LINUX的进程切换

https://blog.csdn.net/michael2012zhao/article/details/10384079

2、[ARM Linux] 每个进程的内核页表为什么单独分配存储空间？

https://www.zhihu.com/question/26825537

3、

https://github.com/gatieme/LDD-LinuxDeviceDrivers/blob/master/study/kernel/02-memory/02-pagetable/01-develop/README.md