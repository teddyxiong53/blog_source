---
title: protobuf之nanopb
date: 2018-12-06 14:07:28
tags:
	- 编程
---





nanopb是一个微型的protobuf实现。

https://github.com/nanopb/nanopb

我们看看使用的效果。

编译：

是进入到nanopb-master/examples/simple目录下去编译。make就好了。这里直接就是一个例子。



现在给一个这样的simple.proto。

```
syntax = "proto2";

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
    message Result {
        required string url = 1;
        optional string title = 2;
        repeated string snippets = 3;
    }
    repeated Result result = 1;
}
```

看看生成的文件是怎么样的。



# network_server例子

这个就是比较贴近实际应用的了。

编译：

```
make
```

运行：

```
#一个shell窗口
./server
#另外开一个shell窗口
./client 
```

实际效果是把根目录的目录打印出来。client后面可以带目录名。

看看代码如何写的。

网卡是loop网卡。

默认path是根目录。

```
message ListFilesRequest {
    optional string path = 1 [default = "/"];
}
```

应该从client这边开始看。

相当于server一个文件服务器，client发送了一个列出目录的请求。



