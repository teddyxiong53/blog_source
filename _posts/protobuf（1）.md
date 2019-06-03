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



# nodejs版本使用

需要nodejs10.14版本才能编译通过。

高了低了都有问题。

person.proto文件

```
package tutorial;

message Person
{
	required string name = 1;
	required int32 age = 2;
	optional string email = 3;
}
```

xhl_test.js

```
const protobuf = require("protobufjs");
protobuf.load("./person.proto").then((root)=> {
    person = root.lookupType("Person");
    console.log(person);
});
```

打印的一部分内容是：

```
Type {
  options: undefined,
  name: 'Person',
  parent:
   Namespace {
     options: undefined,
     name: 'tutorial',
     parent:
      Root {
        options: undefined,
        name: '',
        parent: null,
        resolved: false,
        comment: null,
        filename: null,
        nested: [Object],
        _nestedArray: [Array],
        deferred: [],
        files: [Array] },
     resolved: false,
     comment: null,
     filename: null,
     nested: { Person: [Circular] },
     _nestedArray: null,
     Person: [Circular] },
  resolved: false,
  comment: null,
  filename: 'person.proto',
  nested: undefined,
  _nestedArray: [],
  fields:
   { name:
      Field {
        options: undefined,
        name: 'name',
        parent: [Circular],
        resolved: false,
        comment: null,
        filename: 'person.proto',
        rule: 'required',
        type: 'string',
        id: 1,
        extend: undefined,
        required: true,
        optional: false,
        repeated: false,
        map: false,
        message: [Circular],
        partOf: null,
        typeDefault: null,
        defaultValue: null,
        long: false,
        bytes: false,
        resolvedType: null,
        extensionField: null,
        declaringField: null,
        _packed: null },
     age:
```

可以看出，里面是需要用person.fields['name']这样才能访问我需要的内容。

但是还是不对。



# C++里使用

新建一个addressbook.proto文件。

```
syntax = "proto2";

package tutorial;

message Person {
  required string name = 1;
  required int32 id = 2;
  optional string email = 3;

  enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  message PhoneNumber {
    required string number = 1;
    optional PhoneType type = 2 [default = HOME];
  }

  repeated PhoneNumber phones = 4;
}

message AddressBook {
  repeated Person people = 1;
}
```

编译成c++源文件。

```
protoc -I=./ --cpp_out=./out ./addressbook.proto
```

生成目录：

```
hlxiong@hlxiong-VirtualBox:~/work/test/protobuf$ tree
.
├── addressbook.proto
└── out
    ├── addressbook.pb.cc
    └── addressbook.pb.h
```

生成的代码，可读性非常差。

看看怎么使用。



网络发送，就这样就好了。

```
string data;  
demo::People p;  
p.set_name("Hideto");  
p.set_id(123);  
p.set_email("hideto.bj@gmail.com");  
p.SerializeToString(&data);  
char bts[data.length()];  
strcpy(bts, data.c_str());  
send(connectfd, bts, sizeof(bts), 0);  
```



#C和C++对比

simple.proto

```
syntax = "proto2";

message SimpleMessage {
    required int32 lucky_number = 1;
}
```

把这个的nanopb的C语言版本，跟c++版本的生成文件对比一下。

C语言的生成内容，有效的就是这些：

```
typedef struct _SimpleMessaeg {
    int32_t lucky_number;
} SimpleMessage;

#define SimpleMessage_init_default {0}
#define SimpleMessage_init_zero {0}

#define SimpleMessage_lucky_number_tag 1

extern pb_field_t SimpleMessage_fields[2];
#define SimpleMessage_size 11

pb_field_t SimpleMessage_fields[2] = {
    PB_FIELD(1, INT32, REQUIRED, STATIC, FIRST, SimpleMessage, lucky_number, lucky_number, 0),
    PB_LAST_FIELD
};
```

c++的生成结果。

```

#include <google/protobuf/port_def.inc>
#include <google/protobuf/prot_undef.inc>
//... 头文件包含

//内部实现细节，不要直接使用
struct TableStruct_simple_2eproto {

};
void AddDescriptors_simple_2eproto();
class SimpleMessage;
class SimpleMessageDefaultTypeInternal;
//
class SimpleMessage : public ::google::protobuf::Message
{
public:
    SimpleMessage();
    virtual ~SimpleMessage();
    //拷贝构造
    SimpleMessage(const SimpleMessage& from);
    //移动构造

    inline UnknownFieldSet& unknown_fields() {
        return _internal_metadata_.unknown_fields();
    }

    static const Descriptor* descriptor() {
        return default_instance().GetDescriptor();
    }
    static const SimpleMessage& default_instance();
    static vodi InitAsDefaultInstance();//这个只能内部使用。
    void Swap(SimpleMessage* other);
    //实现
    inline SimpleMessage* New() {
        return CreateMaybeMessage<SimpleMessage>(nullptr);
    }
    void CopyFrom();
    void MergeFrom();
    void Clear();
    bool IsInitialized();
    size_t ByteSizeLong();
private:
    void SharedCtor();
    void SharedDtor();

public://对外的主要就是这些。
    bool has_lucky_number();
    void clear_lucky_number();
    static const kLuckyNumberFieldNumber = 1;
    int32 lucky_number();
    void set_lucky_number(int32 value);
private:
    int32 lucky_number_;
};
//内联实现函数
inline bool SimpleMessage::has_lucky_number() {
    return (_has_bits_[0] & 0x00000001u) != 0;
}
inline int32 SimpleMessage::lucky_number() {
    return lucky_number_;
}
inline void SimpleMessage::set_lucky_number(int32 value) {
    _has_bits_[0] |= 0x00000001u;
    lucky_number_ = value;
}
```



上面看到情况，没有涉及到repeated元素。

对于repeated，有这些特点：

```
xx_size();
add_xx();

```

一个通讯录里有多个人，一个人有多个号码。



# proto2和proto3的对比

对于addressbook.proto文件，这个默认是proto2的，我们把required、optional这些去掉，把头部改成proto3的。

可以得到一个proto3版本的文件。

然后用protoc编译，把v2和v3得到的代码文件进行对比。

没有什么本质区别。

```
Person_PhoneNumber
	这个是因为在Person内部定义，所以前面有Person_前缀。
Person
AddressBook
```

一个message对应一个class。



用nanopb生成看看。数组的，和普通的，都是pb_callback_t类型。

```
/* Struct definitions */
typedef struct _AddressBook {
    pb_callback_t people;
/* @@protoc_insertion_point(struct:AddressBook) */
} AddressBook;
```



参考资料

1、更小、更快、更简单Google ProtoBuf 跨语言通信协议

https://juejin.im/post/5938f1785c497d006b613b0d

2、Google Protocol Buffers 简介（一）

https://www.jianshu.com/p/7de98349cadd

3、protobuf-c的使用（一）构建

https://blog.csdn.net/kid_2412/article/details/52275582

4、在NodeJS中玩转Protocol Buffer

https://blog.csdn.net/zhulin2609/article/details/50977107

5、

https://developers.google.com/protocol-buffers/docs/cpptutorial

6、Google Protocol Buffer 的使用和原理

https://www.ibm.com/developerworks/cn/linux/l-cn-gpb/index.html

7、

https://blog.csdn.net/cscrazybing/article/details/78061475

8、

https://blog.csdn.net/k346k346/article/details/51754431

9、protobuf的数据类型和C++数据类型

https://blog.csdn.net/wangchong_fly/article/details/47614699

10、最常用的两种C++序列化方案的使用心得（protobuf和boost serialization）

https://www.cnblogs.com/lanxuezaipiao/p/3703988.html

11、protobuf c++客户端/服务器例子

https://blog.csdn.net/u014538198/article/details/72389017

12、protobuf repeated类型的使用

https://blog.csdn.net/mycwq/article/details/19622571

13、protobuf 中的嵌套消息的使用 主要对set_allocated_和mutable_的使用

https://blog.csdn.net/xiaxiazls/article/details/50118161