---
title: cpp之delete[]分析
date: 2019-11-28 10:47:51
tags:
	- cpp
---

1

c++对new申请的内存的释放方式有两种：

1、delete

2、delete[]

这两种方式有什么区别呢？

对于基本类型，这两种方式的效果是一样的。

对于class类型，不一样。

看下面的例子：

```
class A
{
private:
    char *m_cBuffer;
    int m_nLen;

public:
    A() { m_cBuffer = new char[m_nLen]; }
    ~A() {
        delete[] m_cBuffer;
        printf("destructor\n");
    }
};
int main()
{
    A *a = new A[10];
    delete[] a;//如果这里用delete a;运行会段错误。
}
```

delete的不同就是，会依次调用对应的析构函数。



参考资料

1、delete 和 delete []的真正区别

https://www.cnblogs.com/wangjian8888/p/7905176.html