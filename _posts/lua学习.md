---
title: lua学习
date: 2017-04-30 22:07:32
tags:
	- lua
---
lua因为解释器很小，只有100多K，所以在嵌入式设备中使用比较方便。lua也在游戏编程中占有一席之地，所以想要了解一下。

# 1. helloworld
在Ubuntu下学习。
安装：` sudo apt-get install lua5.2`。
基本使用如下：

```
teddy@teddy-ubuntu:~/test/lua-test$ lua
Lua 5.2.3  Copyright (C) 1994-2013 Lua.org, PUC-Rio
> print("helloworld")
helloworld
> os.exit()
teddy@teddy-ubuntu:~/test/lua-test$ 
```
把语句放到脚本文件里，然后执行。
新建一个test.lua文件，内容如下：

```
#!/usr/bin/lua
print("hello,lua")
```
用./test.lua来执行就好了。

# 2. 基本语法
## 注释
单行：用`--`。
多行：
```
--[[
comment1
comment2
--]]
```
使用：
```
#!/usr/bin/lua
--comment single line
--[[
comment1
comment2
--]]
print("hello,lua")
```
## 关键字
注意这些：
and/or/not、elseif、function、nil、then、true/false、local、repeat。

## 全局变量
默认情况下，变量都是全局变量。
要删除一个全局变量，只需要给它赋值为nil。
局部变量要用local进行修饰。

## 数据类型
lua有8种基本数据类型，相当于C语言来说，这些类型有点奇怪。
分别是：
nil：只有nil一个值，表示无效值。
boolean：只有true和false两个值。
number：实质是double的。
string：用单引号或者双引号括起来的。还有用`[[`和`]]`括起来的（可以用于字符串里含有引号的情况）。
function：用c或者lua写的函数。（为什么是数据类型？）
userdata：表示C数据结构。
thread：
table：就是键值对。索引从1开始计数。（why？麻烦）

lua里只认为false和nil为假，其他的包括数字0都是真。这个要注意。

## 基本流程语句
一般都用end来结尾的。
支持多个返回值。
支持可变参数。

# 3. 模块与包
从lua5.1开始，lua加入了标准的模块管理机制。
lua的模块是由变量、函数等已知元素组成的table，因此创建一个模块很简单，就是创建一个table。然后把需要对外暴露的常量函数等等放入其中，最后返回这个这个table就好了。
下面以创建一个叫mymodule的模块为例。
新建一个mymodule.lua文件。内容如下：

```
#!/usr/bin/lua
--定义一个叫mymodule的模块
mymodule = {}

--定义一个常量
mymodule.constant1 = "constant1"

--定义一个函数
function mymodule.func1()
	io.write("public function\n")
end
local function func2()
	print("local function \n")
end

function mymodule.func3()
	func2()
end

return mymodule
```
test.lua里内容：
```
#!/usr/bin/lua
require("mymodule")

print(mymodule.constant1)
mymodule.func3()
```
## 加载机制
lua里的require的模块的搜索路径是存放在全局变量package.path中，当lua启动的时候，会议环境变量`LUA_PATH`的值来初始化这个环境变量。如果没有找到这个环境变量，那么使用一个在编译时就定义的默认路径来初始化。
```
teddy@teddy-ubuntu:~$ lua
Lua 5.2.3  Copyright (C) 1994-2013 Lua.org, PUC-Rio
> print(package.path)
/usr/local/share/lua/5.2/?.lua;/usr/local/share/lua/5.2/?/init.lua;/usr/local/lib/lua/5.2/?.lua;/usr/local/lib/lua/5.2/?/init.lua;/usr/share/lua/5.2/?.lua;/usr/share/lua/5.2/?/init.lua;./?.lua
> 
```
如果找lua的模块没有找到，那么就会去找C程序库。对应的搜索路径是package.cpath
```
> print(package.cpath)
/usr/local/lib/lua/5.2/?.so;/usr/lib/i386-linux-gnu/lua/5.2/?.so;/usr/lib/lua/5.2/?.so;/usr/local/lib/lua/5.2/loadall.so;./?.so
> 
```

# 4. 协同程序coroutine
coroutine与线程类似。
比较大的区别是：在任一时刻只有一个coroutine在运行，相当于几个线程共享了一把锁。
基本函数有：create、resume、yield、status、wrap、running。这么6个。
create+resume=wrap。
create之后，是停止状态，要resume才会运行。而wrap一创建就运行。

下面看例子。
```
#!/usr/bin/lua

co = coroutine.create(
	function(i)
		print(i);
	end
)

coroutine.resume(co, 1) -- 1
print(coroutine.status(co)) -- dead

print("---------------------")

co = coroutine.wrap(
	function(i)
		print(i);
	end
)

co(1)

print("---------------------")

co2 = coroutine.create(
	function()
		for i=1,10 do
			print (i)
			if i==3 then
				print(coroutine.status(co2))
				print(coroutine.running())
			end
			coroutine.yield()
		end
	end
)

coroutine.resume(co2)
coroutine.resume(co2)
coroutine.resume(co2)

```
再看用coroutine来模拟生产者消费者问题。
```
#!/usr/bin/lua

local newProductor

function productor()
	local i = 0
	while i<20 do
		i = i+1
		send(i)
	end
end

function consumer()
	while true do
		local i = receive()
		if i>=20 then
			break
		end
		print(i)
	end
end

function receive()
	local status, value = coroutine.resume(newProductor)
	return value
end

function send(x)
	coroutine.yield(x)
end

newProductor = coroutine.create(productor)
consumer()
```

# 5. 文件io
lua操作文件io分为两种模式：简单模式和完全模式。简单模式是和C语言一样的方式。
这个是简单模式的。

```
#!/usr/bin/lua

file = io.open("1.txt", "w+")
io.output(file)
io.write("abc\n")
io.write("123\n")
io.close(file)
file = io.open("1.txt", "r")
io.input(file)
print(io.read())
print(io.read())
io.close(file)
```

# 6. 错误处理
可以用的函数：assert和error。
举例：
```
#!/usr/bin/lua

function add(a,b)
	assert(type(a)=="number", "a is not a number")
	assert(type(b)=="number", "b is not a number")
	return a+b
end
print(add(1,2))
add(x,y)
```
error的用法也很简单：`error("test error", 2)`。后面一个参数是level。有0/1/2这3个可以选。越大越详细。



# lua主要大型项目

nmap的安全插件脚本

openresty

OpenResty® 是一个基于 [Nginx](https://openresty.org/cn/nginx.html) 与 Lua 的高性能 Web 平台，其内部集成了大量精良的 Lua 库、第三方模块以及大多数的依赖项。用于方便地搭建能够处理超高并发、扩展性极高的动态 Web 应用、Web 服务和动态网关。

# lua标准库



Lua 是一门扩展式程序设计语言，被设计成支持**通用过程式编程**，并有相关数据描述设施。 

**同时对面向对象编程、函数式编程和数据驱动式编程也提供了良好的支持。** 

它作为一个强大、轻量的嵌入式脚本语言，可供任何需要的程序使用。

 Lua 由 *clean C（标准 C 和 C++ 间共通的子集）* 实现成一个库。



作为一门扩展式语言，**Lua 没有 "main" 程序的概念**： 

**它只能 *嵌入* 一个宿主程序中工作**， 该宿主程序被称为 *被嵌入程序* 或者简称 *宿主* 。

 宿主程序可以调用函数执行一小段 Lua 代码，可以读写 Lua 变量，可以注册 C 函数让 Lua 代码调用。

 依靠 C 函数，Lua 可以共享相同的语法框架来定制编程语言，从而适用不同的领域。

 **Lua 的官方发布版包含一个叫做 `lua` 的宿主程序示例，** 

它是一个利用 Lua 库实现的完整独立的 Lua 解释器，可用于交互式应用或批处理。

Lua 是一门*动态类型语言*。

 **这意味着变量没有类型；只有值才有类型。**

 语言中不设类型定义。 所有的值携带自己的类型。

由于 Lua 是一门嵌入式扩展语言，其所有行为均源于宿主程序中 C 代码对某个 Lua 库函数的调用。

（单独使用 Lua 时，`lua` 程序就是宿主程序。） 

所以，在编译或运行 Lua 代码块的过程中，无论何时发生错误， **控制权都返回给宿主**，由宿主负责采取恰当的措施（比如打印错误消息）。



Lua 中的每个值都可以有一个 *元表*。 

这个 *元表* 就是一个普通的 Lua 表， 它用于定义原始值在特定操作下的行为。

 如果你想改变一个值在特定操作下的行为，你可以在它的元表中设置对应域。 

例如，当你对非数字值做加操作时， Lua 会检查该值的元表中的 "`__add`" 域下的函数。 

如果能找到，Lua 则调用这个函数来完成加这个操作。



# lua环境变量`_ENV`和`_G`

Lua将环境table保存在一个全局变量_G中，可以对其访问和设置。一般我们把需要被访问的对象和函数等放到这里， 
然后我们可以在需要时通过它来访问和使用。 
可以通过`value = _G["varname"]`或者`value = _G.varname`来获得动态名字的全局变量。

```
> a=1
> b="bb"
> print(_G["a"])
1
> print(_G.b)
bb
```

“环境”是全局的，任何对它的修改都会影响程序的所有部分。

对简单的使用不会有什么问题，**但较复杂的应用，这个会是一大潜在的问题**



Lua5.1允许每个函数拥有一个子集的环境来查找全局变量，

可以通过setfenv来改变一个函数的环境， 

第一个参数若是1则表示当前函数，2则表示调用当前函数的函数（依次类推），

第二个参数是一个新的环境table。



参考资料

1、Lua 5.3 参考手册

https://www.runoob.com/manual/lua53doc/contents.html

2、`Lua中的函数环境、_G及_ENV`

https://blog.csdn.net/whereismatrix/article/details/79704421