---
title: scons之Environment分析
date: 2018-12-10 13:40:13
tags:
	- scons

---





```
hlxiong@hlxiong-VirtualBox:~/work/test/scons$ ls
 foo.c   SConstruct
```

SConstruct内容：

```
env = Environment(CC="gcc",     CCFLAGS="-g")
env.Program("foo.c")
```



```
hlxiong@hlxiong-VirtualBox:~/work/test/scons$ scons -Q
gcc -o foo.o -c -g foo.c
gcc -o foo foo.o
```



查看Environment里的所有东西。

```
import pdb
import SCons
#pdb.set_trace()

env = Environment(CC="gcc",     CCFLAGS="-g")
#env.Program("foo.c")

env_dict = env.Dictionary()
env_dict_keys = env_dict.keys()
env_dict_keys.sort()
for key in env_dict_keys:
	print "%s : %s " % (key, env_dict[key])
```

```
scons -Q
```

得到的东西非常多。我把重要的列出来吧。

```
hlxiong@hlxiong-VirtualBox:~/work/test/scons$ scons -Q
打包相关
AR : ar 
ARCOM : $AR $ARFLAGS $TARGET $SOURCES 
ARFLAGS : rc 
汇编相关
AS : as 
ASCOM : $AS $ASFLAGS -o $TARGET $SOURCES 
ASFLAGS :  
ASPPCOM : $CC $ASPPFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS -c -o $TARGET $SOURCES 
ASPPFLAGS : $ASFLAGS 
C语言相关
CC : gcc 
CCCOM : $CC -o $TARGET -c $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES 
CCFLAGS : -g 
CCVERSION : 5.4.0 
CFILESUFFIX : .c 
CFLAGS :  

C++相关
CPPDEFPREFIX : -D 
CPPDEFSUFFIX :  
CPPSUFFIXES : ['.c', '.C', '.cxx', '.cpp', '.c++', '.cc', '.h', '.H', '.hxx', '.hpp', '.hh', '.F', '.fpp', '.FPP', '.m', '.mm', '.S', '.spp', '.SPP', '.sx'] 
CXX : g++ 
CXXCOM : $CXX -o $TARGET -c $CXXFLAGS $CCFLAGS $_CCCOMCOM $SOURCES 
CXXFILESUFFIX : .cc 
CXXFLAGS :  

ENV : {'PATH': '/usr/local/bin:/opt/bin:/bin:/usr/bin'} 

TOOLS : ['default', 'gnulink', 'gcc', 'g++', 'gfortran', 'gas', 'ar', 'dmd', 'm4', 'filesystem', 'rpcgen', 'jar', 'javac', 'rmic', 'dvipdf', 'gs', 'tar', 'zip'] 
```



控制默认的构造环境：DefaultEnvironment函数

我们已经介绍过的所有的Builder，比如Program和Library，实际上使用一个默认的构造环境。

你可以控制默认构造环境的设置，使用DefaultEnvironment函数：

   DefaultEnvironment(CC=’/usr/local/bin/gcc’)

这样配置以后，所有Program或者Object的调用都将使用/usr/local/bin/gcc编译目标文件。

注意到DefaultEnvironment返回初始化了的默认构造环境对象，这个对象可以像其他构造环境一样被操作。所以如下的代码和上面的例子是等价的：

   env=DefaultEnvironment()

   env[‘CC’]=’/usr/local/bin/gcc’



参考资料

1、Construction Environments

https://scons.org/doc/1.2.0/HTML/scons-user/x1392.html

2、

http://www.jmpcrash.com/?p=1169