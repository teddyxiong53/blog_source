---
title: python之simpledb研究
date: 2023-01-20 18:05:31
tags:
	- Python

---



代码在这里：

https://github.com/coleifer/simpledb

# 运行测试

安装：

```
pip3 install -U simpledb
```

启动服务端：

```
$ simpledb.py -d -t  -p 31339
  .--.
 /( @ >    ,-.  SimpleDB 127.0.0.1:31339
/ ' .'--._/  /
:   ,    , .'
'. (___.'_/
 ((-((-''
```

如果不指定-t选项，那么就是默认使用greenlet，需要安装greenlet。

我还是指定-t的选项。用thread的并发方案。

然后写python代码，连接到这个server。

```
from simpledb import Client
client = Client(port=31339)
client.set('key', {
    'name': 'allen',
    'pets': [
        'kitty',
        'tom'
    ]
})
print(client.get('key'))
```

需要指定port，因为当前的默认port和server监听的对不上。

就是类似redis，get和set接口。



支持的数据类型：

```
str /二进制
数字
null
list：可嵌套
dict ：可嵌套
```

# 代码分析

就一个文件，代码1000行左右。

我只看thread版本实现的。

