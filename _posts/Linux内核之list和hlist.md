---
title: Linux内核之list和hlist
date: 2021-03-04 17:57:51
tags:
	- Linux

---

--

# hlist

hlist也是 一种双向链表，

但不同于list_head，

它的头部只有一个指针，

常被用作哈希表的bucket数组，这样就可减少哈希bucket一半的内存消耗。

hlist的h就是表示hash。



`struct hlist_head` 是 Linux 内核中用于实现哈希表的链表头结构体。哈希表是一种常用的数据结构，它能够在平均情况下以 O(1) 时间复杂度进行查找、插入和删除操作。

`struct hlist_head` 的定义如下：

```
struct hlist_head {
    struct hlist_node *first;
};
```

其中，`first` 指向哈希桶中第一个节点的指针，如果哈希桶为空，则 `first` 为 NULL。

`struct hlist_head` 中还有一个指向下一个节点的指针 `next`，但它不是指向下一个哈希桶，而是指向哈希桶中下一个节点的指针。这是因为哈希表中每个桶可以有多个节点，而这些节点组成一个双向链表。因此，`struct hlist_head` 中包含了一个指向 `struct hlist_node` 的指针，用于链接哈希桶中的节点。

`struct hlist_node` 定义如下：

```
struct hlist_node {
    struct hlist_node *next, **pprev;
};
```

`next` 指向下一个节点，`pprev` 指向前一个节点的 `next` 指针。这样，`struct hlist_node` 就能够和其他节点链接起来，形成双向链表。

# hlist使用举例

下面是一个简单的例子，演示了如何使用 `struct hlist_head` 在 Linux 内核中实现一个简单的哈希表：

```
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/hash.h>
#include <linux/slab.h>
#include <linux/types.h>
#include <linux/list.h>

#define TABLE_SIZE 256

struct my_data {
    int key;
    char value[32];
    struct hlist_node node;
};

static struct hlist_head table[TABLE_SIZE];

static unsigned int my_hashfunc(int key)
{
    return hash_32(key, 32) % TABLE_SIZE;
}

static void my_insert(int key, const char *value)
{
    struct my_data *data = kmalloc(sizeof(struct my_data), GFP_KERNEL);
    unsigned int hashval = my_hashfunc(key);
    data->key = key;
    strcpy(data->value, value);
    INIT_HLIST_NODE(&data->node);
    hlist_add_head(&data->node, &table[hashval]);
}

static struct my_data *my_lookup(int key)
{
    struct my_data *data;
    unsigned int hashval = my_hashfunc(key);
    hlist_for_each_entry(data, &table[hashval], node) {
        if (data->key == key) {
            return data;
        }
    }
    return NULL;
}

static int __init my_init(void)
{
    int i;
    printk(KERN_INFO "Initializing my module\n");
    for (i = 0; i < TABLE_SIZE; i++) {
        INIT_HLIST_HEAD(&table[i]);
    }
    my_insert(1, "Hello");
    my_insert(2, "World");
    return 0;
}

static void __exit my_exit(void)
{
    struct my_data *data, *tmp;
    int i;
    printk(KERN_INFO "Exiting my module\n");
    for (i = 0; i < TABLE_SIZE; i++) {
        hlist_for_each_entry_safe(data, tmp, &table[i], node) {
            hlist_del(&data->node);
            kfree(data);
        }
    }
}

module_init(my_init);
module_exit(my_exit);
MODULE_LICENSE("GPL");
```

上述代码定义了一个 `my_data` 结构体，包含了一个整型键值 `key` 和一个字符串值 `value`，并且包含了一个 `struct hlist_node` 成员 `node`，用于链接哈希桶中的节点。

哈希表的大小为 256，使用 `my_hashfunc` 函数将键值映射到桶中，然后使用 `hlist_add_head` 函数将节点添加到对应的桶中。

在 `my_lookup` 函数中，我们使用 `hlist_for_each_entry` 宏遍历哈希桶中的所有节点，并且比较键值来查找对应的节点。

在模块初始化函数 `my_init` 中，我们初始化所有的哈希桶，然后插入两个数据项：键值为 1，值为 "Hello"，以及键值为 2，值为 "World"。

在模块退出函数 `my_exit` 中，我们遍历所有的哈希桶，删除所有的节点并释放内存。

# list_for_each_entry

`list_for_each_entry` 是 Linux 内核中的一个宏，用于遍历一个给定类型的链表，并对每个链表节点执行操作。

该宏的语法如下：
```
list_for_each_entry(pos, head, member)
```

其中，`pos` 是链表节点的指针变量，`head` 是链表的头指针，`member` 是链表节点在结构体中的成员名。

使用 `list_for_each_entry` 宏可以方便地遍历一个链表，并对每个链表节点进行操作。在遍历过程中，宏会将 `pos` 指针依次指向链表的每个节点，可以通过 `pos` 指针访问节点的成员。

以下是一个示例用法，假设有一个名为 `my_list` 的链表，链表节点类型为 `struct my_struct`，其中 `node` 是链表节点在结构体中的成员：
```c
struct my_struct {
    int data;
    struct list_head node;
};

struct list_head my_list;

// 遍历 my_list 链表的每个节点，并打印数据
struct my_struct *pos;
list_for_each_entry(pos, &my_list, node) {
    printk("Data: %d\n", pos->data);
}
```

在上述示例中，`list_for_each_entry` 宏用于遍历 `my_list` 链表的每个节点，并通过 `pos` 指针访问节点的成员 `data`。在循环体内，可以对每个节点执行特定的操作，例如打印节点的数据。

需要注意的是，`list_for_each_entry` 宏是在 `linux/list.h` 头文件中定义的，因此在使用该宏之前，需要包含该头文件。此外，使用该宏时需要确保链表和节点的类型定义正确，并确保链表的头指针有效。



# 参考资料

1、

https://www.cnblogs.com/x_wukong/p/8506894.html

2、

https://blog.csdn.net/shenwanjiang111/article/details/105355016