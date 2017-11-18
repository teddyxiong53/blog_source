---
title: Python之yaml使用
date: 2017-11-18 09:40:26
tags:
	- Python

---



最常见的情况就是用yaml写配置文件，然后Python应用去读取配置文件。

# 读取yml文件

test.py内容：

```
#!/usr/bin/python 

import yaml

f = open("test.yml")
print yaml.load(f)
```

test.yml内容：

```
name : teddy
age : 20
habit:
    - basketball
    - running
work:
    name: software
    year: 5
```

输出如下：

```
pi@raspberrypi:~/work/test/py-test$ ./test.py 
{'age': 20, 'work': {'name': 'software', 'year': 5}, 'name': 'teddy', 'habit': ['basketball', 'running']}
```

可以看出，是用字典的方式在Python里进行呈现的。



