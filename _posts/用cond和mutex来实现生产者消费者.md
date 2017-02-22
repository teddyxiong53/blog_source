---
title: 用cond和mutex来实现生产者消费者
date: 2017-02-19 23:23:44
tags:
---
代码如下：
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
