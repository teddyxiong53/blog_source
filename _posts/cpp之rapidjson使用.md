---
title: cpp之rapidjson使用
date: 2018-09-30 10:51:51
tags:
	- cpp

---



rapidjson是只依赖头文件的。

你要集成，只需要把include/rapidjson拷贝到你的项目下面。

```
#include "errno.h"

#include <iostream>
#include <fstream>
#include <string>
#include "document.h"

using namespace std;
using namespace rapidjson;

int main()
{
	string buff;
	string tmp;
	ifstream res("../json.txt");
	if(!res.is_open()) {
		perror("xx");
		cout << "open fail" <<endl;
		return -1;
	}
	while(!res.eof()) {
		getline(res, tmp);
		buff.append(tmp + '\n');
	}
	Document document;
	document.Parse(buff.c_str());
	
    if(!document.HasParseError()) {
        if(document.HasMember("hello")) {
        	cout << document["hello"].GetString() << endl;
        }
	}
	
	
}
```

需要准备一个测试文件：json.txt

```
{       
    "hello": "world",
    "t": true ,
    "f": false,
    "n": null,
    "i": 123,
    "pi": 3.1416,
    "a": [1, 2, 3, 4]
}       
```

基本的读取解析，就是上面这样了。



# 另外一篇教程

测试的文件内容是这样的。对应的代码在https://gitee.com/zhaoyf/zhaoyf_csdn/blob/master/test_json/main.cpp

```
{
    "Int": 1, 
    "Double": 12.0000001, 
    "String": "This is a string", 
    "Object": {
        "name": "qq849635649", 
        "age": 25
    }, 
    "IntArray": [
        10, 
        20, 
        30
    ], 
    "DoubleArray": [
        1, 
        2, 
        3
    ], 
    "StringArray": [
        "one", 
        "two", 
        "three"
    ], 
    "MixedArray": [
        "one", 
        50, 
        false, 
        12.005
    ], 
    "People": [
        {
            "name": "qq849635649", 
            "age": 0, 
            "sex": true
        }, 
        {
            "name": "qq849635649", 
            "age": 10, 
            "sex": false
        }, 
        {
            "name": "qq849635649", 
            "age": 20, 
            "sex": true
        }
    ]
}

```

写入的例子。

```
#include <iostream>
#include <fstream>
#include <string>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
using namespace std;

void Serialize_1()
{
	rapidjson::StringBuffer strBuf;
	rapidjson::Writer<rapidjson::StringBuffer> writer(strBuf);
	
	writer.StartObject();
	//int
	writer.Key("Int");
	writer.Int(1);
	//double
	writer.Key("Double");
	writer.Double(12.00001);
	//字符串
	writer.Key("String");
	writer.String("this is a string");
	//结构体
	writer.Key("Object");
	writer.StartObject();
	writer.Key("name");
	writer.String("xhl");
	writer.Key("age");
	writer.Int(20);
	writer.EndObject();
	
	//数组类型
	//整型数组
	writer.Key("IntArray");
	writer.StartArray();
	writer.Int(10);
	writer.Int(20);
	writer.Int(30);
	writer.EndArray();
	//混合数组
	writer.Key("MixedArray");
	writer.StartArray();
	writer.String("one");
	writer.Int(10);
	writer.EndArray();
	
	writer.EndObject();
	string data = strBuf.GetString();
	cout << data << endl;
}

int main()
{
	Serialize_1();
	
}
```



# 相关概念

Document。最重要的概念。代表了一个json文件。





参考资料

1、官方教程

http://rapidjson.org/zh-cn/md_doc_tutorial_8zh-cn.html

2、【腾讯RapidJSON】学习笔记

https://blog.csdn.net/Vivid_110/article/details/53696077

3、rapidjson库的基本使用

这篇文字特别好。很简单全面。

https://blog.csdn.net/qq849635649/article/details/52678822