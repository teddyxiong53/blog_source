---
title: protobuf之python版本使用
date: 2019-11-27 11:50:06
tags:
	- python
---



1

编写addressbook.proto文件如下：

```
syntax = "proto3";
package tutorial;

message AddressBook {
    repeated Person people = 1;
}

message Person {
    string name = 1;
    int32 id = 2;
    string email = 3;
    float money = 4;
    bool work_status = 5;

    repeated PhoneNumber phones = 6;
    MyMessage maps = 7;
}

message PhoneNumber {
    string number = 1;
    PhoneType type = 2;
}

enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK =2;
}

message MyMessage {
    map<int32, int32> mapfield = 1;
}
```

用protoc编译这个文件：

```
mkdir python_out
protoc --python_out=python_out addressbook.proto 
```

在python-out目录下，新建add_person.py文件。

演示了序列化和反序列化。

```
import addressbook_pb2

address_book = addressbook_pb2.AddressBook()
person = address_book.people.add()

person.id = 1
person.name = "aa"
person.email = "aa@xx.com"
person.money = 100
person.work_status = True

phone_number = person.phones.add()
phone_number.number = "1111"
phone_number.type = addressbook_pb2.MOBILE

maps = person.maps

maps.mapfield[1] = 11
maps.mapfield[2] = 22

address_book_str = address_book.SerializeToString()
print(address_book_str)
print(type(address_book_str))

address_book.ParseFromString(address_book_str)
for person in address_book.people:
    print("id:{}, name:{}, email:{}, money:{}, work_status:{}".format(person.id, person.name, person.email, person.money, person.work_status))

for phone_number in person.phones:
    print("number type:{}, number:{}".format(phone_number.type, phone_number.number))
for key in person.maps.mapfield:
    print("key:{}, value:{}".format(key, person.maps.mapfield[key]))
```



参考资料

1、

https://blog.csdn.net/u013210620/article/details/81317731