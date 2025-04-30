---
title: lua栈分析
date: 2022-12-11 09:38:19
tags:
	- lua

---

--

Lua通过一个“虚拟栈”与C/C++程序进行数据交互，所有的Lua C API都是通过操作这个栈来完成相应的数据通信。

 

Lua的这个“虚拟栈”解决了C/C++程序与Lua程序通信的两大问题：

- Lua使用垃圾回收，而C/C++需要手动管理内存。
- Lua使用动态类型，而C/C++使用的是静态类型。

栈的一个slot，是一个lua_Value容器。所以可以存放任何C类型。

在lua代码里，只能每次操作栈顶。

在c代码il，可以操作栈的任意位置。

对栈的操作

```
push 一个value进去
    lua_pushnil
    lua_pushboolean
    lua_pushnumber
    lua_pushinteger
    lua_pushunsiged
    lua_pushlstring
    lua_pushstring
    
查询一个元素的类型
lua_isXX(lua_State *L, int index);

拿到栈内某个index的值。
xxx lua_toXXX(lua_State *L, int index);
```



`lua.h`：提供使用Lua所需的所有函数。这个文件中的所有函数都以`lua_`为前缀。

`luaxlib.h`：使用`lua.h`中公开的公共API，为常见任务提供更高层次的抽象。该文件中的所有函数都以`luaL_`为前缀。

`lualib.h`：提供标准的Lua库。这个文件中的所有函数也都以`luaL_`为前缀。



Lua不分配任何全局内存。

相反，它将所有的状态存储在一个叫做`lua_State`的结构中。

这个结构包含了Lua运行时所需的一切。

在`lua_State`对象周围放置一个互斥锁是一个快速而简单的方法，可以确保任何Lua实例都是线程安全的。

在一个应用程序中创建多个状态并因此创建多个Lua运行时是完全有效的，尽管这样做的用例不多。



要创建一个新的Lua状态，请调用`luaL_newstate()`函数，

它将返回一个指向`lua_State`结构的指针。

这个指针需要传递给所有未来的Lua API调用——这就是 Lua 知道它正在使用什么运行时的方式。

在你的程序运行完毕后，用`lua_close(lua_State*)`函数销毁这个状态。



当你创建一个新的Lua状态时，标准Lua库不会被自动加载。

这可能是个问题，因为Lua程序员至少会期望准Lua库是可用的。

你可以用`luaL_openlibs(lua_State*)`函数加载标准库。



下面的代码演示了如何设置和销毁嵌入式 Lua 运行时：

```c
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"

int main(int argc, char** argv) {
    // 首先, 创建一个新的lua state
    lua_State *L = luaL_newstate();
    // 接下来, 加载所有的标准库
    luaL_openlibs(L);
    
    //在此处编写与 Lua 运行时交互的代码
    
    // 最后，销毁lua state
    lua_close(L);
    return 0;
}
```



# 栈

Lua和C是根本不同的语言。

它们处理一切的方式都不同，如内存管理、类型，甚至是函数调用。

这在试图整合这两种语言时带来了一个问题：

我们如何在这两种语言之间进行交流？

这就是Lua栈出现的地方。



**Lua栈是一个抽象的栈，位于C语言和Lua运行时之间。**

它是一个后进先出（LIFO）的栈。

**这个想法是，C和Lua都知道栈的规则，只要它们都遵守这些规则，它们就可以共存和交流。**



## 栈的使用过程

一般来说，你可以把栈看作是一种共享的数据存储机制。

它通常的工作方式是，你在C语言中把一些值推到栈中，

然后，你调用一个Lua函数，把控制权交给Lua运行时。

运行时将这些值从栈中弹出，

相关的函数完成它的工作并将返回值推回栈。

然后控制权被交还给C，C将返回值从栈中弹出。

![img](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/da63995dc0fb4320a97454ba5e9ef2b9~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.image)





# C语言加载并运行lua脚本

1、创建一个lua虚拟机

```
lua_State *L = luaL_newstate();
```

2、加载lua库。这个是把lua的标准库都加载进来。

```
lua_openlibs(L);
```

3、加载lua脚本

```
int status = luaL_loadfile(L, "test.lua");
if (status == LUA_OK) {
	// load ok
	int ret = lua_pcall(L, 0, LUA_MULTRET, 0);
} else {
	myloge("can not load the lua file");
}
```

完整代码：

```
//都是要包含这3个头文件的。
#include "lauxlib.h"
#include "lua.h"
#include "lualib.h"

//编译：gcc 01-load-lua.c -I/usr/include/lua5.3 -llua5.3
int main(int argc, char const *argv[])
{
    lua_State *L = luaL_newstate();//创建一个lua虚拟机
    //然后要打开lua自带的所有标准库。
    luaL_openlibs(L);
    //然后读取执行文件。
    int status = luaL_loadfile(L, "helloworld.lua");
    int ret = 0;
    if (status == LUA_OK) {
        printf("load lua file ok\n");
        ret = lua_pcall(L, 0, 0, 0);
        printf("lua_pcall ret:%d\n", ret);
    } else {
        printf("load lua file fail\n");
    }
    lua_close(L);
    return 0;
}

```



# C语言调用lua的一个函数

我们有个这样lua函数：

```
function lua_add(a, b)
	return a+b
end
```

现在我们要在C语言里调用这个函数。

```
int callLuaAdd(lua_State *L, int x, int y)
{
	int sum;
	//先拿到名字为lua_add的lua函数。并把它放到栈顶。
	lua_getglobal(L, "lua_add");
	//往lua栈里push 2个参数。
	//从左往右的顺序。
	lua_pushnumber(L, x);
	lua_pushnumber(L, y);
	//调用函数，参数里的2表示参数的个数，1是表示返回值的个数。
	lua_call(L, 2, 1);
	//然后就可以读取放在栈顶的结果了。
	sum = lua_tointeger(L, -1);//-1表示栈顶。
	//最后把结果从栈顶pop掉。
	lua_pop(L, 1);//1表示1个结果。
	return sum;
}
```

# C语言操作lua全局变量

从C语言读写Lua变量非常容易。

正因为如此，Lua经常被用作配置语言或保存和加载程序的状态。

Lua运行时将为你解析和解释文件，消除了手动解析的需要。

**而Lua的语法很适合这类任务。**

在本节中，我们将探讨如何读取作为配置数据的Lua变量。

读取一个全局变量分三步进行。

你必须使用该变量的名称来把它的值推到栈上。

**一旦进入栈，该值就可以被C语言读取。**

在C语言中得到该值后，通过删除旧的副本来清理栈。

你可以使用`lua_getglobal (lua_State*, const char *)`函数将一个全局变量按名称推入栈。

`lua_getglobal`函数使用全局变量的名称，将其值留在栈中。要在C语言中读取这个值，你必须使用`lua_to`函数之一，比如`lua_tonumber`或`lua_tostring`。这些函数在本文的 "从栈中读取 "一节中讨论过。一旦你在C语言中得到了变量的值，通过调用`lua_pop`来清理栈。



让我们看一个如何从Lua中读取变量到C语言的简单例子。

考虑一下我们创建一个游戏角色的用例。

我们想把该角色的属性存储在一个外部配置文件中，以便于编辑。

这个属性文件将看起来像这样：



上面的示例代码在任何内容被推送到栈之前获得了栈的基本索引，然后使用该基本索引的偏移量来读取数值。

你永远不应该假设栈是空的——不要硬编码索引。

**相反，始终使用相对于已知偏移量的索引。**

# lua调用C函数

把一个C函数包装成lua要求的格式。

```
int LuaVec3Magnitude(lua_State* L) {
    double x = lua_tonumber(L, 3);
    double y = lua_tonumber(L, 2);
    double z = lua_tonumber(L, 1);
    
    lua_pop(L, 3);
    double dot = x * x + y * y + z * z;
    if (dot == 0.0) {
    	lua_pushnil(L);
    }else {
    	lua_pushnumber(L, sqrt(dot));
    } 
    return 1;
}
```

# lua虚拟栈交互流程

```
int lua_gettop(L);//返回栈顶索引，也就是栈的长度。
void lua_settop(L, i);
void lua_pushvalue(L, i);//将索引i上的值的副本push到栈顶。
void lua_remove(L, i);//
void lua_insert(L, i);//pop栈顶元素，并插入索引i的位置。
void lua_replace(L, i);//pop栈顶元素，并替换索引i的位置的值
```

在lua的C API的函数文档说明后面，一般有一个这样的说明：

```
[-o, +p, x]
```

```
o
	指的是这个函数会从栈上pop多少个元素
+p
	指的是这个函数把push多少个元素到栈上。
x
	这个函数是否会抛出错误。
	-：表示不会抛出错误。
	e：可能抛出错误
	v：可能抛出有意义的错误。
	m：会抛出内存错误或错误执行gc。
```





参考资料

1、

这篇文章非常好。

https://chenanbao.github.io/2018/07/28/Lua%E8%99%9A%E6%8B%9F%E6%A0%88%E4%BA%A4%E4%BA%92%E6%B5%81%E7%A8%8B/

# 保证栈平衡

在Lua C API中，栈操作是核心功能之一，用于在C代码和Lua运行时之间传递数据。栈平衡指的是在调用API函数后，确保栈的状态（如栈顶位置）符合预期，避免栈溢出或遗留多余数据。以下我将通过示例详细说明Lua C API的栈操作，并分析如何保证栈平衡。

---

### 1. Lua C API栈的基本概念

- **栈结构**：`lua_State`中的栈是一个`TValue`数组，`L->top`指向栈顶。
- **索引**：
  - 正索引：从当前函数（`ci->func`）开始计数。
  - 负索引：从栈顶（`L->top`）向下计数。
- **平衡原则**：
  - 推送（push）操作增加栈顶。
  - 弹出（pop）操作减少栈顶。
  - 调用函数时，参数和返回值需要匹配。

---

### 2. 栈操作示例

以下是几个常见的栈操作示例，展示如何使用API并保持栈平衡。

#### 示例1：推送和弹出值
```c
void example_push_pop(lua_State *L) {
    // 初始栈顶
    int top = lua_gettop(L);

    // 推送几个值
    lua_pushnumber(L, 42);     // 栈: [..., 42]
    lua_pushstring(L, "hello"); // 栈: [..., 42, "hello"]
    lua_pushnil(L);            // 栈: [..., 42, "hello", nil]

    // 检查栈顶变化
    printf("Stack size after push: %d\n", lua_gettop(L) - top); // 输出 3

    // 恢复栈平衡
    lua_settop(L, top);        // 栈: [...]
    printf("Stack size after pop: %d\n", lua_gettop(L) - top);  // 输出 0
}
```
- **操作**：
  - `lua_push*`增加栈顶，每次调用`api_incr_top(L)`。
  - `lua_settop`直接设置栈顶，移除多余值。
- **栈平衡**：通过记录初始`top`并在结束时恢复，确保不遗留数据。

---

#### 示例2：调用Lua函数
```c
void example_call_lua_function(lua_State *L) {
    int top = lua_gettop(L);

    // 获取全局函数 "print"
    lua_getglobal(L, "print");     // 栈: [..., print]
    
    // 推送参数
    lua_pushstring(L, "Hello from C!"); // 栈: [..., print, "Hello from C!"]
    
    // 调用函数：1个参数，0个返回值
    lua_call(L, 1, 0);            // 栈: [...]

    // 检查栈平衡
    lua_assert(lua_gettop(L) == top);
}
```
- **操作**：
  - `lua_getglobal`推送函数。
  - `lua_pushstring`推送参数。
  - `lua_call`消耗函数和参数，不保留返回值（`nresults=0`）。
- **栈平衡**：
  - 初始栈顶为`top`，调用后栈顶回到`top`。
  - `lua_call`自动清理参数和函数，确保平衡。

---

#### 示例3：从Lua表中读取和写入
```c
void example_table_operations(lua_State *L) {
    int top = lua_gettop(L);

    // 创建新表
    lua_createtable(L, 0, 1);     // 栈: [..., {}]

    // 设置字段 t["key"] = 100
    lua_pushstring(L, "key");     // 栈: [..., {}, "key"]
    lua_pushinteger(L, 100);      // 栈: [..., {}, "key", 100]
    lua_settable(L, -3);          // 栈: [..., {}]

    // 获取字段 t["key"]
    lua_getfield(L, -1, "key");   // 栈: [..., {}, 100]
    printf("Value: %d\n", (int)lua_tointeger(L, -1));
    lua_pop(L, 1);                // 栈: [..., {}]

    // 恢复栈平衡
    lua_settop(L, top);           // 栈: [...]
}
```
- **操作**：
  - `lua_createtable`推送新表。
  - `lua_settable`消耗键值对，栈顶不变。
  - `lua_getfield`推送字段值，需手动弹出。
- **栈平衡**：
  - 每次推送后，若不使用值，则通过`lua_pop`或`lua_settop`清理。
  - 最后恢复初始栈顶。

---

#### 示例4：保护模式调用
```c
void example_pcall(lua_State *L) {
    int top = lua_gettop(L);

    // 获取全局函数 "error"
    lua_getglobal(L, "error");    // 栈: [..., error]
    lua_pushstring(L, "test error"); // 栈: [..., error, "test error"]

    // 保护调用：1个参数，0个返回值，无错误处理函数
    int status = lua_pcall(L, 1, 0, 0); // 栈: [..., <error message if failed>]
    if (status != LUA_OK) {
        printf("Error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);            // 栈: [...]
    }

    // 检查栈平衡
    lua_assert(lua_gettop(L) == top);
}
```
- **操作**：
  - `lua_pcall`调用函数，失败时推送错误消息。
  - 成功时栈恢复，失败时需手动弹出错误。
- **栈平衡**：
  - 检查`status`，若出错则清理错误消息。
  - 确保栈顶回到初始状态。

---

### 3. 如何保证栈平衡

Lua C API通过以下机制和实践保证栈平衡：

#### API设计
1. **明确的参数和返回值处理**：
   - `lua_call`和`lua_pcall`自动消耗参数，按`nresults`调整返回值。
   - 如`lua_settable`消耗键值对，不改变栈顶。
2. **栈检查**：
   - `api_checknelems`确保栈上有足够元素。
   - `lua_checkstack`预分配栈空间，避免溢出。

#### 编程实践
1. **记录初始栈顶**：
   - 使用`lua_gettop`保存初始状态，最后恢复。
   ```c
   int top = lua_gettop(L);
   // 操作
   lua_settop(L, top);
   ```
2. **手动清理**：
   - 对推送但不使用的值，使用`lua_pop`或`lua_remove`。
   ```c
   lua_pushnumber(L, 42);
   lua_pop(L, 1); // 移除42
   ```
3. **检查返回值数量**：
   - 调用函数时，指定`nresults`，避免多余返回值。
   - 使用`LUA_MULTRET`时，需调整栈顶。
4. **错误处理**：
   - `lua_pcall`失败时，处理错误对象并清理。

#### 示例：复杂操作的栈平衡
```c
void example_complex(lua_State *L) {
    int top = lua_gettop(L);

    // 创建表并设置值
    lua_createtable(L, 0, 0);     // 栈: [..., {}]
    lua_pushinteger(L, 1);        // 栈: [..., {}, 1]
    lua_pushstring(L, "one");     // 栈: [..., {}, 1, "one"]
    lua_settable(L, -3);          // 栈: [..., {}]

    // 调用函数处理表
    lua_getglobal(L, "pairs");    // 栈: [..., {}, pairs]
    lua_pushvalue(L, -2);         // 栈: [..., {}, pairs, {}]
    lua_call(L, 1, 3);            // 栈: [..., {}, iter, state, firstkey]

    // 遍历并清理
    while (lua_next(L, -3)) {     // 栈: [..., {}, iter, state, key, value]
        lua_pop(L, 1);            // 栈: [..., {}, iter, state, key]
    }                             // 栈: [..., {}, iter, state]

    lua_pop(L, 3);                // 栈: [...]
    lua_assert(lua_gettop(L) == top);
}
```
- **栈平衡**：
  - `lua_call`返回3个值（迭代器、状态、第一个键）。
  - `lua_next`推送键值对，循环结束时清理。
  - 最后弹出多余值，恢复初始栈顶。

---

### 4. 注意事项

- **栈溢出**：调用`lua_checkstack`确保空间。
- **伪索引**：如`LUA_REGISTRYINDEX`，不影响栈顶。
- **垃圾回收**：推送对象后调用`luaC_checkGC`，但不影响栈平衡。
- **多返回值**：使用`LUA_MULTRET`时，手动调整栈顶。

---

### 总结

Lua C API的栈操作通过明确的API语义（如`lua_call`的自动清理）和编程实践（如记录栈顶、手动弹出）保证栈平衡。示例展示了从简单推送、函数调用到表操作的平衡方法。关键是理解每个API对栈的影响，并在操作结束时恢复初始状态。如果你有具体场景想分析，可以告诉我，我会进一步举例说明！

# 参考资料

1、

https://www.cnblogs.com/lsgxeva/p/11158228.html

2、

https://juejin.cn/post/6995343033977798670