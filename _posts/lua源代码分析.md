---
title: lua源代码分析
date: 2022-12-09 12:16:19
tags:
	- lua

---

--

以lua5.3为分析对象。

# 代码风格

虽然看起来不是完全的蛇形命名风格，但是风格还是比较明显。

```
lauxlib.h
	这个是辅助函数文件。
	以libL_xx方式命令。
	核心接口都是lua_xx方式。
	一些需要特别摘出来的内容，会luaX_xx。
	X是一个特定的大写字母。
	lauxlib：
		luaL_xx。L表示lib。
	lbaselib
		luaB_xx。B表示base。
	lcode
		luaK_xx。一般表示k发音的c都缩写为k。这里K表code。
	lcorolib
		luaB_xx。协程函数。还是属于base功能。
	ldebug
		luaG_xx。G表示debug？好吧。
	ldo
		luaD_xx。D表示Data？
	lfunc
		luaF_xx。F表示Function。
	lgc
		luaC_xx。C表示collect收集。
	llex
		luaX_xx。X表示lex。词法分析。
	lmem
		luaM_xx。M表示mem。
	lobject
		luaO_xx。o表示Object。
	lopcodes
		luaP_xx。P表示operate。
	lparser
		luaY_xx。
	lstate
		luaE_xx。
	lstring
		luaS_xx。
	ltable
		luaH_xx。H表示hash？
	ltm
    	luaT_xx。T表示TagMethod。
    lumdump
    	luaU_xx。表示undump。
    lvm
    	luaV_xx。表示vm。
    lzio
    	luaZ_xx。
```

# 从C语言嵌入lua入手

接下来，将所有src中的所有 .c (**lua.c除外**)和 .h 文件加入到工程中，编译，就可以得到我们想要的静态库 liblua.lib 文件了。

在我们自己的软件项目中，只需要 liblua.lib 和几个头文件就可以开发了，用到的头文件有：

- lauxlib.h
- lua.h
- luaconf.h
- lualib.h

现在我们来写一个最简单的C语言控制台程序，并在其中内嵌Lua解释器，运行该程序，可以执行test.lua脚本，在屏幕上打印出我们希望的结果。

在lua-5.3的源代码目录下：

新建mytest.lua：

```
print('hello lua')
```

新建mytest.c

```c
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"


int main(void)
{
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);
    luaL_dofile(L, "./mytest.lua");
    lua_close(L);
    return 0;
}
```

编译：

```
gcc mytest.c -L./ -llua -lm -ldl
```

然后分析用到的这个几个函数和结构体。

## lua_State

 lua_State 中放的是 lua [虚拟机](https://so.csdn.net/so/search?q=虚拟机&spm=1001.2101.3001.7020)中的环境表、注册表、运行堆栈、虚拟机的上下文等数据。

从一个主线程（特指 lua 虚拟机中的线程，即 coroutine）中创建出来的新的 lua_State 会共享大部分数据，但会拥有一个独立的运行堆栈。

所以一个线程对象拥有一个lua_State。

lua_State共享的数据部分是全局状态机（包含GC的数据）.

lua_State 的运行堆栈为调用栈,

lua_State 的数据栈包含当前调用栈信息。



从 C 层面看待 lua ，lua 的虚拟机对象就是一个lua_state 。

但实际上，真正的 lua虚拟机对象被隐藏起来了。

那就是 lstate.h 中定义的结构体  global_State。

同一 lua 虚拟机中的所有执行线程，共享了一块全局数据 global_state 。



参考资料

1、lua 源码分析之线程对象lua_State

https://blog.csdn.net/chenjiayi_yun/article/details/24304607



我觉得这样吧commonheader写成一行的做法，看起来比较清晰。

```
#define CommonHeader	GCObject *next; lu_byte tt; lu_byte marked

struct GCObject {
  CommonHeader;
};
```

# 分析lua.c

这个是解释器的文件。

使用：

```
teddy@teddy-VirtualBox:~/work/test/lua-code-test/lua-5.3$ ./lua --help
./lua: unrecognized option '--help'
usage: ./lua [options] [script [args]]
Available options are:
  -e stat  execute string 'stat'
  -i       enter interactive mode after executing 'script'
  -l name  require library 'name' into global 'name'
  -v       show version information
  -E       ignore environment variables
  --       stop handling options
  -        stop handling options and execute stdin
```



# 参考资料

1、

https://blog.csdn.net/tjcwt2011/article/details/106138625

2、

https://www.miaoerduo.com/2020/02/26/lua-state-tutorial/