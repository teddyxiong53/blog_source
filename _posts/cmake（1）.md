---
title: cmake（1）
date: 2018-06-21 15:19:08
tags:
	- cmake

---





cmake是一个跨平台的编译工具。

可以用简单的语句来描述所有平台的编译。

可以输出各种Makefile和project文件。

类似unix下的automake。



https://cmake.org/documentation



我当前在Ubuntu上默认安装的是3.5.1版本。



# helloworld

写一个CMakelists.txt文件。

```
cmake_minimum_required(VERSION 3.1)
project(xxx)
add_executable(xxx test.cpp)
```

我开始把xxx写成test的，不行，好像test是被保留了。

```
mkdir build
cd build
cmake ../
```

这样生成的目录结构是这样的：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp$ tree
.
├── build
│   ├── CMakeCache.txt
│   ├── CMakeFiles
│   │   ├── 3.5.1
│   │   │   ├── CMakeCCompiler.cmake
│   │   │   ├── CMakeCXXCompiler.cmake
│   │   │   ├── CMakeDetermineCompilerABI_C.bin
│   │   │   ├── CMakeDetermineCompilerABI_CXX.bin
│   │   │   ├── CMakeSystem.cmake
│   │   │   ├── CompilerIdC
│   │   │   │   ├── a.out
│   │   │   │   └── CMakeCCompilerId.c
│   │   │   └── CompilerIdCXX
│   │   │       ├── a.out
│   │   │       └── CMakeCXXCompilerId.cpp
│   │   ├── cmake.check_cache
│   │   ├── CMakeDirectoryInformation.cmake
│   │   ├── CMakeOutput.log
│   │   ├── CMakeTmp
│   │   ├── feature_tests.bin
│   │   ├── feature_tests.c
│   │   ├── feature_tests.cxx
│   │   ├── Makefile2
│   │   ├── Makefile.cmake
│   │   ├── progress.marks
│   │   ├── TargetDirectories.txt
│   │   └── xxx.dir
│   │       ├── build.make
│   │       ├── cmake_clean.cmake
│   │       ├── DependInfo.cmake
│   │       ├── depend.make
│   │       ├── flags.make
│   │       ├── link.txt
│   │       └── progress.make
│   ├── cmake_install.cmake
│   └── Makefile
├── CMakeLists.txt
└── test.cpp

7 directories, 31 files
```

然后我们在build目录下，make。

就得到xxx可执行文件了。

# 基本语法

定义变量

```
set mydir=./
```

条件判断：

```
if(${Platform} STREQUAL ABC
else()
endif()
```

```
if(${Platform} MATCHES "ABC")
```



# 添加宏定义

```
cmake_minimum_required(VERSION 2.8)
add_definitions("-Wall -std=c++11 -DDEBUG=1")
add_executable(xxx main.cpp)
```



# 多目录实用工程

放在我的github上了。

https://github.com/teddyxiong53/c_code/tree/master/cmake_template



# 调试方法

用

```
message([SEND_ERROR | STATUS | FATAL_ERROR] "message to display" ...)
```



指定链接路径

link_directories

添加宏定义。

add_definitions

头文件包含

include_directories

定变量 set



# 参考资料

https://blog.csdn.net/dabenxiong666/article/details/53998998

https://blog.csdn.net/gg_18826075157/article/details/72780431



https://www.cnblogs.com/lidabo/p/7359422.html

