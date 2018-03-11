---
title: 数据结构之TAILQ
date: 2018-03-11 11:05:45
tags:
	- 数据结构
typora-root-url: ..\
---



在很多的代码里都看到tailq这种队列，不知跟一般的队列有什么不一样，现在分析一下。

tailq叫做尾队列。



我就以libevent里的为例。不过所有其他的也是这样的定义。

```
#define TAILQ_ENTRY(type)						\
struct {								\
	struct type *tqe_next;	/* next element */			\
	struct type **tqe_prev;	/* address of previous next element */	\
}
```

我的疑问就是，为什么prev指针，是一个二级指针？



我们先使用起来看看。

定义一个简单的结构体，把上面的内容嵌入进去。

```
struct int_node {
    int val;
    TALQ_ENTRY(int_node) next;
};
```

展开就是：

```
struct int_node {
    int val;
    struct {
        struct int_node *tqe_next;
        struct int_node **tqe_prev;
    } next;
};
```

另外，还有一个配套的结构体。TAILQ_HEAD。

```
#define TAILQ_HEAD(name, type) \
struct name {\
    struct type *tqh_first;\
    struct type **tqh_last;\
}
```

使用是这样：

```
TAILQ_HEAD(int_head, int_node) queue_head;
```

展开后是：

```
struct int_head {
    struct int_node *tqh_first;
    struct int_node *tqh_last;
} queue_head;
```



在内存里的情况是这样：

![tailq数据结构](/images/tailq数据结构.png)

操作步骤：

1、定义一个空的头指针。

```
TAILQ_HEAD(int_head, int_node) queue_head;
```

2、把这个队列头初始化一下。

```
TAILQ_INIT(&queue_head);
```

3、往tail上添加元素1 。

```
struct int_node node1;
node1.val = 1;
TAILQ_INSERT_TAIL(&queue_head, node1, next);
```

我们到这里调试一下看看。

```
#include <sys/queue.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

struct int_node {
    int val;
    TAILQ_ENTRY(int_node) next;
};

TAILQ_HEAD(int_head, int_node) queue_head;

void main()
{
    TAILQ_INIT(&queue_head);
    struct int_node node1;
    node1.val = 1;
    TAILQ_INSERT_TAIL(&queue_head, &node1, next);
    
    return 0;
}
```

```
Breakpoint 1, main () at test.c:16
warning: Source file is more recent than executable.
16          TAILQ_INIT(&queue_head);
(gdb) s
18          node1.val = 1;
(gdb) 
19          TAILQ_INSERT_TAIL(&queue_head, &node1, next);
(gdb) 
21          return 0;
(gdb) p queue_head
$1 = {tqh_first = 0x7efffbdc, tqh_last = 0x7efffbe0}
(gdb) p *queue_head.tqh_first 
$2 = {val = 1, next = {tqe_next = 0x0, tqe_prev = 0x20604 <queue_head>}}
```

4、我们接下来把node2和node3都加进去。

5、现在把元素遍历一遍。

```
void main()
{
    TAILQ_INIT(&queue_head);
    struct int_node node1,node2,node3;
    node1.val = 1;
    node2.val = 2;
    node3.val = 3;
    TAILQ_INSERT_TAIL(&queue_head, &node1, next);
    TAILQ_INSERT_TAIL(&queue_head, &node2, next);
    TAILQ_INSERT_TAIL(&queue_head, &node3, next);
    
    struct int_node *node_tmp;
    int i = 0;
    TAILQ_FOREACH(node_tmp, &queue_head, next) {
        printf("node[%d]:%d \n", i, node_tmp->val);
        i++;
    }
    return 0;
}
```

```
pi@raspberrypi:~/test/libevent$ ./a.out 
node[0]:1 
node[1]:2 
node[2]:3 
```

6、删除node2.

```
    printf("now delete node2:\n");
    TAILQ_REMOVE(&queue_head, &node2, next);
    i = 0;
    TAILQ_FOREACH(node_tmp, &queue_head, next) {
        printf("node[%d]:%d \n", i, node_tmp->val);
        i++;
    }
```

```
now delete node2:
node[0]:1 
node[1]:3 
```

7、在node3前面插入node4.

```
printf("insert node4 before node3 \n");
    struct int_node node4;
    node4.val = 4;
    TAILQ_INSERT_BEFORE(&node3, &node4, next);
    i = 0;
    TAILQ_FOREACH(node_tmp, &queue_head, next) {
        printf("node[%d]:%d \n", i, node_tmp->val);
        i++;
    }
```

```
insert node4 before node3 
node[0]:1 
node[1]:4 
node[2]:3 
```

# 相关话题

1、单向列表。SLIST

2、单向尾队列。

3、列表。list。

4、尾队列。



tailq在linux中没有看到使用。主要是bsd系统里的基础数据结构。

linux中都是用list的。





# 参考文章

1、

http://blog.csdn.net/hunanchenxingyu/article/details/8648794