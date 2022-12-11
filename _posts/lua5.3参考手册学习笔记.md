---
title: lua5.3参考手册学习笔记
date: 2022-12-09 17:24:19
tags:
	- lua

---

--

# 简介

Lua 是一门扩展式程序设计语言，

被设计成支持**通用过程式编程**，

并有相关数据描述设施。

 同时对面向对象编程、函数式编程和数据驱动式编程也提供了良好的支持。 

它作为一个强大、轻量的嵌入式脚本语言，

可供任何需要的程序使用。 

Lua 由 *clean C（标准 C 和 C++ 间共通的子集）* 实现成一个库。

作为一门扩展式语言，Lua 没有 "main" 程序的概念： 

它只能 *嵌入* 一个宿主程序中工作， 该宿主程序被称为 *被嵌入程序* 或者简称 *宿主* 。 

宿主程序可以调用函数执行一小段 Lua 代码，可以读写 Lua 变量，可以注册 C 函数让 Lua 代码调用。 

依靠 C 函数，Lua 可以共享相同的语法框架来定制编程语言，从而适用不同的领域。 

Lua 的官方发布版包含一个叫做 `lua` 的宿主程序示例， 

它是一个利用 Lua 库实现的完整独立的 Lua 解释器，可用于交互式应用或批处理。





# 基本概念

## 值与类型

Lua 是一门*动态类型语言*。 

**这意味着变量没有类型；只有值才有类型。** 

语言中不设类型定义。 

Lua 中所有的值都是 *一等公民*。 这意味着所有的值均可保存在变量中、 当作参数传递给其它函数、以及作为返回值。

# 语言定义

# 编程接口

# 辅助库

# 标准库

## 基础函数

```
assert(a, "xx")
collectgarbage(opt, arg)
	opt是字符串，可选，值有：
		collect：做一次完整的gc，这个是默认的选项。
		stop：停止gc。
		restart：重启gc。
		count：以K为单位返回lua使用的总内存数。
		step：单步运行gc。步长由参数arg来指定。
		setpause：用arg指定gc的休息频率。
		setstepmul：设置gc的step 倍率。
		isrunning：查看gc是否被stop掉。
dofile
	打开一个lua文件，并执行里面的内容。
error
	打印错误。
_G
	保存所有的全局变量。
getmetatable
	如果object不包含元表，返回nil。
ipairs
	参数是一个table，返回3个值：迭代函数、表、0（0是指什么？）
	可以这样用：
	for i,v in ipairs(t) do xx done
	迭代值对是：(1,t[1]),(2,t[2])...
load
	加载一个代码块。
loadfile
	跟load类型，不过是从文件里load。
next
	遍历table。
pairs
pcall
	以保护模式调用函数。
print
	一般用作调试打印。
rawequal
	检测2个值是否相等。这里以及下面的raw的内涵都是：不触发任何元方法。
rawget(table, i)
	获取table某个索引的的内容。
rawlen(v)
	返回对象的长度。
rawset
select(index,...)
	如果index是数字，返回index之后的部分。
	如果是#，则返回长度。
setmetatable(table, metatable)
	设置元表。
tonumber
tostring
type
_VERSION
xpcall
	跟pcall类型，但是可以额外设置一个消息handler。
	
```

## 协程

关于协程的操作作为一个基础库的字库。

被放在一个单独的表（相当于namespace）中。

```
coroutine.create(f)
	创建一个主体函数是f的新的协程。
	f必须是一个lua函数。
	返回的是一个协程，是一个类型为thread的对象。
coroutine.isyieldable()
	如果真正运行的协程可以让出，返回true。
coroutine.resume(co)
	开始或者继续一个协程。
coroutine.running()
coroutine.status(co)
coroutine.wrap(f)
coroutine.yield(...)

```

## 模块

只有一个函数放在全局环境：require函数。其余的都放在package这个namespace里。

```
require(modname)
package.config
	这些不带括号的，表示都是属性，不是函数。
package.cpath
package.loaded
	查看当前哪些module已经被load进来了。
package.loadlib()
package.path
	在这个路劲下依次搜索。
package.preload
package.searchers
package.searchpatch()

```

## 字符串处理

```
string.byte
	返回的是对应的ascii码。
	> s='abc'
	> string.byte(s,1,3)
	97      98      99
string.char(n)
	返回数字对应的ascii字符。
	可以给多个数字。
string.dump(f)
string.find
string.format
string.gmatch
string.gsub
string.len
string.lower
string.match
string.pack
string.packsize
string.rep
string.reverse
string.sub
string.unpack
string.upper

```

## utf8

```
utf8.char
utf8.charpattern
utf8.codes(s)
utf8.codepoint
utf8.len
utf8.offset

```

## table

这个库为table提供了通用的处理函数。都在namespace table里。

```
table.concat
table.insert
table.move
table.pack
table.remove
table.sort
table.unpack

```

## match

```
没什么可说的，就是那些常用的。
```

## io

io库提供了2套不同风格的处理接口。

1、使用隐式的file 句柄。

2、使用显式的file句柄。

如果使用隐式的file句柄，那么都在namespace io下面。

如果使用显式的file句柄，io.open会返回一个句柄，后面的操作都使用这个句柄。

table io里也提供了跟C语言一样的3个基本的文件：

io.stdin、io.stdout、io.stderr。

除非特殊说明，io函数在出错的时候都是返回nil。

```
io.close([file])
io.flush
io.input
io.lines
io.open
io.output
io.popen
io.read
io.tmpfile
io.type
io.write

file:close
file:flush
file:lines
file:read
file:seek
file:setvbuf
file:write

```

## os

```
os.clock()
os.date()
os.difftime()
os.execute()
	相当于C语言的system。
os.exit
os.getenv
os.remove
os.rename
os.setlocale
os.time
os.tmpname

```

## debug

```
debug.debug()
debug.gethook()
debug.getinfo()
debug.getlocal()
debug.getmetatable()
debug.getregistry()
debug.getupvalue()
debug.getuservalue()
debug.sethook()
debug.setlocal()
debug.setmetatable()
debug.setupvalue()
debug.setuservalue()
debug.traceback()
debug.upvalueid()
debug.upvaluejoin()

```



# 参考资料

1、

https://www.runoob.com/manual/lua53doc/