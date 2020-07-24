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





参考资料

1、

http://www.fly63.com/article/detial/3770

2、jsoncpp 不能处理long类型数据

https://blog.csdn.net/chenlei0630/article/details/39644189

3、cJSON: 只能处理 utf-8 编码的 json

https://www.cnblogs.com/personnel/p/12365180.html