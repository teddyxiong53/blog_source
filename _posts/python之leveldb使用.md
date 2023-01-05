---
title: python之leveldb使用
date: 2018-10-12 14:42:51
tags:
	- python
---



安装：

```
sudo pip install leveldb
```



# 基本使用

## 读写

```
#!/usr/bin/python

import leveldb

def single_operate():
	db = leveldb.LevelDB("./data")
	db.Put('key1', 'value1')
	print db.Get('key1')
	db.Delete('key1')
	print db.Get('key1')
	
single_operate()
```

输出是：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ ./test.py 
value1
Traceback (most recent call last):
  File "./test.py", line 12, in <module>
    single_operate()
  File "./test.py", line 10, in single_operate
    print db.Get('key1')
KeyError
```

## 遍历

```
def test_iter():
    db = leveldb.LevelDB('./data')
    for i in xrange(10):
        db.Put(str(i), 'string_%s' % i)
    print list(db.RangeIter(key_from = '2', key_to = '5'))
    print list(db.RangeIter(key_from = '2', key_to = '5',reverse=True))
	
test_iter()
```

输出是：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ ./test.py 
[('2', 'string_2'), ('3', 'string_3'), ('4', 'string_4'), ('5', 'string_5')]
[('5', 'string_5'), ('4', 'string_4'), ('3', 'string_3'), ('2', 'string_2')]
```



# 参考资料

1、LevelDB（适用于写多读少场景）

https://blog.csdn.net/qq_26222859/article/details/79645203