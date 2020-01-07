---
title: cmake（1）
date: 2018-06-21 15:19:08
tags:
	- cmake

---





cmake是一个跨平台的编译工具。

是跨平台的Makefile生成工具。



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



添加链接选项。

```
set_target_properties
```



```
enable_testing
	这个是做什么？
	只需要在最上层目录的CMakeLists.txt里设置一次就好了。
```



list命令和set命令比较



命令不区分大小写。

变量名区分大小写。

我尽量做到这样：

变量名用大写。命令都用小写。



# 常用命令

```
list(APPEND ..)
	往变量里追加值。
string(REPLACE ";" " " CMAKE_CXX_FLAGS "${CXX_FLAGS}")
	
find_pacage(Boost REQURIED)
	效果是生成一个变量：${Boost_INCLUDE_DIRS}
find_path(MYPATH stdio.h) 这样的效果是：MYPATH的之变为stdio.h所在的路径名。
类似的是，
find_library(MYLIB c)
message(${MYLIB})
得到是是：/usr/lib/x86_64-linux-gnu/libc.so

set(CMAKE_BUILD_TYPE release)
string(TOUPPER ${CMAKE_BUILD_TYPE} BUILD_TYPE) #BUILD_TYPE是输出的变量名。
message(${BUILD_TYPE})

install(TARGETS muduo_base DESTINATION lib)
这个对应的是：
./build/release-cpp11/lib/libmuduo_base.a

file命令

```



##include命令

主要用来载入CMakeLists.txt文件，或者cmake模块。

例如：

```
include(CheckFunctionExists) #这个是一个cmake模块。
```





#cmake脚本语言

```
1、#表示注释。
2、命令可以没有参数、有参数、多行参数。
	命令格式：cmd(arg)
3、变量分为两种：cmake预定义的，和自定义的。
	定义变量，用set命令。set(key value)
	message(value) 用来打印调试。
	引用变量是${var}
	set(x 3) # x= "3"
	set(y 1) # y="1"
	message(x y) # display
	所有的变量值都是字符串类型的。
	字符串可以计算为bool值。
	例如，在if和while里。
	"false","off","no"这些值被解释为false。
	变量有两种设置方式：
	1、用set。
	2、在命令行里cmake -DXX=YY这样。
4、逻辑运行。and not or。

```



最简单的CMakeLists.txt文件。

```
message(hello)
```

执行是：cmake ./。

为了让文件显得不那么乱。我们新建这样的目录。

```
build  CMakeLists.txt  src
```

```
hlxiong@hlxiong-VirtualBox ~/work/test/cmake/src $ tree    
.
├── exe
│   └── main.cpp
└── lib
    ├── foo.cpp
    └── foo.hpp
```

执行：

```
cd build
cmake ../
```

这样生成的文件，都在build目录下。

随时可以删掉build目录。

定义变量看看：

```
set(x 3)
set(y 1)
message(x y)
message(${x}${y})
```

注意，引用变量是${}，而不是Makefile里的小括号。



```
set(x 3 2)
message(${x})
```

这样得到的是“32”。

```
set(x hello world !)
message(${x})
```

这样得到是是“helloworld!”。效果是空格被去掉了。

可以用foreach来遍历变量值。

```
set(x hello world !)
foreach(val ${x})
    message(${val})
endforeach()
```

多个目录。

```
add_subdirectory(lib)
add_subdirectory(exe)
```

lib、exe目录下也要有CMakeLists.txt文件。



# cmake预定义变量

基本变量

就是路径、文件、行数。

```
message(${PROJECT_SOURCE_DIR})
message(${PROJECT_BINARY_DIR})
message(${CMAKE_CURRENT_SOURCE_DIR})

message(${CMAKE_CURRENT_LIST_FILE})
message(${CMAKE_CURRENT_LIST_LINE})

message(${PROJECT_NAME})
```

开关选项

```
message(${BUILD_SHARED_LIBS})
message(${CMAKE_C_FLAGS})
message(${CMAKE_CXX_FLAGS})
message(${CMAKE_C_COMPILER})
message(${CMAKE_CXX_COMPILER})
message(${CMAKE_BUILD_TYPE})
```



变量的

# 问题解决

被依赖的库，要写在后面。

```
例如libA。依赖了LibB。
在target_link_libraries(要这样写。
libA
libB
如果顺序写错了，就会报符号找不到的错误。我查一个这样的错误， 查了1个多小时。
```

可以用--start-group来避免顺序问题。





cmake文件被包含的时候，可以用这个保护头，来避免被多次包含时的问题。

```
if (DEFINED JSonParserGuard)
  return()
endif()

set(JSonParserGuard yes)
```



# 参考资料

1、

https://blog.csdn.net/dabenxiong666/article/details/53998998

2、

https://blog.csdn.net/gg_18826075157/article/details/72780431

3、

https://www.cnblogs.com/lidabo/p/7359422.html

4、CMake 指定目标的链接选项

https://blog.csdn.net/icbm/article/details/53390467

5、What does enable_testing() do in cmake?

https://stackoverflow.com/questions/50468620/what-does-enable-testing-do-in-cmake

6、CMake--List用法

https://www.cnblogs.com/narjaja/p/8343765.html

7、

https://github.com/mortennobel/CMake-Cheatsheet/blob/master/CMake_Cheatsheet.pdf

8、CMake 手册详解（二十二）

这个系列很好。

https://www.cnblogs.com/coderfenghc/archive/2012/10/20/2712806.html

9、CMake命令target_link_libraries链接库的顺序

https://blog.csdn.net/zhujianwei31415/article/details/50727952

10、

https://www.cnblogs.com/flyinggod/p/8026789.html

11、

https://blog.csdn.net/Aquester/article/details/84881574

12、cmake教程4(find_package使用)

这个教程写得很好。

https://blog.csdn.net/haluoluo211/article/details/80559341