---
title: glib之gvariant
date: 2019-08-07 16:01:19
tags:
	- glib

---

--

# 简介

GVariant是GLib库中的一种数据类型，用于在应用程序中表示和传递数据。

它提供了一种通用的、类型安全的数据容器，

可以存储多种数据类型，包括基本数据类型（如整数、浮点数、布尔值）、字符串、数组、字典等。

GVariant的设计目标是提供一种灵活、高效的数据表示方式，以适应不同的应用场景。

它具有以下特点：

1. 类型安全：GVariant在运行时对存储的数据类型进行检查，确保数据的正确性和一致性。

2. 可扩展性：GVariant支持嵌套结构，可以构建复杂的数据类型，如多维数组和嵌套字典。

3. 序列化和反序列化：GVariant提供了序列化和反序列化功能，可以将数据转换为二进制格式进行存储或传输，然后重新还原为原始数据。

4. 跨平台兼容性：GVariant的实现不依赖于特定的硬件或操作系统，因此可以在不同的平台上使用和传递数据。

使用GVariant时，您可以通过函数调用来创建、访问和修改GVariant对象。以下是一些常用的函数：

- `g_variant_new()`：创建一个新的GVariant对象。
- `g_variant_get_type()`：获取GVariant对象的数据类型。
- `g_variant_get()`：从GVariant对象中获取存储的值。
- `g_variant_set()`：修改GVariant对象中存储的值。
- `g_variant_serialize()`和`g_variant_deserialize()`：进行GVariant对象的序列化和反序列化。

此外，GVariant还与GLib的信号和属性系统紧密集成，可以在应用程序中方便地进行数据传递和通信。

总结来说，GVariant是GLib库中一种强大的数据类型，用于灵活、高效地表示和传递各种数据。它在GLib和相关的开发框架中广泛应用，为开发者提供了一种方便的数据处理工具。







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

```
typedef enum
{
  G_VARIANT_CLASS_BOOLEAN       = 'b',
  G_VARIANT_CLASS_BYTE          = 'y',
  G_VARIANT_CLASS_INT16         = 'n',
  G_VARIANT_CLASS_UINT16        = 'q',
  G_VARIANT_CLASS_INT32         = 'i',
  G_VARIANT_CLASS_UINT32        = 'u',
  G_VARIANT_CLASS_INT64         = 'x',
  G_VARIANT_CLASS_UINT64        = 't',
  G_VARIANT_CLASS_HANDLE        = 'h',
  G_VARIANT_CLASS_DOUBLE        = 'd',
  G_VARIANT_CLASS_STRING        = 's',
  G_VARIANT_CLASS_OBJECT_PATH   = 'o',
  G_VARIANT_CLASS_SIGNATURE     = 'g',
  G_VARIANT_CLASS_VARIANT       = 'v',
  G_VARIANT_CLASS_MAYBE         = 'm',
  G_VARIANT_CLASS_ARRAY         = 'a',
  G_VARIANT_CLASS_TUPLE         = '(',
  G_VARIANT_CLASS_DICT_ENTRY    = '{'
} GVariantClass;

```



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



# g_variant_iter_next 和g_variant_iter_loop区别

`g_variant_iter_next` 和 `g_variant_iter_loop` 是 GLib 中用于遍历 `GVariant` 迭代器的两个不同函数，它们有以下区别：

### 1. `g_variant_iter_next`

- **用途**：从迭代器中获取下一个元素。
- **返回值**：返回一个布尔值，表示是否成功获取到下一个元素。
- **参数**：需要传入一个迭代器和对应的格式字符串及输出参数。
- **用法**：通常与循环结构一起使用，手动控制遍历。

**示例**：
```c
while (g_variant_iter_next(&iter, "{&o@a{sa{sv}}}", &object_path, &ifaces_and_properties)) {
    // 处理每个元素
}
```

### 2. `g_variant_iter_loop`

- **用途**：简化迭代器的遍历，自动处理循环。
- **返回值**：返回一个布尔值，表示是否成功获取到下一个元素。
- **参数**：需要传入一个迭代器、格式字符串和输出参数。
- **用法**：在循环中使用，内部管理迭代过程，使代码更简洁。

**示例**：
```c
while (g_variant_iter_loop(&iter, "{&o@a{sa{sv}}}", &object_path, &ifaces_and_properties)) {
    // 处理每个元素
}
```

### 主要区别

- **控制流**：`g_variant_iter_next` 需要你手动控制循环，而 `g_variant_iter_loop` 则封装了循环逻辑。
- **简洁性**：使用 `g_variant_iter_loop` 可以使代码更加简洁和易读。

### 总结

选择使用哪个函数取决于具体的需求和个人偏好。如果需要更细粒度的控制，使用 `g_variant_iter_next`；如果希望代码更简洁，使用 `g_variant_iter_loop`。

# 参考资料

1、

https://developer.gnome.org/glib/stable/glib-GVariant.html

2、GLib中的数据类型及操作

https://blog.csdn.net/yanlinembed/article/details/49837655