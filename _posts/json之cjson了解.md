---
title: cjson了解
date: 2018-02-06 20:27:33
tags:
	- cjson

---



cjson是C语言里进行cjson存取操作的库。



假设我们有这么一段json数据：

```
{
    "basic" :{
        "name": "teddy",
        "age": 27,
        "weight": 70.0
    },
    "habbits": [
        "basketball",
        "running"
    ]
}
```





```
#if CJSON_TEST
#include "cJSON.h"

char *cjson_data = "{\
    \"basic\" :{\
        \"name\": \"teddy\",\
        \"age\": 27,\
        \"weight\": 70.0\
    },\
    \"habbits\": [\
        \"basketball\",\
        \"running\"\
    ]\
}";

struct mybasic_t
{
    char name[32];
    int age;
    double weight;
};
struct myhabit_t 
{
    char habbit[2][32];
};

struct myinfo_t
{
    struct mybasic_t basic;
    struct myhabit_t habbits;
};
struct myinfo_t myinfo;

void cjson_test_read()
{
    cJSON *root, *basic, *habbits , *basic_name, *basic_age, *basic_weight;
    root = cJSON_Parse(cjson_data);
    basic = cJSON_GetObjectItem(root, "basic");
    basic_name = cJSON_GetObjectItem(basic, "name");
    memcpy(myinfo.basic.name, basic_name->valuestring, strlen(basic_name->valuestring));
    basic_age = cJSON_GetObjectItem(basic, "age");
    myinfo.basic.age = basic_age->valueint;
    
    basic_weight = cJSON_GetObjectItem(basic, "weight");
    myinfo.basic.weight = basic_weight->valuedouble;
    mylogd("%s:%d:%f", myinfo.basic.name,myinfo.basic.age,myinfo.basic.weight);

    habbits = cJSON_GetObjectItem(root, "habbits");
    int i=0;
    for(i=0; i<2; i++)
    {
        memcpy(myinfo.habbits.habbit[i], 
            cJSON_GetArrayItem(habbits, i)->valuestring, 
            strlen(cJSON_GetArrayItem(habbits, i)->valuestring));
        mylogd("habbits[%d]:%s", i, myinfo.habbits.habbit[i]);
    }
    
}


void cjson_test_write()
{
    
    cJSON *root, *basic, *habbits , *basic_name ,*basic_age;
    root = cJSON_CreateObject();
    basic = cJSON_CreateObject();
    cJSON_AddItemToObject(root, "basic", basic);
    basic_name = cJSON_CreateString("teddy");
    basic_age = cJSON_CreateNumber(27);
    cJSON_AddItemToObject(basic, "name", basic_name);
    cJSON_AddItemToObject(basic, "age", basic_age);
    cJSON_PrintUnformatted(root);
}


#endif

```



我看的是这个很轻量级的版本。

https://github.com/RT-Thread-packages/cJSON/archive/v1.0.2.zip

代码不多。

```
hlxiong@hlxiong-VirtualBox:~/work/study/cJSON-1.0.2$ tree
.
└── cJSON-1.0.2
    ├── cJSON.c
    ├── cJSON.h
    ├── cJSON_port.c
    ├── cJSON_util.c
    ├── cJSON_util.h
    ├── LICENSE
    ├── README.md
    └── SConscript
```

这个是rt-thread专用的。



关于delete

只需要对root对象进行delete就好了。不会有内存泄漏。

不能delete子节点。无论是放在delete root之前或之后，都会导致端错误。



测试数组

```
void test_array()
{
	char text[] = "\
	{\n \
	\"responses\":\n \
	[\n \
		{\n \
			\"header\": {\n \
				\"name\": \"aaa\"\n \
			},\n \
			\"payload\": {\n \
				\"timestamp\": 1\n \
			}\n \
		}, \
		{\n \
			\"header\": {\n \
				\"name\": \"bbb\"\n \
			},\n \
			\"payload\": {\n \
				\"timestamp\": 2\n \
			}\n \
		}\
	]\n \
	}";
	cJSON *root = cJSON_Parse(text);

	cJSON *responses = cJSON_GetObjectItem(root, "responses");
	int n = cJSON_GetArraySize(responses);
	printf("array size:%d\n", n);
	cJSON_Delete(root);
}
```



# int类型长度

cjson里，把int类型，只是32位的。

我看iflyos里，云端的时间戳是用int表示的。

这个还是会有溢出的风险的。

为什么JsonCpp里面为什么没有64位整数？Json起源于javascript，在js中数字的表示可能与高级语言中不一样， 如果一位数字32位表示不了那么js中应该一律都是用double表示， 所以说js中 大整数其实也是double， 这也就能解释为什么在jsoncpp中为什么没提供64为整数转化的方法。



# cJSON_IsReference

这个怎么使用的？

只在内部的create_reference函数里有置位这个flag。

对外的接口是：

```
cJSON_AddItemReferenceToArray
cJSON_AddItemReferenceToObject
```

我都没有使用过。

那么就是说，这个点我当前可以忽略。

那cjson对于字符串常量是怎么处理的？

例如cJSON_CreateString是怎么处理字符串常量的？是进行了一次strdup。

所以我上层调用就直接传递字符串常量就好了。

# json pointer

我看cjson的cJSON_Utils里有json pointer的函数：

```
CJSON_PUBLIC(cJSON *) cJSONUtils_GetPointer(cJSON * const object, const char *pointer);
```

这个是个什么概念呢？

JSON Pointer（JSON指针）是一种用于在JSON文档中定位特定值或元素的字符串表示方法。

它通常用于在JSON文档中进行导航，查找特定路径下的值或对象，

并支持对JSON文档进行操作。

JSON Pointer定义了一些特定的字符和符号来表示路径，以便准确定位JSON文档中的元素。

JSON Pointer使用斜杠（/）作为分隔符来表示层级关系，类似于文件路径。

此外，它还使用一些特殊字符来表示一些操作，例如：

- `/`：表示JSON文档的根级别。
- `/propertyName`：表示对象中名为"propertyName"的属性。
- `/index`：表示数组中的索引。
- `/-`：表示在数组中添加一个新元素。

以下是一些示例，以便更好地理解JSON Pointer的使用：

考虑以下JSON文档：

```json
{
  "person": {
    "name": "John",
    "age": 30,
    "address": {
      "street": "123 Main St",
      "city": "Exampleville"
    },
    "languages": ["English", "French"]
  }
}
```

- `"/person/name"`：指向"John"。
- `"/person/address/city"`：指向"Exampleville"。
- `"/person/languages/0"`：指向"English"。
- `"/person/languages/1"`：指向"French"。

JSON Pointer还支持一些特殊操作，例如：

- `"/person/name"` 的值为 "John"，可以用 `"/person/name" = "Jane"` 来修改为 "Jane"。
- `"/person/languages/-"` 表示在`languages`数组中添加一个新元素。

需要注意的是，JSON Pointer是一种用于定位JSON文档中特定元素的表示方法，并不直接执行实际的操作。在实际应用中，您可能需要使用编程语言的库或工具来解析JSON Pointer并进行相应的操作。

# *JSON Patch*介绍

JSON Patch 是一种用于在 JSON 文档中进行部分更新（patching）的格式和协议。

它允许你描述一系列操作，这些操作可以应用于现有的 JSON 文档，以便对其进行修改、添加、删除或替换。

JSON Patch 通常用于在不替换整个 JSON 文档的情况下，对其中的特定部分进行更改。

JSON Patch 定义了一组操作，每个操作都由一个 JSON 对象表示。

以下是 JSON Patch 支持的几种常见操作：

1. `add`：向 JSON 文档中添加一个新的值或对象。
2. `remove`：从 JSON 文档中移除一个值或对象。
3. `replace`：替换 JSON 文档中的一个值。
4. `move`：将一个值从一个位置移动到另一个位置。
5. `copy`：将一个值从一个位置复制到另一个位置。
6. `test`：测试 JSON 文档中的一个值是否匹配给定的值，用于验证。

每个操作都由一个操作类型字段（如 `add`、`remove` 等）和一些操作特定的字段组成，这些字段指定了操作要作用的位置以及操作所需的值。JSON Patch 中的操作按照顺序依次应用，从而生成最终的修改后的 JSON 文档。

以下是一个简单的 JSON Patch 示例，假设我们有以下 JSON 文档：

```json
{
  "name": "John",
  "age": 30,
  "address": {
    "street": "123 Main St",
    "city": "Exampleville"
  }
}
```

以下是一个 JSON Patch，它将在上述 JSON 文档上应用以下操作：

1. 添加 `{"country": "USA"}` 到 `address` 对象中。
2. 将 `age` 的值从 `30` 替换为 `31`。
3. 从 `address` 对象中删除 `city` 属性。

```json
[
  { "op": "add", "path": "/address/country", "value": "USA" },
  { "op": "replace", "path": "/age", "value": 31 },
  { "op": "remove", "path": "/address/city" }
]
```

应用上述 JSON Patch 操作后，最终的 JSON 文档将变为：

```json
{
  "name": "John",
  "age": 31,
  "address": {
    "street": "123 Main St",
    "country": "USA"
  }
}
```

JSON Patch 可以用于在 RESTful API 中进行部分更新，避免发送整个 JSON 文档，从而减少数据传输量和服务器端的处理负担。

它也被广泛用于一些 JSON 数据库、配置管理和数据同步等场景。

# 测试代码

这个项目的测试代码写得比较全面。值得学习一下。



# 参考资料

1、

http://www.fly63.com/article/detial/3770

2、jsoncpp 不能处理long类型数据

https://blog.csdn.net/chenlei0630/article/details/39644189

3、cJSON: 只能处理 utf-8 编码的 json

https://www.cnblogs.com/personnel/p/12365180.html