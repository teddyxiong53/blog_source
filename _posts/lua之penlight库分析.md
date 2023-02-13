---
title: lua之penlight库分析
date: 2023-02-09 13:54:17
tags:
	- lua

---



lua的一个比较明显的问题就是标准库太弱了。

当前的情况是基本上每个人都自己另外写一套，这样非常不便于交流。

也是在重复发明轮子。

penlight就是一套参考python的标准库进行实现的lua扩展库。

这个库一直在积极维护中（lua的热度不够，我看大多数的库都是很多年的了）

看代码质量也写得不错。所以值得作为一个工具库来使用。

代码在这里：

https://github.com/lunarmodules/Penlight

这里是文档

https://lunarmodules.github.io/Penlight/

这个库是属于lunarmodules组织里的多个lua库之一。

# 介绍

## 目标

lua缺乏battery库，这个经常被诟病的一点。

主要是因为lua的目标是一门可以在任意机器上使用的轻量级语言。

（甚至可以在文件系统的机器上运行）

lua作者的目标不是这个。

所以创造一套好用的库，是社区的责任。

软件设计的一个原则是找到可复用的内容，并进行复用。

如果你发现自己多次写到：

```
io.write(string.format('the num is %d', 42))
```

这样的代码。

那么定义一个printf就很有意义了。

重复的代码不仅难以维护，也难以阅读。

penlight库就是来提取公共常用的代码，并抽象成库。

## 注入还是不注入？



# 库文件分析

按照顺序一个个看看。

## compat.lua

这个没有依赖任何其他的库。

提供的是对不同lua版本的兼容。

提供的接口有：

```
lua51
	判断lua版本是不是5.1版本。
jit
	判断是不是使用的luajit。
jit52
	判断是不是luajit5.2版本。
dir_separator
	目录层次符合。
is_windows
	如果目录分割是\\，那么就是windows。
execute
	相当于C语言的system命令。
	输入参数是：cmd字符串。
	返回值：2个，第一个是bool表示成功与否。第二个是错误码。
	
```

## utils.lua

```
local utils = { _VERSION = "1.13.1" }
	库的版本号。
for k, v in pairs(compat) do utils[k] = v  end
	把compat的函数都导入到utils里。
patterns
	判断是否float、integer、标识符、文件名。
stdmt
	标准元表，提供了4个：
	List、Map、Set、MultiMap。
utils.pack = table.pack
	把table的pack拿过来。
printf
fprintf
	跟C语言的一样风格。
choose
	从2个值里选择一个。
array_tostring
	把数组转成string。
is_type
	判断一个变量是不是某个类型的。
npairs
	类似于标准的pairs、ipairs。
kpairs	
	类似上面。
assert_arg
enum
function_arg
assert_string
on_error
raise
readfile
writefile
readlines
executeex
quote_arg
quit
escape
split
splitv
memoize
add_function_factory
string_lambda
bind1
bind2

```

## config.lua

这个文件的作用是把配置文件读取解析成一个lua table。

包括了ini文件、经典的unix 配置文件。

对外的接口：

```
lines
	返回一个迭代器，可以遍历一个文件的所有行数。
read
	这个是主要接口，就是输入文件，返回一个lua table。
```

## class.lua

对外暴露的接口就是一个class。

```
A = class() -- 定义一个class A。

function A:_init () --定义A的构造函数。
    self.a = 1
end

A1 = class(A) -- 定义A的子类A1，使用A的默认构造函数。

B = class(A) -- 定义A的子类B，

function B:_init () --B重写了构造函数。
    self:super()
    self.b = 2
end

C = class(B) -- 定义B的子类C
D = class(C)
E = class(D)

```



https://stevedonovan.github.io/Penlight/api/libraries/pl.class.html

## test.lua

```
error_handler
complain
asserteq
assertmatch
assertraise
asserteq2
tuple
timer
```

## List.lua

这个是输出一个python风格的list。

```
class(nil,nil,List)
	这句是说明什么？定义一个class List，前面的2个nil什么意思？
```

```
class (base, c_arg, c)	create a new class, derived from a given base class.
```



tests\test-list.lua 看这个的内容

## Map.lua

Map又是基于tablex.lua来做的。

```
Map.len = tablex.size
```



## Set.lua

```
class(Map,nil,Set)
```

这个说明Set是Map的子类。



## types.lua

```
is_callable
type
is_integer
is_empty
check_meta
is_indexable
is_iterable
is_writeable
to_bool
```



# 参考资料

1、官网

https://lunarmodules.github.io/Penlight/manual/01-introduction.md.html#