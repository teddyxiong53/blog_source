---
title: cmake（1）
date: 2018-06-21 15:19:08
tags:
	- cmake

---



--

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
CMake中，变量的值要么是String要么是String组成的List。

CMake没有用=赋值的操作，只有通过set,option来定义变量。
option只能定义OFF,ON的变量。

set mydir=./

//VA=a;b, VA是一个字符串list
set(VA a b)
//VA=a,VA是一个字符串
set(VB a)


```

条件判断：

```
if(${Platform} STREQUAL ABC
elseif()
else()
endif()
```

```
if(${Platform} MATCHES "ABC")
```

command调用语法为

```
identifier(以空格隔开的参数表)
参数可以用()括起来，表示这个单个参数。
如if(TRUE OR (TRUE AND FALSE))
```

参数的形式有：

```
1、方括号形式。
	这个比较麻烦。不管。
2、引号形式。
3、无引号形式。
```

多行注释

```
#[[这是多
行注释]]
```

for循环

```
foreach(loop_var arg1 arg2 ...)
  COMMAND1(ARGS ...)
  COMMAND2(ARGS ...)
  ...
endforeach(loop_var)

举例 
set(mylist "a" "b" c "d")
foreach(_var ${mylist})
     message("当前变量是：${_var}")
endforeach()
```

while循环

```
while(condition)
  COMMAND1(ARGS ...)
  COMMAND2(ARGS ...)
  ...
endwhile(condition)
```

自定义函数

```
function(<name> [arg1 [arg2 [arg3 ...]]])
  COMMAND1(ARGS ...)
  COMMAND2(ARGS ...)
  ...
endfunction(<name>)
```

宏定义

```
宏和function的作用是一样的，但是宏只是对字符串的简单替换。和define类似。
```

## 内置变量

基本上是CMAKE_XX的格式。

从用途划分：

```
1、提供信息。
2、改变行为。
3、描述系统。
4、控制build。
5、语言相关。
6、CTest相关。
7、CPack相关。
```

https://cmake.org/cmake/help/v3.7/manual/cmake-variables.7.html

## 参考资料

CMake基本语法

https://www.cnblogs.com/stonehat/p/7707578.html

cmake内置参数以及常用命令

https://blog.csdn.net/qq_31112205/article/details/105257230

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

```
message(FATAL_ERROR "${}" )
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



## include命令

主要用来载入CMakeLists.txt文件，或者cmake模块。

例如：

```
include(CheckFunctionExists) #这个是一个cmake模块。
```





# cmake脚本语言

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

# cmake实践笔记

## t1

一个最简单的例子。

新建目录t1。在下面新建CMakeLists.txt和main.c。

```
project(hello)
set(SRC_LIST main.c)
add_executable(hello ${SRC_LIST})
```

执行命令：

```
mkdir build
cd build
cmake ../
make
```

## t2

这一步的目的是把HelloWorld改造成更加工程化的样式。

1、添加子目录src。放源代码。

2、添加子目录doc。存放hello.txt这个帮助文档。

3、添加COPYRIGHT、readme

4、添加一个runhello.sh脚本，用来调用hello文件。

5、把可执行文件放入到bin目录。

6、安装hello和runhello.sh到 /usr/bin。doc和COPYRIGHT拷贝到/usr/share/doc/cmake/t2目录。

把顶层的CMakeLists.txt改成：

```
project(hello)
add_subdirectory(src bin)
```

把src下面的CMakeLists.txt改成：

```
add_executable(hello main.c)
```

然后编译，就可以看到可执行文件自动放到了build/bin目录下了。



# 交叉编译

CMake给交叉编译预留了一个很好的变量CMAKE_TOOLCHAIN_FILE，

它定义了一个文件的路径，

这个文件即toolChain，里面set了一系列你需要改变的变量和属性，

包括C_COMPILER,CXX_COMPILER,

如果用Qt的话需要更改QT_QMAKE_EXECUTABLE以及

如果用BOOST的话需要更改的BOOST_ROOT(具体查看相关Findxxx.cmake里面指定的路径)。

CMake为了不让用户每次交叉编译都要重新输入这些命令，因此它带来toolChain机制，

简而言之就是一个cmake脚本，内嵌了你需要改变以及需要set的所有交叉环境的设置。

一个例子：名字为toochain.cmake。

```
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_C_COMPILER /xx-gcc)
set(CMAKE_CXX_COMPILER /xx-g++)
set(CMAKE_FIND_ROOT_PATH /xx/buildroot/target)
# search for programs in the build host directories (not necessary)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# for libraries and headers in the target directories
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

```

cmake -DCMAKE_TOOLCHAIN_FILE=./toolchain.cmake

# 中文手册

这个的对cmake官方教程的翻译。写得不错。可以跟着做一遍。

https://www.zybuluo.com/khan-lau/note/254724



# 选项分析

```
 -S <path-to-source>       
 -B <path-to-build>             
 -D <var>[:<type>]=<value> 
       
 -A <platform-name>        
```

# cmake配置交叉编译工具链

https://www.cnblogs.com/god-of-death/p/14616156.html



The C compiler identification is unknown



Could not find toolchain file: cmake/toolchain.cmake



# 接口库add_library interface

这类库有属性，能`install()`，`export`和`imported`，但可能没有build过程。像`纯头文件库`或`完全针对target的设计`

例如这个：

```
add_library(MultipartParser INTERFACE)
```

就是对于c++里的那种只有头文件的项目。

# string处理

在CMake中，字符串的处理是很常见的任务，例如拼接、分割、替换等。以下是一些常见的CMake字符串处理函数的用法示例：

1. **字符串拼接：**
   ```cmake
   set(NAME "John")
   set(GREETING "Hello, ${NAME}!")
   message(${GREETING})
   ```

2. **字符串长度：**
   
   ```cmake
   set(TEXT "Hello, World!")
   string(LENGTH ${TEXT} LEN)
   message("Length of TEXT is ${LEN}")
```
   
3. **字符串截取：**
   ```cmake
   set(FULL_STRING "This is a long sentence.")
   string(SUBSTRING ${FULL_STRING} 0 4 PARTIAL_STRING)
   message(${PARTIAL_STRING})
   ```

4. **字符串替换：**
   ```cmake
   set(INPUT_STRING "Hello, world!")
   string(REPLACE "world" "CMake" NEW_STRING ${INPUT_STRING})
   message(${NEW_STRING})
   ```

5. **字符串分割为列表：**
   ```cmake
   set(SPLIT_STRING "apple;banana;cherry;date")
   string(REPLACE ";" " " SPLIT_STRING ${SPLIT_STRING})
   separate_arguments(LIST_OF_FRUITS UNIX_COMMAND ${SPLIT_STRING})
   foreach(FRUIT ${LIST_OF_FRUITS})
       message(${FRUIT})
   endforeach()
   ```

6. **字符串转换为大写或小写：**
   ```cmake
   set(UPPER_CASE "hello, cmake!")
   string(TOUPPER ${UPPER_CASE} UPPER_RESULT)
   message(${UPPER_RESULT})

   set(LOWER_CASE "Hello, CMake!")
   string(TOLOWER ${LOWER_CASE} LOWER_RESULT)
   message(${LOWER_RESULT})
   ```

7. **查找子字符串的位置：**
   ```cmake
   set(FIND_STRING "CMake is a great tool.")
   string(FIND ${FIND_STRING} "great" POSITION)
   message("Position of 'great': ${POSITION}")
   ```

这些示例展示了一些CMake字符串处理函数的用法，但CMake支持的字符串操作远不止这些。你可以查阅CMake官方文档来了解更多的字符串处理函数以及它们的用法。

# message用法

在CMake中，`message` 命令用于向终端输出消息，用于调试、信息显示以及构建过程中的反馈。以下是一些常见的 `message` 命令的用法示例：

1. **输出普通文本：**
   ```cmake
   message("Hello, World!")
   ```

2. **输出变量的值：**
   ```cmake
   set(NAME "Alice")
   message("Hello, ${NAME}!")
   ```

3. **输出条件判断的结果：**
   
   ```cmake
   if(WIN32)
       message("Running on Windows")
   else()
       message("Not running on Windows")
   endif()
```
   
4. **输出警告信息：**
   ```cmake
   if(NOT DEFINED MY_VARIABLE)
       message(WARNING "MY_VARIABLE is not defined.")
   endif()
   ```

5. **输出错误信息：**
   ```cmake
   if(NOT DEFINED REQUIRED_VARIABLE)
       message(FATAL_ERROR "REQUIRED_VARIABLE is not defined.")
   endif()
   ```

6. **输出状态信息：**
   
   ```cmake
   message(STATUS "Configuring project...")
```
   
7. **输出调试信息：**
   
   ```cmake
   message(DEBUG "Debugging information: ${DEBUG_INFO}")
   ```

请注意，`message` 命令可以用于输出不同级别的信息，如普通信息、警告、错误、状态等。在构建过程中，它可以帮助你了解变量的值、条件判断的结果以及构建流程中的各种情况。在CMake的生成过程中，你可以在终端或CMake生成的构建日志中看到这些消息。

需要注意的是，`message` 命令在CMakeLists.txt文件中使用，不会影响生成的代码或可执行文件，只是在构建过程中用于输出信息。

# 命令不区分大小写

在大多数情况下，CMake 命令不区分大小写，这意味着你可以使用大写、小写或混合大小写来编写命令，CMake 都会将其解释为相同的命令。例如，`MESSAGE`、`message`、`MeSsAgE` 都会被认为是相同的命令。

然而，CMake 的变量和属性名称是区分大小写的。这意味着 `MY_VARIABLE`、`my_variable` 和 `My_Variable` 都被视为不同的变量。因此，在编写 CMake 文件时，要注意变量和属性名称的大小写。

# cmake定义和使用变量

在 CMake 中，你可以使用 `set` 命令来定义变量，然后可以使用 `${}` 语法来引用这些变量。下面是一些关于定义和使用变量的示例：

1. **定义变量：**
   ```cmake
   set(MY_VARIABLE "Hello, CMake!")
   ```

2. **引用变量：**
   ```cmake
   message(${MY_VARIABLE})
   ```

3. **引用变量中的字符串：**
   
   ```cmake
   set(NAME "Alice")
   message("Hello, ${NAME}!")
```
   
4. **变量的值可以被修改：**
   
   ```cmake
   set(MY_NUMBER 42)
   message("My number is ${MY_NUMBER}")
   set(MY_NUMBER 99)
   message("Now my number is ${MY_NUMBER}")
```
   
5. **默认值和空值：**
   
   ```cmake
   set(DEFAULT_VALUE "Hello, Default!")
   set(NO_VALUE)
   message("Default: ${DEFAULT_VALUE}")
   message("No value: ${NO_VALUE}")
```
   
6. **条件设置变量：**
   ```cmake
   if(WINDOWS)
       set(PLATFORM "Windows")
   else()
       set(PLATFORM "Other")
   endif()
   message("Running on ${PLATFORM}")
   ```

7. **引用多个变量：**
   ```cmake
   set(FIRST_NAME "John")
   set(LAST_NAME "Doe")
   set(FULL_NAME "${FIRST_NAME} ${LAST_NAME}")
   message("Full name: ${FULL_NAME}")
   ```

需要注意的是，CMake 中的变量具有作用域，就像其他编程语言一样。局部变量在定义它们的块内可见，全局变量则在整个文件内可见。此外，CMake 中的变量名是区分大小写的，`MY_VARIABLE` 和 `my_variable` 是不同的变量。

在编写 CMakeLists.txt 文件时，合理使用变量可以帮助你更好地管理构建过程和配置选项。

# cmake list用法

在 CMake 中，列表（List）是一种数据结构，用于存储一系列值。你可以使用列表来存储文件列表、目录列表、编译选项列表等。CMake 提供了一些用于处理列表的函数来进行操作。以下是一些常见的 CMake 列表用法示例：

1. **定义列表：**
   
   ```cmake
   set(FILE_LIST file1.cpp file2.cpp file3.cpp)
```
   
2. **引用列表元素：**
   
   ```cmake
   list(GET FILE_LIST 0 FIRST_FILE)
   message("First file: ${FIRST_FILE}")
```
   
3. **获取列表长度：**
   
   ```cmake
   list(LENGTH FILE_LIST FILE_LIST_LENGTH)
   message("Number of files: ${FILE_LIST_LENGTH}")
```
   
4. **遍历列表：**
   
   ```cmake
   foreach(FILE ${FILE_LIST})
       message("File: ${FILE}")
   endforeach()
```
   
5. **添加元素到列表末尾：**
   ```cmake
   list(APPEND FILE_LIST file4.cpp)
   ```

6. **从列表中移除元素：**
   ```cmake
   list(REMOVE_ITEM FILE_LIST file2.cpp)
   ```

7. **将列表连接为字符串：**
   
   ```cmake
   string(REPLACE ";" " " FILE_LIST_STR "${FILE_LIST}")
   message("Files as string: ${FILE_LIST_STR}")
```
   
8. **使用列表作为循环计数器：**
   ```cmake
   foreach(i RANGE 1 5)
       message("Index: ${i}")
   endforeach()
   ```

需要注意的是，CMake 中的列表是由分号 `;` 分隔的一系列值。你可以使用列表函数来操作这些列表，执行添加、删除、遍历等操作。列表在构建过程中非常有用，可以用于定义文件列表、编译选项列表、库依赖等等。

# cmake macro用法

在 CMake 中，宏（Macro）是一种用于执行一系列命令的自定义函数。宏可以带有参数，允许你在构建过程中重复使用相同的代码块。以下是一些关于 CMake 宏的用法示例：

1. **定义宏：**
   ```cmake
   macro(MyMacro ARG1 ARG2)
       message("Macro called with arguments: ${ARG1} and ${ARG2}")
   endmacro()
   ```

2. **调用宏：**
   ```cmake
   MyMacro("Hello" "CMake")
   ```

3. **宏可以包含多条命令：**
   ```cmake
   macro(PrintVariables)
       message("Value of VAR1: ${VAR1}")
       message("Value of VAR2: ${VAR2}")
   endmacro()

   set(VAR1 "Value 1")
   set(VAR2 "Value 2")

   PrintVariables()
   ```

4. **宏参数可以是可选的：**
   
   ```cmake
   macro(OptionalMacro ARG1 ARG2)
       if(ARG2)
           message("Second argument provided: ${ARG2}")
       else()
           message("Second argument not provided.")
       endif()
endmacro()
   
   OptionalMacro("First Argument")
   OptionalMacro("First Argument" "Second Argument")
```
   
5. **宏内部使用变量：**
   ```cmake
   macro(MacroWithVariables)
       set(LOCAL_VAR "Local Value")
       message("Inside macro: ${LOCAL_VAR}")
   endmacro()

   set(LOCAL_VAR "Global Value")
   message("Outside macro: ${LOCAL_VAR}")

   MacroWithVariables()
   ```

6. **宏可以调用其他宏：**
   ```cmake
   macro(OuterMacro)
       message("Outer macro started.")
       InnerMacro()
       message("Outer macro finished.")
   endmacro()

   macro(InnerMacro)
       message("Inner macro called.")
   endmacro()

   OuterMacro()
   ```

宏是 CMake 中代码复用的重要机制，可以帮助你避免重复编写相同的代码块，提高代码的可维护性和可读性。当你需要在多个地方使用相同的代码时，可以将其封装为宏，并通过调用宏来执行这些操作。

# add_executable

在 CMake 中，`add_executable` 是一个用于定义可执行文件的命令。它用于告诉 CMake 如何将源代码编译成一个可执行文件。以下是 `add_executable` 命令的用法示例：

```cmake
# 定义可执行文件，名称为 my_app
add_executable(my_app main.cpp file1.cpp file2.cpp)

# 将头文件目录添加到可执行文件的包含路径
target_include_directories(my_app PRIVATE ${CMAKE_SOURCE_DIR}/include)

# 将链接的库添加到可执行文件
target_link_libraries(my_app PRIVATE my_library)
```

在上面的示例中：

- `add_executable(my_app main.cpp file1.cpp file2.cpp)`：这行代码定义了一个名为 `my_app` 的可执行文件，它由 `main.cpp`、`file1.cpp` 和 `file2.cpp` 这些源文件编译而来。
- `target_include_directories(my_app PRIVATE ${CMAKE_SOURCE_DIR}/include)`：这行代码将头文件目录添加到可执行文件的包含路径中。`${CMAKE_SOURCE_DIR}` 表示项目的根目录，`include` 是包含头文件的目录。
- `target_link_libraries(my_app PRIVATE my_library)`：这行代码将名为 `my_library` 的库链接到可执行文件。这样，`my_app` 就能够使用 `my_library` 中定义的函数和变量。

请注意，`add_executable` 命令通常会与其他 CMake 命令一起使用，以配置构建过程和链接依赖库。这些命令一起协同工作，将源代码转换为可执行文件。

# add_dependencies

在 CMake 中，`add_dependencies` 是一个用于定义目标之间依赖关系的命令。它允许你指定一个目标依赖于另一个或多个目标，以确保在构建时正确地处理它们的依赖关系。以下是 `add_dependencies` 命令的用法示例：

```cmake
# 定义两个目标：my_app 和 my_library
add_executable(my_app main.cpp)
add_library(my_library my_source.cpp)

# 将 my_app 设置为依赖于 my_library
add_dependencies(my_app my_library)
```

在上面的示例中：

- `add_executable(my_app main.cpp)` 和 `add_library(my_library my_source.cpp)` 分别定义了两个目标：可执行文件 `my_app` 和库 `my_library`。
- `add_dependencies(my_app my_library)` 将 `my_app` 设置为依赖于 `my_library`。这意味着在构建 `my_app` 之前，CMake 将确保构建 `my_library`。

`add_dependencies` 命令对于确保在正确顺序下构建不同的目标非常有用。例如，在构建一个可执行文件之前，可能需要先构建相关的库。通过使用 `add_dependencies` 命令，你可以指定这些依赖关系，从而确保构建过程正确无误。

需要注意的是，`add_dependencies` 命令只是建议构建顺序，它不会强制使目标按特定顺序构建。构建系统会尽力满足这些依赖关系，但如果依赖关系无法满足，可能会导致构建失败。

# set_property

在 CMake 中，`set_property` 是一个用于设置属性的命令。它可以用于为目标、源文件、目录等设置属性，从而影响构建和编译的行为。以下是 `set_property` 命令的用法示例：

```cmake
# 为一个目标设置属性
set_property(TARGET my_target PROPERTY CXX_STANDARD 11)

# 为一个源文件设置属性
set_property(SOURCE my_source.cpp PROPERTY COMPILE_DEFINITIONS MY_DEFINE)

# 为一个目录设置属性
set_property(DIRECTORY ${CMAKE_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT my_project)
```

在上面的示例中：

- `set_property(TARGET my_target PROPERTY CXX_STANDARD 11)`：这行代码为名为 `my_target` 的目标设置属性。在这里，设置了 C++ 标准为 11。这会影响编译过程，使其使用 C++11 特性进行编译。
- `set_property(SOURCE my_source.cpp PROPERTY COMPILE_DEFINITIONS MY_DEFINE)`：这行代码为名为 `my_source.cpp` 的源文件设置属性。在这里，设置了编译宏 `MY_DEFINE`，它将在编译该源文件时生效。
- `set_property(DIRECTORY ${CMAKE_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT my_project)`：这行代码为目录设置属性。在这里，将 Visual Studio 中的启动项目设置为 `my_project`，这将影响在 Visual Studio 中的构建行为。

`set_property` 命令可以用于影响构建过程中的各种行为，如编译选项、链接选项、生成器相关的设置等。需要根据实际需求查阅 CMake 文档以了解更多属性和使用方法。

# INCLUDE(GNUInstallDirs)

在 CMake 构建系统中，`INCLUDE(GNUInstallDirs)` 是一个指令，用于包含 CMake 的标准模块 `GNUInstallDirs`，该模块定义了一些常见的安装目录变量，用于在安装过程中指定文件的目标路径。

`GNUInstallDirs` 模块为不同类型的文件（可执行文件、库文件、头文件、文档等）定义了适当的安装目录，以便将文件正确地安装到系统中。这有助于使软件包在不同的平台上保持一致的安装布局。

以下是一些 `GNUInstallDirs` 模块定义的常见变量：

- `CMAKE_INSTALL_BINDIR`：可执行文件的目录。
- `CMAKE_INSTALL_LIBDIR`：库文件的目录。
- `CMAKE_INSTALL_INCLUDEDIR`：头文件的目录。
- `CMAKE_INSTALL_DATAROOTDIR`：共享数据文件的根目录。
- `CMAKE_INSTALL_DOCDIR`：文档文件的目录。

通过在 CMakeLists.txt 文件中使用 `INCLUDE(GNUInstallDirs)`，你可以在安装时使用这些变量来指定文件的目标路径，以便将文件正确地安装到系统的适当位置。

示例：

```cmake
cmake_minimum_required(VERSION 3.0)
project(MyProject)

# 包含 GNUInstallDirs 模块
include(GNUInstallDirs)

# 安装可执行文件到 bin 目录
install(TARGETS my_executable DESTINATION ${CMAKE_INSTALL_BINDIR})

# 安装库文件到 lib 目录
install(TARGETS my_library DESTINATION ${CMAKE_INSTALL_LIBDIR})

# 安装头文件到 include 目录
install(FILES my_header.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

上面的示例中，通过使用 `CMAKE_INSTALL_BINDIR`、`CMAKE_INSTALL_LIBDIR` 和 `CMAKE_INSTALL_INCLUDEDIR` 等变量，将可执行文件、库文件和头文件安装到了标准的安装目录。

# aux_source_directory

在 CMake 构建系统中，`aux_source_directory` 函数用于从指定的目录中查找源代码文件，并将这些源代码文件的列表存储在一个变量中。

函数的语法如下：

```cmake
aux_source_directory(dir variable)
```

- `dir`：要搜索的目录。
- `variable`：要存储源文件列表的变量名称。

这个函数通常用于简化构建脚本，特别是在需要将一个目录中的多个源文件都添加到一个目标中时。它会自动搜索指定目录中的所有源代码文件，并将它们添加到指定的变量中。

示例：

假设在项目目录下有一个名为 `src` 的文件夹，其中包含多个 `.cpp` 文件。你可以使用 `aux_source_directory` 函数将所有 `.cpp` 文件的列表存储在一个变量中，然后将这个变量传递给 `add_executable` 或 `add_library`。

```cmake
cmake_minimum_required(VERSION 3.0)
project(MyProject)

# 查找 src 目录下的所有 .cpp 文件，并将其保存在 SRCS 变量中
aux_source_directory(src SRCS)

# 添加可执行文件，并将 SRCS 变量中的源文件添加到可执行文件中
add_executable(my_executable ${SRCS})
```

在上面的示例中，`aux_source_directory` 函数将 `src` 目录下的所有 `.cpp` 文件的列表存储在 `SRCS` 变量中，然后将这个变量传递给 `add_executable`。这样就不需要一个个手动列出所有的源文件了。

# cmake install

在 CMake 构建系统中，`install` 命令用于安装编译生成的文件，包括可执行文件、库文件、头文件、文档等，到指定的目录。这样可以将构建出的文件部署到系统中，以便其他程序或用户使用。

`install` 命令的基本语法如下：

```cmake
install(TARGETS targets...
        [[ARCHIVE|LIBRARY|RUNTIME]
          [DESTINATION <dir>]
          [PERMISSIONS permissions...]
          [CONFIGURATIONS [Debug|Release|...]]
          [COMPONENT <component>]
          [OPTIONAL]
         ]
        [...]
       )
```

其中，`TARGETS` 后跟要安装的目标（可执行文件、库文件等），`DESTINATION` 后跟目标安装的路径，`PERMISSIONS` 可以设置文件的权限，`COMPONENT` 可以用于分组安装，`OPTIONAL` 表示可选安装。

以下是一些示例用法：

1. **安装可执行文件：**

   ```cmake
   install(TARGETS my_executable DESTINATION bin)
   ```

   这将把名为 `my_executable` 的可执行文件安装到 `bin` 目录。

2. **安装库文件：**

   ```cmake
   install(TARGETS my_library DESTINATION lib)
   ```

   这将把名为 `my_library` 的库文件安装到 `lib` 目录。

3. **安装头文件：**

   ```cmake
   install(FILES my_header.h DESTINATION include)
   ```

   这将把名为 `my_header.h` 的头文件安装到 `include` 目录。

4. **安装文档：**

   ```cmake
   install(FILES README.md DESTINATION doc)
   ```

   这将把名为 `README.md` 的文档文件安装到 `doc` 目录。

需要注意的是，`DESTINATION` 参数指定了安装的目标路径。通常，你可以使用 CMake 的预定义变量（如 `CMAKE_INSTALL_PREFIX`）来表示安装路径的根目录。例如，`DESTINATION ${CMAKE_INSTALL_PREFIX}/bin` 将可执行文件安装到根目录下的 `bin` 目录。

在 CMakeLists.txt 文件中使用 `install` 命令，可以让你定义在构建后如何将生成的文件部署到系统中。

# findPackage

在 CMake 构建系统中，`find_package` 命令用于查找和导入其他软件包或库的配置文件，以便在你的项目中使用这些库。这可以让你的项目更容易管理依赖关系，并确保正确地链接所需的库。

`find_package` 命令的基本语法如下：

```cmake
find_package(package_name [version] [EXACT] [QUIET] [MODULE]
             [REQUIRED] [COMPONENTS [component1] [component2] ...])
```

- `package_name`：要查找的库或软件包的名称。
- `version`：可选，指定所需的版本号。
- `EXACT`：可选，要求找到的版本号必须与指定的版本号完全匹配。
- `QUIET`：可选，不显示查找过程的输出。
- `MODULE`：可选，使用 CMake 模块进行查找。
- **`REQUIRED`：可选，如果找不到所需的包，将会报错。**
- `COMPONENTS`：可选，列出需要的组件。

当你调用 `find_package` 命令时，CMake 将会尝试在系统上查找指定的软件包，并导入其配置文件，以便在项目中使用。这些配置文件通常包含库的路径、头文件、链接标志等信息，以便正确地编译和链接项目。

示例：

```cmake
cmake_minimum_required(VERSION 3.0)
project(MyProject)

# 查找并导入 OpenSSL 软件包
find_package(OpenSSL REQUIRED)

# 将 OpenSSL 的头文件和库链接到项目中
include_directories(${OPENSSL_INCLUDE_DIR})
target_link_libraries(my_app ${OPENSSL_LIBRARIES})
```

在上面的示例中，`find_package(OpenSSL REQUIRED)` 将查找 OpenSSL 软件包，并导入其配置文件。然后，通过使用 `${OPENSSL_INCLUDE_DIR}` 和 `${OPENSSL_LIBRARIES}` 变量，可以将 OpenSSL 的头文件路径和库链接到项目中。

注意：`find_package` 命令的具体效果取决于所查找的软件包是否提供了正确的 CMake 配置文件。如果你想使用 `find_package` 导入某个库，确保该库支持 CMake 构建，并提供了相应的配置文件。

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

16、掌握CMake编译配置工具，编译设计工作快到飞起！

这篇文档非常好。给一个比较完整的例子。

https://juejin.cn/post/6854573214069161997

17、cmake实践。一个40页的pdf文档。这个是KDE的开发者写的。很有条理。

http://file.ncnynl.com/ros/CMake%20Practice.pdf