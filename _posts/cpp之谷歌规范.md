---
title: cpp之谷歌规范
date: 2020-06-03 13:43:08
tags:
	- cpp

---



```
文件名
	全部小写加下划线。
	cpp文件和h文件成对。
	如果包含大量内联函数的。用xx-inl.h做头文件的命名格式。（后面新的规范已经改了这种要求）
类名
	类型首字母大小，不含下划线。
	所有类型命名都是这个规则。
变量名
	一律小写加下划线。int player_id;
	类成员变量，最后多一个下划线。 int player_id_;
	全局变量，前面加g_前缀。例如g_system_time;
	结构体的成员变量，跟普通变量一样，后面没有下划线。
常量名
	k后面跟大写字母开头的名字。
	const int kDaysInWeek = 7;
函数名
	一般函数都是首字母大写的。采用命令式语气。例如OpenFile。
	而存取函数，或者短小的内联函数，使用小写加下划线。例如set_name、get_name。
枚举
	全部大写加下划线。
```



我觉得谷歌的c++编码规范，我不太喜欢，感觉有些怪异。风格不够统一。

看起来不协调。



# 参考资料

1、C++谷歌命名规范

https://www.jianshu.com/p/f56383486520

2、Google 开源项目风格指南 (中文版)

https://zh-google-styleguide.readthedocs.io/en/latest/

3、**Qt编程规范**

这个比较简单务实。

https://blog.51cto.com/u_15753490/5670387