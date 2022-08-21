---
title: nodejs之ShadowNode
date: 2018-12-22 11:19:17
tags:
	- nodejs
---

--

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



编译过程分析

运行命令：npm run build

实际就是调用./tools/build.py。

```

==> Initialize submodule

git submodule init

git submodule update

这个是把依赖的模块下载下来。
==> Build IoT.js

```



```

IoT.js module configuration:
-- ENABLE_MODULE_ADC = OFF
-- ENABLE_MODULE_ASSERT = ON
-- ENABLE_MODULE_BLE = OFF
-- ENABLE_MODULE_BLEHCISOCKET = OFF
-- ENABLE_MODULE_BLE_CHARACTERISTIC = OFF
-- ENABLE_MODULE_BLE_DESCRIPTOR = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_ACL_STREAM = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_BINDINGS = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_CRYPTO = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_GAP = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_GATT = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_HCI = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_HCI_STATUS = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_MGMT = OFF
-- ENABLE_MODULE_BLE_HCI_SOCKET_SMP = OFF
-- ENABLE_MODULE_BLE_PRIMARY_SERVICE = OFF
-- ENABLE_MODULE_BLE_UUID_UTIL = OFF
-- ENABLE_MODULE_BUFFER = ON
-- ENABLE_MODULE_CHILD_PROCESS = ON
-- ENABLE_MODULE_CONSOLE = ON
-- ENABLE_MODULE_CONSTANTS = ON
-- ENABLE_MODULE_CRYPTO = ON
-- ENABLE_MODULE_CRYPTO_HASH = ON
-- ENABLE_MODULE_DBUS = ON
-- ENABLE_MODULE_DEBUG = ON
-- ENABLE_MODULE_DGRAM = ON
-- ENABLE_MODULE_DNS = ON
-- ENABLE_MODULE_EVENTS = ON
-- ENABLE_MODULE_FS = ON
-- ENABLE_MODULE_GPIO = OFF
-- ENABLE_MODULE_HTTP = ON
-- ENABLE_MODULE_HTTPPARSER = ON
-- ENABLE_MODULE_HTTPS = ON
-- ENABLE_MODULE_HTTPS_CLIENT = ON
-- ENABLE_MODULE_HTTP_AGENT = ON
-- ENABLE_MODULE_HTTP_CLIENT = ON
-- ENABLE_MODULE_HTTP_COMMON = ON
-- ENABLE_MODULE_HTTP_INCOMING = ON
-- ENABLE_MODULE_HTTP_OUTGOING = ON
-- ENABLE_MODULE_HTTP_SERVER = ON
-- ENABLE_MODULE_I2C = OFF
-- ENABLE_MODULE_INTERNAL_PROCESS_NEXT_TICK = ON
-- ENABLE_MODULE_IOTJS_BASIC_MODULES = ON
-- ENABLE_MODULE_IOTJS_CORE_MODULES = ON
-- ENABLE_MODULE_MODULE = ON
-- ENABLE_MODULE_MQTT = ON
-- ENABLE_MODULE_NET = ON
-- ENABLE_MODULE_OS = ON
-- ENABLE_MODULE_PATH = ON
-- ENABLE_MODULE_PIPE_WRAP = ON
-- ENABLE_MODULE_PROCESS = ON
-- ENABLE_MODULE_PROFILER = ON
-- ENABLE_MODULE_PROMISE = ON
-- ENABLE_MODULE_PUNYCODE = ON
-- ENABLE_MODULE_PWM = OFF
-- ENABLE_MODULE_QUERYSTRING = ON
-- ENABLE_MODULE_SAX = ON
-- ENABLE_MODULE_SIGNAL = ON
-- ENABLE_MODULE_SPI = OFF
-- ENABLE_MODULE_STM32F4DIS = OFF
-- ENABLE_MODULE_STREAM = ON
-- ENABLE_MODULE_STREAM_DUPLEX = ON
-- ENABLE_MODULE_STREAM_PASSTHROUGH = ON
-- ENABLE_MODULE_STREAM_READABLE = ON
-- ENABLE_MODULE_STREAM_TRANSFORM = ON
-- ENABLE_MODULE_STREAM_WRITABLE = ON
-- ENABLE_MODULE_STRING_DECODER = ON
-- ENABLE_MODULE_TCP = ON
-- ENABLE_MODULE_TIMERS = ON
-- ENABLE_MODULE_TLS = ON
-- ENABLE_MODULE_TTY = ON
-- ENABLE_MODULE_UART = OFF
-- ENABLE_MODULE_UDP = ON
-- ENABLE_MODULE_URL = ON
-- ENABLE_MODULE_UTIL = ON
-- ENABLE_MODULE_WEBSOCKET = ON
-- ENABLE_MODULE_ZLIB = ON
```

相关测试命令，都是写在package.json里，通过npm run来调用。

有这些命令：

```
"test": "npm run lint && npm run test-jerry && npm run test-iotjs",
    "test-jerry": "deps/jerry/tools/run-tests.py --unittests --jerry-test-suite",
    "test-iotjs": "tools/build.py --run-test --no-check-valgrind",
```

编译出来的可执行文件还是iotjs。



```
对比一下shadownode和iotjs，看看改了什么。

default.config里增加了这些模块
ENABLE_MODULE_SAX
ENABLE_MODULE_DBUS
ENABLE_MODULE_MQTT
ENABLE_MODULE_WEBSOCKET
ENABLE_MODULE_ZLIB

增加了samples目录
js目录下：
	assert.js，增加了几种判断。
	所有文件都加了use strict。
	增加了child_process.js。
	增加了dbus.js、debug.js。
	events.js 修改了实现。
	module.js做了较大改动。
	增加了os.js、path.js、promise.js等。
	
直接看shadownode的提交记录。

```



# 参考资料

1、ShadowNode: 以更轻量级的方式使用 Node.js

https://cnodejs.org/topic/5a68d49fafa0a121784a8f48

2、专访 Yorkie：JavaScript 如何开发 IoT 应用？

https://www.infoq.cn/article/QzyM9la8MrIowe*Mrzkp

3、使用 IoT.js 和 Raspberry Pi 开发物联网应用

https://www.wandianshenme.com/play/jerryscript-iotjs-raspberry-pi-build-iot-application/







