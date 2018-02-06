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





