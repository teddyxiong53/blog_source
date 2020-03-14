---
title: gcc之链接rpath
date: 2020-03-13 09:46:13
tags:
	- gcc

---

1

现在碰到一个buildroot里的连接问题，发现自己对于链接的位置不是很了解。

新建工程，目录结构如下：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ tree
.
├── hello.c
├── Makefile
├── test.c
└── world.c
```

hello.c

```
#include <stdio.h>
extern void world();

void hello()
{
    printf("hello\n");
    world();
}
```

world.c

```
#include <stdio.h>

void world()
{
    printf("world\n");
}
```

test.c

```
extern void hello();

void main()
{
    hello();
}
```

Makefile

```
.PHONY: all clean

CFLAGS += -fPIC
all:
	gcc $(CFLAGS) -c hello.c
	gcc $(CFLAGS) -c world.c
	gcc -shared -o libhello.so hello.o
	gcc -shared -o libworld.so world.o
	gcc test.c -o test -L./ -lhello -lworld
clean:
	rm -f *.o *.so test
```

-fPIC必须加，不然编译无法c文件就无法通过。

最后链接得到test的时候，也必须指定-L./ ，不然链接失败。

ldd libhello.so

```
目前看到是依赖了3个库
linux-vdso.so
libc.so
ld.so.2
```

ldd libworld.so也是这3个库。

其实libhello.so依赖了libworld.so，当前ldd没有体现出来。要体现出这个关系。

需要修改一下命令：先编译world，再编译hello，且加上-lworld -L .

```
	gcc -shared -o libworld.so world.o
	gcc -shared -o libhello.so hello.o -lworld -L .
```

现在再看ldd libhello.so。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ldd libhello.so 
        linux-vdso.so.1 =>  (0x00007fff0758d000)
        libworld.so => ./libworld.so (0x00007f549383a000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f5493470000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f5493c3e000)
```

test要运行成功，还需要设置：

```
export LD_LIBRARY_PATH=./
```

上面这些操作，都是我平时最常用的解决方式。

但是还可以用rpath来解决。

是这样做：

1、unset LD_LIBRARY_PATH，清空这个环境变量。这时候再运行test，是会提示so找不到的。

2、修改Makefile。加上-Wl,-rpath .

```
gcc test.c -o test -L./ -lhello -Wl,-rpath .
```

3、运行test，也可以成功运行的。

由此可见，使用了-rpath参数指定库的路径后，生成的可执行文件的依赖库路径并非就固定不变了。

而是执行时先从-rpath指定的路径去找依赖库，如果找不到，还是会报not fund。



  并非指定-rpath参数后，就抛弃LD_LIBRARY_PATH环境变量，只是多了个可选的依赖库路径而已。



参考资料

1、GCC 中 -L、-rpath和-rpath-link的区别

https://www.cnblogs.com/lsgxeva/p/8257784.html