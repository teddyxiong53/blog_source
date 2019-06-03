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





转化规则：

1、首先转化enum的。会先把所有的enum生成出来，不管enum写在哪个位置。

proto文件这样写。

```
enum XX {
    A_0;
    A_1;
}
```

得到对应的C代码：

```
typedef _XX {
    XX_A_0,
    XX_A_1
} XX;
#define _XX_MIN XX_A_0
#define _XX_MAX XX_A_1
#define _XX_ARRAYSIZE ((XX)XX_A_1 + 1)
```

2、然后是struct的。对应proto里的类型是message。

安装依赖关系，先把被依赖的生成。

空的这样生成：

```
message BlePairCommand{
}
生成
/* Struct definitions */
typedef struct _BlePairCommand {
    char dummy_field;
/* @@protoc_insertion_point(struct:BlePairCommand) */
} BlePairCommand;
```

string类型对应pb_callback_t。



# 对string类型的处理

分为两种情况，一种是指定了长度的，一种是没有指定长度的。

```
required string name = 1;
生成的代码是：
pb_callback_t name;

required string name = 1 [(nanopb).max_size = 40];
生成的代码是：
char name[40];
```

还有二维数组的。

```
repeated string name = 1 [(nanopb).max_size = 40, (nanopb).max_count = 5];
生成：
size_t name_count;
char name[5][40];
```



nanopb可以跟标准版的protoc程序进行配合。

先用protoc生成pb文件。在用nanopb_generator.py把pb文件生成c文件和h文件。

就用ama的试一下，看看效果。

```
user@host:~$ protoc -omessage.pb message.proto
user@host:~$ python ../generator/nanopb_generator.py message.pb
Writing to message.h and message.c
user@host:~$
```

我看Makefile了，默认就是需要依赖protoc的。

```
protoc --plugin=protoc-gen-nanopb=/home/hlxiong/work/tools/nanopb/nanopb-master/generator/protoc-gen-nanopb --nanopb_out=. ./ama.proto
```



是可以分成多个文件，但是还不如我自己手动先拼成一个的。

我把所有的proto文件，按照顺序拼成ama.proto文件。

所有的options文件，拼成ama.options文件。

可以生成数组形式的。

```
typedef PB_BYTES_ARRAY_T(64) ConnectionDetails_identifier_t;
typedef struct _ConnectionDetails {
    ConnectionDetails_identifier_t identifier;
/* @@protoc_insertion_point(struct:ConnectionDetails) */
} ConnectionDetails;
```





nanopb支持proto3的语法，这就是SimpleMessage_init_default的作用了。







参考资料

1、nanopb关于string类型的处理

https://www.jianshu.com/p/cad578f48e0a

2、nanopb文档，很好很详细。

https://jpa.kapsi.fi/nanopb/docs/concepts.html#compiling-proto-files-for-nanopb

3、Discrepancy of max_size between string and bytes types

https://github.com/nanopb/nanopb/issues/107