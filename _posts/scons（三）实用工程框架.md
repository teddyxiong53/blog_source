---
title: scons（三）实用工程框架
date: 2018-02-12 16:59:43
tags:
	- scons

---



在我的GitHub地址这里：c_code/scons_template下建立目录。

build是指定输出的目录。

```
pi@raspberrypi:~/work/test/scons/scons_template$ tree
.
├── app
│   ├── main.c
│   └── SConscript
├── build：输出目录。自动生成的。
│   ├── mod1
│   │   └── src
│   └── mod2
│       └── src
├── link.lds：链接脚本。
├── mod1
│   ├── include
│   │   └── mod1.h
│   ├── SConscript
│   └── src
│       └── mod1.c
├── mod2
│   ├── include
│   │   └── mod2.h
│   ├── SConscript
│   └── src
│       └── mod2.c
├── project_cfg.py：配置中国工程。
├── SConscript：顶层objs文件。
├── SConstruct：入口文件。
├── toolchain.py：配置工具链。
└── tools
    └── building.py：主要的编译动作。
```

现在编译清除都正常。

基本是可用的。后续再完善。

