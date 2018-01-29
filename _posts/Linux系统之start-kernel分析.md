---
title: Linux系统之start_kernel分析
date: 2018-01-29 13:27:44
tags:
	- Linux系统

---



逐行分析start_kernel函数。分析的是linux2.6版本的。

1、smp_setup_processor_id()

这个函数空的。不管。

2、lockdep_init。

这个是用来在编译阶段检测内核中是否有死锁的东西。可以关闭。不管。

3、debug_objects_early_init。

可以关闭。不管。

4、boot_init_stack_canary。

空的。不管。

5、cgroup_init_early。

可以关闭。不管。

6、local_irq_disable。

宏。就是arm指令。禁止中断。

7、early_boot_irqs_off

空的。

8、early_init_irq_lock_class。

空的。

9、lock_kernel。

可以关闭。

10、tick_init。

可以关闭。

11、boot_cpu_init。

拿到cpu id，单核就是0，然后把cpu_online_bits、cpu_active_bits这些置位好。

12、page_address_init。

空的。

13、打印linux版本信息。

14、setup_arch。重要函数。返回的就是cmdline的内容。

```
1、定义tag变量，执行init_tags。这个是一个默认的taglist。保底用的。
2、定义字符串指针from，指向default_command_line。这个是CFG_CMDLINE的值。
3、unwinid_init。空的。
4、setup_processor。参数是machine id
	-- 就是为了查出这个机器的信息，就是在at2440evb.c里mach_des里的信息。
5、根据第四步的返回值，取得机器名。
6、把R2传递过来的__atags_pointer用phys_to_virt转成虚拟地址tags指针来用。
7、如果第一个tag不是core，则是非法的。则用默认的init_tags。
8、调用save_atags。是保存到一个char数组里。
9、调用parse_tags。依次调用parse_tag_core这些对应的函数解析出ROOT_DEV等内容。
10、对struct mm_struct变量init_mm赋值，_text等内容。_end给到brk。
11、把上面的default_command_line给到传递进来的指针。
12、调用parse_early_parm。
```

15、mm_init_owner。

```
参数：
	1、init_mm，在setup_arch里有设置值。
	2、init_task。这个是task_struct类型的。目前还没有处理过。
处理过程就一行，把init_mem的owner设置为init_task。
```

16、setup_command_line。

```
输入：
	1、就是setup_arch得到的命令内容。
处理就是用alloc_bootmem分配了saved_command_line和static_command_line这2个区域。
bootmem使用bitmap来标记页的使用。完成使命后，被都被清空的。被buddy和slab接管。
```

17、setup_nr_cpu_ids。对单CPU，这个是空的。

18、setup_per_cpu_areas。对单cpu也是空的。

19、smp_prepare_boot_cpu。对单cpu也是空的。

20、build_all_zonelists。

```
我们假定不配置NUMA。这个是个比较复杂的东西。我们不用这个配置。
1、判断system_state是否SYSTEM_BOOTING。这个变量贯穿linux启动过程的一个变量。因为SYSTEM_BOOTING是0，所以默认就是SYSTEM_BOOTING状态的。
2、处理比较复杂，涉及到很多新的概念，我暂时不细看。
```

21、page_alloc_init。实际上没做事情。

22、把command line打印出来。

23、parse_early_param。

24、parse_args。

```
注意解析处理的数据，放在一个指定的内存位置上。这个位置是在vmlinux.lds.h里布局定义的。__start___param这里。
```

25、pidhash_init。

```
简单说，就是分配了一块内存，用来放pid hash。
```

26、vfs_caches_init_early。

```
跟第25步类似，分配了2块内存。
```

27、sort_main_extable。

```
排序exception  table。不知道具体用途。
```

28、trap_init。直接返回。

29、mm_init。重要函数。这个之后，就可以用kmalloc函数了。

```
这里涉及到一个SPARSEMEM的东西，我看了一些，x64的默认打开了。而arm的默认的关闭的。
默认配置的是FLATMEM。应该对应的就是最基础的一块内存的情况。
1、page_cgroup_init_flatmem。这个函数有多份。实际上是用到了头文件里的空实现。
2、mem_init。
	这里做了页框的初始化等操作。比较复杂，目前不细看。
3、kmem_cache_init。
	1、create_kmalloc_cache。应该kmalloc就是从这个区域里取得内存的。
4、pgtable_cache_init。空的。
5、vmalloc_init。
```

30、sched_init。

```
比较复杂，暂不细看。
```

31、preempt_init。不打开抢占功能，空的。

32、判断是否禁止中断的，如果没有，禁止，并且打印一行警告信息。

33、rcu_init。

```
比较复杂，暂不细看。
```

34、radix_tree_init。

```
这个是提供系统查询效率的。
```

35、early_irq_init。没什么。

36、init_IRQ。会调用到at2440evb.c里的init_irq（指针注册的）。

37、prio_tree_init。没做太多事情，作用不明。

38、init_timers。

```
后面看。
```

39、hrtimers_init。

```
高精度timer。后面看。
```

40、soft_irq_init。

41、timekeeping_init。

42、time_init。

43、profile_init。空的。

44、early_boot_irqs_on。空的。

45、local_irq_enable。开始打开中断了。

46、允许获取GFP了。因为中断打开了。

47、kmem_cache_init_late。空的。留位置而已。

48、console_init。打开控制台。会调用到芯片的相关设置。

49、把前面累计的错误信息，到这里打出来看。

50、lockdep_init。空的。

51、locking_selftest。进行死锁自测。

52、如果配置了initrd。进行page_to_pfn的操作。

53、page_cgroup_init。空的。

54、enable_debug_pagealloc。如果使能了这个功能，就是给一个全局变量赋值，否则就是空的。

55、kmemtrace_init。空的。

56、kmemleak_init。空的。

57、debug_objects_mem_init。空的。

58、idr_init_cache。就是用kmem_cache_create分配了一块内存。

59、setup_per_cpu_pageset。page相关。具体不清楚。

60、numa_policy_init。很高级的特性，不用，空的。

61、sched_clock_init。就是给一个全局变量赋值了。

62、calibrate_delay。计算jiffies相关的东西。

63、pidmap_init。

64、anon_vma_init。匿名vma初始化。就是kmem_cache_create了一块内存。

65、如果是x86，且efi_enabled，就会efi_enter_virtual_mode。

66、thread_info_cache_init。空的。

67、cred_init。kmem分配内存，证书罐子初始化。

68、fork_init。

```
输入：
	totalram_pages。内存总页数。
处理：
	1、求得max_threads，就是用内存页数去除以某个值。max_threads不小于20.
```

69、proc_caches_init。

```
1、kmem_cache_create了好几个内存块。
2、mmap_init。
```

70、buffer_init。也就是分了一块内存。

71、key_init。空的。

72、security_init。直接返回0 。

73、dbg_late_init。空的。

74、vfs_caches_init。

```
1、先分配了一块内存。叫names_cache。
2、dcache_init。
3、inode_init。
4、files_init。
5、mnt_init。这个内容较多。
	1）sysfs_init。
	2）init_rootfs。这个在ramfs下面。
	3）init_mount_tree。
		do_kern_mount("rootfs")挂载rootfs。
6、bdev_cache_init。块设备。
7、chrdev_init。
```

75、signals_init。就是分配了一块内存。

76、page_writeback_init。后面看。

77、proc_root_init。

```
1、register_filesystem(&proc_fs_type)
2、proc_mkdir各个文件夹。
```

78、cgroup_init。

```
proc_create("crgoups)
```

79、cpuset_init。

80、taskstats_init_early。

81、delayacct_init。空的。

82、check_bugs。

83、acpi_init。空的。

84、sfi_init_late。空的。

85、ftrace_init。空的。

86、rest_init。到这个位置的时候，kernel已经是alive状态了。

这个函数比较大。我们下面再单独拆解。

# rest_init内容

1、rcu_scheduler_starting。就写一个全局变量。

2、用kernel_thread创建kernel_int。

```
kernel_init：
	1、这个虽然创建在kthreadd前面，但是这个函数第一行就是等kthreadd_done。
	2、do_basic_setup。
		1）init_workqueues。
		2）init_tmpfs。
		3）driver_init。这个函数很重要。
			-- devtmpfs_int。
			-- devices_init。
			-- buses_init。
			-- classes_init。
			-- firmware_init。
			-- hypervisor_init。
			-- platform_bus_init。
			-- system_bus_init。
			-- cpu_dev_init。
			-- memory_dev_init。如果内存不可以热拔插，就是空的。
		4）init_irq_proc。
		5）do_initcalls。
	3、sys_open("/dev/console")，然后sys_dup，得到stdin、stdout、stderr。
	4、init_post。这个函数也很重要。
		1）free_initmem。把启动阶段用的内存释放掉。
		2）把system_state设置为SYSTEM_RUNNING。
		3）run_init_process。运行init程序。
		4）运行/bin/sh，进入shell，完成。
```



3、numa_default_policy。空的。

4、用kernel_thread创建kthreadd。

```
也是一个死循环。接受请求，然后不停地create_kthread。
```

5、用complete等kthreadd完成。

6、unlock_kernel。空的。

7、init_idle_bootup_task。

8、preempt_enable_no_resched。空的。

9、schedule。开始调度。

10、preempt_disable。空的。

11、cpu_idle。





#mm_init的疑问

##1.pfn

PFN是Page Frame Number。页框号。取值肯定就是整数了。

取值范围是0到内存页数（内存/4K）。

每个物理内存的Page，内核给了一个数据结构来描述，就是struct page。

每个pfn就唯一对应一个page。

内核有提供对应的宏来进行转换：

```
pfn_to_page
page_to_pfn
```

page也可以和pfn进行转换。

```
pfn_to_virt
```

## 2.slab、slub、slob关系

1、最先由的slab，开源后，大家优化，一年半后，有了slob。

2、slob是针对32M内存以下的嵌入式设备优化的。

3、再过了几个月，slub也出来了。slub是对slab的重构，以后会取代slab和slob。

slab.c、slub.c、slob.c三个文件提供的函数是一样的。

我看后续一般是把slub设置为默认了。就看这个的。







#build_all_zonelists的疑问

内存管理的三个层次：

Node包括Zone，Zone包括Page。

NUMA模型：非一致性内存访问模型。这个跟SMP是一个类型的概念。是对smp不足之处的补充。

SMP用的是UMA模型（一致性内存访问模型）。多个CPU使用同一个内存。这样带来性能的限制，内存是性能提升的瓶颈，即使增加CPU也没用。





#tag的疑问

tag内容的最简单结构是：

```
header：描述core的长度和类型。
core
header：描述header的长度和类型。
mem
none
```



linux在启动过程中需要一些参数，来得到当前的硬件信息或者所需要的资源再内存里的位置。

Documentation/arm/Booting文档里。

1、设置ram。强制的。

2、初始化一个串口。并且通过console传递给kernel。

3、检测MACHINE_TYPE。

4、设置tag list。

以ATAG_CORE开头，以ATAG_NONE结尾。

bootloader应该告诉kernel系统内存的起始地址，尺寸、roofs位置等。

一般建议放在ram的最前面的16K的位置。

5、启动kernel。

建议预留内存的最前面32K不用。

1）禁止所有的dma操作。

2）cpu寄存器设置：r0=0， r1=machine id，r2=tag list在内存的位置。

3）禁止中断。用svc模式。

4）mmu关闭。cache都关闭。

5）直接跳转启动。

