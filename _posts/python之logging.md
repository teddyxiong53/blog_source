---
title: python之logging
date: 2017-07-23 00:13:38
tags:
	- python
	- logging
---

logging是线程安全的。

# 1. 基本使用

```
import logging
logging.debug("this is debug")
logging.info("this is info")
logging.warning("this is warning")
```

这个的运行效果是：

```
teddy@teddy-ubuntu:~/work/test/py-test/logging$ python ./test.py 
WARNING:root:this is warning
```

可以看到，默认设置的级别，只有warning打印出来了。

# 2. 设置日志

```
import logging

logging.basicConfig(level=logging.DEBUG, \
	format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',\
	datefmt='%a, %d %b %Y %H:%M:%S',\
	filename='myapp.log',\
	filemode='w'\
	)
logging.debug("this is debug")
logging.info("this is info")
logging.warning("this is warning")
```

运行效果如下：

```
teddy@teddy-ubuntu:~/work/test/py-test/logging$ python ./test.py 
teddy@teddy-ubuntu:~/work/test/py-test/logging$ ls
myapp.log  test.py
teddy@teddy-ubuntu:~/work/test/py-test/logging$ cat myapp.log 
Sun, 23 Jul 2017 00:21:26 test.py [line:9] DEBUG this is debug
Sun, 23 Jul 2017 00:21:26 test.py [line:10] INFO this is info
Sun, 23 Jul 2017 00:21:26 test.py [line:11] WARNING this is warning
```

