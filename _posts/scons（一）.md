---
title: scons（一）
date: 2018-01-24 16:56:20
tags:
	- scons

---



因为rt-thread里用了这个工具，为了方便调试，把这个构建工具学习一下。

# 1. scons简介

开源的用Python编写的构建工具。

与make相比，有哪些优势？

1、用Python脚本作为配置文件。

2、对于C和C++，默认就支持进行依赖关系分析。

3、跨平台。

# 2. HelloWorld

新建一个目录，scons-test。下面放hello.c和SConstruct这2个文件。

SConstruct文件里就一行：

```
Program('hello.c')
```

然后执行scons命令，就会进行编译。

Program的位置上可以出现的词：

Program：表示编译出一个可执行程序。

Object：表示编译出一个o文件。

清除：

```
scons -c
```

SConstruct的内容是Python脚本。Program是一个类。

但是跟普通的Python脚本还是不同。

它的行为上类似Makefile。调用顺序。

指定输出文件的名字：

```
Program('hello_exe', "hello.c")
```

编译多个c文件：

```
Program('hello_exe', ['hello.c', 'f1.c', 'f2.c'])
```

用Glob来通配C文件：

```
Program('hello_exe', Glob('*.c'))
```

每个文件名都用引号括起来，比较麻烦。可以这样：

```
src_files = Split("f1.c f2.c")
Program('hello_exe', src_files)
```

其实，可以把参数的名字也带上，这样清晰一点：

```
Program(target = 'hello_exe', source=src_files)
```

上面讨论的都是编译了一个程序的，其实编译多少个都无所谓的。

```
Program('hello1', 'hello1.c')
Program('hello2', 'hello2.c')
```



# 3.编译库

为了方便后面的测试，新建4个文件：

```
$ touch f1.c f2.c f3.c f4.c
$ echo "void f1() {printf(\"%s\\n\", __func__);}" > f1.c
$ echo "void f2() {printf(\"%s\\n\", __func__);}" > f2.c
$ echo "void f3() {printf(\"%s\\n\", __func__);}" > f3.c
$ echo "void f4() {printf(\"%s\\n\", __func__);}" > f4.c
```

新建main.c：

```
void main()
{
    f1();
    f2();
    f3();
    f4();
}
```



SConstruct文件：

```
src_files = Glob("f*.c")
Library("foo", src_files)
```

可以明确指定静态库或者动态库：

StaticLibrary或者SharedLibrary。

链接库：

```
src_files = Glob("*.c")
Library("foo", src_files)
Program("hello", "main.c", LIBS=['foo'], LIBPATH=".")
```







# 4.SConstruct和SConscript关系

SConstruct是主要文件。SConscript相当于函数一样的功能，里面最后面会返回一些对象。

在前面的基础上，继续扩展。增加一个子目录d1，下面放一个d1f1.c的文件。

```
teddy@teddy-ubuntu:~/work/test/scons-test$ mkdir d1
teddy@teddy-ubuntu:~/work/test/scons-test$ cd d1
teddy@teddy-ubuntu:~/work/test/scons-test/d1$ touch d1f1.c
teddy@teddy-ubuntu:~/work/test/scons-test/d1$ echo "void d1f1() {printf(\"%s\\n\", __func__);}" > d1f1.c
teddy@teddy-ubuntu:~/work/test/scons-test/d1$ 
```

现在目录结构是：

```
teddy@teddy-ubuntu:~/work/test/scons-test$ tree
.
├── d1
│   ├── d1f1.c
│   └── SConscript
├── f1.c
├── f2.c
├── f3.c
├── f4.c
├── main.c
└── SConstruct
```

SConstruct内容：

```
src_files = Glob("*.c")
subobj = SConscript(['d1/SConscript'])
obj = subobj + Object(src_files )
Program("hello", list(obj))
```

SConscript内容：

````
obj = Object(Glob("*.c"))
Return("obj")
````



# 5.env 

环境变量用于设置编译过程中用到的各种参数。

把下面的代码加入到SConstruct里，可以打印出来看看。

```
env = Environment()
dict = env.Dictionary()
keys = dict.keys()
keys.sort()
for key in keys:
    print "key: %s, value:%s" % (key, dict[key])
```







SourceSignatures("MD5")

SourceSignatures("timestamp")



Depends(hello, 'some file')：明确指定依赖关系。



Import函数。引入变量用的。

```
Import("env")
```

跟Export对应。这个是导出变量的。



File和Dir的用法

```
import pdb
import SCons
#pdb.set_trace()

env = Environment(CC="gcc",     CCFLAGS="-g")
#env.Program("foo.c")

print Dir(".").path
print Dir(".").abspath
print Dir("#").path
print Dir("#.").path
print File("foo.c").srcnode().path
```

输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/scons$ scons -Q
/home/hlxiong/work/test/scons
/home/hlxiong/work/test/scons
/home/hlxiong/work/test/scons
/home/hlxiong/work/test/scons
foo.c
scons: `.' is up to date.
```

Dir('#')表示源代码的顶层目录。



添加自定义选项。

```
import pdb
import SCons
#pdb.set_trace()

env = Environment(CC="gcc",     CCFLAGS="-g")
#env.Program("foo.c")

AddOption("--copy", dest="copy", action="store_true", 
		default=False,
		help="copy rt-thread dir to local"
	)
print GetOption("copy")
```

你可以这样查看这个添加的内容。

```
scons --help
```

```
Local Options:
  --copy                      copy rt-thread dir to local
```

执行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/scons$ scons --copy -Q
True
scons: `.' is up to date.
```



# 参考资料

1、scons使用

https://www.cnblogs.com/blueoverflow/p/4913766.html

2、官方手册

https://scons.org/doc/production/HTML/scons-man.html