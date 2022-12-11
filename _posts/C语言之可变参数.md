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



`...`是占位符。要求至少有一个参数。例如printf，至少有一个fmt参数。

要有机制可以确定可变参数的个数，例如printf的fmt里，就可以通过%d这种格式符号的格式来获取后面实际传递的参数个数。

如果读者对cpu有相当的了解，或者对C语言的函数调用约定非常熟悉，那么用C语言结合汇编来写一个可变参数函数并不难。

但是用到汇编的话，可移植性就很差。

所以ansi C就指定了可移植的可变参数函数的标准。

这个标准包括一个stdarg.h头文件。这个文件里提供了3个宏和一个数据类型。

三个宏：

```
void va_start(va_list ap, last);
type va_arg(va_list ap, type);
void va_end(va_list ap);
```

一个数据类型：

```
va_list
```



void va_start(va_list ap, last);

last是指三个点前面的最后一个参数。

va_arg这个宏，用来获取下一个参数的值。



# 发现我不能理解这个

```
#define QUOTE(...) #__VA_ARGS__
static const char *lua_code = QUOTE(
print("Hello, Lua C API")\n
print("Hello, Lua C API")\n
print("Hello, Lua C API")\n
);

int main(int argc, char const *argv[])
{
    printf("%s", lua_code);
    return 0;
}
```

`#define QUOTE(...) #__VA_ARGS__`这个用法挺神奇的。

发现可变参数这个，我还根本没有搞懂。

需要专门抽时间再研究一下。





# 参考资料

1、揭密X86架构C可变参数函数实现原理

https://blog.csdn.net/linyt/article/details/79772742

2、亲密接触C可变参数函数

https://blog.csdn.net/linyt/article/details/2243605