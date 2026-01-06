---
title: gcc的原子操作学习
date: 2025-12-02 20:15:37
tags:
	- gcc
---

--

# 基本例子

### 基础例子：线程安全的整数加1

```
// atomic_demo.c
#include <stdio.h>
#include <stdatomic.h>
#include <pthread.h>

// 使用 volatile + _Atomic 推荐写法（C11 风格）
_Atomic int counter = 0;          // 原子变量

// 或者纯 GCC 写法（不依赖 C11）
// volatile int counter = 0;

#define N_THREADS   4
#define N_INCREMENTS 1000000

void* thread_func(void* arg) {
    for (int i = 0; i < N_INCREMENTS; i++) {
        // 方法1：推荐的 __atomic 内置函数（GCC 4.8+）
        __atomic_fetch_add(&counter, 1, __ATOMIC_RELAXED);
        
        // 方法2：老式的 __sync 内置函数（兼容性更好，但功能弱）
        // __sync_fetch_and_add(&counter, 1);
        
        // 方法3：最明确指定内存序（推荐用于学习）
        // __atomic_fetch_add(&counter, 1, __ATOMIC_SEQ_CST);
    }
    return NULL;
}

int main() {
    pthread_t threads[N_THREADS];
    
    for (int i = 0; i < N_THREADS; i++) {
        pthread_create(&threads[i], NULL, thread_func, NULL);
    }
    
    for (int i = 0; i < N_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    
    printf("预期结果: %d\n", N_THREADS * N_INCREMENTS);
    printf("实际结果: %d\n", counter);
    
    if (counter == N_THREADS * N_INCREMENTS) {
        printf("原子操作成功！没有发生数据竞争\n");
    } else {
        printf("出现数据竞争！说明没有正确使用原子操作\n");
    }
    
    return 0;
}
```

### 编译命令（强烈建议加上 -pthread）

```
# 推荐的编译方式（开启多线程支持）
gcc -o atomic_demo atomic_demo.c -pthread -O2 -std=c11

# 如果你想对比“没开原子操作会出错”，可以故意注释掉原子函数，改成普通 counter++
# 再用下面命令编译（不优化也容易看出问题）
gcc -o atomic_demo atomic_demo.c -pthread
```

### 常用的 __atomic 原子操作速查（重点记忆这几个）

| 操作              | 函数                                                         | 说明             |
| ----------------- | ------------------------------------------------------------ | ---------------- |
| 加法              | __atomic_fetch_add(&var, val, order)                         | 返回旧值         |
| 减法              | __atomic_fetch_sub(&var, val, order)                         | 返回旧值         |
| 自增（后置）      | __atomic_add_fetch(&var, 1, order)                           | 返回新值         |
| 比较并交换（CAS） | __atomic_compare_exchange_n(&var, &expected, desired, 0, success_order, fail_order) | 最强大的原子操作 |
| 加载              | __atomic_load_n(&var, order)                                 | 原子读取         |
| 存储              | __atomic_store_n(&var, val, order)                           | 原子写入         |

### 内存序（memory order）参数说明（初学先记住这两个）

- __ATOMIC_RELAXED：只保证原子性，不保证顺序（性能最高）
- __ATOMIC_SEQ_CST：顺序一致性（最强，最慢，默认推荐学习用）

等你跑通上面的例子并理解了“为什么需要原子操作”，我们下一步可以讲：

- CAS 实现无锁栈/队列
- ABA 问题
- 不同内存序的性能对比
