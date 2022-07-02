---
title: express之feathers.js研究
date: 2022-01-16 13:17:11
tags:
	- nodejs

---

--

发现feathers的资源挺多的。研究一下。

这样创建一个服务

```
class MessageService 
里面实现了
find and create 
还可以实现
get, update, patch and remove
```

创建一个api server。

就需要引入

```
const feathers = require('@feathersjs/feathers');
const express = require('@feathersjs/express');
const socketio = require('@feathersjs/socketio');
```

安装

```
npm install @feathersjs/socketio @feathersjs/express --save
```

这样访问。

http://localhost:3030/messages

在浏览器里也可以使用feathers。

# 使用cli工具

安装cli工具

```
npm install @feathersjs/cli -g
```

创建一个应用

```
mkdir feathers-chat
cd feathers-chat/
feathers generate app
```

根据提示选择相关的配置。

创建的目录说明

```
没什么特别的。
```

# services

service是feathers框架里的一个核心概念。

一个service是一个实现了特定方法的object。

service实现了统一的、协议无关的接口。用来跟这些数据进行交互：

1、读写数据库。

2、filesystem

3、call其他的api

4、call其他的服务：发送邮件、处理支付、返回某个天气等等

协议无关是指，一个service可以通过rest api、websocket或其他方式进行调用。

service需要实现的方法包括

1、find。根据query找到数据。

2、get。拿到一条数据。

3、create。创建数据。

4、update

5、patch

6、remove。

举例

```
class MyService {
  async find(params) {}
  async get(id, params) {}
  async create(data, params) {}
  async update(id, data, params) {}
  async patch(id, data, params) {}
  async remove(id, params) {}
}

app.use('/my-service', new MyService());

```

这些函数的参数有3个：

1、id。唯一标识一个data。

2、data。用户发送过来的数据，用来create、update、patch等操作。

3、params。可选的，例如query、user等。

上面这些不是必须都实现，至少实现一个。

通过rest api调用的时候，url和函数的对应关系是这样的

| Service method                              | HTTP method | Path                  |
| ------------------------------------------- | ----------- | --------------------- |
| `service.find({ query: {} })`               | GET         | /messages             |
| `service.find({ query: { unread: true } })` | GET         | /messages?unread=true |
| `service.get(1)`                            | GET         | /messages/1           |
| `service.create(body)`                      | POST        | /messages             |
| `service.update(1, body)`                   | PUT         | /messages/1           |
| `service.patch(1, body)`                    | PATCH       | /messages/1           |
| `service.remove(1)`                         | DELETE      | /messages/1           |

## 注册service的方法

一句话就可以：

```
app.use('messages', new MessageService());
```



拿到service并进行调用的方法

```
const messageService = app.service('messages');
const messages = await messageService.find();
```

## service 事件

一个service默认就是一个nodejs EventEmitter。

| Service method     | Service event           |
| ------------------ | ----------------------- |
| `service.create()` | `service.on('created')` |
| `service.update()` | `service.on('updated')` |
| `service.patch()`  | `service.on('patched')` |
| `service.remove()` | `service.on('removed')` |

## 数据库适配

虽然可以适应多种数据后端，但是数据库是最主流的使用方式。

```
内存方式的：
	nedb
	feathers-memory
localstorage方式
	feathers-localstorage
文件系统方式
	feather-nedb
mongodb
mysql
sqlite
elasticsearch
```

当前我们使用nedb来进行举例，因为这个简单。

## 用cli来生成一个service

```
feathers generate service
```

根据提示进行选择即可。

我们创建一个名字为messags的service。

## 自定义service

我们默认生成的工程。里面默认就有一个user的service。

给它加上avatar属性。



# hooks



# chat例子



# 参考资料

1、

https://docs.feathersjs.com/guides/basics/starting.html#our-first-app
