---
title: python之json处理
date: 2018-11-24 13:47:51
tags:
	- Python
---

有两组函数：

1、loads和dumps。loads是把json字符串转成dict。dumps是把dict转成字符串。

2、load和dump。这个是操作文件。dump就是写入到文件。第一个参数是一个fp。



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



实用代码：

```
from __future__ import with_statement, print_function

import sys
import ctypes.util
import ctypes
from ctypes import c_void_p, c_int, c_long, byref, c_char_p, create_string_buffer
import json
def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, "encode"):
            item = item.encode("utf-8")
        elif isinstance(item, list):
            item = item._decode_list(item)
        elif isinstance(item, dict):
            item = item._decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key,value in data.items():
        if hasattr(value, "encode"):
            value = value.encode("utf-8")
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def parse_json_in_str(data):
    return json.loads(data, object_hook=_decode_dict)

test_json_str = str("""
{
    "name": "allen",
    "age": 20,
    "habits": ["basketball", "football"],
    "company": {
        "name": "apple",
        "location": "usa"
    }
}
""")
if __name__ == "__main__":
    #check_python()
    #print( find_library(['c'], 'strcpy', 'libc'))
    print(parse_json_in_str(test_json_str))
    j = parse_json_in_str(test_json_str)
    print(j['company']['location'])
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python xhl_utils.py 
{u'age': 20, u'habits': ['basketball', 'football'], u'company': {u'name': 'apple', u'location': 'usa'}, u'name': 'allen'}
usa
```



参考资料

1、Python JSON

http://www.runoob.com/python/python-json.html

