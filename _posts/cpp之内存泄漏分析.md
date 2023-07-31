---
title: cpp之内存泄漏分析
date: 2018-11-15 14:45:17
tags:
	- cpp

---



# valgrind

就用valgrind来测试一下。

```
std::string g_str;
void main()
{
    g_str = std::string(100, 'a');
}
```

这样并不会内存泄漏。因为g_str不是一个指针。

而且我没有用new。所以也就不需要delete，也无法delete。

# mtrace

用mtrace来做。这个是原理的给malloc和free加上了钩子函数。

不行。我写了一个测试的c文件，是可以的。

放弃mtrace。

mtrace是一个用于检查C/C++程序中内存泄漏和其他内存错误的工具，它与C标准库中的malloc和free函数配合使用。以下是使用mtrace检查内存泄漏的步骤：

1. 在程序中调用mtrace函数：在程序中调用mtrace函数来启用内存跟踪功能，例如：

   `````
   #include <mcheck.h>
   mtrace();
   ```

   这将启用内存跟踪功能，并将所有分配和释放的内存块信息保存在一个跟踪文件中。mtrace函数应该在所有内存分配和释放操作之前调用。

2. 运行程序：使用编译器编译您的C/C++程序，并使用-g选项生成调试信息。然后运行程序，执行所有需要测试的操作。

3. 停止程序并调用muntrace函数：在程序正常退出或发生错误时，调用muntrace函数来停止内存跟踪，并将跟踪文件保存到磁盘上，例如：

   ````
   muntrace();
   ````

4. 分析跟踪文件：使用mtrace命令来分析跟踪文件，例如：

   ````
   mtrace your_program trace_file
   ````

   这将打印出分配和释放内存的详细信息，并标记任何未释放的内存块。您可以查看跟踪文件中的调用栈信息，以确定内存泄漏发生的位置和原因。

5. 修复错误并再次运行程序：一旦发现内存泄漏或其他内存错误，您可以尝试通过修改程序代码来修复错误。然后重新编译程序，并再次运行程序，以确保已经修复了所有的内存错误。

需要注意的是，mtrace工具只能用于检测通过C标准库中的malloc和free函数分配和释放的内存。在使用mtrace工具时，应该确保所有的内存分配和释放操作都是通过这些函数进行的，否则可能会导致检测不到内存泄漏或误报内存泄漏。



https://github.com/apachecn/apachecn-linux-zh/blob/master/docs/master-emb-linux-prog/18.md





# gperftools

这个是谷歌的工具。准确说是一组工具集。

使用了tcmalloc这个内存分配器。

主要有3个工具：

1、heap-profiler。内存监测。

2、heap-checker。检查内存泄漏。

3、cpu-profiler。cpu性能监测。

安装步骤

```
git clone https://github.com/gperftools/gperftools
cd gperftools
./autogen.sh
./configure
make -j8
sudo make install
```

```
git clone git://git.sv.gnu.org/libunwind.git
cd libunwind
./autogen.sh
./configure
make
make install
```

在代码里包含：

```
#include <google/profiler.h>
ProfilerStart("profiler");参数是文件名。随便写。
在适合的位置加上ProfilerStop();
连接加上-lprofiler。
```

然后执行程序，会生成一个profiler的文件。

执行下面的命令，生成统计图片。

```
pprof --gif ./dossos profiler > profiler.gif
```

需要先安装：

```
sudo apt-get install graphviz
```



内存泄漏检查

```
export PPROF_PATH=/usr/local/bin/pprof
```

```
sudo env HEAPCHECK=normal ./dossos
```

# 自己写一个简单的函数来调试内存泄漏

您可以编写一个记录malloc分配的内存的函数，并在程序退出时检查是否有未释放的内存块。以下是一个示例代码：

```
#include <stdio.h>
#include <stdlib.h>

// 定义一个链表节点结构体，用于记录每个分配的内存块
struct mem_block {
    void *addr; // 内存块的地址
    size_t size; // 内存块的大小
    struct mem_block *next; // 下一个内存块
};

static struct mem_block *mem_list = NULL; // 内存块链表头指针

// 自定义的分配内存的函数，记录每个分配的内存块
void *my_malloc(size_t size) {
    void *addr = malloc(size);
    if (addr != NULL) {
        // 分配成功，将该内存块添加到链表中
        struct mem_block *block = malloc(sizeof(struct mem_block));
        block->addr = addr;
        block->size = size;
        block->next = mem_list;
        mem_list = block;
    }
    return addr;
}

// 自定义的释放内存的函数，从链表中删除对应的内存块
void my_free(void *addr) {
    struct mem_block *prev = NULL;
    struct mem_block *curr = mem_list;
    while (curr != NULL) {
        if (curr->addr == addr) {
            // 找到了对应的内存块，从链表中删除
            if (prev == NULL) {
                mem_list = curr->next;
            } else {
                prev->next = curr->next;
            }
            free(curr);
            free(addr);
            return;
        }
        prev = curr;
        curr = curr->next;
    }
}

// 检查是否有未释放的内存块，并输出相关信息
void check_memory_leak() {
    struct mem_block *block = mem_list;
    while (block != NULL) {
        printf("Memory block at %p size %lu not freed\n", block->addr, block->size);
        block = block->next;
    }
}

// 示例程序
int main() {
    // 分配一些内存块
    int *p1 = my_malloc(sizeof(int));
    int *p2 = my_malloc(sizeof(int) * 10);
    char *p3 = my_malloc(100);

    // 释放一些内存块
    my_free(p2);
    my_free(p3);

    // 检查是否有未释放的内存块
    check_memory_leak();

    return 0;
}
```

在该示例代码中，my_malloc和my_free函数是自定义的分配和释放内存的函数，它们将所分配的内存块记录在一个链表中。在程序退出时，可以调用check_memory_leak函数检查是否有未释放的内存块，并输出相关信息。

请注意，该示例代码仅用于演示如何记录和检查分配的内存块，并不能完全替代Valgrind等专业的内存泄漏检测工具。使用自定义的函数记录内存块会增加代码的复杂度和开销，并且可能会忽略一些内存泄漏问题。因此，建议在开发过程中使用专业的内存泄漏检测工具，并在程序发布前进行彻底的测试和调试。

# 参考资料

1、警惕多线程环境string、vector、protobuf等自增长数据结构的隐性内存泄漏

https://blog.csdn.net/u011693064/article/details/72466171

2、google-gperftools分析代码时间分布

https://blog.csdn.net/oujiangping/article/details/77172802

3、gperftools工具检测内存泄漏

https://blog.csdn.net/zhengbin6072/article/details/80222639

4、tcmalloc安装与使用

https://blog.csdn.net/u011217649/article/details/77683126

5、tcmalloc使用的一点经验

http://blog.chinaunix.net/uid-20722087-id-5083864.html

6、C：使用mtrace、memwatch、dmalloc检测内存泄漏

https://my.oschina.net/letiantian/blog/754506