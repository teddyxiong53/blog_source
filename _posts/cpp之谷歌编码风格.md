---
title: cpp之谷歌编码风格
date: 2018-10-12 18:18:51
tags:
	- cpp
---



变量及数组初始化。用等于号或者括号都可以。

```
int x = 3;
int x(3);
string name("Some Name");
string name = "Some Name";
```

以tflite-micro的为例。

```
类名：首字母大写的驼峰。
成员变量：下划线，小写，最后跟一个下划线。
函数参数：小写下划线。
成员函数：首字母大写的驼峰。
```



参考资料

1、【整理】Google代码风格(C++)——格式

https://blog.csdn.net/qq_32320399/article/details/80324613

2、谷歌的各种编码规范

https://github.com/zh-google-styleguide/zh-google-styleguide