---
title: gcc之attribute了解
date: 2019-08-12 17:49:28
tags:
	 - gcc

---

1

# constructor属性

用这个属性修饰的，不需要你明确调用，会在main函数执行前被调用。

构造和析构的顺序是反的。0到100的被保留。

```
#include <stdio.h>

static __attribute__((constructor(101))) void constructor_101()
{
  printf("%s\n", __func__);
}
static __attribute__((constructor(102))) void constructor_102()
{
  printf("%s\n", __func__);
}


static __attribute__((destructor(101))) void destructor_101()
{
  printf("%s\n", __func__);
}
static __attribute__((destructor(102))) void destructor_102()
{
  printf("%s\n", __func__);
}
int main()
{
  printf("main\n");
}
```

打印：

```
constructor_101
constructor_102
main
destructor_102
destructor_101
```



参考资料

1、

https://www.jianshu.com/p/dd425b9dc9db