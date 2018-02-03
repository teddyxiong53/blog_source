---
title: rt-thread（十）调试初始化流程
date: 2018-02-03 16:13:45
tags:
	- rt-thread

---



对rt-thread进行menuconfig，把debug_init打开。

启动，看到开机打印如下：

```
do components intialization.
initialize rti_board_end:0 done
initialize lwip_system_initlwIP-2.0.2 initialized!
:0 done
initialize dfs_init:0 done
initialize rt_mmcsd_blk_init:0 done
initialize rt_mmcsd_core_init:0 done
initialize pl180_init:0 done
initialize rt_system_module_init:0 done
initialize dfs_romfs_init:0 done
initialize nfs_init:0 done
initialize dfs_ramfs_init:0 done
initialize elm_init:0 done
initialize dfs_jffs2_initinit jffs2 lock mutex okay
:0 done
initialize libc_system_init:0 done
initialize pthread_system_init:0 done
initialize clock_time_system_init:0 done
initialize rt_i2c_core_init:0 done
initialize mnt_initSD card capacity 1048576 KB
probe mmcsd block device!
xhl -- mount sd card 
file system initialization done!
xhl -- mount sd card end
:0 done
initialize smc911x_emac_hw_init:0 done
initialize finsh_system_init:0 done
hello rt-thread
```



rt-thread的初始化顺序是这样的：

```
rti_start		--> 0
BOARD_EXPORT	--> 1
rti_board_en	--> 1.end
DEVICE_EXPORT	--> 2
COMPONENT_EXPORT--> 3
FS_EXPORT		--> 4
ENV_EXPORT		--> 5
APP_EXPORT		--> 6
rti_end			--> 6.end
```

这个是靠INIT_EXPORT宏来做的。

```
struct rt_init_desc
{
  const char* fn_name;
  const init_fn_t fn;
};
#define INIT_EXPORT(fn, level)          \
const char __rti_##fn##_name[] = #fn; \
const struct rt_init_desc __rt_init_desc_##fn SECTION(".rti_fn."level) = \
{ __rti_##fn##_name, fn};
```

然后在链接脚本里。进行了排序。自然就按数字进行了排序了。

```
. = ALIGN(4);
__rt_init_start = .;
KEEP(*(SORT(.rti_fn*)))
__rt_init_end = .;
```

