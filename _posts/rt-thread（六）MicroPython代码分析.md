---
title: rt-thread（六）MicroPython代码分析
date: 2018-01-27 10:59:41
tags:
	- rt-thread
	- MicroPython

---



# 1. 代码的配置及下载

现在的rt-thread开始引入packages的机制，就是一些第三方的东西，默认不包含到rt-thread包里来。只是增加了配置项。如果打开了对应的配置项，则会到github上把对应的代码下载下来。并且进行编译。

# 2. 代码目录

大概240个文件。目录结构是这样。

```
├── extmod
├── lib
│   ├── mp-readline
│   └── utils
├── port
│   └── genhdr
└── py
```

# 3. 入口代码

入口是在port/mpy_main.c里。

```
static void python(uint8_t argc, char **argv) {
    if (argc > 1) {
        mpy_main(argv[1]);
    } else {
        mpy_main(NULL);
    }
}
MSH_CMD_EXPORT(python, MicroPython: `python [file.py]` execute python script);
```



mkimage的选项：

```
-A：指定ARCH
-O：指定os
-T：指定image type
-C：指定压缩type
-a：指定load addr
-e：指定entry addr
-n：指定镜像的name
-x：设置是否XIP。
-d：从哪个data文件里来数据。
#查看类的：
-l：查看当前镜像的信息。
```

举例：把zImage做成uImage。其实就是加了一个64字节的头部。头部信息就是arch、os这些信息。

```
mkimage -A arm -O linux -T kernel -C none -a 0x30008000 -e 0x30008000 -n "MyLinux" -d zImage uImage
```

