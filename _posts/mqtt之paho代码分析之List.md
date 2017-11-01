---
title: mqtt之paho代码分析之List
date: 2017-10-18 23:21:36
tags:
	- mqtt
	- iot
	- list

---



这个list是一个典型的双向链表，可以分析一下。

# 数据结构

最基础的是ListElement。

```
typedef struct ListElementStruct {
	struct ListElementStruct *prev, *next;
	void *content;
} ListElement;
```

由ListElement组成的List。

```
typedef struct 
{
	ListElement *first, *last, *current;
	int count;
	size_t size;
} List;

```

数据结构就这2个。

# 接口分析

1、ListInitialize

更加贴切的名字应该是：ListCreate。malloc了一个List的空间。顺便把空间清零了。

```
List* ListInitialize(void);
```

2、ListZero

```
void ListZero(List* newl)
```

就是调用了一下memset。

3、ListAppend

```
void ListAppend(List* aList, void* content, size_t size)
```

