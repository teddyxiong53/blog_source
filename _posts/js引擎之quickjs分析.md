---
title: js引擎之quickjs分析
date: 2023-04-27 10:31:11
tags:
	- quickjs
---

--

本来不打算看这个的，但是看了jerryscript，那个代码也看起来非常繁琐。

而这个看起来就干净整洁很多。所以还是研究一下。

# 资料收集

知乎topic

https://www.zhihu.com/topic/21191363/hot

# 重要概念

## JSRuntime和JSContext关系

在QuickJS中，`JSRuntime`和`JSContext`是两个核心概念，用于管理JavaScript运行时的不同层面。它们之间的关系如下：

1. **JSRuntime**：
   - `JSRuntime`是QuickJS中的最高级别概念，代表一个JavaScript运行时环境。
   - ==一个`JSRuntime`可以包含多个`JSContext`，并且它们之间共享一些全局资源，如原型对象和标准库函数。==
   - `JSRuntime`通常在应用程序初始化时创建，然后在整个应用程序的生命周期内保持不变。这允许多个`JSContext`在同一个运行时环境内执行JavaScript代码，共享运行时环境的资源。

2. **JSContext**：
   - `JSContext`代表一个JavaScript执行上下文，其中可以执行JavaScript代码。
   - ==每个`JSContext`都是相对独立的，拥有自己的JavaScript对象、变量、堆栈等==。这意味着在一个`JSContext`中定义的变量和函数不会自动在其他`JSContext`中可见。
   - `JSContext`通常用于隔离不同部分的JavaScript代码，以确保它们不会相互干扰。例如，你可以在一个`JSContext`中执行一个脚本，然后在另一个`JSContext`中执行另一个脚本，它们之间不会相互影响。

总结来说，`JSRuntime`表示JavaScript的运行时环境，可以包含多个`JSContext`，而每个`JSContext`代表一个独立的JavaScript执行上下文。`JSRuntime`通常在应用程序级别创建和管理，而`JSContext`则用于在不同的上下文中执行JavaScript代码，以实现隔离和分离不同部分的代码逻辑。这种分层的结构有助于确保代码的隔离性和可维护性。



新建：

```
    rt = JS_NewRuntime();
    ctx = JS_NewContext(rt);
```

## JSShape

QuickJS中的`JSShape`是JavaScript对象的内部表示之一，

==用于跟踪对象的属性和属性的特征，==

这包括属性的名称、值、标志等。

`JSShape` 是 QuickJS 引擎用于实现对象属性存储和访问的关键数据结构之一。



具体来说，`JSShape` 存储了以下信息：

1. **属性列表**：包含对象的所有属性。这些属性通常是对象的成员变量，可以包括实例属性和原型属性。属性按名称排序，这有助于提高属性查找的效率。

2. **属性特征**：每个属性都有与之关联的特征，包括属性的标志（例如，是否可写、是否可枚举、是否可配置等）和属性的值。

`JSShape` 的存在使 QuickJS 引擎能够高效地执行属性查找和访问操作。这对于 JavaScript 对象的内部实现非常重要，因为它们可以包含大量属性，且访问属性是 JavaScript 中的常见操作。

需要注意的是，`JSShape` 是 QuickJS 引擎内部使用的数据结构，通常不会直接由 JavaScript 代码访问。开发者主要与 JavaScript 对象和属性交互，而引擎会负责管理底层的 `JSShape` 数据结构以支持这些操作。



## JSModuleDef

在 QuickJS 中，`JSModuleDef` 是一个数据结构，用于表示 JavaScript 模块（ES6 模块）的定义。

它包含了模块的各种属性和信息，

以便在 QuickJS 引擎中加载、解析和执行模块。

`JSModuleDef` 具有以下属性和功能：

1. **`name`（模块名称）**：表示模块的名称，通常对应于模块的文件路径或标识符。

2. **`func`（模块函数）**：一个指向模块执行函数的指针。模块执行函数是 JavaScript 模块的入口点，用于初始化模块的导出对象。

3. **`native_module`（原生模块标志）**：一个标志，指示模块是否为原生模块。原生模块通常是由 C/C++ 编写的模块，通过 QuickJS 的 C API 注册并加载。

4. **`import_list`（导入列表）**：一个列表，包含了模块导入的信息。这些信息通常包括导入的模块名称和导入的变量或名称空间。

5. **`export_list`（导出列表）**：一个列表，包含了模块导出的信息。这些信息指定了哪些变量或值将在模块外部可见。

6. **`import_meta`（导入元数据）**：一个指向包含有关模块导入的元数据的 `JSObject` 的指针。这可以包含有关模块的额外信息，如其来源等。

`JSModuleDef` 数据结构允许 QuickJS 引擎加载和执行模块，并管理模块之间的依赖关系。在应用程序或库中使用 QuickJS 时，你可以创建和注册自定义模块定义，以便在 JavaScript 代码中导入和使用它们。这对于将外部功能模块化并在 JavaScript 中使用非常有用。

通常，模块定义是通过 QuickJS 的 C API 创建并注册的，然后可以在 JavaScript 代码中通过 `import` 语句导入。这种模块系统的支持使 QuickJS 成为一个强大的嵌入式 JavaScript 引擎，可以与应用程序和库集成以支持模块化开发。

# qjsc

`qjsc` 是 QuickJS 提供的一个命令行工具，

==用于将 JavaScript 代码编译成 QuickJS 字节码，==

以便稍后执行。

它的基本用法如下：

```
qjsc [选项] [-o 输出文件] 输入文件
```

其中，`[选项]` 包括各种编译选项，`-o` 用于指定输出文件，而 `输入文件` 是要编译的 JavaScript 源文件。

以下是一些常见的 `qjsc` 选项和用法示例：

- `-o 输出文件`：指定输出文件的名称。
- `-c`：生成 C 代码，使你可以将 QuickJS 字节码嵌入到 C/C++ 应用程序中。
- `-M`：将多个 JavaScript 模块编译成一个字节码文件。
- `-m`：指定生成的字节码文件的模块名称。
- `-e`：指定要编译的 JavaScript 文件。
- `-t`：在生成的 C 代码中包括标准输入/输出处理。
- `-x`：生成源映射文件，用于调试。
- `-v`：增加编译的详细度，输出更多信息。

示例用法：

1. 编译单个 JavaScript 文件为 QuickJS 字节码文件：

   ```bash
   qjsc -o output.qjsc input.js
   ```

2. 生成 C 代码，以便将 QuickJS 字节码嵌入到 C/C++ 应用程序中：

   ```bash
   qjsc -o output.c -c input.js
   ```

3. 将多个 JavaScript 模块编译成一个字节码文件：

   ```bash
   qjsc -o output.qjsc -M -m main_module input.js
   ```

4. 生成源映射文件以进行调试：

   ```bash
   qjsc -o output.qjsc -x input.js
   ```

这些示例涵盖了一些常见的 `qjsc` 用法，但你可以根据你的项目需求使用其他选项。

`qjsc` 是 QuickJS 引擎的一个有用工具，允许你将 JavaScript 代码编译成字节码，以提高执行效率或在嵌入式系统中使用。

可以输出这些类型：

```
typedef enum {
    OUTPUT_C,
    OUTPUT_C_MAIN,
    OUTPUT_EXECUTABLE,
} OutputTypeEnum;

```

输出的名字：

```
    if (!out_filename) {
        if (output_type == OUTPUT_EXECUTABLE) {
            out_filename = "a.out";
        } else {
            out_filename = "out.c";
        }
    }
```

默认就是OUTPUT_EXECUTABLE。

# quickjs自定义一个C语言module

要在 QuickJS 中自定义一个 C 语言模块，你需要完成以下步骤：

1. **编写 C 代码**：首先，你需要编写包含模块功能的 C 代码。这可以是你的模块的实际实现，可以包括函数、变量和其他功能。例如，假设你要创建一个简单的模块，用于计算两个数字的和，你的 C 代码可能如下所示：

   ```c
   #include "quickjs.h"
   
   static JSValue my_add_func(JSContext *ctx, JSValueConst this_val, int argc, JSValueConst *argv) {
       if (argc != 2) {
           return JS_ThrowTypeError(ctx, "Two arguments are required");
       }
       int a, b;
       JS_ToInt32(ctx, &a, argv[0]);
       JS_ToInt32(ctx, &b, argv[1]);
       return JS_NewInt32(ctx, a + b);
   }
   
   static const JSCFunctionListEntry my_module_funcs[] = {
       JS_CFUNC_DEF("add", 2, my_add_func),
       JS_PROP_END
   };
   
   int js_init_module_my_module(JSContext *ctx, JSModuleDef *m) {
       JS_SetModuleExportList(ctx, m, my_module_funcs);
       return 0;
   }
   ```

   这个示例代码定义了一个名为 "my_module" 的模块，包含一个名为 "add" 的函数，用于将两个数字相加。在模块初始化函数 `js_init_module_my_module` 中，使用 `JS_SetModuleExportList` 来导出模块的函数。

2. **注册模块**：在 QuickJS 中注册你的模块，以便在 JavaScript 代码中导入和使用。你可以在 QuickJS 初始化时注册模块。示例如下：

   ```c
   JSModuleDef *m;
   JSContext *ctx;
   
   // 创建模块定义
   m = JS_NewCModule(ctx, "my_module", js_init_module_my_module);
   
   // 注册模块
   JS_AddModuleExportList(ctx, m);
   ```

   在上述示例中，首先使用 `JS_NewCModule` 创建一个模块定义，然后使用 `JS_AddModuleExportList` 注册模块，以便它在 JavaScript 代码中可用。

3. **使用 JavaScript 导入模块**：在你的 JavaScript 代码中，你可以使用 `import` 语句来导入你的自定义模块。例如：

   ```javascript
   import { add } from 'my_module';
   const result = add(5, 3);
   console.log(result); // 输出 8
   ```

这样，你的自定义 C 模块就可以在 QuickJS 中使用了。你可以根据你的需求扩展和自定义模块，以添加更多功能。当你的 C 模块在 QuickJS 中注册并导入后，你可以像使用任何其他 JavaScript 模块一样使用它。

## 官方的fib例子分析

examples\fib.c

## 模块的导入过程分析

```
js_module_loader
	js_module_loader_so
		dlsym(hd, "js_init_module");
			然后这个js_init_module在每个模块定义里有实现。
```

## 接口分析

可以看到接口非常简单清晰。

JS_NewCModule



# QuickJS中的atom设计

QuickJS源码中的atom（32位无符号整数）可以认为是字符串（覆盖的范围包括JS中的关键字、标识符、Symbol等）的别名。

其中最高位为1的atom代表的是整数，为0代表字符串，

所以atom可以表示的整数和字符串个数都是(2^31)-1个。

==引入atom的目的是为了减少内存使用（重复的字符串只存储一次）和提高字符串比较速度（在转换成atom之后，只需要比较两个atom的数值是否一致）。==

其中内置了大概200多个常驻的atom（包括关键字、JS中常见的标识符、JS中内置的Symbol），

在创建runtime的时候就被添加进去了，这些atom不会被清除。

之后在解析JS代码过程中添加的atom，会根据引用计数进行清除。



字符串转换为atom的步骤如下（如果是Symbol，转化为atom就比较简单，只需要往`atom_array`添加并使用其index作为Symbol的atom值即可，并不涉及到`atom_hash`的添加）：

1. 根据字符串的ascii码和atom类型，按照一定规则计算出一个hash值`hash_index`（32位无符号整数）
2. 获取`atom_array`空闲位置`free_atom_index`，然后将字符串的指针添加进去（`atom_array[free_atom_index]=s`。如果`atom_array`空间不足，则还会涉及到`atom_array`的扩充，以3/2的倍数扩充，注意扩充前后已经存储的atom对应的`atom_index`保持不变）
3. 将原来`atom_hash`的`hash_index`位置对应的`atom_index`存放到`s.hash_next`中，再将其修改为`free_atom_index`（这一步如果atom的个数大于`atom_hash`可以存放的数量的两倍，则将`atom_hash`扩充到原来的2倍容量）
4. 将第二步添加到`atom_array`中的位置（`atom_index`）作为该字符串的atom值，在后续的程序中使用



https://zhuanlan.zhihu.com/p/320599997

# 以quickjs分析setTimeout

只要搞明白这个问题，你就已经能自己实现 Event Loop 和 JS 运行时了。

我比较熟悉 QuickJS 引擎，写过两篇相关的教学文章，

下面复读下其中关于 setTimeout 的部分吧。



实际上由于一些历史原因[[1\]](#ref_1)，[ECMA-262](https://www.zhihu.com/search?q=ECMA-262&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540}) 规范里只定义了 Run to Completion 的部分，

并未包含任何对平台 API 的约定。

我们可以认为，狭义的 JS 引擎就是对这部分规范的实现。

==每次[解释执行](https://www.zhihu.com/search?q=解释执行&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540}) JS 脚本，==

==就相当于在 C 语言里调用一个名为 `JS_Eval` 然后同步完成的[函数](https://www.zhihu.com/search?q=函数&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})。==

而 setTimeout 需要的显然不只是单纯进行 `JS_Eval` 的能力，

**它的调用形式是反转过来的，要求在未来自动触发一次对 JS 函数的解释执行，亦即所谓的 callback（回调）**。

从 JS 运行时开发者的视角看来，

==只要走通了 setTimeout 这个最经典的回调例子，==

==就能够支撑起整个事件驱动应用的 Event Loop 架构了。==

因为 UI 应用中对按钮 onclick 等事件的支持，

其实也不外乎是在相应原生事件到来时，去执行相应的[回调函数](https://www.zhihu.com/search?q=回调函数&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})，

其原理是完全一致的。

==这方面 QuickJS 自带的 [libc](https://www.zhihu.com/search?q=libc&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540}) 运行时里有个非常简单优雅的实现案例，==

不妨直接看看 [Fabrice Bellard](https://www.zhihu.com/question/28388113) 大神代码的「实现机理」吧。

QuickJS 引擎编译时默认会内置 `std` 和 `os` 两个原生模块，能这样用 setTimeout 来支持异步：

```js
import { setTimeout } from "os";

setTimeout(() => { /* ... */ }, 0);
```



这个 `"os"` 模块就来自上面说的 libc 运行时，

==具体代码不属于引擎本体，==

==而是位于 `quickjs-libc.c` 文件里，==

也是通过标准化的 QuickJS API 挂载上去的原生模块。

这个原生的 setTimeout 函数是怎么实现的呢？

它的源码其实很少，像这样：

```c
static JSValue js_os_setTimeout(JSContext *ctx, JSValueConst this_val,
                                int argc, JSValueConst *argv)
{
    int64_t delay;
    JSValueConst func;
    JSOSTimer *th;
    JSValue obj;

    func = argv[0];
    if (!JS_IsFunction(ctx, func))
        return JS_ThrowTypeError(ctx, "not a function");
    if (JS_ToInt64(ctx, &delay, argv[1]))
        return JS_EXCEPTION;
    obj = JS_NewObjectClass(ctx, js_os_timer_class_id);
    if (JS_IsException(obj))
        return obj;
    th = js_mallocz(ctx, sizeof(*th));
    if (!th) {
        JS_FreeValue(ctx, obj);
        return JS_EXCEPTION;
    }
    th->has_object = TRUE;
    th->timeout = get_time_ms() + delay;
    th->func = JS_DupValue(ctx, func);
    list_add_tail(&th->link, &os_timers);
    JS_SetOpaque(obj, th);
    return obj;
}
```

可以看出，这个 setTimeout 的实现中，并没有任何[多线程](https://www.zhihu.com/search?q=多线程&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})或 poll 的操作，

只是把一个存储 timer 信息的结构体通过 `JS_SetOpaque` 的方式，

挂到了最后返回的 JS 对象上而已，

是个非常简单的同步操作。

因此，就和调用原生 fib 函数一样地，**在 eval 执行 JS 代码时，遇到 setTimeout 后也是同步地执行一点 C 代码后就立刻返回，没有什么特别之处**。



但为什么 setTimeout 能实现异步呢？

关键在于 eval 之后，我们就要启动 Event Loop 了。

熟悉 QuickJS 的朋友知道，QuickJS 支持直接把 JS 编译成[可执行文件](https://www.zhihu.com/search?q=可执行文件&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})，

这时候它会生成并编译一份标准的 C 代码，

在里面的 `main` 函数里调用 QuickJS 的 API 来启动 Event Loop。

我们可以通过 `qjs -c hello.js` 这行命令 dump 出相应的 C 文件，

直接看到启动 Event Loop 时的相关[逻辑](https://www.zhihu.com/search?q=逻辑&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})：

```
// ...
int main(int argc, char **argv)
{
  // ...
  // eval JS 字节码
  js_std_eval_binary(ctx, qjsc_hello, qjsc_hello_size, 0);
  // 启动 Event Loop
  js_std_loop(ctx);
  // ...
}
```

因此，eval 后的这个 `js_std_loop` 就是真正的 Event Loop，而它的源码则更是简单得像是[伪代码](https://www.zhihu.com/search?q=伪代码&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})一样：

```
/* main loop which calls the user JS callbacks */
void js_std_loop(JSContext *ctx)
{
    JSContext *ctx1;
    int err;

    for(;;) {
        /* execute the pending jobs */
        for(;;) {
            err = JS_ExecutePendingJob(JS_GetRuntime(ctx), &ctx1);
            if (err <= 0) {
                if (err < 0) {
                    js_std_dump_error(ctx1);
                }
                break;
            }
        }

        if (!os_poll_func || os_poll_func(ctx))
            break;
    }
}
```

这不就是在双重的死循环里先执行掉所有的 Job（也就是 Promise 带来的[微任务](https://www.zhihu.com/search?q=微任务&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})），

然后调 `os_poll_func` 吗？

可是，[for 循环](https://www.zhihu.com/search?q=for 循环&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})不会吃满 CPU 吗？

这是个[前端](https://www.zhihu.com/search?q=前端&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})同学们容易误解的地方：

**在原生开发中，进程里即便写着个死循环，也未必始终在前台运行，可以通过[系统调用](https://www.zhihu.com/search?q=系统调用&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})将自己挂起**。



例如，一个在死循环里通过 sleep 系统调用不停休眠一秒的进程，

就只会每秒被系统执行一个 tick，其它时间里都不占资源。

而这里的 `os_poll_func` 封装的，

就是原理类似的 poll 系统调用（准确地说，用的其实是 [select](https://link.zhihu.com/?target=https%3A//man7.org/linux/man-pages/man2/select.2.html)），

从而可以借助[操作系统](https://www.zhihu.com/search?q=操作系统&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})的能力，

使得只在【[定时器](https://www.zhihu.com/search?q=定时器&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})触发、[文件描述符](https://www.zhihu.com/search?q=文件描述符&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})读写】等事件发生时，

让进程回到前台执行一个 tick，把此时应该运行的 JS 回调跑一遍，而其余时间都在后台挂起。

在这条路上继续走下去，就能以经典的[异步非阻塞方式](https://www.zhihu.com/search?q=异步非阻塞方式&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})来实现整个运行时了。



鉴于 `os_poll_func` 的代码较长，这里只概括下它与 timer 相关的工作：

- 如果上下文中存在 timer，将到期 timer 对应的回调都执行掉。
- 找到所有 timer 中最小的时延，用 select 系统调用将自己挂起这段时间。



这样，setTimeout 的「底层原理」就非常容易说清楚了：

**先在 eval 阶段简单设置一个 timer 结构，然后在 Event Loop 里用这个 timer 的参数去调用操作系统的 poll，从而在被唤醒的下一个 tick 里把到期 timer 对应的 JS 回调执行掉就行**。





参考资料

1、

https://www.zhihu.com/question/463446982/answer/1927497540

# 把quickjs改造为一个运行时

https://zhuanlan.zhihu.com/p/104333176

# quickjs剖析系列文章



https://www.zhihu.com/column/c_1337176691518140416

1、

https://blog.csdn.net/Innost/article/details/98491709

2、

https://blog.csdn.net/wsyzxxn9/article/details/114116614

3、

https://blog.csdn.net/HaaSTech/article/details/120948020