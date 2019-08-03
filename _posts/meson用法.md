---
title: meson用法
date: 2019-08-03 16:32:19
tags:
	- 编译

---

1

现在看到不少的工程是用meson.build来做编译脚本的。

了解一下。

安装meson和ninja。

依赖python3.5版本以上和ninja 1.5版本以上。

```
git clone https://github.com/mesonbuild/meson.git
然后把目录加入到PATH环境变量里。
```

```
sudo apt install ninja-build
```



ninja是谷歌为了开发chrome而做的工具。

进行编译：

```
在有meson.build的目录下，执行meson.py build。
然后会在当前目录生成一个build目录。
进入到build目录。
ninja 
然后就会进行编译。
```

meson.build文件。

```
project('tutorial', 'c')
executable('demo', 'test.c')
```

test.c文件：

```
#include<stdio.h>

int main(int argc, char **argv) {
  printf("Hello there.\n");
  return 0;
}
```



参考资料

1、使用 meson 编译代码

https://blog.csdn.net/CaspianSea/article/details/78848021

