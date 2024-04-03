---
title: js之微型解释器elk研究
date: 2022-07-19 19:52:07
tags:
	- js

---

--

代码在这里：

https://github.com/cesanta/elk

elk.c文件只有1000行左右。写得非常紧凑。值得认真学习掌握。

但是编译系统不是很完善。

我看examples/cmdline这个例子。

里面支持了require命令。

编译：

```
cd examples/cmdline
cp ../../elk* ./
# 修改main.c，加上#include "elk.c"
# 编译
gcc main.c -lm
```

然后可以运行a.out。

写一个aaa.js。内容如下：

```
let func1 = function() {
	print("hello 1");
}
```

必须要这么写。下面的写法不行，会提示解析错误。

```
function func1() {
	print("hello 1");
}
```

然后运行：

```
./a.out -e "require(\"aaa.js\");func1();"
```

就可以正常解析这个文件了。

其实我这个有点多此一举了。

在main.c的头部的注释里，有说明怎么编译和测试的。

```
// Example Elk integration. Demontrates how to implement "require".
// Create file "api.js" with the following content:
//  ({
//    add : function(a, b) { return a + b; },
//    mul : function(a, b) { return a * b; },
//  })
//
// Compile main.c and run:
//   $ cc main.c ../../elk.c -I../.. -o cli
//   $ ./cli 'let math = require("api.js"); math.mul(2,3);'
//   6
//   Executed in 0.663 ms. Mem usage is 3% of 8192 bytes.
```



但是elk的使用场景是什么呢？

单片机？

# esp32例子分析

这个是全链路的，比较完整。

总体的逻辑是：

1、在板端运行一个webserver（基于mongoose库），程序框架的arduino的。使用了freertos。

2、webserver支持http和ws这2种协议。

协议升级是这里做的：

```
static void cb(struct mg_connection *c, int ev, void *ev_data, void *fn_data) {
  if (ev == MG_EV_HTTP_MSG) {
    struct mg_http_message *hm = (struct mg_http_message *) ev_data;
    if (mg_http_match_uri(hm, "/ws")) {
      mg_ws_upgrade(c, hm, NULL);
    } else {
      mg_http_reply(c, 302, "Location: http://elk-js.com/\r\n", "");
    }
  } else if (ev == MG_EV_WS_MSG) {
```

3、websocket上使用了jsonrpc。执行收到的js脚本内容。并把执行结果返回。

# 提交历史分析

第一个提交是2019年10月7日。

最开始是闭源的。以libelk.a和elk.h的方式提供。

第二次提交增加了unittest。

2021年5月2日，把之前发布的a文件都去掉了。

然后开源了。

# 对外接口分析

一个跟C语言对接的实现接口是这样：

```
static jsval_t gpio_write(struct js* js, jsval_t *args, int nargs)
{
    //先检查参数。
    bool ret ;
    ret = js_chkargs(args, nargs, "dd");
    if (!ret) {
        return js_mkerr(js, "bad args");
    }
    int pin = js_getnum(args[0]);
    int val = js_getnum(args[1]);
    printf("write pin:%d value:%d\n", pin ,val);
    return js_mknull();
}
```

关键是这个参数的检查字符串是怎么定义的。

```
只有4个字母的情况。
b：bool
d：数字
s：字符串
j：js对象。
```

# 用elk+mongoose实现一个精简的nodejs

官方代码下的esp32js下面就是实现了这个功能。

可以简单分析一下。

## 我要用自己的js解释器实现一个最小的nodejs运行时，有哪些接口是需要实现的？

要实现一个最小的 Node.js 运行时，你需要实现以下基本接口和功能：

1. **模块加载器（Module Loader）**：
   - 支持 `require()` 函数，用于加载模块。
   - 实现模块缓存，以避免重复加载相同的模块。

2. **全局对象（Global Object）**：
   - 实现类似于 `global` 对象的全局对象，使其包含 Node.js 中的常用全局函数和对象，比如 `process`、`console` 等。

3. **文件系统访问（File System Access）**：
   - 实现类似于 Node.js 的 `fs` 模块，提供对文件系统的访问和操作功能，包括文件读写、目录操作等。

4. **网络通信（Network Communication）**：
   - 实现类似于 Node.js 的 `http` 或 `https` 模块，提供基本的 HTTP 或 HTTPS 服务器和客户端功能。

5. **事件驱动（Event-Driven）**：
   - 实现事件驱动的机制，比如类似于 Node.js 的 `EventEmitter`，用于处理事件和回调函数。

6. **异步 I/O（Asynchronous I/O）**：
   - 支持非阻塞 I/O 操作，使得程序可以异步地处理文件读写、网络请求等操作，而不会阻塞主线程。

7. **定时器（Timers）**：
   - 实现类似于 `setTimeout()`、`setInterval()` 等定时器功能，用于执行延迟或周期性任务。

8. **进程管理（Process Management）**：
   - 提供类似于 `process` 模块的功能，包括获取命令行参数、退出程序等。

9. **错误处理（Error Handling）**：
   - 实现错误处理机制，能够捕获并处理运行时错误，以及提供友好的错误提示和日志输出。

10. **模块系统（Module System）**：
    - 实现模块系统，使得可以按照 Node.js 的模块规范加载和导出模块。

以上是最基本的接口和功能，你可以根据需求和实现难度逐步完善和扩展这个运行时环境。

### 实现require

```
// Example Elk integration. Demontrates how to implement "require".
// Create file "api.js" with the following content:
//  ({
//    add : function(a, b) { return a + b; },
//    mul : function(a, b) { return a * b; },
//  })
//
// Compile main.c and run:
//   $ cc main.c ../../elk.c -I../.. -o cli
//   $ ./cli 'let math = require("api.js"); math.mul(2,3);'
//   6
//   Executed in 0.663 ms. Mem usage is 3% of 8192 bytes.
```

### 异步回调怎么实现



# 对elk的理解

主要用途还是要可动态传递控制逻辑到板端。

主要是对C接口进行调用组合。



# 把elk理解消化后实现一个python版本

主要是token解析。

也可以尝试自己扩展一些语法元素进去。



# elk绑定lvgl

