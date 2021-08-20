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

可以同时配置多个源。

```
teddy@teddy-ThinkPad-SL410:~$ cat ~/.pip/pip.conf 
[global]
index-url=http://pypi.douban.com/simple
extra-index-url=http://mirrors.aliyun.com/pypi/simple/
extra-index-url=https://pypi.tuna.tsinghua.edu.cn/simple/
extra-index-url=http://pypi.mirrors.ustc.edu.cn/simple/

[install]
trusted-host=pypi.douban.com
trusted-host=mirrors.aliyun.com
trusted-host=pypi.tuna.tsinghua.edu.cn
trusted-host=pypi.mirrors.ustc.edu.cn
```

还可以在命令行加参数直接加速。

```
sudo pip3 install numpy -i https://pypi.doubanio.com/simple
```

