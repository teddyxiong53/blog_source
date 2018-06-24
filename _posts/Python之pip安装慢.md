---
title: Python之pip安装慢
date: 2018-06-06 23:19:19
tags:
	- Python

---



在这个文件写入这些内容就好了。

~/.pip/pip.conf 

```
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com 
```



如果是windows下， 则是在C:\Users\Administrator\pip目录下，新建pip.ini文件。

填入上面的内容。

