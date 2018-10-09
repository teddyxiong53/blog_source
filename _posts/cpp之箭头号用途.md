---
title: cpp之箭头号用途
date: 2018-10-08 19:11:17
tags:
	- cpp

---



看avs代码，看到这种：

```
template <typename Task, typename... Args>
    auto submit(Task task, Args&&... args) -> std::future<decltype(task(args...))>;
```

这个箭头号是做什么的？

这个的正式名称是trailing return type。中文翻译是尾置返回类型。

跟在形参后， 已一个箭头号开头。

任何函数都可以使用尾置返回类型。不过主要用途是用在返回类型比较复杂的时候。

例如，定义一个返回数组指针的函数。

```
int (*func(int i))[10];//返回一个指针，这个指针指向的是一个含有10个int数字的区域。
```

可以用尾置返回类型来简化一下。

```
auto func(int i) -> int(*)[10];
```



# 参考资料

1、arrow operator (->) in function heading

https://stackoverflow.com/questions/22514855/arrow-operator-in-function-heading

2、使用尾置返回类型(trailing return type)

https://blog.csdn.net/oyoyg/article/details/79615951