---
title: C语言之可变参数
date: 2018-09-22 11:58:17
tags:
	- Linux

---



一直很少字节写C语言的可变参数函数，但是看printf函数的实现，就必须把这个点搞懂。

现在深入学习一下。

先看一个简单的例子。

```
#include <stdio.h>
#include <stdarg.h>
int var_param_test(int num ,...)
{
    int i;
    int ret = 0;
    va_list vl;//实际上就是char *
    va_start(vl, num);
    printf("num:%d, vl:%d\n", num, *vl);
    for(i=0; i<num-1; i++) {
        ret = va_arg(vl, int);
        printf("ret:%d, *vl:%d\n",ret, *vl);
    }
    va_end(vl);
    return ret;

}
int main()
{
    var_param_test(5,1,2,3,4,5);

}

```

运行结果。

```
num:5, vl:1
ret:1, *vl:2
ret:2, *vl:3
ret:3, *vl:4
ret:4, *vl:5
```



至少有一个参数。例如printf，至少有一个fmt参数。





# 参考资料

