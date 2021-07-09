---
title: qt之Q_ENUM
date: 2021-07-09 11:16:33
tags:
	- qt

---

--

之前做一个比较大工程，核心数据里面有很多是枚举变量，

需要频繁地使用枚举量到字符串和字符串到枚举量的操作，

为了实现这些操作，我把每个枚举类型后面都附加了两个类似Enum_to_String()和String_to_Enum()的函数，程序显得很臃肿。

这时候就非常羡慕C#或者java等兄弟语言，内核内置了枚举量和字符串转换的方法。

最近读Qt文档时偶然间发现，

Qt内核其实已经提供了这个转换机制，

使得我们能用很少的代码完成枚举量和字符串的转换，

甚至还能实现其他更酷更强大的功能，

下面我们就来看看如何使用Qt的这个功能。

简单来讲，Qt还是使用一组宏命令来完成枚举量扩展功能的（正如Qt的其他核心机制一样），

这些宏包括

Q_ENUM,

Q_FLAG,

Q_ENUM_NS,

Q_FLAG_NS，

Q_DECLARE_FLAGS，

Q_DECLARE_OPERATORS_FOR_FLAGS，

这些宏的实现原理和如何展开如何注册到Qt内核均不在本文的讲解范围，本文只讲应用。

Q_ENUM的使用

```

```



Q_ENUM使用起来很很简单，对不对？但是还是有几个注意事项需要说明：

Q_ENUM只能在使用了Q_OBJECT或者Q_GADGET的类中，

类可以不继承自QObject，

但一定要有上面两个宏之一（Q_GADGET是Q_OBJECT的简化版，提供元对象的一部分功能，但不支持信号槽）；

Q_ENUM宏只能放置于所包含的结构体定义之后，放在前面编译器会报错，

结构体定义和Q_ENUM宏之间可以插入其他语句，但不建议这样做；

一个类头文件中可以定义多个Q_ENUM加持的结构体，

结构体和Q_ENUM是一一对应的关系；

Q_ENUM加持的结构体必须是公有的；

Q_ENUM宏引入自Qt5.5版本，之前版本的Qt请使用Q_ENUMS宏，

但Q_ENUMS宏不支持QMetaEnum::fromType()函数(这也是Q_ENUMS被弃用的原因)。




参考资料

1、Qt中的枚举变量,Q_ENUM,Q_FLAG,Q_NAMESPACE,Q_ENUM_NS,Q_FLAG_NS以及其他

https://blog.csdn.net/qq_36179504/article/details/100895133