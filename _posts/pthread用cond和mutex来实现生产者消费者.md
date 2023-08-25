---
title: 用cond和mutex来实现生产者消费者
date: 2017-02-19 23:23:44
tags:
---
--

# 代码

```
#include <stdlib.h>
#include <pthread.h>
#include <stdio.h>

#define BUF_SIZE 16
#define OVER -1

struct prodcons 
{
	int buffer[BUF_SIZE];
	pthread_mutex_t lock;
	int writepos, readpos;
	pthread_cond_t notempty;
	pthread_cond_t notfull;
};

struct prodcons buffer;

static void init(struct prodcons * b)
{
	pthread_mutex_init(&b->lock, NULL);
	pthread_cond_init(&b->notempty, NULL);
	pthread_cond_init(&b->notfull, NULL);
	b->writepos = b->readpos = 0;
}


static void put(struct prodcons *b, int data)
{
	pthread_mutex_lock(&b->lock);
	while((b->writepos+1)%BUF_SIZE == b->readpos)
	{
		pthread_cond_wait(&b->notfull, &b->lock);
	}
	b->buffer[b->writepos++] = data;
	if(b->writepos >= BUF_SIZE)
	{
		b->writepos = 0;
	}
	pthread_cond_signal(&b->notempty);
	pthread_mutex_unlock(&b->lock);
	
}


void *producer(void *arg)
{
	int i;
	for(i=0; i<100; i++)
	{
		printf("%d --> \n", i);
		put(&buffer, i);
	}
	put(&buffer, OVER);
	return NULL;
}


static int get(struct prodcons *b)
{
	int data;
	pthread_mutex_lock(&b->lock);
	while(b->writepos == b->readpos)
	{
		pthread_cond_wait(&b->notempty, &b->lock);
	}
	data = b->buffer[b->readpos];
	b->readpos ++;
	if(b->readpos >= BUF_SIZE)
	{
		b->readpos = 0;
	}
	pthread_cond_signal(&b->notfull);
	pthread_mutex_unlock(&b->lock);
	return data;
}

void *consumer(void * arg)
{
	int d;
	while(1)
	{
		d = get(&buffer);
		if(d == OVER)
		{
			break;
		}
		printf("-->%d\n", d);
		
	}
	return NULL;
}

int main()
{
	pthread_t tha, thb;
	void *ret;
	init(&buffer);
	pthread_create(&tha, NULL, producer, 0);
	pthread_create(&thb, NULL, consumer, 0);
	pthread_join(tha, &ret);
	pthread_join(thb, &ret);
	printf("main thread exit \n");
	return 0;
}
```

# pthread为什么cond wait的时候，要先进行mutex lock

在使用 POSIX 线程库（pthread）中的条件变量（`pthread_cond_t`）时，使用 `pthread_cond_wait` 函数时需要先进行互斥锁（mutex）的加锁操作，有以下几个原因：

1. **确保同步：** 条件变量通常与互斥锁一起使用，以实现线程之间的同步。在等待条件变量时，线程需要首先获得互斥锁，以确保在等待条件变量时不会有其他线程修改相关的共享数据。

2. **避免竞态条件：** 如果在等待条件变量时不加锁，其他线程可能会同时修改条件并调用 `pthread_cond_signal` 或 `pthread_cond_broadcast`，导致信号丢失或条件不正确。通过加锁，可以防止这种竞态条件。

3. **防止虚假唤醒（Spurious Wakeup）：** 在某些情况下，线程可能会在没有满足条件的情况下被虚假地唤醒。在等待条件变量时加锁可以防止这种情况，因为只有在确保条件满足时才会进入等待状态。

综上所述，加锁是为了保护共享资源的一致性，避免竞态条件，并确保在等待条件变量时不会发生虚假唤醒。一般情况下，使用条件变量时，代码结构类似于：

```c
pthread_mutex_lock(&mutex);
while (!condition) {
    pthread_cond_wait(&cond, &mutex);
}
// 执行在条件满足后的操作
pthread_mutex_unlock(&mutex);
```

这种结构确保在等待条件变量时始终先获得互斥锁，以确保线程安全和正确的同步。

# wait的时候为什么要用while循环？直接wait不可以吗？

使用 `while` 循环来包裹 `pthread_cond_wait` 的主要目的是为了防止虚假唤醒（Spurious Wakeup）。虚假唤醒指的是在没有满足条件的情况下，线程被唤醒的现象。尽管这可能在某些情况下比较罕见，但为了确保程序的正确性和可靠性，我们应该考虑这种情况。

假设你在没有使用 `while` 循环的情况下使用 `pthread_cond_wait`，代码可能如下所示：

```c
pthread_mutex_lock(&mutex);
pthread_cond_wait(&cond, &mutex); // 等待条件满足
// 执行在条件满足后的操作
pthread_mutex_unlock(&mutex);
```

在这种情况下，如果有多个线程在等待相同的条件变量，当另一个线程调用 `pthread_cond_signal` 或 `pthread_cond_broadcast` 唤醒一个或多个等待线程时，被唤醒的线程可能会假设条件已满足，然后继续执行操作。但是，由于条件可能在线程被唤醒后并未真正满足，这可能导致错误的行为。

通过使用 `while` 循环，我们可以在线程被唤醒后再次检查条件，以确保条件真正满足。如果条件仍然不满足，线程会继续等待。这样可以防止虚假唤醒带来的问题，确保程序的正确性。

综上所述，虽然在大多数情况下虚假唤醒可能很少发生，但使用 `while` 循环来包裹 `pthread_cond_wait` 是一种良好的编程实践，可以提高代码的鲁棒性和可靠性。

# 什么情况下会出现虚假唤醒

虚假唤醒是在多线程编程中可能出现的一种情况，其中一个或多个线程在没有明确被唤醒的情况下，由于一些原因被意外地唤醒。这可能发生在使用条件变量进行线程同步时，尽管条件未满足，但线程仍然被唤醒。

虚假唤醒可能的原因包括：

1. **操作系统或线程库的实现：** 操作系统或线程库的实现可能会引入虚假唤醒。这可能是由于底层调度算法、线程调度策略或硬件中断等原因造成的。

2. **条件变量的使用不当：** 如果条件变量的使用不当，可能导致虚假唤醒。例如，在使用条件变量时没有使用 `while` 循环来检查条件是否真正满足，或者在使用 `pthread_cond_signal` 或 `pthread_cond_broadcast` 唤醒线程时没有正确设置条件。

3. **编译器优化：** 一些编译器可能对代码进行优化，可能会在不正确的时间点触发唤醒。

为了避免虚假唤醒，通常建议使用 `while` 循环来包裹等待条件变量的代码块，以确保条件满足后才执行后续操作。例如：

```c
pthread_mutex_lock(&mutex);
while (!condition) {
    pthread_cond_wait(&cond, &mutex);
}
// 执行在条件满足后的操作
pthread_mutex_unlock(&mutex);
```

这样可以在唤醒后再次检查条件，确保不会在条件未满足时执行操作。通过遵循这种惯例，可以防止虚假唤醒引起的问题，确保多线程程序的正确性和可靠性。