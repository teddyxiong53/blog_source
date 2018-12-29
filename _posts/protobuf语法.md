---
title: protobuf语法
date: 2018-12-29 15:31:55
tags:
	- protobuf

---



只参考一篇文章，比较全面了。

先给一个简单例子，下面的讨论都基于这个例子来展开。

```
message SearchRequest {
    required string query = 1;
    optional int32 page_number = 2;
    optional int32 result_per_page = 3;
}
```

指定field类型。string、int32.

分配id。1、2、3就是id。

指定字段规则。required、optional、repeated。

一个proto文件里，可以定义多个message。

注释：用`//`来注释。

proto的类型跟c++里的类型对应关系是这样：

```
double	double
float	float
int32	int32
int64	int64
string 	string
bytes	string
```



# optional

可以给optional指定默认值，这样在解析没有这个值的时候，可以给默认值。

例如我们给上面的result_per_page指定默认10.

```
optional int32 result_per_page = 3 [default = 10];
```

# enum

给上面的内容加上一个enum。

目前是这样：

```
message SearchRequest {
    required string query = 1;
    optional int32 page_number = 2;
    optional int32 result_per_page = 3 [default = 10];
    enum Corpus {
        UNIVERSAL = 0;
        WEB = 1;
        IMAGES = 2;
        LOCAL = 3;
        NEWS = 4;
        PRODUCTS = 5;
        VIDEO = 6;
    }
    optional Corpus corpus = 4 [default = UNIVERSAL];
}

message SearchResponse {
    repeated Result result = 1;
}

message Result {
    required string url = 1;
    optional string title = 2;
    repeated string snippets = 3;
}

```

# import

包含其他文件。



# 嵌套类型

改成这样。

```
message SearchResponse {
    message Result {
        required string url = 1;
        optional string title = 2;
        repeated string snippets = 3;
    }
    repeated Result result = 1;
}
```



# oneof

为了节省内存。

得到的是C语言的union类型这种形式。



参考资料

1、Protobuf 语法指南

https://colobu.com/2015/01/07/Protobuf-language-guide/