---
title: nodejs之全局安装找不到
date: 2019-01-22 10:17:18
tags:
	- nodejs

---



我全局安装了express，但是使用的时候，却提示找不到。

```
Error: Cannot find module 'express'
```

网上找了下，说是需要把npm prefix -g，看得到的路径加入到PATH环境变量里。

```
hlxiong@hlxiong-VirtualBox:~/work/test/express$ npm prefix -g
/home/hlxiong/.nvm/versions/node/v10.14.0
```

我这么做了。还是不行。

继续找。

需要设置NODE_PATH这个环境变量。

我在~/.bashrc的最后一行，加上这：

```
export NODE_PATH=~/.nvm/versions/node/v10.14.0/lib/node_modules
```

source一下，就可以了。



参考资料

1、Nodejs全局安装模块后找不到命令的解决方法

https://blog.csdn.net/tp7309/article/details/78287952

2、Loading from the global folders

https://nodejs.org/api/modules.html#modules_loading_from_the_global_folders