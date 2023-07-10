---
title: ringbuffer环形缓冲区
date: 2023-07-06 16:24:43
tags:
	- 基础

---

--

# ringbuffer介绍

环形缓冲区（Ring Buffer），也称为循环缓冲区或循环队列，是一种常用的数据结构，用于在固定大小的缓冲区中循环存储数据。它具有高效的读写性能，特别适用于在生产者和消费者之间传递数据的场景。

环形缓冲区的特点包括：

1. 固定大小：环形缓冲区有一个预定义的固定大小，通常是2的幂，例如64、128、256等。这样的大小选择有助于使用位运算来实现循环的索引操作，提高性能。

2. 循环存储：环形缓冲区通过使用两个指针（读指针和写指针）来实现循环存储。当读或写指针到达缓冲区的末尾时，它们会回到缓冲区的开头。这样就可以循环使用缓冲区，而不需要移动数据。

3. 高效读写：由于环形缓冲区的读写指针可以循环移动，读写操作可以在常数时间内完成。这使得环形缓冲区在高吞吐量的数据传输场景中非常高效。

4. 生产者-消费者模式：**环形缓冲区通常用于生产者-消费者模式**，其中一个或多个生产者将数据写入缓冲区，一个或多个消费者从缓冲区读取数据。环形缓冲区通过使用互斥锁或信号量等同步机制来实现生产者和消费者之间的线程安全。

5. 容易实现：**环形缓冲区的实现相对简单，通常使用数组作为底层数据存储，配合指针操作来管理数据的读写位置。**

环形缓冲区在许多应用中都有广泛的应用，特别适合用于实时数据处理、嵌入式系统、网络数据传输和音视频处理等场景，其中需要高效的数据传输和缓存。

# rt-thread里的实现

注释里有这个：

```
    /* use the msb of the {read,write}_index as mirror bit. You can see this as
     * if the buffer adds a virtual mirror and the pointers point either to the
     * normal or to the mirrored buffer. If the write_index has the same value
     * with the read_index, but in a different mirror, the buffer is full.
     * While if the write_index and the read_index are the same and within the
     * same mirror, the buffer is empty. The ASCII art of the ringbuffer is:
     *
     *          mirror = 0                    mirror = 1
     * +---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
     * | 0 | 1 | 2 | 3 | 4 | 5 | 6 ||| 0 | 1 | 2 | 3 | 4 | 5 | 6 | Full
     * +---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
     *  read_idx-^                   write_idx-^
     *
     * +---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
     * | 0 | 1 | 2 | 3 | 4 | 5 | 6 ||| 0 | 1 | 2 | 3 | 4 | 5 | 6 | Empty
     * +---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
     * read_idx-^ ^-write_idx
     *
     * The tradeoff is we could only use 32KiB of buffer for 16 bit of index.
     * But it should be enough for most of the cases.
     *
     * Ref: http://en.wikipedia.org/wiki/Circular_buffer#Mirroring */
```

gpt解释是：

该注释解释了一个环形缓冲区（Ring Buffer）的实现，其中使用读索引（read_index）和写索引（write_index）来管理缓冲区中的数据。

该环形缓冲区使用索引的最高有效位（Most Significant Bit，MSB）作为镜像位（mirror bit）。可以将这个镜像位看作是缓冲区添加了一个虚拟的镜像，并且读取和写入指针分别指向正常的缓冲区或镜像缓冲区。如果写索引和读索引具有相同的值，但位于不同的镜像中，则表示缓冲区已满。而如果写索引和读索引相同且位于同一个镜像中，则表示缓冲区为空。

使用ASCII图示来表示环形缓冲区如下所示：

```
       mirror = 0                    mirror = 1
+---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
| 0 | 1 | 2 | 3 | 4 | 5 | 6 ||| 0 | 1 | 2 | 3 | 4 | 5 | 6 | Full
+---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
 read_idx-^                   write_idx-^

+---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
| 0 | 1 | 2 | 3 | 4 | 5 | 6 ||| 0 | 1 | 2 | 3 | 4 | 5 | 6 | Empty
+---+---+---+---+---+---+---+|+~~~+~~~+~~~+~~~+~~~+~~~+~~~+
read_idx-^ ^-write_idx
```

其中，`mirror = 0` 表示正常的缓冲区，`mirror = 1` 表示镜像缓冲区。读索引和写索引分别指向缓冲区中的数据位置。根据读索引和写索引的位置以及所处的镜像，可以判断缓冲区是满的还是空的。

该环形缓冲区的一个权衡是，由于使用了索引的高位作为镜像位，因此在16位的索引中只能使用32KiB的缓冲区。但是对于大多数情况来说，这应该已经足够使用了。

该实现参考了维基百科上关于环形缓冲区的文章，链接为：http://en.wikipedia.org/wiki/Circular_buffer#Mirroring

# glib ringbuffer使用

GLib库提供了一个称为GQueue的数据结构，可以用作环形缓冲区（ring buffer）。GQueue是一个双向链表，它提供了在队列的两端进行插入和删除操作的功能。

以下是使用GLib库中的GQueue实现环形缓冲区的示例：

```c
#include <glib.h>

int main() {
    GQueue* ringBuffer = g_queue_new();

    // 向环形缓冲区添加元素
    g_queue_push_tail(ringBuffer, "Element 1");
    g_queue_push_tail(ringBuffer, "Element 2");
    g_queue_push_tail(ringBuffer, "Element 3");

    // 从环形缓冲区删除元素
    gchar* element = g_queue_pop_head(ringBuffer);
    g_print("Dequeued element: %s\n", element);
    g_free(element);

    // 获取环形缓冲区的长度
    gint length = g_queue_get_length(ringBuffer);
    g_print("Length of ring buffer: %d\n", length);

    // 清空环形缓冲区
    g_queue_clear(ringBuffer);

    // 释放环形缓冲区的内存
    g_queue_free(ringBuffer);

    return 0;
}
```

在上述示例中，首先使用 `g_queue_new()` 函数创建一个新的GQueue对象，表示环形缓冲区。

然后，使用 `g_queue_push_tail()` 函数将元素添加到环形缓冲区的尾部。

使用 `g_queue_pop_head()` 函数从环形缓冲区的头部删除一个元素，并返回被删除的元素。

通过 `g_queue_get_length()` 函数可以获取环形缓冲区的长度。

使用 `g_queue_clear()` 函数可以清空环形缓冲区中的所有元素。

最后，使用 `g_queue_free()` 函数释放环形缓冲区的内存。

需要在编译时链接GLib库，可以使用如下命令编译上述示例：

```
gcc -o ringbuffer ringbuffer.c `pkg-config --cflags --libs glib-2.0`
```

请确保已经正确安装GLib库。GLib库提供了许多其他功能和数据结构，可以根据需求进行扩展和调整环形缓冲区的实现。

# 一篇文章

https://embeddedartistry.com/blog/2017/05/17/creating-a-circular-buffer-in-c-and-c/

# gpt写一个简单的

```
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct {
    unsigned char *buffer;  // 缓冲区指针
    int size;               // 缓冲区大小
    int count;              // 缓冲区中元素的数量
    int head;               // 缓冲区的头部索引
    int tail;               // 缓冲区的尾部索引
} ringbuffer;

// 初始化环形缓冲区
void ringbuffer_init(ringbuffer *rb, int size) {
    rb->buffer = (unsigned char *)malloc(size * sizeof(unsigned char));
    rb->size = size;
    rb->count = 0;
    rb->head = 0;
    rb->tail = 0;
}

// 销毁环形缓冲区
void ringbuffer_destroy(ringbuffer *rb) {
    free(rb->buffer);
}

// 检查环形缓冲区是否为空
bool ringbuffer_is_empty(const ringbuffer *rb) {
    return rb->count == 0;
}

// 检查环形缓冲区是否已满
bool ringbuffer_is_full(const ringbuffer *rb) {
    return rb->count == rb->size;
}

// 向环形缓冲区中写入指定长度的数据
// 返回成功写入的元素数量
int ringbuffer_push(ringbuffer *rb, const unsigned char *data, int length) {
    if (ringbuffer_is_full(rb)) {
        return 0;  // 缓冲区已满，无法写入新元素
    }

    int elements_to_write = (length < rb->size - rb->count) ? length : (rb->size - rb->count);

    // 将数据写入环形缓冲区
    for (int i = 0; i < elements_to_write; i++) {
        rb->buffer[rb->tail] = data[i];
        rb->tail = (rb->tail + 1) % rb->size;  // 更新尾部索引
    }

    rb->count += elements_to_write;
    return elements_to_write;
}

// 从环形缓冲区中读取指定长度的数据
// 返回成功读取的元素数量
int ringbuffer_pop(ringbuffer *rb, unsigned char *data, int length) {
    if (ringbuffer_is_empty(rb)) {
        return 0;  // 缓冲区为空，无法读取元素
    }

    int elements_to_read = (length < rb->count) ? length : rb->count;

    // 从环形缓冲区中读取数据
    for (int i = 0; i < elements_to_read; i++) {
        data[i] = rb->buffer[rb->head];
        rb->head = (rb->head + 1) % rb->size;  // 更新头部索引
    }

    rb->count -= elements_to_read;
    return elements_to_read;
}

// 获取环形缓冲区中元素的数量
int ringbuffer_count(const ringbuffer *rb) {
    return rb->count;
}

// 环形缓冲区的简单测试程序
int main() {
    ringbuffer rb;
    ringbuffer_init(&rb, 10);

    unsigned char data[] = {0x11, 0x22, 0x33, 0x44, 0x55};
    int data_length = sizeof(data) / sizeof(data[0]);

    unsigned char read_data[10];

    // 写入数据
    int written = ringbuffer_push(&rb, data, data_length);
    printf("Elements written: %d\n", written);
    printf("Count: %d\n", ringbuffer_count(&rb));
    printf("head:%d, tail:%d\n", rb.head, rb.tail);
    // 读取数据
    int read = ringbuffer_pop(&rb, read_data, 3);
    printf("Elements read: %d\n", read);
    printf("Count: %d\n", ringbuffer_count(&rb));
    printf("head:%d, tail:%d\n", rb.head, rb.tail);
    // 再次写入数据
    unsigned char more_data[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};
    int more_data_length = sizeof(more_data) / sizeof(more_data[0]);
    written = ringbuffer_push(&rb, more_data, more_data_length);
    printf("Elements written: %d\n", written);
    printf("Count: %d\n", ringbuffer_count(&rb));
    printf("head:%d, tail:%d\n", rb.head, rb.tail);
    // 读取数据
    read = ringbuffer_pop(&rb, read_data, 10);
    printf("Elements read: %d\n", read);
    printf("Count: %d\n", ringbuffer_count(&rb));
    printf("head:%d, tail:%d\n", rb.head, rb.tail);
    ringbuffer_destroy(&rb);

    return 0;
}

```

