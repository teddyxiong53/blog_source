---
title: dlopen
date: 2020-06-10 13:11:08
tags:
	- Linux

---

1

函数原型：

```
#include <dlfcn.h>
void *dlopen(const char *filename, int flags);
int dlclose(void *handle);
```

编译的时候，需要-ldl来链接。

dlopen是载入一个动态库。

返回一个handle。后续可以通过handle来使用动态库。

```
dlsym
dladdr
dlinfo
	这3个函数，都是通过handle来进行操作的。
```

dlopen的时候，如果filename为空，那么返回的handle就是当前进程。

```
#include "mylog.h"
#include <dlfcn.h>


typedef double (*func_type)(double) ;

int main(int argc, char const *argv[])
{
    func_type f;
    void *handle = dlopen("libm.so.6", RTLD_NOW);
    if(!handle) {
        myloge("load fail");
        return -1;
    }
    dlerror();//清空错误。
    f = (func_type)dlsym(handle, "cos");
    char *error = dlerror();
    if(error) {
        myloge("error:%s", error);
        return -1;
    }
    mylogd("%f", (*f)(2.0));
    return 0;
}
```



参考资料

1、man手册



