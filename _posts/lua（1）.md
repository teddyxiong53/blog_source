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

# lua发展历史

Lua 是一种轻量级、高效的脚本语言，最初由巴西里约热内卢天主教大学（Pontifical Catholic University of Rio de Janeiro）的一个研究小组开发。下面是 Lua 的发展历史：

1. 1993 年，Lua 诞生。最初的 Lua 是由 Roberto Ierusalimschy、Waldemar Celes 和 Luiz Henrique de Figueiredo 开发的。Lua 最初的目标是为**巴西工业界的嵌入式系统**提供一种灵活、轻量级的脚本语言。

2. 1996 年，Lua 发布了第一个公开版本 Lua 2.5。这个版本增加了很多新的特性，包括函数闭包、垃圾回收、协同程序等。

3. 1998 年，Lua 3.0 发布。这个版本增加了新的数据类型（如表）、更加灵活的函数调用、强化的垃圾回收等特性。

4. 2001 年，Lua 4.0 发布。这个版本加入了更多的语言特性，如元表、元方法、协议、面向对象编程等。

5. 2003 年，Lua 5.0 发布。这个版本加入了更强大的函数处理能力、更灵活的模块系统、更好的错误处理等特性。同时还加入了 Lua 语言的 JIT 编译器（LuaJIT）。

6. 2006 年，Lua 5.1 发布。这个版本加入了一些新的特性，如尾调用优化、局部变量声明等。

7. 2011 年，Lua 5.2 发布。这个版本增加了对 UTF-8 编码的原生支持、增强的错误处理、更强大的模块系统等。

8. 2015 年，Lua 5.3 发布。这个版本加入了更多的语言特性，如整数类型、无符号整数类型、正则表达式等。

9. 2019 年，Lua 5.4 发布。这个版本加入了更多的新特性，如新的整数类型、更灵活的元表处理、更好的错误处理等。

今天，Lua 仍然是一种流行的脚本语言，被广泛地应用于游戏开发、嵌入式系统、Web 开发等领域。Lua 的设计精简、易于学习和使用，同时也具有很高的性能和扩展性，这使得它成为了许多程序员的首选脚本语言之一。



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

调用时的 player.takeDamage(player, 20) 稍显不和谐（据说用术语叫做 DRY），于是就要出动「冒号操作符」这个专门为此而生的语法糖了：

```
player:takeDamage(20)              --> 等同于 player.takeDamage(player, 20)
function player:takeDamage(amount) --> 等同于 function player.takeDamage(self, amount)
```

https://www.kancloud.cn/thinkphp/lua-guide/43811



在 Lua 中，冒号（`:`）和点号（`.`）都可以用于访问对象的成员，但它们之间有一些区别。

点号（`.`）用于访问对象的成员时，需要明确指定对象的名称。例如：

```lua
local person = {name = "Alice", age = 20}
print(person.name) -- 输出 "Alice"
```

上述代码中，我们定义了一个名为 `person` 的表，该表包含两个成员 `name` 和 `age`。然后，我们使用点号（`.`）来访问表中的 `name` 成员，输出其值。

冒号（`:`）用于调用对象的方法时，它会自动将对象本身作为第一个参数传递给方法。例如：

```lua
local person = {name = "Alice", age = 20}

function person:sayHello()
    print("Hello, my name is " .. self.name)
end

person:sayHello() -- 输出 "Hello, my name is Alice"
```

上述代码中，我们定义了一个名为 `person` 的表，该表包含两个成员 `name` 和 `age`，以及一个名为 `sayHello` 的方法。注意，该方法的定义中使用了冒号（`:`）来指定 `person` 表为方法的接收者。

然后，我们使用冒号（`:`）来调用 `sayHello` 方法，该方法会输出一个问候语，其中包含 `name` 成员的值。注意，我们不需要手动指定 `person` 表为方法的第一个参数，因为冒号（`:`）会自动将 `person` 表作为该方法的第一个参数传递给它。

**综上所述，冒号（`:`）和点号（`.`）都可以用于访问对象的成员，但冒号（`:`）主要用于调用对象的方法，并自动将对象本身作为第一个参数传递给方法。**

## 类

类的意义在于提取一类对象的共同点从而实现量产（我瞎扯的 >_<）。

同样木有 Class 概念的 Javascript 使用 prototype 实现面向对象，

**Lua 则通过 Metatable 实现与 prototype 类似的功能。**



## `self.__index = self `

这句的作用是什么？

顾名思义 Metatable 也是一个 Table，

可以通过在其中存放一些函数（称作 metamethod）从而修改一些默认的求值行为（如何显示为字符串、如何相加、如何连接、如何进行索引）。

Metatable 的 `__index` 域设置了「如何进行索引」的方法。

例如调用 foo.bar 时，如果在 foo 中没有找到名为 bar 的域时，

则会调用 Metatable：__index(foo, bar)。





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

## 继承

```lua
RMBPlayer = Player:create()
function RMBPlayer:broadcast(message)
	print(message)    
end
function RMBPlayer:takeDamage(amount)
	self.health = self.health - amount/(self.money/100)    
end
vip = RMBPlayer:create{money = 200}
vip:takeDamage(20)
vip:broadcast('haha')
```



参考资料

1、

https://blog.csdn.net/skillart/article/details/98346459

2、

https://blog.csdn.net/weixin_34301307/article/details/85976950

## 参考资料

https://www.runoob.com/lua/lua-object-oriented.html

https://www.kancloud.cn/thinkphp/lua-guide/43811

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
luaL_newlib(L, l);
```

有两种级别，一种是只是导出一个全局变量。一种是导出成模块。

导出成全局变量的方式简单一些

## 导出成全局变量

```c
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"
#include "mylualib.h"
#include "mylog.h"
#include <time.h>
char *os()
{
    return "Linux";
}

static int los(lua_State *L)
{
    lua_pushstring(L, os());
    return 1;
}
double now()
{
    struct timespec now = {};
    clock_gettime(CLOCK_REALTIME, &now);
    return now.tv_sec + now.tv_nsec * 1e-9;
}

static int lnow(lua_State *L)
{
    lua_pushnumber(L, now());
    return 1;
}
int main(void)
{
    lua_State *L = luaL_newstate();
    // 打开标准库
    luaL_openlibs(L);
    // 打开我的自定义库
    // luaopen_sys(L);
    luaL_Reg sys_libs[] = {
        {"os", los},
        {"now", lnow},
        {NULL, NULL}
    };
    luaL_newlib(L, sys_libs);
    lua_setglobal(L,"sys");//这句就是把sys导出成全局变量
    int ret = 0;
    ret = luaL_dofile(L, "./test-mylib.lua");
    if (ret) {
        myloge("execute lua file fail, %d", ret);
    }
    lua_close(L);
    return 0;
}
```

## 导出成模块

这样就可以的。

```
int luaopen_mycomplib(lua_State* L)
{
	const char *libName = "mycomplib";
	luaL_register(L, libName, mylibs);
	return 1;
}
```

不对，luaL_register这个是老版本的函数，

```
/* compatibility with old module system */
#if defined(LUA_COMPAT_MODULE)

LUALIB_API void (luaL_pushmodule) (lua_State *L, const char *modname,
                                   int sizehint);
LUALIB_API void (luaL_openlib) (lua_State *L, const char *libname,
                                const luaL_Reg *l, int nup);

#define luaL_register(L,n,l)	(luaL_openlib(L,(n),(l),0))

#endif
```

https://zilongshanren.com/post/lua-call-cpp-functions/

这篇文章有讲到方法。但是没有没有讲模块的。

注意：这里C函数参数里的Lua栈是私有的，每一个函数都有自己的栈。当一个c/c++函数把返回值压入Lua栈以后，该栈会自动被清空。

这个好像有讲模块的。

https://www.cnblogs.com/ring1992/p/6002890.html

但是还是luaL_register。

这个在新版本的替代函数是什么？

这里有提到一些。

https://wiki.gentoo.org/wiki/Lua/Porting_notes#luaL_openlib

Calls such as `luaL_openlib(L, name, lreg, x)` and `luaL_register(L, name, lreg)` should be carefully rewritten because a global table with the given name will be searched and possibly created. When possible, it should be rewritten to `luaL_setfuncs(L, lreg, 0)`.



Lua5.2 以后取消了这个接口，不过可以通过luaL_setfunc方法看来实现

```cpp
#undef luaL_register
#define luaL_register(L,n,f) \
	{ if ((n) == NULL) luaL_setfuncs(L,f,0); else luaL_newlib(L,f); }
#endif
```

luaL_newlib可以实现？

luaopen_sys，名字的前缀是固定的吗？

https://stackoverflow.com/questions/46517127/lua-c-api-add-number-to-new-lib



这里有一些例子。

https://cpp.hotexamples.com/examples/-/-/luaL_newlib/cpp-lual_newlib-function-examples.html

这里有一些库。

http://webserver2.tecgraf.puc-rio.br/~lhf/ftp/lua/

这个是5.3下面写C module的文章。这个应该可以。

http://m.blog.chinaunix.net/uid-21706718-id-5787226.html

### 规则

*luaopen_clibs* 函数必须满足命名规则，即固定前缀 *luaopen_ +*动态库名（不包含后缀*.so*）



这篇文章有说得有操作性。我最终参考这个实现了。

http://lua-users.org/lists/lua-l/2013-08/msg00123.html

代码是这样：

```
void init_lua_libs(lua_State* L)
{
    // 打开标准库
    luaL_openlibs(L);
    /* 注入lua搜索域 */
    lua_getglobal(L,"package");
	lua_getfield(L,-1,"preload");
	lua_pushcfunction(L,luaopen_sys);
	lua_setfield(L,-2,"sys");
    lua_pushcfunction(L,luaopen_timer);
	lua_setfield(L,-2,"timer");
}
```

这样就把自定义的sys和timer这2个C语言写的模块注册进去了。

可以这样正常require并使用。

```
local sys = require "sys"
print(sys.os())
local timer = require "timer"
print(timer.timer())
```



## 注入lua搜索域



## 参考资料

https://blog.csdn.net/Andy_93/article/details/79404515

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

# 为什么lua函数有的可以省略括号



https://blog.csdn.net/Dionysos_lai/article/details/47974747

# lua_rawset作用

早在之前我们就讲述过，如果对一个表进行查找的时候，若表中不存在该值，则会查找该表的元表访问其原表`__index`字段来解决。

    而若对表输入一个不存在的值，则会查找该表的原表访问其原表`__newindex`字段来解决。
    
    而rawset & rawget则是绕过原表这一过程，直接把操作这个表相应的结论直接输出


```
lua_newtable(L);            //创建一个表格，放在栈顶
lua_pushstring(L,"mydata"); //压入key
lua_pushnumber(L,66);        //压入value
lua_settable(L,-3);         //弹出key,value，并设置到table里面去
			//原来这个是通过直接操作栈的位置来实现弹出的目的。弹出来，就相当于设置到lua里去了。
			//就像填入子弹，扣动扳机一样。
lua_pushstring(L,"subdata");//压入key
lua_newtable(L);            //压入value,也是一个table
lua_pushstring(L,"mydata"); //压入subtable的key
lua_pushnumber(L,53);
valuelua_settable(L,-3);    //弹出key,value,并设置到subtable
lua_settable(L,-3);         //这时候父table的位置还是-3,弹出key,value(subtable),
                            //并设置到table里去
lua_pushstring(L,"mydata2");//同上
lua_pushnumber(L,77);
lua_settable(L,-3);
return1;
//栈里就一个table其他都被弹掉了。如果要返回一个数组，
//用如下代码：(注意那个关于trick的注释，我在等官方的解释。
//经过验证，这个问题只在windows版本调用dll中方法的时候出现。WinCE正常)
lua_pushstring(L,"arri");
lua_newtable(L);
{
    //atrick:otherwisetheluaenginewillcrash.ThiselementisinvisibleinLuascript
    lua_pushnumber(L,-1);
    lua_rawseti(L,-2,0);
    for(int i=0; i<arri.size(); i++)
    {
        lua_pushnumber(L, arri);
        lua_rawseti(L, -2, i+1);
    }
}
lua_settable(L,-3);
```



https://blog.csdn.net/cooclc/article/details/115346937

# userdata的元表



https://blog.csdn.net/Kiritow/article/details/85012879

# 函数api对栈的影响

这里按字母次序列出了所有 C API 中的函数和类型。 每个函数都有一个这样的提示： [-o, +p, *x*]

对于第一个域，`o`， 指的是该函数会从栈上弹出多少个元素。

 第二个域，`p`， 指该函数会将多少个元素压栈。 

（**所有函数都会在弹出参数后再把结果压栈。**）

 `x|y` 这种形式的域表示该函数根据具体情况可能压入（或弹出） `x` 或 `y` 个元素；

 问号 '`?`' 表示 我们无法仅通过参数来了解该函数会弹出/压入多少元素 （比如，数量取决于栈上有些什么）。

 第三个域，`x`， 解释了该函数是否会抛出错误： '`-`' 表示该函数绝对不会抛出错误； '`e`' 表示该函数可能抛出错误； '`v`' 表示该函数可能抛出有意义的错误。

# lua c api接口的返回值的含义

表示返回的结果的个数。

返回0表示没有参数返回，返回1表示返回一个结果。

# local type = type写法的好处

可以减少一次到_G查表的过程。

# lua的注释规范

```lua
--- 测试用表
-- @class table
-- @name testTable
-- @field testA 测试字段A
-- @field testB 测试字段B
testTable =
{
    testA = nil,
    testB = nil,
}
--- 测试函数
-- @param a 参数a
-- @param b 参数b
-- @return 返回1
-- @usage testFun(1, 2)
-- @see testTable
function testFun(a, b)
    return 1

end
```



https://blog.csdn.net/caomx0125/article/details/79424608

# c和lua的性能差距

是30倍。

```
--[[
经过测试: 100万此编码/解码两者性能相差30倍, 正好是lua与C的性能差距.
]]
```

而python的典型值是100倍。

# 以C为主还是以lua为主

lua与c是很方便的交互的，

但是在实际的游戏项目中，我们首先必须确定的一个问题就是，

代码逻辑是以lua为主还是以c为主。

lua为主的游戏就是逻辑主要由lua负责，核心的对性能要求较高的逻辑则由c负责，游戏中的数据大多由lua负责。

c为主的游戏则是逻辑主要由c负责，lua只是负责简单的配置。



这两种方式都有优劣，对于实际游戏项目来说，个人认为，应该采用lua为主，c作为高性能核心的方式。

之所以这样选择，是因为游戏的逻辑变动很大，

我们需要快速的进行代码迭代，这个对于lua来说非常方便。

而对于核心引擎，因为变化不大，同时对性能要求较高，所以采用c是一个很好的选择。



在实际的游戏项目中，我们会遇到这样一个问题，

假设c提供的函数为 int func(int a, int b)，

如果这个函数要提供给lua使用，我们需要写一个对应的注册函数，如下:

```
int func_wrapper(lua_State* pState)
{
    int a = int(lua_tonumber(pState, 1));
    int b = int(lua_tonumber(pState, 2));
    int ret = func(a, b);
    lua_pushnumber(pState, ret);
    return 1;
}

lua_register(pState, func_wrapper, "func");

```

对于任意的c函数，我们需要写一个对应的wrapper用来注册给lua。

如果项目中只有几个c函数，那么无所谓，

但是如果需要注册给lua的c函数很多，

那么对于每一个c函数写一个wrapper，是一件很不现实的事情。

并且如果c函数的参数或者返回值有变化，我们同时需要修改对应的wrapper函数。

**基于上述原因，我们需要一套自动机制，能够将任意的c函数注册给lua使用。**

实际来说，我们需要提供一个函数，对于任意的c函数func，

我们只需要调用register(func, "func")，那么就能直接注册给lua使用。



https://blog.51cto.com/u_15469043/4893891

# 注册一个C函数到lua

用`lua_register`这个函数就可以了。

实际上是一个宏定义。

```
     #define lua_register(L,n,f) \
            (lua_pushcfunction(L, f), lua_setglobal(L, n))
```

# 5.1升级到5.3



https://www.cnblogs.com/zsb517/p/6822870.html

# LUA_PATH和LUA_CPATH

可以直接设置环境变量，例如在bashrc里设置：

```
## final ;; ensure that default path will be appended by Lua
export LUA_PATH="<path-to-add>;;"
export LUA_CPATH="./?.so;/usr/local/lib/lua/5.3/?.so;
                /usr/local/share/lua/5.3/?.so;<path-to-add>"
```





https://stackoverflow.com/questions/26446333/how-to-set-the-lua-path-and-lua-cpath-for-the-zerobrane-studio-in-linux



#  lua_pushliteral和lua_pushstring有何区别？

通常在push字符串字面值时使用lua_pushliteral,

在push字符串指针是使用lua_pushstring。  



原因是前者通过sizeof(字符串字面值)/sizeof(char)计算长度，而后者通过strlen计算长度。

 

因此前者只能push字符串字面值，但速度比后者快。

而后者既可push字符串字面值，也可push字符串指针。

```
const char *lua_pushliteral (lua_State *L, const char *s);
```

这个宏等价于 [`lua_pushstring`](https://www.jishuchi.com/read/lua-5.3/1981#lua_pushstring)，区别仅在于只能在 `s` 是一个字面量时才能用它。它会自动给出字符串的长度。



# lua的调试方法

官方提供的就是debug这个标准库。

这个是给lua增加gdb这样的支持，看起来不错。但是不是我现在需要的。

https://catbro666.github.io/posts/f9a188a7/



参考资料

1、

https://www.runoob.com/lua/lua-debug.html

# lua代码加载和热更新的方式

由于在游戏服务器的架构中，大部分的进程都是有状态的，

所以就非常依赖热更新。

Lua 方便的热更新是其得以在手游后端开发中大量使用的重要原因，

本篇来讲一下我了解过的 Lua 的一些代码加载和热更新方式。

## dofile

使用 dofile 进行代码加载是最简单粗暴的，

在进程启动的时候，直接将本进程所有要用到的脚本文件使用 dofile 加载进来。

如果需要重新加载，那么就对修改过的文件再次执行 dofile 重新加载一次。

但是这样加载有一个不好的地方，

就是每个文件都要对应的使用一个全局变量 Table 来进行保存，

而且如果这个 Table 被别的文件里使用 local 引用了，那么即使重新 dofile 加载一次，原来的引用还是保存了原先那个 Table 的地址。

## loadfile

使用 loadfile 加载文件，会得到一个中间函数，

**这个中间函数执行完**就跟直接调用 dofile 加载效果是一样的了。

**但是因为有了一个中间函数，就有一些操作的机会。**

可以使用 setfenv 将加载结果的函数放在一个新创建的 Table 中执行，

这样既解决了需要全局变量的问题，也解决了别的地方引用的问题。给出一个简单的实现方法。

## require

require 是 Lua 官方提供的加载模块的接口，

不仅可以加载 Lua 模块，也可以加载 C 模块。

**它加载过的模块会被放在 package.loaded 中**，对同一个模块第二次加载，不会重复加载，会直接返回旧的模块给调用者。



需要重新加载的时候需要首先将 package.loaded 中对应模块设为 nil，然后再次执行 require。

但是这样也有一个问题，那就是如果在某个地方使用 local 变量引用了 require 的结果，那么更新以后它引用的还是旧的模块。





参考资料

1、

https://wmf.im/p/lua-%E7%9A%84%E4%BB%A3%E7%A0%81%E5%8A%A0%E8%BD%BD%E5%92%8C%E7%83%AD%E6%9B%B4%E6%96%B0%E6%96%B9%E5%BC%8F/

# C语言调用lua文件并打印详细出错信息

```
lua_State *L = luaL_newstate();
luaL_openlibs(L);

lua_pushcfunction(L,traceback);
int r = luaL_loadfile(L,"test.lua");
//第四个参数表示将错误信息msg传入栈1所在的函数(错误处理函数)
r = lua_pcall(L,0,0,1);
if (r != LUA_OK)
	printf("call err\n%s\n", lua_tostring(L,-1));    
else
	printf("call succ\n");
```

traceback函数这么写：

```
static int traceback( lua_State *L)
{
    const char *msg = lua_tostring(L,-1);
    if (msg)
    {
        /*打印发生错误时的堆栈信息,msg是错误信息,附加到打印的堆栈最前端
        1是指从第一层开始回溯
        这个函数之后,lua_tostring(L,-1)即可获取完整的堆栈和错误信息.
        */
        luaL_traceback(L,L,msg,1);
    }
    else
    {
        lua_pushliteral(L,"no message");
    }
}
```



https://blog.csdn.net/GetterChange/article/details/52629471

# 对三元运算符的模拟

```
total>=128 and 128 or total
```

这个跟C语言里的：

```
total >=128 ? 128 : total
```

是等价的。

# lua延时

居然没有sleep这样的标准函数提供。

虽然我可以通过C来扩展。

# 协程用法

把协程就当成用户态线程来理解就好了。

相关概念进行一一对等。

## coroutine.create(f)

create只有一个参数，就是一个function。这个相当于pthread_create函数。

返回的是一个协程对象。

```
local co = coroutine.create(function ()
    print('in coroutine')
    return 'coroutine return'
end)
print(co)
print(coroutine.resume(co))
```

输出是这样：

```
thread: 0x55b5fb1ec6c8
in coroutine
true    coroutine return
```

通过resume运行，返回2个值，

## coroutine.resume(co, [, val1, ...])

开始或者继续运行协程。

当第一次运行一个协程对象时，

他会从主函数出开始运行。

val1这些值会以参数的形式传入到处理函数里。

当一个协程被yield后，

```
local co = coroutine.create(function (input)
    print("input:"..input)
    local param1, param2 = coroutine.yield("yield")
    print("param1 is :"..param1)
    print("param2 is :"..param2)
    return "return"
end)
--第一次执行
print(coroutine.resume(co, "function input"))
print("this is main chunk")
--第二次执行
print(coroutine.resume(co, "aa", "bb"))
```



输出：

```
input:function input
true    yield     这个是coroutine.yield("yield")返回过来的。被第一个print打印出来。
this is main chunk
param1 is :aa
param2 is :bb
true    return
```

resume是在保护模式下运行，如果有任何错误发生。

lua是不会显示任何错误的。

而是返回false加错误msg。

同时这个协程的状态变成dead。

下面通过yield一个不存在的值来模拟一个错误。

```
local co = coroutine.create(function ()
    print('error test')
    coroutine.yield(aa.a)
end)
print(coroutine.resume(co))
print(coroutine.status(co))

```



```
error test
false   test/test.lua:3: attempt to index a nil value (global 'aa')
dead
```

# lua_tothread作用

在学习lua虚拟机与C交互过程中, 看到一个很令人奇怪的API,

 lua_tothread.

[lua官方手册](http://cloudwu.github.io/lua53doc/manual.html#lua_tothread)上只是说明lua_tothread的作用是将一个thread(coroutine)以lua_State的形式表示出来, 

但是总是搞不清这个API应该在什么情况下使用.



在调用luaL_newstate函数去创建一个lua虚拟机时, 

lua就会自动在这个状态中创建一个新thread(coroutine), 

这个线程被称为主线程. 

除了调用lua_close之外, 

这个主线程永远不会被回收.



在lua中每个coroutine都有一个lua_State与之关联, 

甚至于coroutine.create的返回值其实就是一个lua_State的指针, 

这一点可以从[实验](https://gist.github.com/findstr/c38da28d3a247448fb43)得到证实, 

所以lua_tothread的作用也就是与coroutine相关联的lua_State的指针返回.



参考资料

1、

https://blog.gotocoding.com/archives/345

# package.searchers[2]

在Lua内部，是通过searchers来区分不同的加载方式。

Lua一共有4种searchers，

**用来加载lua模块的和加载C模块的分别是第2个和第3个。**

第1个searcher叫做preload，

它使用`package.preload`这个内部table，根据加载模块的名称，去找到对应的加载函数来加载模块，例如：



参考资料

1、

https://zhuanlan.zhihu.com/p/346355282

# lua实现枚举类型



# lua_pcall

p表示protect，表示保护环境。

```
if (luaL_loadfile(L, fname) || // 读取文件，将内容作为一个函数压栈
    lua_pcall(L, 0, 0, 0))     // 执行栈顶函数，0个参数、0个返回值、无出错处理函数（出错时直接把错误信息压栈）
    error();
```



```
--test.lua
function test(x,y)
    return x + y
end
lua_loadfile(L,"test.lua");

--调用
lua_pushnumber(L,10);   --x 值入栈
lua_pushnumber(L,20);   --y 值入栈
lua_pcall(L,2,1,0);
```

如果没有错误此时栈顶的值为30

如果运行出错，lua_pcall会返回一个非零的结果,如果指定了错误处理函数会先调用错误处理函数，然后再将错误信息入栈，在将返回结果和错误信息入栈之前会先将函数和参数从栈中移除。错误处理函数必须在被调用函数和其他参数之前入栈



`lua_call` 和 `lua_pcall` 是 Lua API 中的两个函数，它们都用于调用 Lua 函数，但是它们的行为和用法有所不同。

`lua_call` 函数用于调用一个 Lua 函数，它的原型如下：

```c
void lua_call(lua_State *L, int nargs, int nresults);
```

其中，`L` 是 Lua 状态机指针；`nargs` 是传递给函数的参数数量；`nresults` 是期望从函数返回的结果数量。调用 `lua_call` 函数时，Lua 会从栈顶弹出 `nargs` 个参数，并将它们传递给函数。然后，Lua 会执行函数，并将返回值压入栈中，返回值的数量由 `nresults` 指定。如果函数执行过程中发生了错误，Lua 会将错误信息压入栈中，并返回一个错误码。

`lua_pcall` 函数与 `lua_call` 类似，也用于调用一个 Lua 函数，但是它提供了额外的错误处理功能，它的原型如下：

```c
int lua_pcall(lua_State *L, int nargs, int nresults, int msgh);
```

其中，`L` 是 Lua 状态机指针；`nargs` 是传递给函数的参数数量；`nresults` 是期望从函数返回的结果数量；`msgh` 是一个错误处理函数的索引。调用 `lua_pcall` 函数时，Lua 会从栈顶弹出 `nargs` 个参数，并将它们传递给函数。然后，Lua 会执行函数，并将返回值压入栈中，返回值的数量由 `nresults` 指定。如果函数执行过程中发生了错误，Lua 会调用指定的错误处理函数，并将错误信息压入栈中，然后返回一个错误码。如果没有指定错误处理函数，Lua 会将错误信息输出到标准错误流中。

总之，`lua_call` 和 `lua_pcall` 都用于调用 Lua 函数，但是 `lua_pcall` 提供了额外的错误处理功能，可以更好地控制错误信息和行为。在使用这两个函数时，需要注意参数和返回值的数量，以及错误处理机制。



## 指定错误处理函数

在使用 `lua_pcall` 函数时，可以通过第四个参数来指定错误处理函数。第四个参数是一个整数类型，表示栈中错误处理函数的位置。如果该参数为 0，表示不指定错误处理函数，Lua 会将错误信息输出到标准错误流中。如果该参数为正数，表示栈中错误处理函数的索引，如果该参数为负数，则表示从栈顶向下的索引。例如，如果栈中的第三个元素是错误处理函数，可以将该参数设置为 3。

下面是一个示例，演示如何指定错误处理函数：

```c
int my_error_handler(lua_State *L) {
    const char *msg = lua_tostring(L, -1);
    fprintf(stderr, "Error: %s\n", msg);
    return 1;
}

int main(int argc, char **argv) {
    lua_State *L = luaL_newstate();  // 创建 Lua 状态机
    luaL_openlibs(L);  // 打开 Lua 标准库

    // 加载 Lua 文件
    if (luaL_loadfile(L, "test.lua") != LUA_OK) {
        fprintf(stderr, "Failed to load file: %s\n", lua_tostring(L, -1));
        lua_close(L);
        return 1;
    }

    // 获取错误处理函数
    lua_pushcfunction(L, my_error_handler);
    int error_handler_index = lua_gettop(L);

    // 调用函数
    lua_getglobal(L, "add");  // 获取函数
    lua_pushnumber(L, 10);  // 压入参数 a
    lua_pushnumber(L, 20);  // 压入参数 b
    if (lua_pcall(L, 2, 1, error_handler_index) != LUA_OK) {  // 调用函数，并处理错误
        fprintf(stderr, "Failed to call function: %s\n", lua_tostring(L, -1));
        lua_close(L);
        return 1;
    }

    // 获取返回值
    double result = lua_tonumber(L, -1);
    printf("Result: %.2f\n", result);

    lua_close(L);  // 关闭 Lua 状态机
    return 0;
}
```

在上面的代码中，首先定义了一个名为 `my_error_handler` 的错误处理函数。当发生错误时，该函数会将错误信息输出到标准错误流中，**并返回 1 表示已经处理了错误**。然后，使用 `lua_pushcfunction` 函数将错误处理函数压入栈中，并获取其索引。在调用 `lua_pcall` 函数时，将错误处理函数的索引作为第四个参数传递。如果函数执行过程中发生错误，Lua 会调用指定的错误处理函数，并将错误信息压入栈中，然后返回一个错误码。

需要注意的是，错误处理函数必须满足一定的条件，例如必须返回一个整数类型的值表示处理结果，必须从栈顶获取错误信息等。在使用错误处理函数时，需要仔细阅读文档，并进行适当的测试。



## my_error_handler 返回值说明

在使用 `lua_pcall` 函数时，如果指定了错误处理函数，那么当函数执行过程中发生错误时，Lua 会调用指定的错误处理函数，并将错误信息压入栈中。错误处理函数必须从栈顶获取错误信息，并返回一个整数类型的值表示处理结果。这个返回值具体表示什么意义，取决于函数执行的上下文和使用场景。

在一般情况下，错误处理函数的返回值可以有以下几种：

- 如果返回 0，表示继续抛出错误（rethrow），将错误信息传递给上一级调用者处理。
- 如果返回非 0 的整数，表示错误已经被处理，Lua 不再将错误信息传递给上一级调用者，而是认为错误已经被处理掉了，继续执行后面的代码。
- 如果错误处理函数没有返回任何值，或者返回的值不是整数类型，Lua 会将返回值视为 1，表示错误已经被处理。

需要注意的是，错误处理函数的返回值只有在发生错误时才会被使用。如果函数执行过程中没有发生错误，错误处理函数不会被调用，返回值也不会被使用。因此，在编写错误处理函数时，需要考虑到错误处理函数的返回值可能会被忽略。

## 参考资料

1、

https://www.kancloud.cn/thinkphp/lua-guide/43808

2、

https://blog.csdn.net/u010782644/article/details/79641284



# setfenv

这个函数是用来设置环境的。

为什么需要这个函数？

因为我们在全局环境里设置变量的时候，很容易碰到名字冲突。

尤其是在使用某些库的时候。

会出现变量之间相互覆盖的情况。

这个时候，我们就需要一个非全局的环境来解决这个问题。

setfenv就是用来做这个事情的。

setfenv的原型是：

```
setfenv(f, table)
当参数1是一个函数的时候，表示设置这个函数的环境。
当参数1是一个数字的时候：
	为1时，表示当前函数。
	为2时，表示自己的上一层函数。
	为3时，表示自己上两层函数。
	为N时，依次类推。
```

所谓函数的环境，

一个环境就是一个table。

函数被限定为智能访问这个table里的东西。

看下面的代码：

```lua
newfenv = {}
setfenv(1, newfenv) -- 这个就是吧当前的env设置为一个空的table。
--里面找不到print函数的。所以下面的函数会报错。
print(1)
```

可以这样来继承已有的内容

```lua
a = 10
newfenv = {_G = _G}
setfenv(1, newfenv)
_G.print(1)
_G.print(_G.a)
_G.print(a) -- 这个会找不到，因为新的table是没有a，但是可以通过_G.a来访问
```

从上面看到，这个做法有一点不方便。

可以用metatable来改进一下。

```
newfenv = {}
setmetatable(newfenv, {__index = _G})
setfenv(1, newfenv)
print(1)
```

这样对于没有冲突的符号，直接访问就可以。

如果是有冲突的符号，那么通过`_G.xx`的方式来访问。

可以用getfenv(f)函数来查看函数的环境。默认是返回`_G`。





参考资料

1、

https://blog.csdn.net/u013517637/article/details/53999170



# 模块

lua的模块是由变量、函数等构成的table。

因此创建一个模块很简单。

就是创建一个table。

然后把需要export的变量、函数放进去，最后返回这个table就好了。

格式是这样的：

```lua
module = {} -- 定义一个名为module的模块
module.constant = "this is a constant" -- 定义常量
--定义一个函数
function module.func1()
	io.write("this is a public function")
end
local function module.func2()
   print("this is a private function") 
end

function module.func3()
    func2()
end

return module
```

加载模块：

```
require ("module")
或者
require "module"

更好的做法是，给个名字。
local m = require("module")
```

require的返回值，取决于导入的文件的返回值。

如果没有返回值，那么默认是返回true。

# 函数的本质

第六章 More About Functions 中说到我们平时在 Lua 中写的函数声明

```
function foo (x) return 2*x end
```

其实是一种语法糖，本质上我们可以把它写成如下代码：

```
foo = function (x) return 2*x end
```

于是也就可以说

- Lua 中的所有函数都是匿名函数，之前所谓「具名函数」只是保存了某个匿名函数的变量罢了。
- Lua 中的函数声明其实只是一个语句而已。

# lua标准库



# Lua 函数用法和它的"诡异"之处

Lua 函数调用时, 需要带括号(对于单个参数的函数,某些值不需要用括号, 如字符串, 表). 

```
例如
print("123")可以
print "1123" 也可以。
require "xx" 可以
require("xx") 也可以

函数调用必须带括号, 除了单个参数的函数, 并且参数类型为字符串, 表构造器时, 可以不带括号.
```

但是注意return是可以带括号也可以不带括号的.

这里重点说到括号, 因为括号和返回多值的函数关系很大, 也就是"诡异"的地方, 后面会举例.



**函数可以作为一个语句执行**, 那有点类似一个过程语言, 执行完的函数结果被抛弃掉.

例如 : 

print("abc") -- 这作为一个语句执行.

函数也可以在一个表达式中执行, 那么结果会被返回, 对于多值函数需要注意返回的值的个数.

例如 :

i = math.sin(123)  -- **这里的math.sin函数在表达式中, 所以结果返回**.



参考资料

1、

https://developer.aliyun.com/article/11384

# 把penlight库研究透

这个研究透了，lua的语法和应用就基本没有问题了。



# `_G`和`_ENV`关系

在 Lua 中，`_ENV` 是一个预定义的全局变量，用于存储当前环境的变量和函数。每个 Lua 块（例如函数、代码块或模块）都有一个独立的环境，其中包含了该块中定义的所有变量和函数。在运行 Lua 块时，Lua 会根据当前块的环境来查找变量和函数。

可以通过 `_ENV` 变量来访问和修改当前环境的变量和函数。在 Lua 5.1 及之前的版本中，可以使用全局函数 `setfenv` 和 `getfenv` 来更改和获取当前块的环境；在 Lua 5.2 及之后的版本中，可以使用 `_ENV` 变量来更改和获取当前块的环境。

下面是一个简单的例子，演示如何使用 `_ENV` 变量来访问和修改当前环境的变量和函数：

```lua
-- 定义一个全局变量
x = 10

-- 定义一个函数
function f()
    print(x)
end

-- 创建一个新的环境
local env = {x = 20}

-- 在新环境下运行函数
setfenv(f, env)
f() -- 输出 "20"

-- 更改当前块的环境
_ENV = env
print(x) -- 输出 "20"
```

上述代码中，我们先定义了一个全局变量 `x` 和一个函数 `f`，并将它们存储在默认的全局环境中。然后，我们创建了一个新的环境 `env`，其中定义了一个新的变量 `x`。在使用 `setfenv` 函数将函数 `f` 的环境设置为新环境后，我们调用函数 `f`，发现它输出了新环境中的变量 `x` 的值。接着，我们使用 `_ENV` 变量将当前块的环境更改为新环境，然后输出全局变量 `x` 的值，发现它也等于新环境中的变量 `x` 的值。

需要注意的是，使用 `_ENV` 变量来修改当前块的环境可能会导致命名冲突和作用域污染。因此，在使用 `_ENV` 变量时需要格外小心，确保不会引入错误或不必要的副作用。

# 

参考资料

1、

https://juejin.cn/post/6844904121862995981

# ipairs和pairs区别

`ipairs` 和 `pairs` 都是 Lua 中用于迭代表的函数，它们之间的区别在于迭代的方式不同。

`ipairs` 函数用于迭代数组，它会返回数组中的每一个元素。具体来说，它会返回数组中的下标和对应的元素值。使用 `ipairs` 函数迭代数组时，迭代顺序是从下标 1 开始，一直到最后一个下标。

下面是一个使用 `ipairs` 函数迭代数组的例子：

```lua
local array = {1, 2, 3, 4, 5}
for i, v in ipairs(array) do
    print(i, v)
end
```

上述代码中，我们定义了一个数组 `array`，然后使用 `ipairs` 函数迭代该数组。在循环中，变量 `i` 表示当前元素的下标，变量 `v` 表示当前元素的值。

`pairs` 函数用于迭代表中的键值对，它会返回表中的每一个键值对。具体来说，它会返回键和对应的值。使用 `pairs` 函数迭代表时，迭代顺序是不确定的，因为 Lua 中的表是无序的。

下面是一个使用 `pairs` 函数迭代表的例子：

```lua
local table = {name = "Alice", age = 20, city = "New York"}
for key, value in pairs(table) do
    print(key, value)
end
```

上述代码中，我们定义了一个表 `table`，然后使用 `pairs` 函数迭代该表。在循环中，变量 `key` 表示当前键的名称，变量 `value` 表示当前键对应的值。

综上所述，`ipairs` 和 `pairs` 是用于迭代表的函数，它们之间的区别在于迭代的方式不同。`ipairs` 用于迭代数组，返回数组中的元素和下标；`pairs` 用于迭代表，返回表中的键和对应的值。

# 定义一个class

在 Lua 中，没有显式的类（class）概念，但可以通过表（table）和元表（metatable）来实现类似于面向对象的编程。

下面是一个简单的例子，演示如何使用表和元表来实现一个类：

```lua
-- 定义一个类
local Person = {}

-- 定义该类的构造函数
function Person:new(name, age)
    local obj = {name = name, age = age}
    setmetatable(obj, self)
    self.__index = self
    return obj
end

-- 定义该类的方法
function Person:sayHello()
    print("Hello, my name is " .. self.name)
end

-- 创建一个该类的实例
local person = Person:new("Alice", 20)
person:sayHello() -- 输出 "Hello, my name is Alice"
```

上述代码中，我们定义了一个名为 `Person` 的表，该表包含一个构造函数 `new` 和一个方法 `sayHello`。注意，我们将 `Person` 表作为元表，并将 `self` 设置为其元表，以便实现继承和方法调用。

在构造函数 `new` 中，我们创建了一个新的表 `obj`，并将其设置为 `self` 的元表。然后，我们设置 `self.__index` 为 `self`，以便在 `obj` 中查找属性时可以继承 `self` 中的属性。最后，我们返回 `obj`，作为该类的一个实例。

在方法 `sayHello` 中，我们使用 `self` 来访问该实例的属性 `name`，并输出一条问候语。

最后，我们使用 `Person:new` 创建了一个该类的实例 `person`，并使用 `person:sayHello()` 调用了该实例的方法 `sayHello`。

需要注意的是，虽然 Lua 中没有显式的类概念，但我们可以通过表和元表的组合来实现类似于面向对象的编程。

# lua的self

在 Lua 中，`self` 是一个特殊的关键字，用于指代当前对象或当前方法的接收者。`self` 通常在方法定义中使用，以便在方法中访问对象的属性和方法。

下面是一个简单的例子，演示如何使用 `self` 来访问对象的属性和方法：

```lua
-- 定义一个类
local Person = {}

-- 定义该类的构造函数
function Person:new(name, age)
    local obj = {name = name, age = age}
    setmetatable(obj, self)
    self.__index = self
    return obj
end

-- 定义该类的方法
function Person:sayHello()
    print("Hello, my name is " .. self.name)
end

-- 创建一个该类的实例
local person = Person:new("Alice", 20)
person:sayHello() -- 输出 "Hello, my name is Alice"
```

上述代码中，我们定义了一个名为 `Person` 的表，该表包含一个构造函数 `new` 和一个方法 `sayHello`。在方法 `sayHello` 中，我们使用 `self` 来访问该实例的属性 `name`，并输出一条问候语。

需要注意的是，在定义方法时，我们使用冒号（`:`）来指定该方法的接收者为当前对象。在方法内部，我们可以使用 `self` 来访问对象的属性和方法，也可以使用点号（`.`）来访问对象的属性和方法，例如 `self.name` 和 `self:sayHello()` 都是合法的。

在构造函数中，我们将对象的元表设置为 `self`，以便在对象中查找属性时可以继承 `self` 中的属性。然后，我们将 `self.__index` 设置为 `self`，以便在对象中查找方法时可以继承 `self` 中的方法。

综上所述，`self` 是一个特殊的关键字，用于指代当前对象或当前方法的接收者。在方法定义中，我们可以使用冒号（`:`）来指定该方法的接收者为当前对象，并使用 `self` 来访问对象的属性和方法。



# 有没有使用lua作为插件系统的编辑器

是的，有许多编辑器都使用 Lua 作为插件系统，以实现各种扩展和定制功能。以下是其中一些编辑器：

1. TextAdept：这是一款轻量级的文本编辑器，使用 Lua 作为插件脚本语言，可以通过编写 Lua 脚本来实现自定义的功能和扩展，例如自动完成、代码折叠、语法高亮和代码片段等。

2. ZeroBrane Studio：这是一款专门为 Lua 开发者设计的集成开发环境（IDE），使用 Lua 作为插件脚本语言，可以通过编写 Lua 脚本来实现自定义的功能和扩展，例如调试、自动完成、代码片段和语法检查等。

3. Hammerspoon：这是一款强大的自动化工具，使用 Lua 作为脚本语言，可以通过编写 Lua 脚本来实现自动化的任务和应用程序控制，例如窗口管理、剪贴板管理、应用程序启动和停止等。

4. SciTE：这是一款开源的文本编辑器，使用 Lua 作为脚本语言，可以通过编写 Lua 脚本来实现自定义的功能和扩展，例如自动完成、代码折叠、语法高亮和代码片段等。

5. Adobe Lightroom：这是一款数字照片管理和处理软件，使用 Lua 作为插件脚本语言，可以通过编写 Lua 脚本来增强和扩展软件的功能，例如自定义滤镜、批量处理和导出等。

这些编辑器的成功证明了 Lua 作为插件脚本语言的优越性，通过使用 Lua 可以实现强大的扩展和定制功能。如果您是开发者或者需要使用编辑器进行定制和扩展，可以尝试使用这些编辑器，并编写 Lua 脚本来实现自定义的功能和扩展。

# LUA_MULTRET

`LUA_MULTRET` 是 Lua 中一个常量，它表示可以返回任意数量的返回值。具体来说，当在调用一个 Lua 函数时，将参数 `n` 设置为 `LUA_MULTRET`，就可以让该函数返回任意数量的返回值。例如，可以使用如下代码来调用一个 Lua 函数并获取其所有返回值：

```lua
function foo(...)
    return ...
end

local results = {foo(1, 2, 3, 4, 5)}
```

在上面的代码中，`foo` 函数使用了 `...` 语法，可以接收任意数量的参数，并将这些参数作为返回值返回。在调用 `foo` 函数时，将参数 `n` 设置为 `LUA_MULTRET`，就可以获取 `foo` 函数返回的所有返回值，并将它们存放在 `results` 数组中。

需要注意的是，在使用 `LUA_MULTRET` 时，需要保证接收返回值的栈空间足够，否则可能会导致栈溢出的问题。可以使用 `lua_checkstack` 函数增加栈的大小，以确保栈空间足够。

另外，需要注意的是，在使用 `LUA_MULTRET` 时，返回值数量是不确定的，因此需要在调用之前确定返回值的数量，并根据返回值的数量来决定如何处理返回值。可以使用 `lua_gettop` 函数来查询返回值的数量。

# **LUA_REGISTRYINDEX**

`LUA_REGISTRYINDEX` 是 Lua 中的一个预定义常量，**它表示全局注册表（registry）的索引**。

全局注册表是一个特殊的表，

**可以用于存储 Lua 程序中的任意类型的值，并且这些值不会被垃圾回收。**



具体来说，当我们需要在 Lua 程序中存储一些全局的数据，但是又不希望这些数据被垃圾回收时，可以将这些数据存储在全局注册表中。

可以使用 Lua API 中的 `lua_newtable` 函数创建一个新的表，并使用 `luaL_ref` 函数将该表的引用存储到全局注册表中。

之后，就可以使用该引用来获取该表，或者从该表中取出数据。

在 Lua 中，使用 `LUA_REGISTRYINDEX` 常量可以直接访问全局注册表，而不需要通过 Lua 栈来操作。

例如，可以使用如下代码向全局注册表中存储一个字符串变量：

```c
lua_pushstring(L, "Hello, world!");
int ref = luaL_ref(L, LUA_REGISTRYINDEX);
```

在上面的代码中，我们首先将一个字符串 `"Hello, world!"` 压入 Lua 栈中，然后使用 `luaL_ref` 函数将该字符串的引用存储到全局注册表中。

此时，栈中已经没有值了，我们可以使用 `LUA_REGISTRYINDEX` 常量来获取全局注册表，并使用上面的引用来获取该字符串：

```c
lua_rawgeti(L, LUA_REGISTRYINDEX, ref);
const char *str = lua_tostring(L, -1);
printf("%s\n", str);
```

在上面的代码中，我们使用 `lua_rawgeti` 函数从全局注册表中获取之前存储的字符串，然后使用 `lua_tostring` 函数将其转换为 C 字符串，并打印出来。

需要注意的是，全局注册表是一个全局的数据结构，因此应该尽量避免在其中存储大量的数据，以免影响程序的性能。

同时，由于全局注册表中的数据不会被垃圾回收，因此在使用完毕后，需要及时将其从全局注册表中移除，以避免内存泄漏。

可以使用 `luaL_unref` 函数将之前存储的引用从全局注册表中移除。

# lua_upvalueindex 

`lua_upvalueindex` 是 Lua 中的一个预定义常量，用于访问当前函数的上值（upvalue）。

在 Lua 中，一个函数可以访问其外部函数中定义的局部变量，这些局部变量被称为上值。在编写 C 函数并将其注册到 Lua 中时，可以使用 `lua_pushcclosure` 函数创建一个闭包，并将其作为一个函数对象返回给 Lua。在创建闭包时，需要将该闭包的上值存储在一个专门的表中，并将该表作为闭包的一部分存储在 Lua 栈中。

当 Lua 调用闭包时，可以使用 `lua_upvalueindex` 常量访问闭包的上值。具体来说，`lua_upvalueindex(i)` 表示闭包中第 `i` 个上值在栈中的索引位置。例如，如果一个闭包有两个上值，可以使用如下代码来获取它们的值：

```c
int upvalue1 = lua_tointeger(L, lua_upvalueindex(1));
const char *upvalue2 = lua_tostring(L, lua_upvalueindex(2));
```

在上面的代码中，我们使用 `lua_upvalueindex(1)` 和 `lua_upvalueindex(2)` 分别获取闭包中第一个和第二个上值在栈中的索引位置，并使用 `lua_tointeger` 和 `lua_tostring` 函数将它们转换为对应的 C 类型。

需要注意的是，当使用 `lua_upvalueindex` 访问闭包的上值时，需要保证当前栈顶的是闭包对象。可以使用 `lua_iscfunction` 函数来检查当前栈顶的值是否是一个闭包。如果不是闭包，使用 `lua_upvalueindex` 可能会导致程序崩溃。

下面是一个使用 `lua_upvalueindex` 的例子：

```c
// 定义一个 C 函数，并将其注册到 Lua 中
static int myfunc(lua_State *L) {
    int upvalue1 = lua_tointeger(L, lua_upvalueindex(1));
    printf("upvalue1 = %d\n", upvalue1);
    return 0;
}

int main() {
    lua_State *L = luaL_newstate();
    lua_pushinteger(L, 42);
    lua_pushcclosure(L, myfunc, 1);
    lua_setglobal(L, "myfunc");
    lua_getglobal(L, "myfunc");
    lua_call(L, 0, 0);
    lua_close(L);
    return 0;
}
```

在上面的代码中，我们定义了一个 C 函数 `myfunc`，并将其注册到 Lua 中。在 `myfunc` 函数内部，我们使用 `lua_upvalueindex(1)` 获取闭包的第一个上值，并使用 `lua_tointeger` 函数将其转换为整数类型，并打印出来。在 `main` 函数中，我们首先创建一个 Lua 状态机，并将整数值 `42` 压入栈中。然后，我们使用 `lua_pushcclosure` 函数创建一个闭包，并将其存储为全局变量 `myfunc`。之后，我们使用 `lua_getglobal` 函数获取 `myfunc` 全局变量，并使用 `lua_call` 函数调用它。在调用 `myfunc` 函数时，Lua 会将闭包对象压入栈中，从而使得 `lua_upvalueindex` 函数可以访问闭包的上值。最后，我们使用 `lua_close` 函数关闭 Lua 状态机，并释放内存。

# Lua 使用了 C 的 longjmp 机制来处理错误。

是的，Lua 在内部实现中使用了 C 的 `longjmp` 机制来处理错误。

具体来说，当 Lua 遇到一个错误时，它会通过 `longjmp` 跳转到一个事先设定的错误处理程序，

**从而避免了多层函数调用的返回过程。**

在 Lua 中，错误通常以字符串的形式表示，并通过 `lua_error` 函数抛出。

当调用 `lua_error` 函数时，Lua 会将错误信息压入栈中，并跳转到事先设定的错误处理程序。

这个错误处理程序通常是由 Lua 库提供的，但也可以由应用程序自己定义。

在错误处理程序中，可以通过 `lua_tolstring` 函数获取错误信息，并进行相应的处理。

需要注意的是，由于 `longjmp` 会跳过多层函数调用的返回过程，因此在错误处理程序中不能直接返回，否则会导致未定义的行为。

通常情况下，错误处理程序会通过 `longjmp` 跳转回某个安全点，从而继续执行程序。

在跳转回安全点之前，可能需要进行一些清理工作，例如释放资源、回滚事务等。

下面是一个简单的例子，演示了如何在 Lua 中抛出和处理错误：

```c
int my_lua_func(lua_State *L) {
    int x = luaL_checkinteger(L, 1);
    if (x < 0) {
        lua_pushstring(L, "x must be non-negative");
        return lua_error(L);
    }
    // do something with x
    return 0;
}

int main() {
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);
    lua_pushcfunction(L, my_lua_func);
    lua_setglobal(L, "my_lua_func");
    int ret = luaL_dostring(L, "my_lua_func(-1)");
    if (ret != LUA_OK) {
        const char *errormsg = lua_tostring(L, -1);
        printf("Error: %s\n", errormsg);
        lua_pop(L, 1);
    }
    lua_close(L);
    return 0;
}
```

在上面的代码中，我们定义了一个 Lua 函数 `my_lua_func`，该函数接受一个整数参数 `x`，并检查其是否为非负数。

如果 `x` 是负数，我们使用 `lua_pushstring` 函数将错误信息压入栈中，并通过 `lua_error` 函数抛出错误。

在主函数中，我们使用 `luaL_dostring` 函数执行一个 Lua 代码，该代码调用了 `my_lua_func(-1)`，即传入了一个负数参数。

如果执行出错，我们通过 `lua_tostring` 函数获取错误信息，并打印出来。最后，我们使用 `lua_close` 函数关闭 Lua 状态机，并释放内存。

# lua协程的实现原理

Lua 内部使用 C 的 `longjmp` 机制让出一个协程。 

因此，如果一个 C 函数 `foo` 调用了一个 API 函数， 而这个 API 函数让出了（直接或间接调用了让出函数）。 

**由于 `longjmp` 会移除 C 栈的栈帧， Lua 就无法返回到 `foo` 里了。**



# 参考资料

1、

