---
title: glib之gvariant
date: 2019-08-07 16:01:19
tags:
	- glib

---

1

GVariant是一种可变数据类型。

可以包括一个或者多个值，同时包含了类型信息。

可以包含简单类型，例如int。

也可以包含复杂类型，例如一个键值对。

GVariant是不可变的，一旦创建，它的类型和内容都不能被改变。

GVariant在数据序列号的时候很有用。

例如dbus，和用GSettings保存参数的时候。

基本用法：

```
GVariant *v = g_variant_new("u", 40);
这表示一个整数，它的值为40 。
```

GVariant是线程安全的。



参考资料

1、

https://developer.gnome.org/glib/stable/glib-GVariant.html