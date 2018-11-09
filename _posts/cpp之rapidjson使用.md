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

Document。最重要的概念。代表了一个json文件。不是，是代表了一个完整的json对象。



# 分配器

这个搞得复杂。其实根本没有必要。都是用的这个，就是malloc和free在做。

```
class CrtAllocator {
public:
    static const bool kNeedFree = true;
    void* Malloc(size_t size) { 
        if (size) //  behavior of malloc(0) is implementation defined.
            return std::malloc(size);
        else
            return NULL; // standardize to returning NULL.
    }
    void* Realloc(void* originalPtr, size_t originalSize, size_t newSize) {
        (void)originalSize;
        if (newSize == 0) {
            std::free(originalPtr);
            return NULL;
        }
        return std::realloc(originalPtr, newSize);
    }
    static void Free(void *ptr) { std::free(ptr); }
};
```

还有内存池的方式的。可能是用来在分配进行使用的场合吧。避免出现内存碎片。



# 官网教程

rapidjson是json解析器和生成器。

特定：

1、小而全。

2、速度快。

3、独立。不依赖STL。

4、对内存友好。

5、对Unicode友好。



把一个json字符串解析到一个DOM（Document）。

再把DOM转成json字符串。

```
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include <iostream>

int main()
{
	char *json = "{\"project\": \"rapidjson\", \"stars\":10}";
	rapidjson::Document d;
	d.Parse(json);
	
	rapidjson::Value& s = d["stars"];
	s.SetInt(s.GetInt() + 1);
	
	rapidjson::StringBuffer buffer;
	rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
	d.Accept(writer);
	std::cout << buffer.GetString() << std::endl;
	return 0;
}
```



API的分类：

1、DOM API。上面我们看的都是这种。

2、SAX API

3、Schema API



在调用构造函数后，得到的Value 或者Document，默认是null的。

需要使用SetXxx函数来设置类型，或者进行赋值操作。

```
Document d;
d.SetObject();

或者
Value v;
v.SetInt(10);//等价于v = 10;

```



#参考资料

1、官方教程

http://rapidjson.org/zh-cn/md_doc_tutorial_8zh-cn.html

2、【腾讯RapidJSON】学习笔记

https://blog.csdn.net/Vivid_110/article/details/53696077

3、rapidjson库的基本使用

这篇文字特别好。很简单全面。

https://blog.csdn.net/qq849635649/article/details/52678822