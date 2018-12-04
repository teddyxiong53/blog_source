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



参考资料

1、gcc/g++中生成map文件

https://blog.csdn.net/liyongming1982/article/details/6663714