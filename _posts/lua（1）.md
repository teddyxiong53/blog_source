---
title: lua（1）
date: 2022-12-08 12:05:19
tags:
	- lua

---

--

现在决定投入精力把lua掌握。

基础语法没有什么可看的。就从实际应用入手。

2个方向：

1、lua web开发。

2、lua gui开发。



做这一切之前，先搭建环境。

lua有没有官方的包管理机制？

先在ubuntu下安装lua吧。

提供了3个版本：5.1、5.2、5.3

那当然用最新的。

```
sudo apt install lua5.3 
```

那么这3个版本有什么明显的区别没有？

# lua版本区别

Lua的版本差异确实是比较让人头疼的事情，

之前在移动端一直采用Android下使用LuaJit，

Ios下使用Lua5.1。

这次升级到Xlua（lua5.3版本）主要有两方面的原因：

一是ulua后续维护比价差，决定要升级到xlua，

另一方面是公司在上线检查中提示禁止Luajit的使用（一些Crash无法解决），当然顺便解决了bit64位问题。

5.2中抛弃module，建议使用require进行加载， 可能是考虑到Module定义对全局表的污染， 

Lua5.2开始取消了环境表的概念，取消setfenv/getfenv方法，增加了_Env来管理。



参考资料

1、这篇文章提到了不少干货

https://www.cnblogs.com/zsb517/p/6822870.html

2、从 Lua 5.2 迁移到 5.3

https://blog.codingnow.com/2015/01/lua_52_53.html

# lua包管理

Luarocks 是一个 Lua 包管理器，

基于 Lua 语言开发，

提供一个命令行的方式来管理 Lua 包依赖、安装第三方 Lua 包等，

社区比较流行的包管理器之一，

另还有一个 LuaDist，

Luarocks 的包数量比 LuaDist 多，更细节的两者对比可参阅

http://notebook.kulchenko.com/zerobrane/lua-package-managers-luadist-luarocks-and-integration-with-zerobrane-studio

在谷歌上搜索lua包管理。看到的结果都是luarocks。那就选用这个吧。

怎么安装呢？

luarock的官网在这里：

https://luarocks.org/

官网推荐的安装方式就是通过源代码安装：

```
wget https://luarocks.org/releases/luarocks-3.9.1.tar.gz
```

要编译luarocks，需要安装lua的开发库。

```
sudo apt install liblua5.3-dev
```

然后configure、make、make install就可以。

验证一下luarocks安装是否有用。

```
# 安装一个luasocket的库
sudo luarocks install luasocket
```

然后在lua repl里执行：

```
require "socket"
```

但是我这里没有效果。还是提示找不到这个。

再安装一般，看到最后是打印了这个：

```
luasocket 3.1.0-1 is now installed in /home/teddy/luarocks-3.9.1/./lua_modules (license: MIT)
```

这个怎么是安装到我的当前路径呢？

不应该。

当前路径就当前路径吧。

那么看怎么把当前路径加入到lua的搜索path里。

这里有说怎么指定搜索路径的。

https://www.runoob.com/lua/lua-modules-packages.html

我再安装了一次。正常了。

```
luasocket 3.1.0-1 is now installed in /usr/local (license: MIT)
```

可以正常require了。



## 加载机制

对于自定义的模块，模块文件不是放在哪个文件目录都行，函数 require 有它自己的文件路径加载策略，它会尝试从 Lua 文件或 C 程序库中加载模块。

require 用于搜索 Lua 文件的路径是存放在全局变量 package.path 中，当 Lua 启动后，会以环境变量 LUA_PATH 的值来初始这个环境变量。如果没有找到该环境变量，则使用一个编译时定义的默认路径来初始化。

当然，如果没有 LUA_PATH 这个环境变量，也可以自定义设置，在当前用户根目录下打开 .profile 文件（没有则创建，打开 .bashrc 文件也可以），例如把 "~/lua/" 路径加入 LUA_PATH 环境变量里：



```
#LUA_PATH
export LUA_PATH="~/lua/?.lua;;"
```

文件路径以 ";" 号分隔，最后的 2 个 ";;" 表示新加的路径后面加上原来的默认路径。

这两种写法都是合法的。

```
require("<模块名>")
```

或者

```
require "<模块名>"
```

## luarocks用法

luarocks查看配置：

```
luarocks config
```



参考资料

1、

https://segmentfault.com/a/1190000003920034

# 进行web开发

现在lua和包管理都配置好了。

现在看看怎么跑一个lua web的HelloWorld。

Orbit

orbit是lua的mvc web框架。

使用`luarocks`搜索并安装`wsapi-xavante`，`wsapi-xavante`是支持Web服务API的Web服务器。

```
sudo luarocks install wsapi-xavante
```

会自动安装依赖的。

得到wsapi这个命令：

```
wsapi --help
```

https://keplerproject.github.io/wsapi/

wsapi是Lua WebSever API的缩写。

最近的版本是2014年的。这也太古老了吧。

看来这个方向在lua并不是热门。

安装：

```
sudo luarocks install kepler-xavante
```



这个后面研究一下openwrt的界面就好了。

https://www.jianshu.com/p/94342efd9467

# 进行gui开发

我就看lua widget的开发。

叫wxlua。

官网：

https://wxlua.sourceforge.net/

用luarocks安装是不行的。

```
Error: No results matching query were found for Lua 5.3.
```

那就可以引出下一个话题：lua怎么安装虚拟环境，就像pyvenv那样。

# lua多版本共存

安装luaver工具：

```
curl https://raw.githubusercontent.com/dhavalkapil/luaver/master/install.sh -o install.sh && . ./install.sh
```

执行命令后提示要手动把下面2行加到bashrc的最后。

```
[ -s ~/.luaver/luaver ] && . ~/.luaver/luaver
[ -s ~/.luaver/completions/luaver.bash ] && . ~/.luaver/completions/luaver.bash
```

luaver --help查看帮助信息。

命令还是非常简单清晰的。

我现在使用luaver安装5.1的版本。

```
luaver install 5.1
luaver use 5.1
```

lua查看一下，的确切换到5.1了。

```
teddy@teddy-VirtualBox:~$ lua
Lua 5.1  Copyright (C) 1994-2006 Lua.org, PUC-Rio
> 
```

# 在5.1的基础上安装wxlua

还需要用luaver来管理luarocks

```
luaver list-luarocks
```

当前是没有的。

```
luaver install-luarocks
```

这个要指定版本号。



实际上就是到这里去下载： https://luarocks.github.io/luarocks/releases/

看网页下，最新的是3.9.1。



```
luaver install-luarocks 3.9.1
```

使用：

```
luaver use-luarocks 3.9.1
```

可以看到已经切换了：

```
teddy@teddy-VirtualBox:~$ which luarocks
/home/teddy/.luaver/luarocks/3.9.1_5.1/bin/luarocks
```

安装luarocks

```
luarocks install wxlua
```

还是找不到。

搜索一下怎么安装wxlua。

https://github.com/pkulchenko/wxlua/blob/master/wxLua/docs/install.md

这样太麻烦了。

先不做吧。

1、

https://stackoverflow.com/questions/30362466/with-multiple-versions-of-lua-installed-is-it-possible-to-specify-which-one-luar



# lua代码初步分析

看一下乱的源代码。

就看lua5.3的。这个已经有一段时间了。应用应该比较广泛。

用source insight来读一下代码。

不过现在最新的版本是5.4的。

# 背景

Lua程序设计语言 是一个简洁、轻量、可扩展的脚本语言。Lua读作/’lua/（噜啊），是葡萄牙语中"Luna"（月亮）的意思。Lua是一种轻量语言，它的官方版本只包括一个精简的核心和最基本的库。这使得Lua体积小、启动速度快。它用标准ANSI C语言编写并以源代码形式开放，编译后仅仅一百余K，可以很方便的嵌入别的程式里。

Lua的目标是成为一个很容易嵌入其它语言中使用的语言。很多应用程序使用Lua作为自己的嵌入式脚本语言，以此来实现可配置性、可扩展性。这其中包括大话西游II、仙境传说、魔兽世界、战锤40k、博德之门、轩辕剑外传汉之云等。

# luadoc

看https://github.com/hoelzro/lua-repl 这个项目的提交记录。

看到提到了luadoc这个东西，是靠从注释里提取内容来生成文档。

# lua-repl

rockspec的内容，可以作为学习参考对象。

```
package = 'luarepl'
version = '0.1-1'
source  = {
    url = 'http://...'
}
description = {
  summary  = 'A reusable REPL component for Lua, written in Lua',
  homepage = 'https://github.com/hoelzro/lua-repl',
  license  = 'MIT/X11',
}
dependencies = {
  'lua >= 5.1'
}
build = {
  type = 'builtin',
  modules = {
    ['repl']         = 'repl/init.lua',
    ['repl.sync']    = 'repl/sync.lua',
    ['repl.console'] = 'repl/console.lua',
  },
  install = {
      bin = { 'rep.lua' },
  }
}
```

`['repl']         = 'repl/init.lua',`

这个模块目录的组织方式。

# json4lua

## luasocket

json4lua依赖了luasocket。

luasocket为什么没有官方内置支持？

没有必要内置。这样就太臃肿了。

代码：

https://github.com/lunarmodules/luasocket

# teal语言：带类型的lua

就相当于ts之于js。

https://github.com/teal-language/tl

# lua面向对象

## 点号和冒号的区别

点号后面跟属性，冒号后面跟方法。

## `self.__index = self `

这句的作用是什么？

Lua 查找一个表元素时的规则，其实就是如下 3 个步骤:

1.在表中查找，如果找到，返回该元素，找不到则继续
2.判断该表是否有元表，如果没有元表，返回 nil，有元表则继续。
3.判断元表有没有 `__index` 方法，如果 `__index `方法为 nil，则返回 nil；如果 `__index `方法是一个表，则重复 1、2、3；如果 __index 方法是一个函数，则返回该函数的返回值。



简单来说，就是为了保持住继承链。

下面写法正常。

```
local class = {}

function class:new()
    self.__index = self
    return setmetatable({}, self)
end

function class:say()
    print(11)
end

local o1 = class:new()
o1.say()

local o2 = o1:new() //通过o1来调用方法。
o2.say()
```

下面的写法则o2找不到say方法。

```
local class = {}
class.__index = class

function class:new()
    return setmetatable({}, self)
end

function class:say()
    print(11)
end

local o1 = class:new()
o1.say()

local o2 = o1:new()
o2.say()

```



参考资料

1、

https://blog.csdn.net/skillart/article/details/98346459

2、

https://blog.csdn.net/weixin_34301307/article/details/85976950

## 参考资料

https://www.runoob.com/lua/lua-object-oriented.html

# 调试方法

Lua 提供了 debug 库用于提供创建我们自定义调试器的功能。Lua 本身并未有内置的调试器，但很多开发者共享了他们的 Lua 调试器代码。

# 文件io

lua处理文件io有两种模式：

1、简单模式，跟C语言一样。

2、完全模式。

简单模式适合在做一些简单的文件操作时使用。

在一些高级文件操作是，简单模式就无法满足了。

简单模式只处理一个文件。都以io为前缀。

```
file = io.open('1.txt', 'r')
-- 设置输入文件为file
io.input(file)
-- 打印读取出来的一行。
print(io.read())
-- 关闭文件
io.close(file)

-- 以append模式打开
file = io.open('1.txt', 'a')
-- 设置输出到file
io.output(file)
io.write('aaa')
io.close(file)

```

完全模式，以文件句柄为前缀。

```
file = io.open('1.txt', 'r')
print(file:read())
file:close()

```

# lua打开C库文件

Lua和C是很容易结合的，使用 C 为 Lua 写包。

与Lua中写包不同，C包在使用以前必须首先加载并连接，在大多数系统中最容易的实现方式是通过动态连接库机制。

Lua在一个叫loadlib的函数内提供了所有的动态连接的功能。

这个函数有两个参数:库的绝对路径和初始化函数。所以典型的调用的例子如下:





参考资料

1、

https://blog.csdn.net/ai5945fei/article/details/107839295

2、

这篇文章很详细了。

https://blog.csdn.net/qq_18138105/article/details/123631730



# require和dofile的区别

在lua中require和dofile都是用来加载和执行模块的，那么他们有什么不同呢？

在加载一个.lua文件的时候，require会先在package.loaded中查找此模块是否存在，如果存在则直接返回模块，如果不存在，则加载此模块。

dofile会对读入的模块编译执行，**每调用dofile一次，都会重新编译执行一次。**

require它的参数只是文件名，而dofile要求参数必须带上文件名的后缀。

https://blog.csdn.net/LF_2016/article/details/78272558

# lua函数

## 多个返回值

```
> s,e = string.find('hello world', 'world')
> s
7
> e
11
```

## 可变参数

跟C语言类似，用3个点表示函数有可变的参数。

lua把函数的参数放在一个叫arg的table里。

arg的内容，出来参数本身，还有1个自带的成员：n。表示参数个数。

例如我们实现一个接受可变参数的myprint函数。

```
function myprint(...)
    for i,v in ipairs{...} do
        print(v)
    end

end
myprint(1,2,3)
```



https://blog.csdn.net/fanyun_01/article/details/69063148

# 自己注册C函数到lua里

这个是从distri.ua里看到的。

```c
luaL_Reg lib[] = {
    {"GetSystTick", lua_getsystick},
    {"GetPid", lua_GetPid}
};
luaL_newLib(L, l);
```



# luaL_newmetatable

在通过lua绑定C++对象时，

常用的接口有以下几个

lua_register、

lua_getgloba/lua_setglobal、

lua_setfield(L, LUA_REGISTRYINDEX, "xxx")/lua_getfield(L, LUA_REGISTRYINDEX, "xxx")、

_G、

luaL_newmetatable/luaL_getmetatable，

他们调用过程中数据数据存放在哪里，对lua的底层数据结构有什么影响？

针对lua5.3.4，lua虚拟机针对每个进程有个lua_State私有数据，

而这些进程共享一个全局数据global_State。

global_State中有一个l_registry注册表，这是一个预定义出来的表，可以用来保存任何代码想保存的 Lua 值。 这个表可以用有效伪索引 `LUA_REGISTRYINDEX`来定位，当然全局数据也是放在里面。具体的l_registry结构如下：

![img](../images/random_name/1507476-20181015145551383-704475532-1670758143960.jpg)



如上图可以看到，

l_registry的index为1指向lua_State对象，

index为2指向global表，

而所有的库都是初始化到这个表中。

下面分情况说明一下：

- 当我们在lua中使用print或者io.open时，相当于是引用`l_registry[2] [“print”]和 l_registry[2][“io”][“open”]`元素
- 当我们在lua中定义全局函数print_tree时，相当于写入元素`l_registry[2`][“print_tree”]
- 当我们在代码中使用`_G.print_tree和print_tree`时，实际是引用`l_registry[2][“_G”][“print_tree”] 和 l_registry[2][“print_tree”]，`两者实际等价。因为`l_registry[2][“_G”] = l_registry[2]，`相当于引用自身。
- luaL_getmetatable/luaL_newmetatable是操作l_registry这个表。当我们使用luaL_getmetatable(L, tabname)进行查找时，实际是在查找l_register[tabname]是否存在。当调用luaL_newmetable(L, tabname)时首先判断l_register[tabname]是否存在，存在返回0.不存在就创建l_register[tabname] = {__name=tabname}，并返回1。**一种类型的C++对象，元表是一样的，可以共享元表定义，不用每个对象自己单独创建元表。所以使用luaL_newmetatable()会比较合适。**

```
通过上述的分析，可以很清楚的解释第2点的关系了：

l_registry[2]、_G、全局表几个概念等价
lua_register只是把c函数注册到全局table，即注册到l_registry[2]中
lua_setglobal和lua_getglobal只是修改和查询全局表，即l_registry[2]这个表
lua_setfield(L, LUA_REGISTRYINDEX, "xxx")/lua_getfield(L, LUA_REGISTRYINDEX, "xxx")只是修改更上层的l_registry这个表，可以用来保存C/C++代码想保存的lua值。
luaL_newmetatable/luaL_getmetatable底层调用lua_setfield(L, LUA_REGISTRYINDEX, "xxx")/lua_getfield(L, LUA_REGISTRYINDEX, "xxx")，修改l_registry这个表
```



参考资料

1、

这篇文章非常好。

https://www.cnblogs.com/liao0001/p/9791087.html



# upvalue是什么

lua与C的交互中,经常会遇到upvalues,那么什么是upvalue呢?

简单的说,upvalue就是**lua函数中引用到的外部变量**.这么说有两层意思:

1 他不是函数的局部变量,即在函数中没有用local修饰

2 **他不是[全局变量](https://so.csdn.net/so/search?q=全局变量&spm=1001.2101.3001.7020),即他在函数外部还是要用local修饰**

看下面例子就知道了

```
local upval = 123
local fun()
    upval = upval + 1  --upval就是函数fun的upvalue
    local var = 456    --不是upvalue
    global_val = 789   --也不是upvalue
end
```

在与C的交互中,可以用lua_getupvalue来获取upvalue的名字,并把它的值压栈,例如:

我们都知道，Lua里面的function实际上都是闭包（closure），

而upvalue便是它引用到的上下文变量（“引用到”三个字很关键），

业界一般又称为外部局部变量(external local variable），

如果要翻译的话，个人偏好翻译为“上文变量”。



如何获取和设置upvalue？这两个方法在[debug库](http://blog.csdn.net/ecidevilin/article/details/53048445)里（也就是说，正常编程的时候，非万不得已不要用，就算是万不得已，也尽量不要用）。



参考资料

https://blog.csdn.net/zxm342698145/article/details/79710179

https://blog.csdn.net/ecidevilin/article/details/77892113



# lua的#的作用

对字符串来说，#取字符串的长度，但对于table需要注意。

lua的table可以用数字或字符串等作为key， #号得到的是用**整数作为索引的最开始连续部分的大小**, 如果t[1] == nil, 即使t[5], t[6], t[7]是存在的，#t仍然为零。对于这类tb[1],tb[2]....才能获取到正确的长度。

因此，在平时开发过程中不建议使用#来直接获取table的元素个数。建议采用下面的封装方法，获取table的元素个数。注意，print(table.length(tab))，结果为2，记录的是非nil的元素。print(table.length(tab1))结果为3。

```
function table.length(t)
    local i = 0
    for k, v in pairs(t) do
        i = i + 1
    end
    return i
end
```



# 参考资料

1、

