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



cmake交叉编译

找第三方库和头文件怎么做？

首先需要知道：

1、cmake不能判断出目标系统，需要我们指定。

2、需要使用交叉编译对应的头文件和库。不能使用host的。

```
cmake -D CMAKE_TOOLCHAIN_FILE="/path/xx"
```

CMAKE_TOOLCHAIN_FILE这个文件里来指定交叉编译工具。

重点是3个变量：

```
CMAKE_SYSTEM_PROCESSOR
CMAKE_C_COMPILER
CMAKE_CXX_COMPILER
```

需要外部依赖，cmake默认提供的是：

```
find_program
find_library
find_file
find_path
find_package
```

但是默认是到host的目录下去找，找到的不是我们想要的。

这个时候，需要设置：

```
CMAKE_FIND_ROOT_PATH
	这个就是你指定到那个路径下去搜索。
CMAKE_FIND_ROOT_PATH_MODE_PROGRAM
	搜索program的模式。有3个值：
		never
		only
			只在CMAKE_FIND_ROOT_PATH这个路径下搜索。
		both
			除了CMAKE_FIND_ROOT_PATH，还搜索你的系统目录。
CMAKE_FIND_ROOT_PATH_MODE_LIBRARY
	跟上面类似，只是这个是搜索library。
CMAKE_FIND_ROOT_PATH_MODE_INCLUDE 
```

一个例子。新建文件cross.cmake

```
SET(CMAKE_SYSTEM_NAME Linux)

SET(CMAKE_FIND_ROOT_PATH  /opt/eldk-2007-01-19/ppc_74xx /home/alex/eldk-ppc74xx-inst)

SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```





为了能支持各种常见的库和包，cmake自带了很多模块。

可以通过`cmake --help-module-list`命令来查看你的cmake支持的模块列表。

也可以查看cmake的module路径。

在Ubuntu下，是/usr/share/cmake-3.5/Modules目录。

例如这个目录下有个文件叫FindBZip.cmake。

查看帮助信息：

```
cmake --help-module FindBZip2
```

可以看到，这个的效果是得到5个变量：

```
BZIP2_FOUND
BZIP2_INCLUDE_DIR
BZIP2_LIBRARIES
BZIP2_NEED_PREFIX
BZIP2_VERSION_STRING
```

但是也有很多的库是在/usr/shaer/cmake-3.5/Modules目录下没有对应的cmake文件的。

对于这种库，怎么处理呢？

例如我现在要用的ffmpeg，就不能找到。

这个就需要你自己写对应的cmake文件。也可以网上找别人写的。

我们在项目目录下新建cmake/Modules目录。把你写的xx.cmake文件放进去。

然后把这个路径添加到CMAKE_MODULE_PATH变量里。

```
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "{CMAKE_SOURCE_DIR}/cmake/Modules/")
```



find_package是如何工作的？

1、在模块路径下寻址FindXxx.cmake文件，会有些找${CMAKE_MODULE_PATH}里的，后面再去找/usr/share目录下的。



ffmpeg头文件和库文件查找



pkg_check_modules



FindPkgConfig.cmake

这个的作用是：查找到pkg-config文件，添加pkg_get_variable、pkg_check_modules、pkg_search_module这3个命令。

下面3个变量会被设置：

```
PKG_CONFIG_FOUND
PKG_CONFIG_EXECUTABLE
PKG_CONFIG_VERSION_STRING
```

pkg_check_modules

```
这个命令的作用是：
	检查模块，设置
```

cmake -D传递的CMAKE_FIND_ROOT_PATH，这样在CMakeLists.txt里得到的不对。



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

13、CMake交叉编译

http://zhixinliu.com/2016/02/01/2016-02-01-cmake-cross-compile/

14、CMake如何查找链接库

http://www.yeolar.com/note/2014/12/16/cmake-how-to-find-libraries/

15、CMake configuration for ffmpeg in C++ project

https://stackoverflow.com/questions/50760024/cmake-configuration-for-ffmpeg-in-c-project