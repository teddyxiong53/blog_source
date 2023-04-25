---
title: 编程之map文件分析
date: 2018-12-04 09:51:13
tags:
	- 编程

---



要分析map文件，首先是先简单生成一个。

怎么生成？

```
gcc -o test test.c -Wl,-Map,test.map
```

test.c文件内容。

```
int global_var = 1;

void func1(int a)
{
    int b;
    b = a;
}
int func2()
{
    global_var = 2;
}
int main()
{
    int local_var = 1;
    func1(local_var);
    func2();
}

```

# 什么是map文件

简单来说，map文件就是通过编译器编译之后，生成的程序、数据及IO空间信息的一种映射文件，

里面包含函数大小，入口地址等一些重要信息。

从map文件我们可以了解到：

程序各区段的寻址是否正确

程序各区段的size，即目前存储器的使用量

程序中各个symbol的地址

各个symbol在存储器中的顺序关系(这在调试时很有用)

各个程序文件的存储用量



# 怎样生成map文件

如何生成？

**生成map文件是链接器ld的功能**，有两种方式可以生成map文件：

通过gcc参数-Wl,-Map,：

gcc -o helloworld helloworld.c -Wl,-Map,file_name.map

通过ld参数-Map：

ld -Map file_name.map helloworld.o -o helloworld



做出可执行文件下载到机器上，你如何知道程序段或数据段会不会太大，会不会超过ROM或RAM的size？

你如何知道Link脚本有没有写错，每个程序区段都确实寻址到符合机器的存储器设定？

当然你可以下载进机器运行就知道了吗？

但是认为负责整合的工程师一定要检查下map文件，有些问题只会造成系统的不稳定，而不会马上死机，这种问题最麻烦。



注意：静态变量和静态函数不会出现在map文件中！



# 参考资料

1、gcc/g++中生成map文件

https://blog.csdn.net/liyongming1982/article/details/6663714