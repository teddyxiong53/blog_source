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



# 4. 默认配置

在port/mpconfigport.h里。如果这里没有配置，就用py/mpconfig.h里的默认值。



# 5. mp项目了解

mp的官网在这里：http://www.micropython.org/

这个实现是以python3的为参考的。

实现了生成器、异常处理等高级特性。只需要256K的rom和16K的ram就可以跑起来。

官方有推出一款叫做pyboard的开发板来做这个。

