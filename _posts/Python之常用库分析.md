---
title: Python之常用库分析
date: 2017-09-17 14:48:53
tags:
	- python

---



# 1. sys

我们先以这个为例，看看help(sys)的输出内容的构成：

```
1、NAME：sys
2、FILE：built-in
3、MOUDULE DOCS：就是一个链接。
4、description：这个对应的就是sys.py文件的最前面的注释里的东西。
分为3个部分：
	动态对象
	静态对象
	函数
	
```

## sys模块的动态对象：

argv：

path：这个就是模块的搜索路径。

modules：这个是载入的所有模块。

stdin/stdout/stderr：

displayhook：是个函数指针这样的东西。应该是可以自己修改实现。

excepthook：出异常的时候回调。

exitfunc：退出时回调。

## 静态对象

version：

copyright：

maxint：

platform：windows上是win32。

`__stdin__`：

## 函数

exit()



在sys.py里的相关实现是这样的：

```
exc_type = None

executable = 'C:\\Python27\\python.exe'

exec_prefix = 'C:\\Python27'

float_repr_style = 'short'

hexversion = 34013424

maxint = 2147483647
maxsize = 2147483647
maxunicode = 65535
```



```
argv = [] # real value of type <type 'list'> skipped

builtin_module_names = () # real value of type <type 'tuple'> skipped

flags = None # (!) real value is ''

float_info = None # (!) real value is ''

long_info = None # (!) real value is ''
```



```
stderr = open('') # real value of type <type 'file'> replaced

stdin = open('') # real value of type <type 'file'> replaced

stdout = open('') # real value of type <type 'file'> replaced

```

总结上面的内容，我们经常用的就是sys.argv和sys.exit这2个。



# 2. os

这个的内容比sys要多很多。主要是就是os和os.path常用。

## os的常用函数

对于数据的处理，通常是增删改查。我们就按这个顺序记忆：

增：

os.mkdir：可以新建目录。

os.open：可以新建文件。

删：

os.remove：

os.removedirs：

改：

os.chdir

查：

os.getcwd：

os.listdir：

其他：

os.system：系统调用。

## os.path模块常用函数

路径相关的函数，感觉以查询性质的为主。

主要用途：查询绝对路径，查询文件名字，查询路径名。

查询是否存在，查询访问、创建、修改时间。

查询是文件还是目录。

# 3. time

分为查询和修改时间。

## 变量

timezone

tzname

## 函数

gmtime：和ctime输出一样，字符串格式的时间。

time：

sleep：睡眠函数，以秒为单位。

mktime：

tzset：





# 4. threading



# 5. subprocess

