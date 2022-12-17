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

注：通过后面的学习，发现这个点就是可变参数宏的语法（我之前只了解了可变参数函数的）。

（可以类比C++11新增的可变参数模板）

# gnu c的可变参数宏

在GNU C中，从C99开始，宏可以接受可变数目的参数，就象可变参数函数一样。

和函数一样，**宏也用三个点…来表示可变参数**

## `__VA_ARGS__` 宏

`__VA_ARGS__` 宏用来表示可变参数的内容，

简单来说就是将左边宏中 … 的内容原样抄写在右边`__VA_ARGS__` 所在的位置。

如下例代码：

```
#include <stdio.h>
#define debug(...) printf(__VA_ARGS__)
int main(void)
{
    int year = 2018；
    debug("this year is %d\n", year);  //效果同printf("this year is %d\n", year);
}
```

## 可变参数别称

另外，通过一些语法，你可以给可变参数起一个名字，而不是使用__VA_ARGS__ ，如下例中的args：

```
#include <stdio.h>
#define debug(format, args...) printf(format, args)
int main(void)
{
    int year = 2018；
    debug("this year is %d\n", year);  //效果同printf("this year is %d\n", year);
}
```

## **无参传入情况**

与可变参数函数不同的是，

可变参数宏中的可变参数必须至少有一个参数传入，

不然会报错，

为了解决这个问题，需要一个特殊的“##”操作，

如果可变参数被忽略或为空，“##”操作将使预处理器(preprocessor)去除掉它前面的那个逗号。

如下例所示

```
#include <stdio.h>
#define debug(format, args...) printf(format, ##args)
int main(void)
{
    int year = 2018；
    debug("hello, world");  //只有format参数，没有args可变参数
}
```

## 宏连接符##

举个例子：宏定义为#define XNAME(n) x##n，代码为：XNAME(4)，则在预编译时，宏发现XNAME(4)与XNAME(n)匹配，则令 n 为 4，然后将右边的n的内容也变为4，然后将整个XNAME(4)替换为 x##n，亦即 x4，故最终结果为 XNAME(4) 变为 x4。如下例所示：

```
#include <stdio.h>
#define XNAME(n) x##n
#define PRINT_XN(n) printf("x" #n " = %d\n", x##n);
int main(void)
{
    int XNAME(1) = 14; // becomes int x1 = 14;
    int XNAME(2) = 20; // becomes int x2 = 20;
    PRINT_XN(1);       // becomes printf("x1 = %d\n", x1);
    PRINT_XN(2);       // becomes printf("x2 = %d\n", x2);
    return 0;
}
```



# 参考资料

1、揭密X86架构C可变参数函数实现原理

https://blog.csdn.net/linyt/article/details/79772742

2、亲密接触C可变参数函数

https://blog.csdn.net/linyt/article/details/2243605