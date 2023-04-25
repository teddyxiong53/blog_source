---
title: Linux内核之bootargs解析
date: 2018-03-18 18:36:43
tags:
	- Linux内核

---



# 介绍

bootargs 是 uboot 在启动 Linux 内核时传递给内核的引导参数，参数中一般包含启动存储介质、文件系统分区及挂载方式和终端串口等参数。

bootargs是环境变量中的重中之重，

甚至可以说整个环境变量都是围绕着bootargs来设置的。

bootargs的种类非常非常的多，

我们平常只是使用了几种而已。

bootargs非常的灵活，内核和文件系统的不同搭配就会有不同的设置方法，

甚至你也可以不设置 bootargs,

而直接将其写到内核中去（在配置内核的选项中可以进行这样的设置），

正是这些原因导致了bootargs使用上的困难。

bootargs的种类非常的多，而且随着kernel的发展会出现一些新的参数，使得设置会更加灵活多样。



uboot启动kernel的时候，会传递一些bootargs过去。

例如这样：

```
8250.nr_uarts=1 bcm2708_fb.fbwidth=656 bcm2708_fb.fbheight=416 bcm2708_fb.fbswap=1 vc_mem.mem_base=0x3ec00000 vc_mem.mem_size=0x40000000  dwc_otg.lpm_enable=0 console=ttyS0,115200 console=tty1 root=/dev/sda2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
```

那么内核里支持哪些bootargs的设置呢？

我没有找到一个权威的列表。我在源代码里进行搜索。总结出下面的内容。

bootargs分为2部分：

1、early param。

2、setup。



early param是这样定义的。

```
early_param("initrd", early_initrd);
```

你只要搜索early_param。就可以找出内核可以设置的参数来了。
大概有20到30个左右。

常用的early param有：
1、debug。启动时打印详细。
2、quiet。启动时没有什么打印。
3、loglevel=xx。设置log级别。
4、mem=128M。



而setup的则多一些。很多。而且是各个bsp可以自己定义的。下面我把搜索的结构中不常用的部分删掉。

架构只留下arm的S3C24XX的。

现在我知道为什么没有标准的参考表了。因为这个东西是可以用户自己定制的。所以很难给出一个权威参考。

```
teddy@teddy-ubuntu:~/work/mylinuxlab/kernel/linux-stable$ find -name "*.c" | xargs grep -nwr "__setup" 

./kernel/profile.c:99:__setup("profile=", profile_setup);
./kernel/printk/printk.c:153:__setup("printk.devkmsg=", control_devkmsg);
./kernel/printk/printk.c:1958:__setup("console=", console_setup);
./kernel/printk/printk.c:1986:__setup("no_console_suspend", console_suspend_disable);
./kernel/futex.c:299:__setup("fail_futex=", setup_fail_futex);
./kernel/gcov/fs.c:87:__setup("gcov_persist=", gcov_persist_setup);
./kernel/resource.c:1494:__setup("reserve=", reserve_setup);
./kernel/resource.c:1623:__setup("iomem=", strict_iomem);
./kernel/sched/core.c:2296:__setup("schedstats=", setup_schedstats);
./kernel/sched/topology.c:480:__setup("isolcpus=", isolated_cpu_setup);
./kernel/sched/topology.c:961:__setup("relax_domain_level=", setup_relax_domain_level);
./kernel/sched/autogroup.c:207:__setup("noautogroup", setup_autogroup);
./kernel/sched/idle.c:51:__setup("nohlt", cpu_idle_poll_setup);
./kernel/sched/idle.c:58:__setup("hlt", cpu_idle_nopoll_setup);
./kernel/reboot.c:557:__setup("reboot=", reboot_setup);
./kernel/cgroup/debug.c:383:__setup("cgroup_debug", enable_cgroup_debug);
./kernel/cgroup/cgroup.c:5558:__setup("cgroup_disable=", cgroup_disable);
./kernel/cgroup/cgroup-v1.c:1316:__setup("cgroup_no_v1=", cgroup_no_v1);
./kernel/capability.c:37:__setup("no_file_caps", file_caps_disable);
./kernel/hung_task.c:65:__setup("hung_task_panic=", hung_task_panic_setup);
./kernel/time/tick-sched.c:401:__setup("nohz_full=", tick_nohz_full_setup);
./kernel/time/tick-sched.c:506:__setup("nohz=", setup_tick_nohz);
./kernel/time/hrtimer.c:527:__setup("highres=", setup_hrtimer_hres);
./kernel/time/ntp.c:1035:__setup("ntp_tick_adj=", ntp_tick_adj_setup);
./kernel/time/clocksource.c:1051:__setup("clocksource=", boot_override_clocksource);
./kernel/time/clocksource.c:1070:__setup("clock=", boot_override_clock);
./kernel/audit.c:1581:__setup("audit=", audit_enable);
./kernel/audit.c:1601:__setup("audit_backlog_limit=", audit_backlog_limit_set);
./kernel/delayacct.c:35:__setup("nodelayacct", delayacct_setup_disable);
./kernel/watchdog.c:86:__setup("nmi_watchdog=", hardlockup_panic_setup);
./kernel/watchdog.c:96:__setup("hardlockup_all_cpu_backtrace=", hardlockup_all_cpu_backtrace_setup);
./kernel/watchdog.c:190:__setup("softlockup_panic=", softlockup_panic_setup);
./kernel/watchdog.c:197:__setup("nowatchdog", nowatchdog_setup);
./kernel/watchdog.c:204:__setup("nosoftlockup", nosoftlockup_setup);
./kernel/watchdog.c:214:__setup("softlockup_all_cpu_backtrace=", softlockup_all_cpu_backtrace_setup);
./kernel/fork.c:783:__setup("coredump_filter=", coredump_filter_setup);
./kernel/signal.c:1140:__setup("print-fatal-signals=", setup_print_fatal_signals);
./fs/dcache.c:3577:__setup("dhash_entries=", set_dhash_entries);
./fs/nfs/nfsroot.c:119:__setup("nfsrootdebug", nfs_root_debug);
./fs/nfs/nfsroot.c:156:__setup("nfsroot=", nfs_root_setup);
./fs/inode.c:1925:__setup("ihash_entries=", set_ihash_entries);
./fs/namespace.c:49:__setup("mhash_entries=", set_mhash_entries);
./fs/namespace.c:59:__setup("mphash_entries=", set_mphash_entries);
./init/main.c:163:__setup("reset_devices", set_reset_devices);
./init/main.c:342:__setup("init=", init_setup);
./init/main.c:354:__setup("rdinit=", rdinit_setup);
./init/main.c:794:__setup("initcall_blacklist=", initcall_blacklist);
./init/main.c:970:__setup("rodata=", set_debug_rodata);
./init/calibrate.c:23:__setup("lpj=", lpj_setup);
./init/do_mounts.c:52:__setup("load_ramdisk=", load_ramdisk);
./init/do_mounts.c:70:__setup("ro", readonly);
./init/do_mounts.c:71:__setup("rw", readwrite);
./init/do_mounts.c:299:__setup("root=", root_dev_setup);
./init/do_mounts.c:309:__setup("rootwait", rootwait_setup);
./init/do_mounts.c:332:__setup("rootflags=", root_data_setup);
./init/do_mounts.c:333:__setup("rootfstype=", fs_names_setup);
./init/do_mounts.c:334:__setup("rootdelay=", root_delay_setup);
./init/initramfs.c:522:__setup("retain_initrd", retain_initrd_param);
./init/do_mounts_md.c:281:__setup("raid=", raid_setup);
./init/do_mounts_md.c:282:__setup("md=", md_setup);
./init/do_mounts_initrd.c:35:__setup("noinitrd", no_initrd);
./init/do_mounts_rd.c:35:__setup("prompt_ramdisk=", prompt_ramdisk);
./init/do_mounts_rd.c:44:__setup("ramdisk_start=", ramdisk_start_setup);
./net/ethernet/eth.c:67:__setup("ether=", netdev_boot_setup);
./net/ipv4/ipconfig.c:1692:__setup("ip=", ip_auto_config_setup);
./net/ipv4/ipconfig.c:1698:__setup("nfsaddrs=", nfsaddrs_config_setup);
./net/ipv4/ipconfig.c:1709:__setup("dhcpclass=", vendor_class_identifier_setup);
./net/ipv4/tcp.c:3459:__setup("thash_entries=", set_thash_entries);
./net/ipv4/tcp_metrics.c:994:__setup("tcpmhash_entries=", set_tcpmhash_entries);
./net/ipv4/udp.c:2800:__setup("uhash_entries=", set_uhash_entries);
./net/core/dev.c:671:__setup("netdev=", netdev_boot_setup);
./block/blk-core.c:1935:__setup("fail_make_request=", setup_fail_make_request);
./block/elevator.c:137:__setup("elevator=", elevator_setup);
./block/partitions/efi.c:118:__setup("gpt", force_gpt_fn);
./block/partitions/cmdline.c:59:__setup("blkdevparts=", cmdline_parts_setup);
./block/blk-timeout.c:20:__setup("fail_io_timeout=", setup_fail_io_timeout);
./lib/locking-selftest.c:41:__setup("debug_locks_verbose=", setup_debug_locks_verbose);
./lib/fault-inject.c:14: * setup_fault_attr() is a helper function for various __setup handlers, so it
./lib/fault-inject.c:15: * returns 0 on error, because that is what __setup handlers do.
./lib/dma-debug.c:1077:__setup("dma_debug=", dma_debug_cmdline);
./lib/dma-debug.c:1078:__setup("dma_debug_entries=", dma_debug_entries_cmdline);
./lib/dma-debug.c:1736:__setup("dma_debug_driver=", dma_debug_driver_setup);
./lib/dynamic_debug.c:648:__setup("ddebug_query=", ddebug_setup_query);
./mm/slab.c:505:__setup("noaliencache", noaliencache_setup);
./mm/slab.c:516:__setup("slab_max_order=", slab_max_order_setup);
./mm/slab_common.c:64:__setup("slab_nomerge", setup_slab_nomerge);
./mm/failslab.c:39:__setup("failslab=", setup_failslab);
./mm/memory_hotplug.c:85:__setup("memhp_default_state=", setup_memhp_default_state);
./mm/memory.c:125:__setup("norandmaps", disable_randmaps);
./mm/kasan/report.c:382:__setup("kasan_multi_shot", kasan_set_multi_shot);
./mm/huge_memory.c:475:__setup("transparent_hugepage=", setup_transparent_hugepage);
./mm/mmap.c:2403:__setup("stack_guard_gap=", cmdline_parse_stack_guard_gap);
./mm/page_alloc.c:2883:__setup("fail_page_alloc=", setup_fail_page_alloc);
./mm/page_alloc.c:7205:__setup("hashdist=", set_hashdist);
./mm/mempolicy.c:2544:__setup("numa_balancing=", setup_numabalancing);
./mm/slub.c:1290:__setup("slub_debug", setup_slub_debug);
./mm/slub.c:3745:__setup("slub_min_order=", setup_slub_min_order);
./mm/slub.c:3755:__setup("slub_max_order=", setup_slub_max_order);
./mm/slub.c:3764:__setup("slub_min_objects=", setup_slub_min_objects);
./mm/slub.c:4762:__setup("slub_memcg_sysfs=", setup_slub_memcg_sysfs);
./mm/memcontrol.c:5917:__setup("cgroup.memory=", cgroup_memory);
./mm/memcontrol.c:6172:__setup("swapaccount=", enable_swap_account);
./mm/hugetlb.c:2881:__setup("hugepages=", hugetlb_nrpages_setup);
./mm/hugetlb.c:2888:__setup("default_hugepagesz=", hugetlb_default_setup);


./arch/arm/plat-iop/pci.c:403:__setup("iop3xx_init_atu", iop3xx_init_atu_setup);
./arch/arm/kernel/setup.c:78:__setup("fpe=", fpe_setup);
./arch/arm/kernel/traps.c:62:__setup("user_debug=", user_debug_setup);
./arch/arm/mach-s3c24xx/mach-qt2410.c:303:__setup("tft=", qt2410_tft_setup);
./arch/arm/mach-s3c24xx/mach-jive.c:267:__setup("mtdset=", jive_mtdset);
./arch/arm/mach-s3c24xx/mach-mini2440.c:576:__setup("mini2440=", mini2440_features_setup);
./arch/arm/mm/init.c:812:__setup("keepinitrd", keepinitrd_setup);
./arch/arm/mm/alignment.c:985:__setup("noalign", noalign_setup);
./arch/arm/mm/mmu.c:240:__setup("noalign", noalign_setup);
```

# 常用的bootargs

但是我还是总结一下常用的setup。

分别分布在这么几大块。

## 调试打印

1、console=

## nfs相关

nfsroot=

## 初始化相关

init=
rdinit=
initcall_blacklist=
rodata=
lpj=
ro
rw
root=
rootwait
rootflags=
rootfstype=
rootdelay=
noinitrd

## 网络相关

ether=
ip=
netdev=

## 用户自定义



# /proc/cmdline和bootargs



在linux启动时候，串口log中会打印cmdline

```
[    0.000000] c0 0 (swapper) Kernel command line: earlycon androidboot.selinux=permissive uart_dma keep_dbgclk_on clk_ignore_unused initrd=0xd0000000,38711808 rw crash_page=0x8f040000 initrd=/recoveryrc boot_reason=0x2000 ota_status=0x1001
```

在linux启动完成后，通过 cat /proc/cmdline也是可以看到cmdline. 那么cmdline是如何添加的呢？

(1)、 在dts中的bootargs中添加

```
/ {
    model = "yyyyyyy";
    compatible = "yyyyyyy", "xxxxxxxx";

    chosen {
        /*
         * initrd parameters not set in dts file since the ramdisk.img size
         * need to check in uboot, and the initrd load address and size will
         * set in uboot stage.
         */
        bootargs = "earlycon androidboot.selinux=permissive uart_dma keep_dbgclk_on clk_ignore_unused";
        stdout-path = "serial0:115200";
    };
......
}

```

(2)、在uboot中添加

u-boot/common/cmd_bootm.c

```
append_bootargs("recovery=1");

sprintf(dm_buf,"init=/init skip_initramfs rootwait root=/dev/dm-0 dm=\"system none ro,0 1 android-verity /dev/mmcblk0p%d\"",ret);
append_bootargs((const char *)dm_buf);

```

(3)在mkbootimg的参数里添加

```
INTERNAL_BOOTIMAGE_ARGS += --cmdline "$(INTERNAL_KERNEL_CMDLINE)"
```



在跳转linux kernel之前(如uboot中)，

**将cmdline数据放到了FDT中，**

然后将FDT的地址写入到了X0中。

然后再跳转linux kernel.



别问我怎么知道的，请看kernel-4.14/Documentation/arm64/booting.txt

linux kernel从stext开始启动，整个流程大概就是读取X0(FDT地址)保存到X21中，又将X21保存到`__fdt_pointer`全局变量中
然后再将`__fdt_pointer`解析处**cmdline数据到boot_command_line全局变量中**

在setup_arch()的时候，调用setup_machine_fdt将fdt解析到了boot_command_line全局变量中

```
在start_kernel()打印了cmdline.
asmlinkage __visible void __init start_kernel(void)
{
…
pr_notice(“Kernel command line: %s\n”, boot_command_line);
…
}
```



参考资料

1、

https://blog.csdn.net/weixin_42135087/article/details/107957684



https://blog.csdn.net/TommyMusk/article/details/103946029



# boot_command_line

全局变量

1.command_line

2.default_command_line

3.saved_command_line

内核参数的解析一共有两处，一处是setup_arch()->parse_cmdline()用于解析内核参数中关于内存的部分，另外一处是start_kernel()->parse_option()用于解析其余部分。

根据执行的先后顺序，可以将处理函数分为三个大类，他们分别存在于下面三个段：

```cpp
__setup_start = .; *(.init.setup) __setup_end = .;
__early_begin = .; *(.early_param.init) __early_end = .;
__start___param = .; *(__param) __stop___param = .;
```

这三个段存储的不是参数，而是command line参数所需要的处理函数。

1 .early_param.init段

它所处理的参数例如：initrd=, cachepolicy=, nocache, nowb, ecc=, vmalloc=, mem=等等。

这些处理函数是通过__early_param宏来定义的，例如：





参考资料

1、Linux command line详细解析

https://blog.csdn.net/CHS007chs/article/details/80743624

# 参考资料

1、

https://blog.csdn.net/skyflying2012/article/details/41142801

2、

https://blog.csdn.net/Industio_CSDN/article/details/122035752

3、

https://www.cnblogs.com/eleclsc/p/11444898.html