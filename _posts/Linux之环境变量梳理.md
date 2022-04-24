---
title: Linux之环境变量梳理
date: 2018-04-12 20:54:19
tags:
	- Linux

---

--

每个进程运行都有自己的环境变量。

也可以认为，shell及其在该shell中运行的子进程共用的变量，称为环境变量。

一个进程的变量有很多，分为该进程的自定义变量，及其环境变量。

# shell里环境变量

| 命令   | 说明                                                         |
| ------ | ------------------------------------------------------------ |
| set    | 显示当前shell的所有变量，包括/etc/bashrc，/etc/profile、用户环境变量、自定义环境变量。连同脚本内容一起显示出来。 |
| env    | 当前用户的环境变量。不多，十几个。                           |
| export | 显示的是从shell导出的环境变量。shell关闭后就消失了。         |
| unset  | 删除环境变量。例如unset PATH，这个就会导致ls都不可用了。     |

# C语言操作环境变量

获取环境变量

```
extern char **environ;
```

这样来打印当前的所有环境变量。

```

#include <stdio.h>
extern char ** environ;//本程序的环境变量
int main(int argc, char * argv[])
{
    int count = 0;
    while (environ[count])
    {
        puts(environ[count]);
        ++count;
    }
    printf("总行数=%d\n", count);
}
```

### `getenv`、`setenv`、`unsetenv`函数

`getenv`、`setenv`、`unsetenv`函数三个函数存在`stdlib.h`中。



# 参考资料

1、linux环境变量、environ、getenv、setenv、unsetenv

https://blog.csdn.net/native_lee/article/details/105268018



