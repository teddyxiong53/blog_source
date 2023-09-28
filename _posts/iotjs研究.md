---
title: iotjs研究
date: 2021-11-19 19:16:33
tags:
	- nodejs

---

--

jerryscript + iotjs 等价于v8引擎 + nodejs。

就是这样的对应关系。

iotjs代码量相对不大，而且是纯C语言写的，所以我感觉可以研究一下。

用 C 语言来扩展 iotjs 不是太难的事情，

但是将 GUI 集成到 iotjs 却是有些麻烦的。

主要原因在于 iotjs 有个主循环 (main loop)，

GUI 自己也有个主循环 (main loop)，

两者不同并存，只能选一个。

这里 AWTK 为例，介绍一下如何将 GUI 集成到 iotjs 中，这对将 GUI 集成到 nodejs 也是有参考价值。



在集成 AWTK 到 iotjs 时，我选择了以 iotjs 的主循环为主。这并不是唯一的正确方案，做这个选择的主要原因有：

让 AWTK 作为 iotjs 的模块，保持 iotjs 本身的开发方式。

避免修改 iotjs。iotjs 对我来说是第三方模块，修改第三方模块，会增加后期的维护成本。



我们把 AWTK 主循环的一次循环提取成一个 step，然后把它放到 iotjs 的定时器中，每隔 16 毫秒（最大 60FPS) 调用一次，这样可以模拟 GUI 的主循环了。



要将 GUI 集成到 iotjs，GUI 必须要把对外提供的API全部绑定到 jerryscript。

这个对 AWTK 来说只是举手之劳的事情，

AWTK 通过提取注释来生成 IDL，

再根据 IDL 来生成各种语言的绑定，这让绑定工作变得轻松，同时也降低了后期的维护成本。



AWTK-JS 这个项目提供了对 jerryscript 的绑定，我们把它编译成一个库，即可在 AWTK-iotjs 中使用了。



zlg官方的集成iotjs和awtk

https://github.com/zlgopen/awtk-iotjs



# 资源收集

这个法国老哥有不少模块是基于iotjs的。

https://github.com/rzr/webthing-iotjs



# iotjs内部

## 设计

iotjs基于jerryscript和libtuv。

JerryScript 是一个轻量级的 Javascript 引擎，

旨在运行在物联网的小型设备上，

而 libuv 是一个支持异步 I/O 的库。

有一个层将 JerryScript 和 libuv 绑定到 IoT.js。

我们将在本文档的 Javascript Binding 和 libuv Binding 部分进行介绍。



IoT.js 核心层位于这些绑定层之上。

这个核心层在这个项目中扮演着核心角色，

为上层提供运行主事件循环、与 Javascript 引擎交互、通过 libuv 管理 I/O 资源、管理对象的生命周期、提供内置模块等基本功能。

## JavaScript binding

许多现代 Javascript 引擎都带有嵌入的 API，

以提供用于编译和执行 Javascript 程序、访问 Javascript 对象及其值、处理错误、管理对象生命周期等的功能。

您可以将 Javascript 绑定层视为上层（IoT.js 核心）和底层 Javascript 引擎之间的接口。

虽然 IoT.js 目前只支持 JerryScript，

但未来我们有机会扩展支持 Javascript 引擎（如 Duktape 或 V8）。

出于这个原因，我们希望保持层独立于特定的 Javascript 引擎。

在iotjs_binding.h中可以看到该层的接口。



### jerry_value_t

这个结构体代表了一个JavaScript object。

上层会通过这个结构体来访问JavaScript object。

这个结构体提供了这些工具函数

```
创建一个js obj，通过iotjs_jval_create_xx函数。
创建一个js obj，通过一个value
创建一个js obj，它的实现是在C里面实现的。
创建一个js Error对象
增加ref cnt
减少ref cnt
检查obj 类型
调用一个js函数
eval一个js 脚本
set和get native数据给js obj
```

### native handler

有些操作，例如io、network、device control、多任务等等，

不能通过纯js来实现。

iotjs通过native handler的机制来执行这些操作。

你可以理解成js函数实现在C代码里。

### embedding api

现在很多的js引擎，都提供embedding api。

iotjs使用这些api来创建内置模块和native handler。

## libuv binding

iotjs使用libuv来执行异步io和线程。

### iotjs_handlewrap_t

这个结构体是用来binding一个js obj和一个libuv handler。

iotjs_handlewrap_t继承了iotjs_jobjectwrap_t结构体。因为它跟一个js obj关联了。

### iotjs_reqwrap_t

这个结构体是包装了libuv请求数据和js callback函数。

并确保js callback在io操作期间是alive状态的。

异步io操作在iotjs里是这样做的

1、js module调用builtin函数来执行io操作。

2、builtin创建iotjs_reqwrap_t来包装uv_req_s和js callback函数。

3、builtin调用libuv来执行io操作。

4、在io操作完成后，libuv调用builtin after handler（内置的后处理函数？韩国人的英文有点难懂）

5、内置的后处理函数 拿到iotjs_reqwrap_t（里面包含了io处理的结果和callback函数）

6、内置的后处理函数调用js callback。

7、内置的后处理函数释放iotjs_reqwrap_t。

## iotjs core

### life cycle

iotjs的处理过程如下

1、初始化jerryscript引擎。

2、执行空的脚本，创建一个初始化的js context。

3、初始化builtin module。包括process这个

4、执行iotjs.js，创建入口函数。

5、运行入口函数。

6、初始化process模块。

7、load用户的脚本。

8、运行用户脚本。

9、run eventloop，直到没有事件。

10、clean up

### builtin module

使用embedding api，在C语言里实现的js obj。

或者使用js实现的，包括src/js目录下的这些文件。

### eventloop





# jerryscript api文档

https://jerryscript.net/api-reference/

# jerryscript的设计

JerryScript 和当前多级自适应即时编译（JIT）引擎相比，是一个纯粹的解释器。

所以它没有保存编译后代码的开销，

甚至它的解析器也不保存抽象语法树（AST）。

它直接将源码按行解释成字节码。

对于数据表现，JerryScript 中的对象在大小上做了优化。

JerryScript 使用压缩的指针、固定大小的字节码块、预分配对象池和数值对象的多种表示等方式同时达到遵守标准和内存优化。

我们将持续不断的用各种方式减少内存消耗。

JavaScript 在嵌入式设备开发中是非常便利的。

它支持异步函数回调和异步 I/O，

这对基于事件驱动的硬件编程是非常有用的。

最后，JavaScript 是网页编程中使用最广的语言。

将物联网设备和互联网生态系统（web ecosystem）相互配合，

对于构建物联网生态系统来说是一个明智的选择。

因此，许多互联网标准，如 HTTP、JSON、REST 已经成为物联网连接标准化的中心，

唯一缺少的就是 JavaScript。

我们认为 JavaScript 在应用程序和服务互通层上是最重要的一环。



IoT.js 的核心是向下兼容 Node.js。

为了做到这一点，IoT.js 遵守 CommonJS 规范中的模块化编程，

并且支持 Node.js API 中核心功能的子集。

针对物联网，我们正在定义嵌入式设备控制和物联网编程的标准模块。

截至目前，我们定义了第一个通用输入输出接口（GPIO）访问 API 的候选规范，并且实现了它的原型。

我们认为，为了体现它的真正价值，这些活动应该在物联网社区的共识下完成。

这就是我们开源 IoT.js 的原因。



参考资料

https://www.infoq.cn/article/2015/08/iotjs-jerryscript-samsung

# libuv设计文档

http://docs.libuv.org/en/v1.x/design.html



刚刚开源的「鸿蒙 2.0」以 JavaScript 作为 IoT 应用开发的框架语言。



对于 JerryScript 的使用，有同场景重度应用经验的当属 [RT-Thread](https://link.zhihu.com/?target=https%3A//github.com/RT-Thread/rt-thread) 创始人 

[@午夜熊](https://www.zhihu.com/people/ae873d644f3c069551f734c3db6a5867)

，他们和某国内一线厂商合作研发的智能手表就用 JerryScript 实现了 UI，目前产品马上就要上市了。他们团队对 JerryScript 的一些使用反馈也吻合上述评价，概括说来是这样的：



- JerryScript 在体积和内存占用上，相比 QuickJS 有更好的表现。
- JerryScript 的稳定性弱于 QuickJS，有一些难以绕过的问题。
- JerryScript 面对稍大（1M 以上）的 JS 代码库，就有些力不从心了。



HarmonyOS是一款面向万物互联时代的、全新的分布式操作系统；

它实现了一个非常轻量级的 MVVM 模式。

通过使用和 vue2 相似的属性劫持技术实现了响应式系统。

鸿蒙 JS 框架支持 ECMAScript 5.1；js runtime 没有使用 V8，也没有使用 jscore。而是选择了 JerryScript。

JerryScript 是用于物联网的超轻量 JavaScript 引擎。

Jerryscript是由三星开发的一款JavaScript引擎，是为了让JavaScript开发者能够构建物联网应用。物联网设备在CPU性能和内存空间上都有着严重的制约。因此，三星设计了JerryScript引擎，它能够运行在小于64KB内存上，且全部代码能够存储在不足200KB的只读存储（ROM）上。说到这里，我想身为前端的我们是不是该搞点事情，比如给自己的华为手表上写一个APP应用，让他定时叫你敷面膜；或者写一个新闻APP，类似今日头条，数据么，可以造假；

# iotjs-express

iotjs和express都是我要深入研究进行掌握的。

https://github.com/rzr/iotjs-express

我的iotjs已经编译好，加入到PATH里了。

下载iot-express的代码。

运行：

```
make start
```

然后访问地址即可。

代码分析

对外暴露的，就相当于一个Express类。

这个类主要使用的方法：

```
listen
	内部是http.createServer，server处理消息的回调是Express的request方法。
	
```

所以，重点就是看request的实现。

```
request函数有2个参数，一个req，一个res。
1、首先给res写上一些可以确定的header信息。
2、给req加上req.params = {}这个属性。
3、解析req的类型，是get还是put。用的express.parse函数。
	返回ture或者false。
4、拿到应用层app.set('/', function(req, res){})这样注册进来的回调函数。
把callback传递给handleRequest函数处理。
5、如果是get，那么直接调用注册的应用层回调。
6、如果是post，调用Express.receive函数。
receive函数就是在把数据收完之后，进行json解析，再调用应用层注册的回调。
```

## mqtt example分析

在iotjs-express目录下面，还有server-mqtt.js和client-mqtt.js。

express跟mqtt又怎么结合使用的呢？

就是相当于client自己不直接进行mqtt操作，发给server来做这个操作。

我没有看明白这个的应用场景。

先不看了。



# 代码下markdown文档阅读

net的例子

写一个test.js，内容如下：

```
var net = require('net')
var port = 1234
var server = net.createServer()
server.listen(port)
server.on('connection',  function(socket) {
    socket.on('data', function(data) {
        socket.write("echo: " + data)
    })
})
```

执行：

```
iotjs ./test.js
```

用nc连接测试：

```
nc localhost 1234
xx
echo: xx
```

# js代码分析

看src/js目录下的代码。

我主要关注net、http、events这个系列的。因为我用node，主要也是做webserver来用的。

## net

net.js里的类：我分析代码看到的。

```

SocketState
Socket
	继承了stream.Duplex
	有方法：
		connect：参数options和callback。
			callback是给connect事件用的。
			最后返回this。
		write：
			参数是：data和callback。
			直接转给了Duplex去做。
		end：
			参数是：data和callback。
			转给stream的end方法。
			最后返回this。
		destroy：
			销毁socket。
		destroySoon：
			快速销毁。
		setKeepAlive：
			保持连接。
		address
			返回socket name
		setTimeout：
			设置超时，单位ms。
	属性：
		remoteAddress
		remoteFamily
		remotePort
		localAddress
		localPort
Server类
	继承了EventEmitter。
	方法：
		listen
		address
		close
		
对外暴露的模块方法：
exports.createServer
exports.connect = exports.createConnection
对外暴露的类：
exports.Socket  = Socket
exports.Server = Server 
```

总的来说，就2个东西：创建socket和创建server。

## http

```
对外暴露的类：
exports.ClientRequest
exports.ServerResponse 继承了OutgoingMessage
exports.IncomingMessage
exports.OutgoingMessage
exports.Agent
exports.Server

对外暴露的方法：
exports.request
exports.createServer
exports.get //是request方法的一个特例。
```

总的来说，就是2类。

服务端和客户端。各有3个类，

服务端一个方法：createServer

客户端一个方法：request。

## iotjs.js

这个相当于node的核心js文件。所有的全局变量和函数都在这里。

值得分析一下。

## module.js

这个说明了iotjs是如何进行模块的查找的。



# src\iotjs_js.c

```
 * This file is generated by tools/js2c.py
```

是把内置的js模块都编译到C文件里的方式。

```
const iotjs_js_module_t js_modules[] = {
  { module_assert, MODULE_assert_IDX },
  { module_buffer, MODULE_buffer_IDX },
  { module_console, MODULE_console_IDX },
  { module_dns, MODULE_dns_IDX },
  { module_events, MODULE_events_IDX },
  { module_fs, MODULE_fs_IDX },
  { module_http, MODULE_http_IDX },
  { module_http_client, MODULE_http_client_IDX },
  { module_http_common, MODULE_http_common_IDX },
  { module_http_incoming, MODULE_http_incoming_IDX },
  { module_http_outgoing, MODULE_http_outgoing_IDX },
  { module_http_server, MODULE_http_server_IDX },
  { module_iotjs, MODULE_iotjs_IDX },
  { module_module, MODULE_module_IDX },
  { module_net, MODULE_net_IDX },
  { module_stream, MODULE_stream_IDX },
  { module_stream_duplex, MODULE_stream_duplex_IDX },
  { module_stream_internal, MODULE_stream_internal_IDX },
  { module_stream_readable, MODULE_stream_readable_IDX },
  { module_stream_writable, MODULE_stream_writable_IDX },
  { module_timers, MODULE_timers_IDX },
  { module_util, MODULE_util_IDX },
  { NULL, 0 }
};
```

# iotjs_module_get

```
  const jerry_value_t process = iotjs_module_get("process");
  iotjs_jval_set_property_jval(global, "process", process);
```

src\modules\iotjs_module_buffer.c

这里面注册的module的各个方法：

```
jerry_value_t iotjs_init_buffer(void) {
  jerry_value_t buffer = jerry_create_external_function(buffer_constructor);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_BYTELENGTH,
                        buffer_byte_length);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_COMPARE, buffer_compare);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_COPY, buffer_copy);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_WRITE, buffer_write);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_WRITEDECODE,
                        buffer_write_decode);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_WRITEUINT8,
                        buffer_write_uint8);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_READUINT8,
                        buffer_read_uint8);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_SLICE, buffer_slice);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_TOSTRING, buffer_to_string);
  iotjs_jval_set_method(buffer, IOTJS_MAGIC_STRING_FROM_ARRAYBUFFER,
                        buffer_from_array_buffer);

  return buffer;
}
```



# 参考资料

1、集成 AWTK 到 iotjs

这个是李先静的文章

https://blog.csdn.net/chongdingxi9493/article/details/101005502

2、官方文档

https://github.com/jerryscript-project/iotjs/blob/master/docs/devs/Developer-Tutorial.md

高级话题

https://github.com/jerryscript-project/iotjs/blob/master/docs/devs/Advanced-Development.md

3、官方pdf文档

https://wiki.tizen.org/images/d/db/01-IoTjs_and_JerryScript_Overview.pdf

4、这个个人网站有不少相关文章，值得读一下。

https://txiaozhe.github.io/2019/12/13/javascript-in-iot/

5、jerryscript文档集合

https://www.lhsz.xyz/read/jerryscript-2.1-en/f403b80e7a4c1a7a.md

6、

https://www.jb51.net/article/220411.htm