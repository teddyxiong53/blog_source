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

# 类型

基本类型

```

[Name]  [Code in D-Bus]  [Data Type in glib]  [Data Type in libdbus-C++]
BYTE         ‘y’            guchar                  unsigned char           
BOOLEAN      ‘b’            gboolean                bool
INT16        ‘n’            gint16                  signed short
UINT16       ‘q’            guint16                 unsigned short
INT32        ‘i’            gint                    int
UINT32       ‘u’            guint                   unsigned int
INT64        ‘x’            gint64                  signed long long
UINT64       ‘t’            guint64                 unsigned long long
DOUBLE       ‘d’            gdouble                 double
STRING       ‘s’            const gchar *           std::string
OBJECT_PATH  ‘o’            const gchar *           DBus::Path :public std::string
UNIX_FD      ‘h’            GVariant *              int
SIGNATURE    ‘g’            const gchar *           DBus::Signature :public std::string

```

复杂类型

```
[Name]   [Code in D-Bus]   [Data Type in glib]  [Data Type in libdbus-C++]
STRUCT      ‘(‘ and ‘)’         Gvariant            DBus::Struct<>
ARRAY       ‘a’                 Gvariant            std::vector<>
VARIANT     ‘v’                 Gvariant            DBus::Variant
DICT_ENTRY  ‘{’ and ‘}’
(Only appear after ‘a’)     Gvariant    When it is used together with ‘a’,it is             
                                        represented by std::map<>
```

结构体的序列化

```
GVariant *pmark = NULL;
gdouble m1 = 1;
gdouble m2 = 2;
gchar *sm1 = "aa";
gchar *sm2 = "bb";
pmark = g_variant_new("((sd)(sd))", sm1,m1,sm2,m2);
```

结构体的反序列化

```
g_variant_get(pmark, "((sd)(sd))", &sm1,&m1,&sm2,&m2);
```



参考资料

1、

https://developer.gnome.org/glib/stable/glib-GVariant.html

2、GLib中的数据类型及操作

https://blog.csdn.net/yanlinembed/article/details/49837655