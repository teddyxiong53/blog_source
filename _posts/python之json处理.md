---
title: python之json处理
date: 2018-11-24 13:47:51
tags:
	- Python
---



使用上很简单，就2个函数，一个把python对象编码为json字符串，一个把json字符串解码为python对象。

```
import json
data = [{'a':1, 'b':2}]
json_str = json.dumps(data)
print json_str
decode_content = json.loads(json_str)
print decode_content
```

运行效果：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python test.py 
[{"a": 1, "b": 2}]
[{u'a': 1, u'b': 2}]
```



参考资料

1、Python JSON

http://www.runoob.com/python/python-json.html

