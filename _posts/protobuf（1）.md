---
title: protobuf（1）
date: 2018-11-28 11:10:28
tags:
	- 编程
typora-root-url: ..\
---



看ama的协议，看到.proto后缀的文件，搜索了一下，发现是属于一种protobuf的编程语言写的。

现在了解一下。

# 什么是protobuf

是谷歌推出的，用于不同语言之间进行通信的一个标准。

本来是在谷歌内部使用的。后面开源了。

全称是Google Protocol Buffer。

其作用开源参考xml文件。

优点是更加小、更快。

是序列化的数据结构。

在谷歌内部长期使用，稳定可靠。

开源支持c、c++、python、java等多种语言。

编码后，消息更小，方便传输和存储。

保证了向前兼容。

# HelloWorld

看看怎么写一个简单程序，把这个东西用起来。

我们用c++写一个例子，进行读写操作。

首先下载protobuf的代码。

地址在这：https://github.com/protocolbuffers/protobuf

编译：

```
./autogen.sh
./configure
make -j4
sudo make install
```

编译还比较耗时。

安装之后，需要sudo ldconfig一下，不然 会报对应的so文件找不到。

写一个person.proto文件。内容如下：

```
package tutorial;

message Person
{
	required string name = 1;
	required int32 age = 2;
	optional string email = 3;
}
```

执行：

```
protoc -I=./ --cpp_out=./ ./person.proto 
```

生成文件：

```
hlxiong@hlxiong-VirtualBox:~/work/test/protobuf$ ls
person.pb.cc  person.pb.h  person.proto
```

package在c++里，被转成了namespace。

生成的文件比较复杂，不方便阅读。

支持的语言是这些：

```
 --cpp_out=OUT_DIR   
 --csharp_out=OUT_DIR
 --java_out=OUT_DIR  
 --js_out=OUT_DIR    
 --objc_out=OUT_DIR  
 --php_out=OUT_DIR   
 --python_out=OUT_DIR
 --ruby_out=OUT_DIR  
```

不支持C语言。

看看python的生成结果。

```
 protoc -I=./ --python_out=./ ./person.proto 
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/protobuf$ ls
person_pb2.py  person.proto
```

那么生成的文件，应该怎么使用呢？



# C语言版本

虽然谷歌官方没有提供C语言支持，但是有第三方的开源支持。

代码在这里：

https://github.com/protobuf-c/protobuf-c

是需要在编译安装了protobuf默认版本的基础上，再安装这个，相当于是一个补丁。



# 怎么使用生成的文件

还是回到c++版本，我们生成了c++文件和头文件，怎么使用呢？

新建一个main.cpp文件。

```
#include "person.pb.h"
#include <iostream>

int main()
{
	tutorial::Person person;
	person.set_name("allen");
	//person.set_age(20);
	//person.set_email("allen@xx.com");
	
	std::cout << "name:" << person.name() << std::endl;
}
```

编译：

```
 g++ -std=c++11 main.cpp person.pb.cc  -lprotobuf
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/protobuf$ ./a.out 
[libprotobuf FATAL google/protobuf/generated_message_util.cc:785] CHECK failed: (scc->visit_status.load(std::memory_order_relaxed)) == (SCCInfoBase::kRunning): 
terminate called after throwing an instance of 'google::protobuf::FatalException'
  what():  CHECK failed: (scc->visit_status.load(std::memory_order_relaxed)) == (SCCInfoBase::kRunning): 
已放弃 (核心已转储)
```

会挂掉。

不知道为什么。

# python版本的使用

当前目录写一个test.py文件。

```
from person_pb2 import Person

p = Person()
p.name = "allen"
print p.name
```



参考资料

1、更小、更快、更简单Google ProtoBuf 跨语言通信协议

https://juejin.im/post/5938f1785c497d006b613b0d

2、Google Protocol Buffers 简介（一）

https://www.jianshu.com/p/7de98349cadd

3、protobuf-c的使用（一）构建

https://blog.csdn.net/kid_2412/article/details/52275582