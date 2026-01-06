---
title: pipewire之spa-pod官方文档总结
date: 2025-05-30 16:03:37
tags:
	- 音频
---

--

# 官方文档分析

### SPA POD 文档翻译总结

本文件描述了 **SPA POD**（Plain Old Data），一种数据容器，类似于 **DBus Variant** 或 **LV2 Atom**，支持嵌套结构、向量、数组、序列及多种基本类型。

数据在内存中按顺序布局，可直接存储或跨进程/线程交换，无需额外序列化。

以下是文档翻译总结，保留专有名词术语和图表。

#### 概述
**SPA POD** 由 32 位大小字段、32 位类型字段和内容组成，起始地址按 8 字节对齐，支持跳过未知类型。**POD** 可在实时线程中高效构建和解析，无需内存分配，使用 **SPA** 类型系统定义基本类型和容器。

#### 类型
**POD** 支持以下基本 **SPA** 类型：

- **SPA_TYPE_None**：无值或空指针。
- **SPA_TYPE_Bool**：布尔值。
- **SPA_TYPE_Id**：枚举值。
- **SPA_TYPE_Int**、**SPA_TYPE_Long**、**SPA_TYPE_Float**、**SPA_TYPE_Double**：32/64 位数值类型。
- **SPA_TYPE_String**：字符串。
- **SPA_TYPE_Bytes**：字节数组。
- **SPA_TYPE_Rectangle**：包含宽高的矩形。
- **SPA_TYPE_Fraction**：包含分子分母的分数。
- **SPA_TYPE_Bitmap**：位数组。

容器类型：
- **SPA_TYPE_Array**：等大小对象数组。
- **SPA_TYPE_Struct**：类型和对象集合。
- **SPA_TYPE_Object**：带属性的对象。
- **SPA_TYPE_Sequence**：定时 **POD** 序列。

其他类型：
- **SPA_TYPE_Pointer**：内存中的类型指针。
- **SPA_TYPE_Fd**：文件描述符。
- **SPA_TYPE_Choice**：值选择。
- **SPA_TYPE_Pod**：通用 **POD** 类型。

#### 构建 POD
通常使用 **struct spa_pod_builder** 构建 **POD**，需初始化内存区域，支持动态扩展内存。常见方式是在栈上构建，无需分配内存，若缓冲区不足会报错。示例：

```c
uint8_t buffer[4096];
struct spa_pod_builder b;
spa_pod_builder_init(&b, buffer, sizeof(buffer));
```

##### 构建 Struct
构建包含 **Int** 和 **Float** 的 **struct**（类似 JSON 数组）：

```c
struct spa_pod_frame f;
spa_pod_builder_push_struct(&b, &f);
spa_pod_builder_int(&b, 5);
spa_pod_builder_float(&b, 3.1415f);
struct spa_pod *pod;
pod = spa_pod_builder_pop(&b, &f);
```

使用变参构建器简化：

```c
pod = spa_pod_builder_add_struct(&b,
	SPA_POD_Int(5),
	SPA_POD_Float(3.1415f));
```

变参构建器不支持 **sequence** 或 **array**。

##### 构建 Object
**Object** 包含属性，类似 JSON 对象。示例：

```c
spa_pod_builder_push_object(&b, &f, SPA_TYPE_OBJECT_Props, SPA_PARAM_Props);
spa_pod_builder_prop(&b, SPA_PROP_device, 0);
spa_pod_builder_string(&b, "hw:0");
spa_pod_builder_prop(&b, SPA_PROP_frequency, 0);
spa_pod_builder_float(&b, 440.0);
pod = spa_pod_builder_pop(&b, &f);
```

快捷方式：

```c
pod = spa_pod_builder_add_object(&b,
	SPA_TYPE_OBJECT_Props, SPA_PARAM_Props,
	SPA_PROP_device,    SPA_POD_String("hw:0"),
	SPA_PROP_frequency, SPA_POD_Float(440.0f));
```

建议按升序推送属性键以优化性能。

##### Choice 值
**Choice** 表示属性或 **struct** 的值范围或枚举，包含 **choice** 类型和同类型值数组。**Choice** 类型包括：

- **SPA_CHOICE_None**：无选择，首个值为当前值。
- **SPA_CHOICE_Range**：范围（默认、最小、最大）。
- **SPA_CHOICE_Step**：带步长的范围（默认、最小、最大、步长）。
- **SPA_CHOICE_Enum**：枚举（默认、备选值）。
- **SPA_CHOICE_Flags**：标志位掩码。

示例（频率范围）：

```c
struct spa_pod_frame f2;
spa_pod_builder_push_object(&b, &f, SPA_TYPE_OBJECT_Props, SPA_PARAM_Props);
spa_pod_builder_prop(&b, SPA_PROP_frequency, 0);
spa_pod_builder_push_choice(&b, &f2, SPA_CHOICE_Range, 0);
spa_pod_builder_float(&b, 440.0);   //  default
spa_pod_builder_float(&b, 110.0);   //  min
spa_pod_builder_float(&b, 880.0);   //  max
pod = spa_pod_builder_pop(&b, &f2);
pod = spa_pod_builder_pop(&b, &f);
```

快捷方式：

```c
pod = spa_pod_builder_add_object(&b,
	SPA_TYPE_OBJECT_Props, SPA_PARAM_Props,
	SPA_PROP_frequency, SPA_POD_CHOICE_RANGE_Float(440.0f, 110.0f, 880.0f));
```

##### Choice 示例
描述 **SPA_TYPE_OBJECT_Format**（用于 **SPA_PARAM_EnumFormat**）：

```c
pod = spa_pod_builder_add_object(&b,
	SPA_TYPE_OBJECT_Format, SPA_PARAM_EnumFormat,
	SPA_FORMAT_mediaType,      SPA_POD_Id(SPA_MEDIA_TYPE_audio),
	SPA_FORMAT_mediaSubtype,   SPA_POD_Id(SPA_MEDIA_SUBTYPE_raw),
	SPA_FORMAT_AUDIO_format,   SPA_POD_CHOICE_ENUM_Id(4,  //  4 values follow
					SPA_AUDIO_FORMAT_S16, //  default
					SPA_AUDIO_FORMAT_S16, //  alternative1
					SPA_AUDIO_FORMAT_S32, //  alternative2
					SPA_AUDIO_FORMAT_F32  //  alternative3
				   ),
	SPA_FORMAT_AUDIO_rate,     SPA_POD_CHOICE_RANGE_Int(
					44100,		//  default
					8000,		//  min
					192000		//  max
				   ),
	SPA_FORMAT_AUDIO_channels, SPA_POD_Int(2));
```

##### 固定值
使用 **spa_pod_object_fixate()** 移除 **choice** 值，将 **choice** 类型设为 **SPA_CHOICE_None**，仅保留默认值。上述示例固定后等价于：

```c
pod = spa_pod_builder_add_object(&b,
	SPA_TYPE_OBJECT_Format, SPA_PARAM_EnumFormat,
	SPA_FORMAT_mediaType,      SPA_POD_Id(SPA_MEDIA_TYPE_audio),
	SPA_FORMAT_mediaSubtype,   SPA_POD_Id(SPA_MEDIA_SUBTYPE_raw),
	SPA_FORMAT_AUDIO_format,   SPA_POD_Id(SPA_AUDIO_FORMAT_S16),
	SPA_FORMAT_AUDIO_rate,     SPA_POD_Int(44100),
	SPA_FORMAT_AUDIO_channels, SPA_POD_Int(2));
```

#### 解析 POD
解析 **POD** 包括验证字节、检查类型、遍历 **object** 或 **struct** 项、提取数据。

##### 验证字节
使用 **spa_pod_from_data()** 检查字节是否包含有效 **POD**：

```c
struct spa_pod *pod;
pod = spa_pod_from_data(data, maxsize, offset, size);
```

##### 检查 POD 类型
使用 **spa_pod_is_bool()**、**spa_pod_is_int()** 等检查类型，简单类型可通过 **spa_pod_get_bool()**、**spa_pod_get_int()** 提取值。检查 **object** 类型使用 **spa_pod_is_object_type()**。

##### Struct 字段
遍历 **struct** 字段：

```c
struct spa_pod *pod, *obj;
SPA_POD_STRUCT_FOREACH(obj, pod) {
	printf("field type:%d\n", pod->type);
}
```

推荐使用解析器处理 **struct**。

##### Object 属性
遍历 **object** 属性：

```c
struct spa_pod_prop *prop;
struct spa_pod_object *obj = (struct spa_pod_object*)pod;
SPA_POD_OBJECT_FOREACH(pod, prop) {
	printf("prop key:%d\n", prop->key);
}
```

按键查找属性，推荐从前一键开始以优化性能：

```c
struct spa_pod_prop *prop;
prop = spa_pod_find_prop(obj, NULL, SPA_FORMAT_AUDIO_format);
prop = spa_pod_find_prop(obj, prop, SPA_FORMAT_AUDIO_rate);
```

##### 解析器
初始化 **struct spa_pod_parser**：

```c
struct spa_pod_parser p;
spa_pod_parser_pod(&p, obj);
```

进入容器（如 **struct**）：

```c
struct spa_pod_frame f;
spa_pod_parser_push_struct(&p, &f);
```

解析字段：

```c
uint32_t id, val;
spa_pod_parser_get_id(&p, &id);
spa_pod_parser_get_int(&p, &val);
spa_pod_parser_pop(&p, &f);
```

##### 变参解析器
解析 **struct**：

```c
spa_pod_parser_get_struct(&p,
	SPA_POD_Id(&id),
	SPA_POD_Int(&val));
```

解析 **object**（支持可选字段，使用 **SPA_POD_OPT_** 前缀）：

```c
uint32_t id, type, subtype, format, rate = 0, channels = 0;
spa_pod_parser_get_object(&p,
	SPA_TYPE_OBJECT_Format, &id,
	SPA_FORMAT_mediaType,      SPA_POD_Id(&type),
	SPA_FORMAT_mediaSubtype,   SPA_POD_Id(&subtype),
	SPA_FORMAT_AUDIO_format,   SPA_POD_Id(&format),
	SPA_FORMAT_AUDIO_rate,     SPA_POD_OPT_Int(&rate),
	SPA_FORMAT_AUDIO_channels, SPA_POD_OPT_Int(&channels));
```

**Sequence** 或 **array** 需使用迭代器解析。

##### Choice 值
解析器处理 **SPA_CHOICE_None** 类型的 **choice** 值，提取单一值。其他 **choice** 类型需解析为 **struct spa_pod** 后手动检查：

```c
uint32_t id, type, subtype;
struct spa_pod *format;
spa_pod_parser_get_object(&p,
	SPA_TYPE_OBJECT_Format, &id,
	SPA_FORMAT_mediaType,      SPA_POD_Id(&type),
	SPA_FORMAT_mediaSubtype,   SPA_POD_Id(&subtype),
	SPA_FORMAT_AUDIO_format,   SPA_POD_Pod(&format));
```

使用 **spa_pod_get_values()** 获取值数组：

```c
struct spa_pod *value;
uint32_t n_vals, choice;
value = spa_pod_get_values(pod, &n_vals, &choice);
switch (choice) {
case SPA_CHOICE_None:
        //  one single value
	break;
case SPA_CHOICE_Range:
        uint32_t *v = SPA_POD_BODY(values);
	if (n_vals < 3)
		break;
	printf("default value: %u\n", v[0]);
	printf("min value: %u\n", v[1]);
	printf("max value: %u\n", v[2]);
	break;
default:
	break;
}
```

#### 过滤
对两个同类型 **POD**（如 **object**、**struct**）执行过滤，生成兼容两者的新 **POD**，常用于查找端口兼容格式。示例：

```c
pod = spa_pod_builder_add_object(&b,
	SPA_TYPE_OBJECT_Format, SPA_PARAM_EnumFormat,
	SPA_FORMAT_mediaType,      SPA_POD_Id(SPA_MEDIA_TYPE_audio),
	SPA_FORMAT_mediaSubtype,   SPA_POD_Id(SPA_MEDIA_SUBTYPE_raw),
	SPA_FORMAT_AUDIO_format,   SPA_POD_CHOICE_ENUM_Id(4,
					SPA_AUDIO_FORMAT_S16,
					SPA_AUDIO_FORMAT_S16,
					SPA_AUDIO_FORMAT_S32,
					SPA_AUDIO_FORMAT_F32));

filter = spa_pod_builder_add_object(&b,
	SPA_TYPE_OBJECT_Format, SPA_PARAM_EnumFormat,
	SPA_FORMAT_mediaType,      SPA_POD_Id(SPA_MEDIA_TYPE_audio),
	SPA_FORMAT_mediaSubtype,   SPA_POD_Id(SPA_MEDIA_SUBTYPE_raw),
	SPA_FORMAT_AUDIO_format,   SPA_POD_CHOICE_ENUM_Id(3,
					SPA_AUDIO_FORMAT_S16,
					SPA_AUDIO_FORMAT_S16,
					SPA_AUDIO_FORMAT_F64));

struct spa_pod *result;
if (spa_pod_filter(&b, &result, pod, filter) < 0)
	goto exit_error;
```

结果等价于：

```c
result = spa_pod_builder_add_object(&b,
	SPA_TYPE_OBJECT_Format, SPA_PARAM_EnumFormat,
	SPA_FORMAT_mediaType,      SPA_POD_Id(SPA_MEDIA_TYPE_audio),
	SPA_FORMAT_mediaSubtype,   SPA_POD_Id(SPA_MEDIA_SUBTYPE_raw),
	SPA_FORMAT_AUDIO_format,   SPA_AUDIO_FORMAT_S16);
```

#### POD 布局
**POD** 以 32 位大小/类型对开头（本地字节序），后接负载数据和填充，填充至 8 字节对齐，总大小为 `ROUND_UP_8(8 + size)`：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   type                                                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   payload ...                                                 |
   .                                                |  ... padding .
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### POD 类型布局
##### None (1)
无负载，大小为 0：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   0                                                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   1                                                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

##### Bool (2)
存储 32 位整数，0 为假，非 0 为真：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   4                                                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   2                                                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   value (int32)                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   padding                                                     |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

##### Id (3)
32 位无符号整数，引用类型表索引：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   4                                                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   3                                                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   id (uint32)                                                 |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   padding                                                     |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Int (4)
32 位有符号整数：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   4                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   4                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   value (int32)                                               |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   padding                                                     |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Long (5)
64 位有符号整数：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   8                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   5                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   value (int64)                                               |
   +                                                               +
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Float (6)
32 位浮点数：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   4                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   6                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   value (float32)                                             |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   padding                                                     |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Double (7)
64 位浮点数：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   8                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   7                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   value (float64)                                             |
   +                                                               +
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### String (8)
以 0 结尾的字符串，大小包括终止符：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   8                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   chars ....                                                  |
   .                                                               .
   |                                            ... 0 | padding..  |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Bytes (9)
字节数组，大小为字节数：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   9                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   bytes ....                                                  |
   .                                                               .
   |                                                  | padding..  |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Rectangle (10)
包含宽高：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   8                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   10                                                          |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   width (uint32)                                              |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   height (uint32)                                             |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Fraction (11)
包含分子分母：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   8                                                           |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   11                                                          |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   num (uint32)                                                |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   denom (uint32)                                              |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Bitmap (12)
位数组，存储为 8 位字节：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   12                                                          |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   bits (uint8) ...                                            |
   .                                                               .
   |                                                  | padding..  |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

##### Array (13)
同类型等大小对象数组：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   13                                                          |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   child_size                                                  |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   child_type                                                  |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   child1 (child_size bytes) ...                               |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   childN (child_size bytes) ...                               |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

表示为：`Array[Int](<val1>,<val2>,...)`

##### Struct (14)
多个 **POD** 组合：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   14  (Struct)                                                |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size1                                                       |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   type1                                                       |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   payload 1...                                                |
   .                                                |  ... padding .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   sizeN                                                       |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   typeN                                                       |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   payloadN ...                                                |
   .                                                |  ... padding .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

表示为：`Struct(<pod1 type>:<pod1 description>,...)`

##### Object (15)
属性集合：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   15                                                          |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   object_type                                                 |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   object_id                                                   |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   property1                                                   |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   propertyN                                                   |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

属性格式：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   key (uint32)                                                |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   flags (uint32)                                              |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   POD value ...                                               |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
```

表示为：`Object[type,id](key1:<pod1>,key2:<pod1>,...)`

##### Sequence (16)
定时事件序列（如 MIDI 或控制更新）：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   16                                                          |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   unit                                                        |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   pad                                                         |
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   |   control1                                                    |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+--++-++-++-++-++-++-++-++-++-++-++-++-++-+
   .                                                               .
   +-+-+-+-+-+-++-++-++-++-++-++-++-++-++-++-++-+
   |   controlN                                                    |
   .                                                               .
   +-+-+-+-+-+-++-++-++-++-++-++-++-++-++-++-++-+
```

控制单元：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-++-++-++-++-++-++-++-++-++-++-++-+
   |   offset (uint32)                                             |
   +-+-+-+-+-+-++-++-++-++-++-++-++-++-++-++-++-+
   |   type (uint32)                                               |
   +-+-+-+-+-+-++-++-++-++-++-+-++-++-++-++-++-++-+
   |   POD value ...                                               |
   .                                                               .
   +-+-+-+-+-+-++-++-++-++-++-+-++-++-++-++-++-++-+
```

##### Pointer (17)
内存指针，通常不序列化：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   16                                                          |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   17                                                          |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   type                                                        |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   padding (must be 0)                                         |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   native pointer value ...                                    |
   .                                               | .. padding    .
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
```

##### Fd (18)
64 位文件描述符，序列化时为消息中 **fd** 的索引：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   8                                                           |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   18                                                          |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   fd (int64) ...                                                |
   +                                                               +
   |                                                               |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
```

##### Choice (19)
可能值数组：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   size                                                        |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   19                                                          |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   type                                                        |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   flags                                                       |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   child_size                                                  |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   child_type                                                  |
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   child1 (child_size bytes) ...                               |
   .                                                               .
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   .                                                               .
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
   |   childN (child_size bytes) ...                               |
   .                                                               .
   +-+-+-+-+-+-++-++-+-++-++-++-++-++-++-++-++-++-+
```

**type** 为 **spa_choice_type**：
- **None (0)**：仅 **child1** 有效。
- **Range (1)**：**child1** 为默认值，范围为 **child2** 至 **child3**。
- **Step (2)**：**child1** 为默认值，范围为 **child2** 至 **child3**，步长为 **child4**。
- **Enum (3)**：**child1** 为默认值，备选值为数组值。
- **Flags (4)**：**child1** 为默认值，标志位为数组值。

##### Pod (20)
值为 **POD** 本身。

总结：**SPA POD** 是一种高效的数据容器，支持多种基本类型和容器，布局紧凑，适合实时处理。使用 **spa_pod_builder** 构建，**spa_pod_parser** 解析，支持 **choice** 值和过滤，广泛用于 **SPA** 系统的数据交换。
