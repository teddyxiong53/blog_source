---
title: nodejs之ShadowNode
date: 2018-12-22 11:19:17
tags:
	- nodejs
---

1

这个对我的最大意义，在于可以让我比较清晰地看完nodejs的基本接口。





这个是nodejs的嵌入式版本，内存占用更低，速度更快。

不使用v8做JavaScript引擎，使用三星开源的JerryScript。

最近看到rokid用了这个在智能音箱里做js运行时。所以研究一下。

rokid有个人叫yorkie，专门在做这一块的。在cnode论坛上比较活跃。

shadownode比nodejs，有这些特点：

1、更快的启动速度。

2、更小的内存占用。

3、更省内存。



shadownode目前支持的模块，还不是非常多。

但是基础的都有了。

默认还支持dbus的通信方式。

对于Linux系统，这个特点非常有用。

从这里下载代码。

https://github.com/yodaos-project/ShadowNode

编译：

```
npm run build
```

可执行文件是build/x86_64-linux/debug/bin/iotjs。

运行：

```
 ./build/x86_64-linux/debug/bin/iotjs ./test/run_pass/test_console.js
```



编译还是靠调用了cmake来做的。

```
ex.check_run_cmd('cmake', cmake_opt)
```

代码都在src目录下，都是C语言写的。

入口文件是iotjs_main.c。里面就一这么点代码：

```
#include "iotjs.h"

int main(int argc, char** argv) {
  return iotjs_entry(argc, argv);
}

```

文件倒不多，不到200个。

依赖的东西，放在deps目录下。

有这些：

```
├── http-parser
├── jerry：是JavaScript引擎。
├── libmqtt
├── libtuv：事件循环的基础。
└── mbedtls：https支持。
```



参考资料

1、ShadowNode: 以更轻量级的方式使用 Node.js

https://cnodejs.org/topic/5a68d49fafa0a121784a8f48

2、专访 Yorkie：JavaScript 如何开发 IoT 应用？

https://www.infoq.cn/article/QzyM9la8MrIowe*Mrzkp

3、使用 IoT.js 和 Raspberry Pi 开发物联网应用

https://www.wandianshenme.com/play/jerryscript-iotjs-raspberry-pi-build-iot-application/







