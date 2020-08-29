---
title: Linux内存（六）
date: 2018-04-03 10:37:25
tags:
	- Linux内核

---



这篇文章是对《Linux内核设计与实现》第12章的总结。

在内核里分配内存，比在用户态里分配内存要复杂许多。

导致这种问题的原因有：

1、根本原因是内核空间不能像用户空间那样奢侈地使用内存。

2、内核一般不能睡眠。

3、处理内存分配错误，对于内核也不是一件容易的事情。

4、内存分配机制不能太复杂。

所以，机制不能太复杂，复杂就转移到使用上来了。



# page

我们看看page对应的结构体。为了方便讨论，我去掉容易导致干扰的部分。

```
struct page {
  ulong flag;
  atomic_t _count;
  atomic_t _mapcount;
  ulong private;
  struct address_space *mapping;
  pgoff_t index;
  struct list_head lru;
  void *virtual;
};
```

我们看看其中比较重要的成员。

1、flag。

存放page的状态的，包括page是不是脏页、是不是被锁定在内存里，flag的每一个bit表示一种状态。

2、_count。

引用计数。等于-1时，表示内核还没有引用这一页。内核不应该直接访问这个成员，而是要用page_count()函数来访问。

3、virtual。

是页的虚拟地址。对于高端内存，并没有固定映射，它的virtual就是NULL。



内核可以通过page获取到什么信息？

1、页是不是空闲的。

2、如果不是空闲的，是谁占用了这个页。

3、占有页的可能是 ：用户进程、动态的内核数据、静态内核代码、page cache。

# zone

因为硬件的限制，内核不能对所有的page一视同仁。

有些page在特定的物理地址上，用途受到限制。

所以，内核就引入了zone的概念，对page进行分类。

导致问题的原因有：

1、一些硬件只能用特定地址的内存进行dma操作。

2、物理内存太大，超过了虚拟地址空间。

所以呢，就划分了这4种zone：

1、ZONE_DMA。

2、ZONE_DMA32。

3、ZONE_NORMAL。

4、ZONE_HIGHMEM。

zone跟CPU架构是相关的，有些架构可以都是ZONE_NORMAL。

在x86上，是这样的：

```
低于16M的部分  ZONE_DMA
16M到896M     ZONE_NORMAL
高于896M的    ZONE_HIGHMEM
```

# 拿到一个page

最核心的函数是alloc_pages。

所有的api有这些：

```
1、struct page *alloc_page(mask) //分配一页。返回值是page指针。
2、ulong get_zeroed_page(mask) //分配一页，并且清零
3、struct page *alloc_pages(mask, order) //分配多页
4、ulong __get_free_page(mask) //返回值是ulong的。
5、ulong __get_free_pages(mask, order)
```

释放的API：

```
void free_page(ulong addr);
void free_pages(ulong addr, order);
void __free_pages(struct page *page, order);
```

错误的释放，会导致内核挂掉的。内核是完全信任自己的。

## mask的分类

内核里分配内存，跟用户空间的不同就是，它多了一个mask参数。

这些mask可以分为3类：

1、行为修饰符。

2、区域修饰符。

3、类型。

###行为修饰符有：

```
__GFP_WAIT：可以睡眠。
__GFP_HIGH：可以从紧急事件缓冲池里获取。
__GFP_IO：可以启动磁盘IO。
__GFP_FS：可以启动文件系统io
__GFP_COLD：使用cache里快啊哟淘汰出去的page
__GFP_NOWARN：不要打印失败警告。
__GFP_REPEAT：分配失败的时候，再分配一次，不过一般还是会失败的 。
__GFP_NOFALL：一直分配到成功为止。
__GFP_NORETRY：分配失败的时候，绝不会重新分配。
__GFP_NO_GROW：在slab里内部使用。
```

用法举例：

```
ptr = kmalloc(size, __GFP_WAIT | __GFP_IO | __GFP_FS);
```

说明可以阻塞，执行IO，必要时还可以执行文件系统操作。这就给了内核很大的宽容，内核可以想办法给你找到空闲的内存。

### zone修饰符

```
__GFP_DMA
__GFP_DMA32
__GFP_HIGHMEM：这个可以从normal或者highmem分配。
```

优先从normal区域分配。

kmalloc不能用highmem标志，因为返回的是逻辑地址。而不是page指针。

实际上，你不指定就是最好的选择。

### 类型标志

```\
GFP_ATOMIC：在中断、底半部等不能睡眠的地方。
GFP_NOWAIT：和GFP_ATOMIC类似，不同的是，不会从紧急内存池分配，这就增加了分配失败的可能性。
GFP_NOIO
GFP_NOSYS
GFP_KERNEL：最常用的就是这个。可能会阻塞。
GFP_USER：给用户进程分配内存。
GFP_HIGHUSER：从highmem分配用户空间进程的内存。
GFP_DMA
```

上面这些标准，类型标志，是给开发者用的。带下划线的尽量别去用。

类型标志是对上面的封装。

```
#define GFP_KERNEL	(__GFP_WAIT | __GFP_IO | __GFP_FS)
```

所以，结论就是经常用GFP_KERNEL和GFP_ATOMIC这2个。

# vmalloc

vmalloc是通过分配非连续的物理page，再“修正”页表，把内存映射到逻辑地址空间的连续区域内，这样就在逻辑地址上是连续的了。

为了这种连续，需要专门建立页表项。

糟糕的是，通过vmalloc获取到的page必须要一个个单独进行映射，因为物理上不连续，这就导致了比直接内存映射大得多的TLB抖动。

**vmalloc是在不得已的时候采用。就是要获取大块内存的时候。**

# slab层

为了便于数据的频繁分配和回收，需要引入空闲链表。

**空闲链表是用来存放已经加工好的结构体，你要用的时候，就从里面取一个出来用就好了。**

**省去了初始化这个加工过程。**

你不用的时候，直接放回去就好了。不要砸掉（就是销毁释放）。

空闲链表就是kmem_cache。

这样解决了这么几个问题：

1、频繁分配释放带来的内存碎片问题。

2、频繁初始化带来的性能问题。

## slab层的设计

slab层把不同的对象划分为不同的cache组。

例如task_struct组、inode组。

kmalloc的内存，是里面的通用组。

我们以inode为例进行分析，inode代表的内涵是磁盘索引节点在内存里的体现。

struct inode由inode_cachep（这个是按规范命名的）来进行分配。

struct kmem_cache，这个结构体包含了3个链表，slabs_full、slabs_partial、slabs_empty。

都放在kmem_list3这个结构体里。

```
struct kmem_list3 *nodelists[MAX_NUMNODES];
```

```
struct kmem_list3 {
	struct list_head slabs_partial;	/* partial list first, better asm code */
	struct list_head slabs_full;
	struct list_head slabs_free;
```

slab存在的意义，就是要减少page的分配和释放。

## slab分配器的接口

1、创建一个cache。

```
struct kmem_cache *kmem_cache_create(char *name, size, align, flags, ctor_func);
```

flags的取值一般有：

```
SLAB_HWCACHE_ALIGN：把一个slab里所有的对象，按照cacheline进行对齐。可以提高性能，但是会增加内存消耗。
SLAB_POISON：slab填入0xa5这种值。这就是所谓的“中毒”，可以用来判断是否已经被初始化过。
SLAB_RED_ZONE：在已经分配的内存附近插入红色警戒区，用来探测越界行为。
SLAB_PANIC：在分配失败的时候，提醒slab层。在只许成功不许失败的地方用。
SLAB_CACHE_DMA：一般别用。
```

ctor_func：是cache的构造函数。只有在需要追加新的页到cache的时候，才被调用。

但是这个已经被内核抛弃了。不用了。

2、销毁。

```
int kmem_cache_destroy(struct kmem_cache *cachep);
```

要使用这个函数，要满足2个条件：

```
1、这个cache里的slab都是空的。
2、在kmem_cache_destroy的过程中，不再访问这个cache。
```

3、分配和释放。

```
void *kmem_cache_alloc(cachep, flags)
void kmem_cache_free(cachep, void *objp);
```

下面，我们用task_struct对应的cache来进行分析。

1、首先，定义一个全局的指针。

```
struct kmem_cache *task_struct_cachep;
```

2、在内核初始化的时候，fork_init里面。

```
task_struct_cachep = kmem_cache_create("task_struct", sizeof(struct task_struct), L1_CACHE_BYTES, SLAB_PANIC|SLAB_NOTRACK, NULL);
```

3、当调用fork的时候，在do_fork里会：

```
struct task_struct *tsk;
tsk = kmem_cache_alloc(task_struct_cachep, GFP_KERNEL);
```

进程执行完成后，如果没有子进程在等待的话，对应的task_struct就会被释放。

```
kmem_cache_free(task_struct_cachep, tsk);
```



# 在栈上分配内存

在用户空间，我们可以很奢侈地使用栈空间，因为用户空间的栈很大，而且可以动态增加。

内核里却不能这么做，内核里的栈是固定而且很小的。

所以绝对不允许递归。

栈溢出的时候，悄无声息，但是肯定会引起严重的问题。

最好的情况是挂掉，最坏的情况是破坏你的磁盘数据。

# 高端内存

高端内存的page，不可能有逻辑地址。

如果要映射一个给定的page到内核地址空间。可以用kmap这个函数。

这个函数定义在highmem.c里。

```
void *kmap(struct page *page)
{
	might_sleep();
	if (!PageHighMem(page))
		return page_address(page);
	return kmap_high(page);
}
```

可以看出，它其实也可以用在低端内存上。这样就是直接返回页的逻辑地址。

kmap只能用在进程上下文。因为会睡眠。

永久映射数量是有限的，你不用的时候，就kunmap掉。

如果你要创建一个映射，又不想睡眠，内核提供了临时映射的机制。也叫原子映射。

有一组保留的映射。

临时映射使用的函数是：

```
void *kmap_atomic(struct page *page, enum km_type type);
```

# per-cpu分配

一般来说，per-cpu数据放在一个数组里，CPU核心号，就是数组里的索引值。

这种其实是老的用法。但是还可以用。典型的用法是这样。

```
unsigned long xxx_percpu[NR_CPUS];
int cpu;
cpu = get_cpu();//获得当前的cpu，并且禁止内核抢占。
func(xxx_percpu[cpu]);
put_cpu();//激活内核抢占。
```

这里没有加锁，因为没有必要，是安全的。

内核在2.6版本，引入的新的per-cpu接口。

1、定义。

```
DEFINE_PER_CPU(type, name);
```

2、操作。

```
get_cpu_var(name)++;
put_cpu_var(name);
```

你还可以指定操作某个核心上的数据。不过慎用。

```
per_cpu(name, cpu)++;//
```

3、动态分配per-cpu。

```
void *alloc_percpu(type);
void free_percpu(void *);
```

## 使用per-cpu的好处

1、减少了数据的锁定。

2、减少了每个核心的cache失效的可能性。

唯一的要求就是调度要上锁，这个代价很小。













