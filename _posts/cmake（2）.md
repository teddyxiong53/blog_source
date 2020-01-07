---
title: cmake（2）
date: 2020-01-04 13:52:08
tags:
	- cmake

---

1

现在重新梳理一遍cmake。

先看一个只编译一个c++文件的最简单的工程的样子。

```
cmake_minimum_required(VERSION 3.5)
project(demo1)
set(CMAKE_CXX_STANDARD 11)
set(SOURCE_FILES main.cpp)

add_executable(demo1 ${SOURCE_FILES})
```

cmake默认是编译release版本。

如果要指定编译debug版本。

这样执行：

```
cmake -DCMAKE_BUILD_TYPE=RELEASE ../
make
```

把cmake当成一门编程语言来学习。

如何进行打印，如何定义变量，对变量赋值，输出变量的值？

```
message("hello world")#输出。
set(name "xhl") # 定义变量name，并赋值为xhl
message("hello ${name}")#使用变量的值
```

定义变量，还可以在cmake命令后面跟-Dname=value这样来定义。

```
cmake -Dname=xhl
```



如何就是看基本的流程控制。

条件判断和循环。

条件判断

```
if(WIN)
    message("this is win")
else()
    message("this is not win")
endif()
```

for循环

```
set(FILES f1.cpp f2.cpp main.cpp)

foreach (f ${FILES})
    message("file:" ${f})
endforeach()
```



下面看看多个文件编译的情况。

```
project(demo3)
file(GLOB SRC_LIST ./*.cpp)
add_executable(demo3 ${SRC_LIST})
```



再看多目录的情况。

```
project(demo4)
aux_source_directory(. SRC_LIST)
message("1 src list is :" ${SRC_LIST})
aux_source_directory(f1 SRC_LIST)
message("2 src list is :" ${SRC_LIST})
add_executable(demo4 ${SRC_LIST})
```

目录情况是这样：

```
├── CMakeLists.txt
├── f1
│   └── f1.cpp
└── main.cpp
```



生成静态库、动态库

头文件和库的安装

安装到指定路径

库版本的生成

如何卸载cmake安装的库和头文件。

```
project(demo5)

aux_source_directory(. SRC_LIST)
add_library(demo5 STATIC ${SRC_LIST})
# 动态库的情况：
# add_library(demo5 SHARED ${SRC_LIST})
install(TARGETS demo5 DESTINATION lib)
install(FILES demo5.h DESTINATION include)
```

默认安装的目录是：

```
-- Installing: /usr/local/lib/libdemo5.a
-- Installing: /usr/local/include/demo5.h
```

指定安装目录

```
set(CMAKE_INSTALL_PREFIX ../install)
```

卸载：用下面的命令就可以卸载了。注意要sudo权限。

```
sudo xargs rm < install_manifest.txt
```

指定lib版本。

```
project(demo5)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(DEMO5_VERSION_MAJOR 1)
set(DEMO5_VERSION_MINOR 1)
set(DEMO5_VERSION_PATCH 1)
set(DEMOT_VERSION ${DEMO5_VERSION_MAJOR}.${DEMO5_VERSION_MINOR}.${DEMO5_VERSION_PATCH})

aux_source_directory(. SRC_LIST)
add_library(demo5 SHARED ${SRC_LIST})
set_target_properties(demo5 PROPERTIES VERSION
    ${DEMOT_VERSION} SOVERSION ${DEMO5_VERSION_MAJOR}
)
```



上面讨论的都是简单的情况，实际的项目，往往都需要依赖第三方库。怎么添加第三方库的依赖呢？

靠find_package这个函数。find_package会在模块路径里查找Find.cmake。

当我们的编译需要使用第三方的软件的时候，我们需要知道：
1、去哪里找头文件。对应于-I选项。
2、去哪里找库文件。对应于-L选项。
3、需要链接哪些库。对应于-l选项。



以libcurl为例。
需要借助/usr/share/cmake-3.5/Modules目录下的FindCURL.cmake。

```
find_package(CURL REQUIRED)
include_directories({CURL_INCLUDE_DIR})
target_link_libraries(xxx {CULR_LIBRARY})
```

再以bzip2为例。
有一个FindBZip2.cmake模块。
只要使用find_package(BZip2)调用这个模块。
cmake就会给一些变量赋值。然后就可以在CMakeLists.txt里使用这些变量了。

```
cmake --help-module FindBZip2
 BZIP2_FOUND - system has BZip2
 BZIP2_INCLUDE_DIR - the BZip2 include directory
 BZIP2_LIBRARIES - Link these to use BZip2
 BZIP2_NEED_PREFIX - this is set if the functions are prefixed with BZ2_
 BZIP2_VERSION_STRING - the version of BZip2 found (since CMake 2.8.8)
```

使用bzip2的例子。

```
project(helloworld)
add_executable(helloworld hello.c)
find_package (BZip2)
if (BZIP2_FOUND)
    include_directories(${BZIP_INCLUDE_DIRS})
    target_link_libraries (helloworld ${BZIP2_LIBRARIES})
endif (BZIP2_FOUND)
```

需要连接第三方库的时候，我们除了使用add_executable，还需要使用target_link_library来指定需要链接的库。



接下来看看从cmake文件里传递宏定义到C代码里。

可以使用add_definitions函数。

```
add_definitions(-DUSE_BUILDROOT)
```







参考资料

1、CMake 教程一

这个教程不错，主要参考这个写的。

https://blog.csdn.net/haluoluo211/article/details/80397814