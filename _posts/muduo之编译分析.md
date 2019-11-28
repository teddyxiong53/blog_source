---
title: muduo之编译分析
date: 2019-11-28 11:47:51
tags:
	- cpp
---

1

从build.sh看起。

```
set -x  # 这个是打开脚本的详细输出。
SOURCE_DIR=`pwd` # 指定代码目录
BUILD_DIR=${BUILD_DIR:-../build} # 这些如果没有指定，就用后面的默认值。

```

compile_commands.json

这个文件是如何生成的？

可能是cmake的某个配置就可以生成的。

是靠CMAKE_EXPORT_COMPILE_COMMANDS 这个。

可能是默认就是打开的。

```
./build/release-cpp11/CMakeCache.txt:113:CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON
```

```
cmake \
           -DCMAKE_BUILD_TYPE=$BUILD_TYPE \
           -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR \
           -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
           $SOURCE_DIR \
  && make $*
```

cmake，带上-D参数，和代码路径。

把build.sh的参数都传递给make 。



然后就看顶层的CMakeLists.txt。

```
project(muduo C CXX) # 指定项目名字和使用的语言。

enable_testing() # 使能测试。
```



```
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release")
endif() # 如果没有指定编译类型，默认为release版本。
```

然后就是设置CXXFLAGS

然后看muduo/base下的CMakeLists.txt文件。





参考资料

1、

https://cmake.org/cmake/help/v3.5/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html