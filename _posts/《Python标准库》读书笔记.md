---
title: 《Python标准库》读书笔记
date: 2018-07-15 21:25:53
tags:
	- 读书笔记

---



目录结构如下：

```
1、文本
	string
	textwrap
	re
	difflib
2、数据结构
	collections
	array
	heapq
	bisect
	Queue
	struct
	weakref
	copy
	pprint
3、算法
	functools
	itertools
	operator
	contextlib
4、日期和时间
	time
	datetime
	calendar
5、数学计算
	decimal
	fractions有理数
	random
	math
6、文件系统
	os.path
	glob
	linecache
	tempfile
	shutil
	mmap
	codecs
	StringIO
	fnmatch模式匹配
	dircache：缓存目录列表
	filecmp：比较文件
7、数据持久化存储和交换
	pickle
	shelve
	anydbm
	whichdb
	sqlite3
	xml.etree.ElementTree
	csv
8、数据压缩与归档
	zlib
	gzip
	bz2
	tarfile
	zipfile
9、加密
	hashlib
	jmac
10、进程与线程
	subprocess
	signal
	threading
	multiprocessing
11、网络通信
	socket
	select
	SocketServer
	asyncore
12、Internet
	urlparse
	BaseHTTPServer
	urllib
	urllib2
	Base64
	robotparser
	Cookie
	uuid
	json
	xmlrpclib
	SimpleXMLRPCServer
13、Email
	smtplib
	smtpd
	imaplib
	mailbox
14、应用构建模块
	getopt
	optparse
	argparse
	readline
	getpass
	shlex
	ConfigParser
	日志
	fileinput
	atexit
	sched
15、国际化与本地化
	gettext
	locale
16、开发工具
	pydoc
	doctest
	unittest
	traceback
	cgitb
	pdb
	trace
	profile和pstats：性能分析
	timeit：测量执行时间
	compileall
	pyclbr：类浏览器
17、运行时特性
	site：全站点配置
	sys
	os
	platform
	resource
	gc
	sysconfig
18、语言工具
	warnings
	abc
	dis：字节码反汇编
	inspect
	exceptions
19、模块与包
	imp
	zipimport
	pkgutil
	
```



# 第一章 文本

 对于Python程序员来说，最常用的文本处理工具就是string类。

另外，标准库也提供了大量的其他的工具。来帮你高效完成文本处理。

在Python2.0以前，使用的是string模块的函数。而不是string对象的方法。

## string

string模块保留了和诺德有用的常量和类。这是我们要讨论的重点。

**capwords函数**

用来把所有的单词的首字母大写。看不出这个有什么实际用途。

```
import string
s = "abc def"
print s
print string.capwords(s)
```

```
abc def
Abc Def
```

**maketrans函数**

这个函数会创建转换表。可以进行一个简单的加密。

例如用1代替a，用2代替b。这样就可以写密信了。

```
import string
s = "hello world"
leet = string.maketrans("abcdefghij", "0123456789")
print s.translate(leet)
```

得到

```
74llo worl3
```

## 模板

没有看出这种模板的意义何在。

```
import string
values = {
    'var': 'foo'
}

t = string.Template("""
Variable: $var
Escape: $$
Variable in text: ${var}iable
"""
)

print 'TEMPLATE:', t.substitute(values)

s = """
Variable: %(var)s
Escape: %%
Variable in text: %(var)siable
"""

print 'INTERPOLATION:', s % values

```

## textwrap

这个是用来格式化打印的。

先不管。

## re正则表达式

这个复杂，专门有文章来学习。这里略过。

## difflib

对我来说没用。略过先。



# 第二章 数据结构

Python包含了很多的标准数据结构，例如tuple、list、dict、set。这些都是内置类型。

对于很多应用这些就够用了。

但是Python也同时提高了一些更加强大的数据结构。

## collections

专门文章学习。

## array

```
import array
import binascii

s = 'this is the array'
a = array.array('c', s)
print 'as string:', s
print 'as array:', a
print 'as hex:' , binascii.hexlify(a)
```

```
as string: this is the array
as array: array('c', 'this is the array')
as hex: 7468697320697320746865206172726179
```

## heapq

这个是堆排序算法。

有点复杂，当前对我没用。跳过。

## bisect



## Queue



## struct



## 引用

这个也涉及到比较深的语法问题。不管先。



# 第三章 算法

## functools

管理函数的工具。

提供了一些工具来调整或者扩展函数和其他可回调对象，而不用完全重写函数。

functools提供的主要工具就是partial类。

它可以用来包装一个有默认参数的可回调对象。

```
import functools

def myfunc(a, b=2):
    print 'call myfunc with:', (a,b)
    return

def show_details(name, f, is_partial=False):
    print '%s:'  % name
    print 'object:',f
    if not is_partial:
        print '__name__:', f.__name__
    else:
        print 'func:', f.func
        print 'args:', f.args
        print 'keywords:', f.keywords
    return

show_details('myfunc', myfunc)
myfunc('a', 3)
print '--------------'

p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
```



```
C:\Python27\python.exe D:/work/pycharm/py_test/test.py
myfunc:
object: <function myfunc at 0x01F77670>
__name__: myfunc
call myfunc with: ('a', 3)
--------------
partial with named default:
object: <functools.partial object at 0x01F12690>
func: <function myfunc at 0x01F77670>
args: ()
keywords: {'b': 4}
```

看了这些代码，感觉也没有什么明显的用途。先略过。



# 第四章 时间和日期

Python没有内置时间类型。但是提供了3标准库。

time、datetime、calendar。



# 第五章 数学计算



# 第六章 文件系统





 