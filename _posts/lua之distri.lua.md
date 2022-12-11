---
title: lua之distri.lua
date: 2022-12-10 20:03:19
tags:
	- lua

---

--

代码在这里：

https://github.com/sniperHW/distri.lua

看起来规模适中。有实用性。

把所有依赖都放到一起了。

而且luasocket的代码是以C代码的方式放进来的。我需要这个东西。

看看是怎么跟lua关联到一起使用的。

代码可以编译过。

看readme。

可以这样测试：

这个是pingpong测试。

```
./distrilua examples/hello.lua
./distrilua examples/pingclient.lua
```

rpc测试

```
./distrilua examples/rpcserver.lua
./distrilua examples/rpcclient.lua
```

看这个作者写了不少的不错的东西。follow了。

https://github.com/sniperHW



https://github.com/sniperHW/Survive

Survive是使用distri.lua框架实现的一个小型手游服务端示例.除了aoi和astar两个模块以外,所有游戏逻辑皆使用lua编写.



大概看了一下hello.lua的内容，感觉代码质量不错。是面向对象的写法。

这个项目值得深入看看。

是个比较合适的C和lua混合编程的例子。



# 编译过程分析

```
LDFLAGS = -lpthread -lrt -lm -lssl -lcrypto
INCLUDE = -IKendyNet/include -Ideps -Ideps/lua-5.3.0/src 
```

连接的库和包含的头文件目录。

KendyNet。这个是作者写的一个底层库。代码也在仓库里。

使用了jemalloc这个malloc库。

最终连接得到distrilua这个二进制文件。

## KendyNet

https://github.com/sniperHW/kendynet

作者现在又用go语言重写了这个库。

不管当前仓库里集成的是c语言的版本。

是一个轻量级的网络通信库。

这个暂时不深入去看。

# 流程分析

看distrilua是怎么可以读取执行lua文件的。

另外查找lua的路径怎么工作的。

另外luasocket怎么编译的。

src\distri.c 这个是入口文件。

它的执行就是要一个lua作为参数。

```
	if(argc < 2){
		printf("usage distrilua luafile\n");
		return 0;
	}
```

```
reg_luasocket(L);
```

luasocket是这样注册进去的。

具体做法就是把符号一个个注册进去。



# 这个写法

```
lua_setglobal(L,"C");
	g_engine = kn_new_engine();	    		
	reg_luasocket(L);
```

是不是把下面的函数都注册到C这个全局的table内部呢？

# 这里集成的luasocket不是第三方的

从代码看，是作者自己写的，因为使用的底层库是自己的kendynet。

代码复杂度没有那么高。所以可以分析一下。

是不是可以研究透彻后，自己基于libev来模拟？

# KendyNet分析

应该是一个基于io多路复用的网络框架。

作者对宏是特别喜欢使用。

复杂度还是有的。作者对C和lua都非常熟练。

可以从这里弄一些模块到我的系统里。

# 以lualog.c为切入点

对外暴露的接口是：

```
void reg_lualog(lua_State *L);
```

底层实现是KendyNet\include\log.h这里面。

```
enum{
	LOG_INFO = 0,
	LOG_ERROR,
};

#define MAX_FILE_SIZE 1024*1024*256  //日志文件最大大小256MB
```

日志级别非常简单。

```
	lua_newtable(L);	
	REGISTER_CONST(LOG_INFO);
	REGISTER_CONST(LOG_ERROR);
	
    luaL_Reg log_methods[] = {
        {"Log", lua_write_log},		
        {NULL, NULL}
    };
```



luaL_testudata 这个函数的作用是什么？

检查函数的第 `arg` 个参数是否是一个类型为 `tname` 的用户数据 （参见 `luaL_newmetatable` )。 它会返回该用户数据的地址

在C代码里注册进去的函数，就像标准库一样，可以直接使用。

不用进行require操作。



作者的C代码风格跟我的风格基本一致，看起来挺舒服的。

# 把minheap的代码提取到我的lua-apps的仓库

这个是一个典型的C执行lua文件。lua文件内部又使用自己定义的C语言的模块的典型过程。

现在跑起来了。可以看到效果。

代码目录在：

https://github.com/teddyxiong53/lua-apps/tree/main/get-from-distrilua

现在仔细分析一下代码，看看有哪些值得总结的经验。



参考资料

1、

