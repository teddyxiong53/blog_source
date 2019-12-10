---
title: Linux内核之container_of宏分析
date: 2019-12-09 09:42:38
tags:
	 - Linux

---

1

container_of这个宏的作用是：

通过成员变量，拿到外层结构体。

```
container_of(ptr, type, member) 
3个参数：
	
```

先看一个代码。

```
#include <stdio.h>
 
#define offsetof(TYPE, MEMBER) ((size_t) &((TYPE *)0)->MEMBER)
 
struct test_struct {
    int num;
    char ch;
    float fl;
};
 
int main(void)
{
    printf("offsetof(struct test_struct, num) = %d\n",offsetof(struct test_struct, num));
    printf("offsetof(struct test_struct,  ch) = %d\n",offsetof(struct test_struct, ch));
    printf("offsetof(struct test_struct,  fl) = %d\n",offsetof(struct test_struct, fl)); 
    return 0;
}
```

这个的输出是：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
offsetof(struct test_struct, num) = 0
offsetof(struct test_struct,  ch) = 4
offsetof(struct test_struct,  fl) = 8
```



```
#include <stdio.h>

#define offsetof(TYPE, MEMBER) ((size_t) & ((TYPE *)0)->MEMBER)

#define container_of(ptr, type, member) ({	    \
	const typeof( ((type *)0)->member ) *__mptr = (ptr);    \
	(type *)( (char *)__mptr - offsetof(type,member) ); })

struct student
{
    char name[32];
    int age;
    double score;
};

int main(void)
{
    struct student *temp_jack;
    struct student jack = {"jack", 18, 89.4};
    int *page = &(jack.age);
    temp_jack = container_of(page, struct student, age);

    printf("jack's name is %s\n", temp_jack->name);
    printf("jack's age is %d\n", temp_jack->age);
    printf("jack's score is %.2f\n", temp_jack->score);

    return 0;
}

```



参考资料

1、Linux内核中的container_of函数简要介绍

https://blog.csdn.net/caihaitao2000/article/details/80559967