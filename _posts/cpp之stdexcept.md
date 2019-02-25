---
title: cpp之stdexcept
date: 2019-02-25 15:56:17
tags:
	- cpp

---



stdexcept这个头文件里有这些类：

```
逻辑错误
logic_error
domain_error
invalid_argument
length_error
out_of_range

运行时错误
runtime_error
range_error
overflow_error
underflow_error
```

测试：

```
int main()
{
    throw std::logic_error("xx");
}
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/cpp/build $ ./test                
terminate called after throwing an instance of 'std::logic_error'
  what():  xx
[1]    13188 abort      ./test
```



参考资料

1、

http://www.cplusplus.com/reference/stdexcept/