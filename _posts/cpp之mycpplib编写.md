---
title: cpp之mycpplib编写
date: 2019-02-25 14:38:17
tags:
	- cpp

---



这个是把陈硕的recipes这个代码库学习一遍。

学习到的技巧。

```
1、为了避免包含循环包含头文件，可以进行前向类型声明。
	例如声明：struct tm;然后就可以在头文件里使用了，不需要包含time.h了。

```

编码风格：

```
1、成员变量最后跟一个下划线。
2、常量用k做前缀。
```



自己写一遍。

```
hlxiong@hlxiong-VirtualBox ~/work/test/mycpplib $ tree         
.
├── datetime
│   ├── copyable.h
│   ├── TimeZone.cc
│   └── TimeZone.h
├── logging
└── thread
```

本来是打算先写logging的，但是发现logging下面用到了Timestamp。所以就先写datetime目录。

```
1、先写copyable.h。
	这个里面就是一个空类。表示保留拷贝构造函数。
2、写Date.h和Date.cc。
	因为TimeZone依赖了这个类。
	这里有儒略历，但是这个历法已经不用了啊。为什么要写这个呢？
	儒略历的只是中间值。不管。
3、TimeZone.cc里比较繁琐。没有什么价值，直接拷贝过来先。
4、看Timestamp.cc的。
5、写Date_test.cc和Date_unittest.cc这2个文件。
datetime部分就算写完了。
```

写logging部分：

```
1、先写LogStream.h。

```

