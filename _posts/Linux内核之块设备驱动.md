---
title: Linux内核之块设备驱动
date: 2018-04-06 16:48:25
tags:
	- Linux内核

---



一直没有去读一下Linux块设备的驱动代码。现在以软盘的为切入口，来对块设备驱动进行阅读。

# 什么是块设备

块设备是跟字符设备相对应的一种设备。

1、块设备只能以块为单位进行读写。

2、块设备对于io请求有对应的缓冲区。

3、块设备可以随机读写。但是一般为了提高效率，会调整为顺序读写。



# 怎样描述一个块设备？

用结构体struct block_device。这个跟struct char_device_struct是对应的。

```
1. dev_t bd_dev
2. int bd_openers
3. struct inode * bd_inode
4. struct super_block *bd_super
5. struct mutex bd_mutex
6. struct list_head bd_inodes
7. void * bd_claiming
8. void * bd_holder
9. int bd_holders
10. bool bd_write_holder
11. struct list_head bd_holder_disks
12. struct block_device *bd_contains
13. uint bd_block_size
14. struct hd_struct *bd_part
15. uint bd_part_count 
16. int bd_invalidated
17. struct gendisk *bd_disk
18. struct list_head bd_list
19. ulong bd_private
20. int bd_fsfreeze_count
21. struct mutex bd_fsfreeze_mutex
```



用一个struct gendisk来描述一个磁盘。磁盘是最主要的块设备了。定义在linux/gendisk.h里。

```
1. int major 
2. int first_minor 
3. int minors
4. char disk_name[]
5. char *(*devnode)(struct gendisk *gd, mode_t *mode)
6. uint events
7. uint async_events
8. struct disk_part_tbl *part_tbl
9. struct hd_struct part0
10. struct block_device_operations *fops
11. struct request_queue *queue
12. void *private_data 
13. int flags
14. struct device *driverfs_dev //to be removed
15. struct kobject *slave_dir
16. struct timer_rand_state *random;
17. atomic_t sync_io
18. struct disk_events *ev
19. int node_id
```

上面结构体里，struct block_device_operations是重要结构体。

```
1. open
2. release
3. ioctl
4. compat_ioctl
5. direct_access
6. check_events
7. media_change //这个是对于U盘和SD卡这种可插拔的设备。
8. unlock_native_capacity
9. revalidate_disk
10. getgeo
11. swap_slot_free_notify
12. struct module *owner
```



# 对gendisk的操作

1、分配。

```
struct gendisk *disk = alloc_disk(minor);
```

2、注册。

```
void add_disk(disk);
```

3、释放。

```
del_gendisk(disk)
```

4、引用计数。

```
struct kobject *get_disk(disk)
void put_disk(disk)
```

# 块设备的读写过程分析

读写的请求是struct request。定义在linux/blkdev.h里。

```
1. struct list_head queuelist;
2. struct call_single_data csd
3. struct request_queue *q;
4. uint cmd_flags
5. enum rq_cmd_type_bits cmd_type
6. ulong atomic_flags
7. int cpu
8. uint __data_len
9. sector_t __sector
10. struct bio *bio
11. struct bio *biotail
12. struct hlist_node hash
13. union {
  struct rb_node rb_node
  void *completion_data;
}
14. union {
  void *elevator_private[3]
  struct {
    uint seq
    struct list_head list
  } flush
}
15. struct gendisk *rq_disk;
16. struct hd_struct *part
17. ulong start_time
18. ushort nr_phys_segments
19. ushort ioprio
20. int ref_count
21. void *special
22. char *buffer
23. int tag
24. int errors
25. uchar __cmd[]
26. uchar *cmd
27. ushort cmd_len
28. uint extra_len, sense_len, resid_len
29. void *sense
30. ulong deadline
31. struct list_head timeout_list
32. uint timetout
33. int retries
34. rq_end_io_fn *endio
35. void *end_io_data
36. struct request *next_rq;
```

读写的基本单位是struct bio

```
1. sector_t bi_sector
2. struct bio *bi_next
3. struct block_device *bi_bdev
4. ulong bi_flags
5. ulong bi_rw
6. ushort bi_vcnt
7. ushort bi_idx
8. uint bi_phys_segments
9. uint bi_size
10. uint bi_seg_front_size, bi_seg_back_size
11. uint bi_max_vecs
12. uint bi_comp_cpu
13. aotmic_t bi_cnt
14. struct bio_vec *bi_io_vec
15. bio_end_io_t *bi_end_io
16. void *bi_private
17. bio_destructor_t *bi_destructor
18. struct bio_vec bi_inline_vecs[0]
```





# mtd和块设备关系

MTD  是一个虚拟层。

既提供了字符设备的操作接口， 也实现了块设备的操作接口。

提供的/dev/mtd0节点就是字符设备节点，对应的/dev/mtdblock0就是设备节点。实际上是同一个设备。

```
/ # ls /dev/mtd* -l
crw-rw----    1 0        0          90,   0 Mar 24  2018 /dev/mtd0
crw-rw----    1 0        0          90,   1 Mar 24  2018 /dev/mtd0ro
crw-rw----    1 0        0          90,   2 Mar 24  2018 /dev/mtd1
crw-rw----    1 0        0          90,   3 Mar 24  2018 /dev/mtd1ro
crw-rw----    1 0        0          90,   4 Mar 24  2018 /dev/mtd2
crw-rw----    1 0        0          90,   5 Mar 24  2018 /dev/mtd2ro
crw-rw----    1 0        0          90,   6 Mar 24  2018 /dev/mtd3
crw-rw----    1 0        0          90,   7 Mar 24  2018 /dev/mtd3ro
brw-rw----    1 0        0          31,   0 Mar 24  2018 /dev/mtdblock0
brw-rw----    1 0        0          31,   1 Mar 24  2018 /dev/mtdblock1
brw-rw----    1 0        0          31,   2 Mar 24  2018 /dev/mtdblock2
brw-rw----    1 0        0          31,   3 Mar 24  2018 /dev/mtdblock3
/ # 
```

# sbull

现在看ldd3的代码例子sbull来学习。



主要接口：

```
int register_blkdev(unsigned int major, const char *name);
	创建一个块设备。
unregister_blkdev(unsigned int major, const char *name);
	卸载一个块设备。

```



```
注册一个块设备驱动的流程：
1、创建一个块设备。
	sbull_major = register_blkdev(sbull_major, "sbull");
2、分配一个request_queue。
	dev->queue = blk_init_queue(sbull_request, &dev->lock);
3、分配一个gendisk。
	dev->gd = alloc_disk(SBULL_MINORS);
		SBULL_MINORS 这个参数表示对应设备可以有的分区数。
4、设置gendisk。
	dev->gd->major = sbull_major;
	dev->gd->first_minor = which*SBULL_MINORS;
	dev->gd->fops = &sbull_ops;
	set_capacity(dev->gd, nsectors*(hardsect_size/KERNEL_SECTOR_SIZE));
5、注册gendisk。
	add_disk(dev->gd);
	
```



```
主要涉及的结构体：
bio
	包含
	一个磁盘存储区标识符
	一个或多个描述与IO操作相关的内存区段（bio_vec数组）
	bio中的每个段是由一个bio_vec数据结构描述的
request
	request：一个request中包含了一个或多个bio
	为什么要有request这个结构呢？它存在的目的就是为了进行io的调度。
	通过request这个辅助结构，我们来给bio进行某种调度方法的排序，
	从而最大化地提高磁盘访问速度。
	
request_queue
	每个磁盘对应一个request_queue.该队列挂的就是request请求。
	
block_device

```



在通用块层启动一次新的IO操作时，会调用bio_alloc函数分配一个新的bio结构，bio是由slab分配器分配的。内核同时也为bio_vec结构分配内存池。

一个bio可能有很多个bio段，这些bio段可能在内存上不连续（位于不同的页），但他们在磁盘上对应的位置是连续的。

请求到达block层后，通过generic_make_request这个入口函数，
在通过调用一系列相关的函数把bio变成了request

具体的做法如下：
如果几个bio要读写的区域是连续的，
	即积攒成一个request
	（一个request上挂多个连续的bio，就是我们通常说的“合并bio请求”）
如果一个bio跟其他的bio都连不上
	那它就自己创建一个新的request，把自己挂在这个request下。

每个bio对应着一个连续的扇区段。故一个请求可以构造出多个bio。



# /proc/partitions

```
major minor  #blocks  name

 179        0    7634944 mmcblk0
 179        1       4096 mmcblk0p1
 179        2      65536 mmcblk0p2
 179        4       8192 mmcblk0p4
 179        5      32768 mmcblk0p5
 179        6       8192 mmcblk0p6
 179        7      65536 mmcblk0p7
 179        8    1048576 mmcblk0p8
 179        9    6311936 mmcblk0p9
```

# blkid

定位/打印块设备属性

```
# blkid 
/dev/system: TYPE="squashfs"
/dev/data: UUID="a20d2768-2408-48c1-8323-7d426a3510cc" BLOCK_SIZE="4096" TYPE="ext4"
```



# 参考资料

1、22.Linux-块设备驱动之框架详细分析(详解)

这篇文章的分析思路很清晰，贴代码的方式也很好，值得学习。

这个系列文章都不错。

https://www.cnblogs.com/lifexy/p/7651667.html

2、bio，request，request_queue的关系

https://blog.csdn.net/jasonLee_lijiaqi/article/details/82850689

3、

https://blog.csdn.net/gd0306/article/details/83244170