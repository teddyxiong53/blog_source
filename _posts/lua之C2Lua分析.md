---
title: lua之C2Lua分析
date: 2024-05-01 13:02:49
tags:
	- lua

---

--

代码在这里

https://github.com/FASTSHIFT/C2Lua

项目没有积极维护。

但是这个思路值得分析学习一下。

# 作用

有这样的一个test.h头文件。里面有这些C函数、变量的声明。

```
extern int value;

char* CFunction(int a,float b,const char* c);
uint32_t millis();
double getsum(float n1, float n2);
char *getStr(void);

typedef struct{ int a; int b;} struct_t;
enum {A, B};


unsigned long gpio_set(uint8_t pin, bool val);
const char * UserInput();
void Nop();
double* testFunc(float* n1, int* n2, const char* str);
```

需要把这些包装成lua可以调用的函数。

得到test.cpp。

以`double* testFunc(float* n1, int* n2, const char* str);`这个为例，要得到这个。

```
static int Lua_testFunc(lua_State* L)
{
    /* get 3 param(s) from lua */
    float n1 = luaL_checknumber(L, 1);
    int n2 = luaL_checkinteger(L, 2);
    const char* str = luaL_checkstring(L, 3);

    /* call c function */
    double testFunc_retval = *testFunc(&n1, &n2, str);

    /* push c function return value to lua */
    lua_pushnumber(L, testFunc_retval);
    return 1;
}

```



```
apt-cache search lua-dev
```

这个搜索不到。

还是自己直接手动编译lua吧。

https://blog.csdn.net/DeliaPu/article/details/114271100

lua还是用5.3的版本。因为看起来这个目前算是使用比较广泛的。



```
sudo apt-get install libreadline-dev
wget http://www.lua.org/ftp/lua-5.3.0.tar.gz
tar zxf lua-5.3.0.tar.gz
cd lua-5.3.0
make linux test
sudo make install
```

install的时候是这样：

```
cd src && mkdir -p /usr/local/bin /usr/local/include /usr/local/lib /usr/local/man/man1 /usr/local/share/lua/5.3 /usr/local/lib/lua/5.3
cd src && install -p -m 0755 lua luac /usr/local/bin
cd src && install -p -m 0644 lua.h luaconf.h lualib.h lauxlib.h lua.hpp /usr/local/include
cd src && install -p -m 0644 liblua.a /usr/local/lib
cd doc && install -p -m 0644 lua.1 luac.1 /usr/local/man/man1

```

库是/usr/local/lib目录

头文件是/usr/local/include目录

可执行文件是/usr/local/bin目录

现在lua可以用了。

