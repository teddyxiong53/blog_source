---
title: Linux之内存问题调试
date: 2018-03-28 19:52:38
tags:
	- Linux

---



如果碰到了oom问题，应该怎样进行调试呢？

可以通过下面这些文件和手段来帮助定位。

#1、/proc/sys/vm/min_free_kbytes

这个是系统开始回收内存的阈值，当内存小于这个值的时候，就开始回收内存。

```
/proc/sys/vm # cat min_free_kbytes 
970
```

我们可以修改它的大小。

```
/proc/sys/vm # echo 10240 > ./min_free_kbytes 
/proc/sys/vm # cat min_free_kbytes 
10240
```

#2、/proc/sys/vm/drop_caches

这个是用来清空缓存的。

当前内存情况是这样：

```
/proc/sys/vm # free
             total       used       free     shared    buffers     cached
Mem:         59000       7004      51996          0          0        664
-/+ buffers/cache:       6340      52660
Swap:            0          0          0
```



```
/proc/sys/vm # echo 1 > /proc/sys/vm/drop_caches
sh (808): drop_caches: 1
/proc/sys/vm # free 
             total       used       free     shared    buffers     cached
Mem:         59000       6920      52080          0          0        600
-/+ buffers/cache:       6320      52680
Swap:            0          0          0
```

可以写入的值有1/2/3 。

1：清理页缓存。

2：清理文件缓存。

3：都清理。

#3、/proc/sysrq-trigger

打印内存信息。

```
~ # echo m > /proc/sysrq-trigger 
sysrq: SysRq : Show Memory
Mem-Info:
active_anon:35 inactive_anon:0 isolated_anon:0
 active_file:329 inactive_file:68 isolated_file:0
 unevictable:0 dirty:4 writeback:0 unstable:0
 slab_reclaimable:683 slab_unreclaimable:774
 mapped:292 shmem:0 pagetables:6 bounce:0
 free:27306 free_pcp:19 free_cma:0
Node 0 active_anon:140kB inactive_anon:0kB active_file:1316kB inactive_file:272kB unevictable:0kB isolated(anon):0kB isolated(file):0kB mapped:1168kB dirty:16kB writeback:0kB shmem:0kB writeback_tmp:0kB unstable:0kB all_unreclaimable? no
Normal free:109224kB min:1380kB low:1724kB high:2068kB active_anon:140kB inactive_anon:0kB active_file:1316kB inactive_file:272kB unevictable:0kB writepending:16kB present:131072kB managed:120724kB mlocked:0kB kernel_stack:408kB pagetables:24kB bounce:0kB free_pcp:76kB local_pcp:76kB free_cma:0kB
lowmem_reserve[]: 0 0
Normal: 2*4kB (UM) 2*8kB (UM) 5*16kB (UME) 2*32kB (U) 2*64kB (UE) 1*128kB (M) 1*256kB (E) 4*512kB (M) 4*1024kB (UME) 2*2048kB (M) 24*4096kB (M) = 109224kB
397 total pagecache pages
0 pages in swap cache
Swap cache stats: add 0, delete 0, find 0/0
Free swap  = 0kB
Total swap = 0kB
32768 pages RAM
0 pages HighMem/MovableOnly
2587 pages reserved
0 pages cma reserved
```

打印线程信息。

```
echo t > /proc/sysrq-trigger
init            S    0     1      0 0x00000000
[<80681d30>] (__schedule) from [<80681e40>] (schedule+0x88/0x98)
[<80681e40>] (schedule) from [<80123d84>] (do_wait+0x210/0x298)
[<80123d84>] (do_wait) from [<80124438>] (kernel_wait4+0xb4/0x140)
[<80124438>] (kernel_wait4) from [<80124554>] (SyS_wait4+0x90/0xc8)
[<80124554>] (SyS_wait4) from [<80107600>] (ret_fast_syscall+0x0/0x48)
kthreadd        S    0     2      0 0x00000000
[<80681d30>] (__schedule) from [<80681e40>] (schedule+0x88/0x98)
[<80681e40>] (schedule) from [<8013e8e8>] (kthreadd+0x154/0x234)
[<8013e8e8>] (kthreadd) from [<801076d0>] (ret_from_fork+0x14/0x24)
```

打印CPU寄存器信息。

```
~ # echo p > /proc/sysrq-trigger
sysrq: SysRq : Show Regs
```



# 参考资料

1、内存问题排查手段及相关文件介绍

http://www.cnblogs.com/muahao/p/6772795.html