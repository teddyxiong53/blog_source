---
title: yoda.js分析
date: 2020-08-28 15:35:08
tags:
	- nodejs

---

--

我先把runtime和package这2个目录照着写一遍。

可能是可以在电脑上跑起来的。

从这里可以看出。

```
var configPath = process.env.YODA_RUN_MODE === 'host'
  ? path.join(__dirname, '../../etc/yoda')
  : '/etc/yoda'
```



但是暂时不想投入精力去折腾编译的。

因为项目被放弃，也并没有大力支持对外开放，所以相关的脚本不完善。

一边写一边看。

这个闭包实现的一次性调用。

```
module.exports.once = function (callback) {
    var called = false
    var ret 
    return function dedupCallback() {
        if (!called) {
            called = true
            ret = callback.apply(this.arguments)
        }
        return ret
    }
}
```

实现delay函数

```
module.exports.delay = function (ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}
```

实现单例，也是靠闭包。

# 关于变量的名字

```
AppChargeur
	Chargeur这个是法语。我感觉可能有不少的单词是法语的。也是一个坑爹的习惯。
	表示充电器。
```



# endoscope

这个提取出来了。

后面我有需要可以复用

# 所有文件层次

| 子目录   | 描述                               |
| -------- | ---------------------------------- |
| include  | 构建时依赖的项目头文件             |
| packages | 通用模块接口，用于调用系统底层服务 |
| res      | 资源文件包括灯光和音效             |
| runtime  | 核心代码与服务                     |
| test     | 单元测试                           |
| tools    | 调试工具                           |

| 源码目录 | 设备目录              |
| -------- | --------------------- |
| res      | /opt/res              |
| apps     | /opt/apps             |
| runtime  | /usr/yoda             |
| packages | /usr/lib/node_modules |

```
$ tree -I '*node_module*|.git|*vendor*|test|res'
.
├── benchmark
│   ├── boot.sh
│   ├── endoscope
│   │   ├── counter.js
│   │   ├── enum.js
│   │   └── histogram.js
│   └── multimedia
│       └── mediaplayer.js
├── client
│   └── c
│       ├── CMakeLists.txt
│       ├── Doxyfile
│       ├── example
│       │   └── example.c
│       ├── include
│       │   ├── yodaos_api_defines.h
│       │   ├── yodaos_inner.h
│       │   └── yodaos_sdk.h
│       └── src
│           ├── flora.c
│           ├── util.c
│           └── yodaos_sdk.c
├── cmake
│   ├── module
│   │   └── FindNodeAddon.cmake
│   ├── packages.cmake
│   ├── yodart-api.cmake
│   └── yodart.cmake
├── CMakeLists.txt
├── codecov.yml
├── CODEOWNERS
├── Dockerfile
├── docs
│   ├── configure-ota.md
│   ├── get-started-with-native-app.md
│   ├── protocol-fauna.md
│   └── README.md
├── etc
│   ├── hotplug.d
│   │   └── ntp
│   │       └── post-ntpd-event
│   ├── manifest.json
│   └── yoda
│       ├── app-loader-config.json
│       ├── component-config.json
│       ├── dbus-config.json
│       ├── env.json
│       ├── flora-config.json
│       ├── keyboard.json
│       └── memory-sentinel.json
├── include
│   ├── async_invoke.h
│   ├── common.h
│   ├── iotjs_helper.h
│   ├── napi.h
│   └── napi-inl.h
├── LICENSE.md
├── package.json
├── package-lock.json
├── packages
│   ├── glob
│   │   ├── CMakeLists.txt
│   │   ├── common.js
│   │   ├── LICENSE
│   │   ├── package.json
│   │   └── sync.js
│   ├── logger
│   │   ├── binding.cc
│   │   ├── CMakeLists.txt
│   │   └── index.js
│   ├── lru-cache
│   │   ├── CMakeLists.txt
│   │   ├── index.js
│   │   ├── LICENSE
│   │   ├── linked-list.js
│   │   └── package.json
│   ├── minimatch
│   │   ├── balanced-match.js
│   │   ├── brace-expansion.js
│   │   ├── CMakeLists.txt
│   │   ├── concat-map.js
│   │   ├── index.js
│   │   ├── LICENSE
│   │   └── package.json
│   ├── step
│   │   ├── CMakeLists.txt
│   │   ├── example.js
│   │   ├── index.js
│   │   ├── LICENSE.txt
│   │   ├── package.json
│   │   ├── README.md
│   │   └── README-zh.md
│   ├── tape
│   │   ├── bin
│   │   │   └── tape.js
│   │   ├── CMakeLists.txt
│   │   ├── index.js
│   │   ├── lib
│   │   │   ├── deep-equal
│   │   │   │   ├── index.js
│   │   │   │   └── lib
│   │   │   │       ├── is_arguments.js
│   │   │   │       └── keys.js
│   │   │   ├── default_stream.js
│   │   │   ├── defined.js
│   │   │   ├── function-bind
│   │   │   │   ├── implementation.js
│   │   │   │   └── index.js
│   │   │   ├── is-callable.js
│   │   │   ├── minimist.js
│   │   │   ├── object-inspect.js
│   │   │   ├── resolve
│   │   │   │   ├── index.js
│   │   │   │   └── lib
│   │   │   │       ├── async.js
│   │   │   │       ├── caller.js
│   │   │   │       ├── core.js
│   │   │   │       ├── core.json
│   │   │   │       ├── node-modules-paths.js
│   │   │   │       └── sync.js
│   │   │   ├── results.js
│   │   │   ├── resumer.js
│   │   │   ├── test.js
│   │   │   └── through.js
│   │   ├── LICENSE
│   │   ├── package.json
│   │   └── README.md
│   ├── @yoda
│   │   ├── audio
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── src
│   │   │       └── AudioNative.cc
│   │   ├── battery
│   │   │   ├── CMakeLists.txt
│   │   │   └── index.js
│   │   ├── bluetooth
│   │   │   ├── a2dp.js
│   │   │   ├── a2dp-statemap.js
│   │   │   ├── CMakeLists.txt
│   │   │   ├── helper.js
│   │   │   ├── hfp.js
│   │   │   ├── hfp-statemap.js
│   │   │   ├── index.js
│   │   │   ├── player.js
│   │   │   ├── protocol.json
│   │   │   └── stream.js
│   │   ├── bolero
│   │   │   ├── base-class.js
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── loader.js
│   │   ├── endoscope
│   │   │   ├── CMakeLists.txt
│   │   │   ├── exporter
│   │   │   │   └── flora.js
│   │   │   ├── index.js
│   │   │   ├── metric
│   │   │   │   ├── counter.js
│   │   │   │   ├── enum.js
│   │   │   │   ├── histogram.js
│   │   │   │   └── _metric.js
│   │   │   ├── package.json
│   │   │   ├── README.md
│   │   │   └── registry.js
│   │   ├── env
│   │   │   ├── CMakeLists.txt
│   │   │   └── index.js
│   │   ├── exodus
│   │   │   ├── CMakeLists.txt
│   │   │   └── index.js
│   │   ├── httpsession
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── src
│   │   │       └── httpsession.cc
│   │   ├── input
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── src
│   │   │       ├── InputNative.cc
│   │   │       └── InputNative.h
│   │   ├── light
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── src
│   │   │       ├── LightNative.cc
│   │   │       └── LightNative.h
│   │   ├── manifest
│   │   │   ├── CMakeLists.txt
│   │   │   └── index.js
│   │   ├── multimedia
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   ├── mediaplayer.js
│   │   │   ├── sounder.js
│   │   │   └── src
│   │   │       ├── media-player.cc
│   │   │       ├── media-player.h
│   │   │       └── wav-player.cc
│   │   ├── network
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── package.json
│   │   ├── oh-my-little-pony
│   │   │   ├── CMakeLists.txt
│   │   │   ├── health-reporter.js
│   │   │   └── index.js
│   │   ├── ota
│   │   │   ├── CMakeLists.txt
│   │   │   ├── condition.js
│   │   │   ├── const.js
│   │   │   ├── index.js
│   │   │   ├── lock.js
│   │   │   └── persistance.js
│   │   ├── property
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── src
│   │   │       └── PropertyNative.cc
│   │   ├── system
│   │   │   ├── CMakeLists.txt
│   │   │   ├── index.js
│   │   │   └── src
│   │   │       └── SystemNative.cc
│   │   ├── util
│   │   │   ├── CMakeLists.txt
│   │   │   ├── compose.js
│   │   │   ├── delegate.js
│   │   │   ├── deprecate.js
│   │   │   ├── fs.js
│   │   │   ├── index.js
│   │   │   ├── _.js
│   │   │   ├── json.js
│   │   │   ├── math.js
│   │   │   ├── path.js
│   │   │   └── time.js
│   │   └── wifi
│   │       ├── CMakeLists.txt
│   │       ├── index.js
│   │       └── src
│   │           └── binding.cc
│   └── @yodaos
│       ├── application
│       │   ├── application.js
│       │   ├── audio-focus.js
│       │   ├── class-loader.js
│       │   ├── CMakeLists.txt
│       │   ├── index.js
│       │   ├── now-playing-center.js
│       │   ├── package.json
│       │   ├── service.js
│       │   ├── symbol.js
│       │   └── vui
│       │       ├── app-task.js
│       │       ├── atomic-task.js
│       │       ├── index.js
│       │       └── sequential-flow.js
│       ├── effect
│       │   ├── CMakeLists.txt
│       │   ├── index.js
│       │   └── package.json
│       ├── keyboard
│       │   ├── CMakeLists.txt
│       │   ├── index.js
│       │   └── package.json
│       ├── mm
│       │   ├── bootstrap.js
│       │   ├── CMakeLists.txt
│       │   ├── index.js
│       │   ├── mock.js
│       │   ├── package.json
│       │   ├── README.md
│       │   └── test.js
│       ├── speech-synthesis
│       │   ├── CMakeLists.txt
│       │   ├── index.js
│       │   ├── package.json
│       │   ├── src
│       │   │   ├── logger.h
│       │   │   ├── pcm-player.cc
│       │   │   ├── pcm-player.h
│       │   │   ├── speech-synthesizer.cc
│       │   │   ├── speech-synthesizer.h
│       │   │   └── thr-pool.h
│       │   └── symbol.js
│       ├── storage
│       │   ├── CMakeLists.txt
│       │   ├── index.js
│       │   └── package.json
│       └── voice-interface
│           ├── CMakeLists.txt
│           ├── index.js
│           └── package.json
├── README.md
├── runtime
│   ├── app
│   │   ├── app-bridge.js
│   │   ├── default-launcher.js
│   │   ├── executable-launcher.js
│   │   └── light-launcher.js
│   ├── app-runtime.js
│   ├── client
│   │   ├── api
│   │   │   └── default.json
│   │   ├── ext-app-entry.js
│   │   ├── ext-helper.js
│   │   ├── ext-instrument-entry.js
│   │   ├── translator-in-process.js
│   │   └── translator-ipc.js
│   ├── component
│   │   ├── app-loader.js
│   │   ├── app-scheduler.js
│   │   ├── audio-focus.js
│   │   ├── broadcast.js
│   │   ├── chronos.js
│   │   ├── dbus-registry.js
│   │   ├── dispatcher.js
│   │   ├── effect.js
│   │   ├── flora.js
│   │   ├── keyboard.js
│   │   ├── media-controller.js
│   │   ├── memory-sentinel.js
│   │   ├── permission.js
│   │   └── visibility.js
│   ├── constants.js
│   ├── descriptor
│   │   ├── activity.js
│   │   ├── audio-focus.js
│   │   ├── broadcast.js
│   │   ├── chronos.js
│   │   ├── effect.js
│   │   ├── keyboard.js
│   │   ├── media-controller.js
│   │   ├── runtime.js
│   │   └── visibility.js
│   ├── lib
│   │   ├── config.js
│   │   └── descriptor.js
│   └── services
│       ├── healthz
│       │   └── healthz
│       ├── lightd
│       │   ├── bin
│       │   │   └── play.js
│       │   ├── effects.js
│       │   ├── example
│       │   │   └── test.js
│       │   ├── flora.js
│       │   ├── helper.js
│       │   ├── index.js
│       │   ├── README.md
│       │   ├── service.js
│       │   └── tests
│       │       ├── appSound.js
│       │       ├── appsound-loadtest.js
│       │       ├── callback.js
│       │       ├── effects-breathing-test.js
│       │       ├── led-test.js
│       │       ├── lightMethod.js
│       │       └── play-loadtest.js
│       ├── otad
│       │   ├── delegation.js
│       │   ├── index.js
│       │   ├── otad
│       │   ├── step.js
│       │   └── wget.js
│       └── vuid
│           ├── index.js
│           └── watchdog.js
└── tools
    ├── apt-get-install-deps.sh
    ├── brew-install-deps.sh
    ├── build-yodart.sh
    ├── clang-format
    ├── configure-network
    ├── coverage-install
    ├── coverage-instrument
    ├── generate-api-c.js
    ├── generate-api-json.js
    ├── helper
    │   ├── merge-tests.js
    │   └── upgrade.js
    ├── install-shadow-node.sh
    ├── memory-viewer
    ├── readlog
    ├── README.md
    ├── rklogger
    │   ├── CMakeLists.txt
    │   └── rklogger.c
    ├── runtime-install
    ├── runtime-op
    ├── switch-env
    ├── testci
    └── upgrade

88 directories, 307 files
```

总共大概300个文件。

主要的目录里就是runtime和package。

## runtime目录结构

下面一共60个文件。

```
.
├── app
│   ├── app-bridge.js
│   ├── default-launcher.js
│   ├── executable-launcher.js
│   └── light-launcher.js
├── app-runtime.js
├── client
│   ├── api
│   │   └── default.json
│   ├── ext-app-entry.js
│   ├── ext-helper.js
│   ├── ext-instrument-entry.js
│   ├── translator-in-process.js
│   └── translator-ipc.js
├── component
│   ├── app-loader.js
│   ├── app-scheduler.js
│   ├── audio-focus.js
│   ├── broadcast.js
│   ├── chronos.js
│   ├── dbus-registry.js
│   ├── dispatcher.js
│   ├── effect.js
│   ├── flora.js
│   ├── keyboard.js
│   ├── media-controller.js
│   ├── memory-sentinel.js
│   ├── permission.js
│   └── visibility.js
├── constants.js
├── descriptor
│   ├── activity.js
│   ├── audio-focus.js
│   ├── broadcast.js
│   ├── chronos.js
│   ├── effect.js
│   ├── keyboard.js
│   ├── media-controller.js
│   ├── runtime.js
│   └── visibility.js
├── lib
│   ├── config.js
│   └── descriptor.js
└── services
    ├── healthz
    │   └── healthz
    ├── lightd
    │   ├── bin
    │   │   └── play.js
    │   ├── effects.js
    │   ├── example
    │   │   └── test.js
    │   ├── flora.js
    │   ├── helper.js
    │   ├── index.js
    │   ├── README.md
    │   ├── service.js
    │   └── tests
    │       ├── appSound.js
    │       ├── appsound-loadtest.js
    │       ├── callback.js
    │       ├── effects-breathing-test.js
    │       ├── led-test.js
    │       ├── lightMethod.js
    │       └── play-loadtest.js
    ├── otad
    │   ├── delegation.js
    │   ├── index.js
    │   ├── otad
    │   ├── step.js
    │   └── wget.js
    └── vuid
        ├── index.js
        └── watchdog.js

```



### app-runtme.js

这个是主要的入口文件。

对外提供的：AppRuntime类。

```
module.exports = AppRuntime
```

这个类的组成：

构造方法：

```
1、是EventEmitter的子类。
2、初始化这些实例属性：
inited：bool类型
hibernated：bool类型。
2个loader：
Component loader
descriptor loader
	调用了他们的构造函数，构造函数没有执行load的操作。
	需要单独调用load函数才执行load操作。
```

prototype方法：

```
init
	1、如果发现inited已经是true，直接返回Promise.resolve()
	2、遍历Component目录里，依次执行load操作。
	3、进行descriptor的load操作。
	4、对Component依次进行init操作。
	5、调用Component中的apploader这个组件的reload方法。最后调用到loadApp方法。
	6、然后广播yodaos.on-system-booted 这个消息。
	7、最后打开url：this.openUrl('yoda-app://setup/init')
	openUrl会把setup当前hostname取出来。对应成appId去执行。
```

setup具体传递给谁了？如何处理了？

setup这个是靠package.json里注册的名字。

谁注册了这个名字，就是谁处理。

这个信息可以从这里获取到。

https://yodaos-project.github.io/yoda-book/zh-cn/guidance/01-build-your-first-app.html



应用可以通过 URL 的形式唤起其它应用，并将当前的交互托付给能处理这个 URL 的应用。

如果希望处理某个域名的 URL，需要在应用的 package.json 中注册这个 URL，如下是注册一个 foobar.app 域名的例子：

```json
{
  "name": "com.example.app.foobar",
  "manifest": {
    "hosts": [
      "foobar.app"
    ]
  }
}
```

而注册了该域名的应用就可以通过如下代码处理如 `yoda-app://foobar.app/data/media/music.mp3` 的 URL 请求：

看看这个测试例子的。

test\@yodaos\application\application.test.js

在network里有这样：

```
./opt/apps/network/app.js:72:      case '/setup':
```

我这个是在yodaos-repo完整编译的rootfs里找到的。

在yodajs里没有找到这个目录。

看现在yodajs的版本更新一些。难道是后面删掉了？

把github上仓库切到这个tag tag: v7.30.2看看。

这个时候确实还是有apps目录。

我也把代码切到这个版本来读吧。

# 重新用v7.30.2版本来看

这个目录结构都有较大的不同。

# rokidos v2 设计文档

v2-design-document-draft.md

基本原则是，拥抱web社区。

重新设计了大多数的package。

```
Event
KeyboardEvent
UIEvent
Bluetooth
SpeechSynthesis
SpeechRecognize
MediaSource
MediaStream
NetworkInformation
Storage
	window.localStorage
	window.sessionStorage
WebSocket
```

优先选择WEB API，而不是nodejs。

并不意味着抛弃nodejs生态。

所有的模块仍然是一个nodejs package。

但是我们把他们封装进activation process。

这意味着你可以通过window这个全局对象来访问所有模块，就像你在浏览器里做的那样。

支持的App

1、LightApp。

2、ExtApp。通过DBus。

内置的LightApp有：

```
First Guidance
System
Volume Controls
```

内置的ExtApp有：

```
Network
CloudApp Client
Alarm & Reminder
Bluetooth
```



配置

```
设备名字的规则是${namePrefix}-${sn.slice(-6)}
triggerWords
	定制你的唤醒词。
tts
	定制你的tts发声人。
network
	定义重连的间隔。
Bluetooth
	ttl时间定义。
	
```



# 看test代码

# performance

这个模块很简单，但是很实用。

通过stub函数进行打桩。

# cloudapi

对应这个目录

runtime\lib\cloudapi

包括了这些功能：

1、login和设备bind。

2、设备unbind。

3、更新基本信息。

4、reset用户信息。

5、确认nlp请求。

6、mqtt请求。



对外暴露的是CloudStore 这个class。

构造函数

```
参数：
	一个option对象。
属性：
	cloudgw
	mqttClient
	config
```

prototype方法

```
connect
	参数：masterID。
	调用login/request.sh脚本来做的。
	
handleResponse
	参数：一个obj。
	处理：
		相当于连接成功后，创建cloudgw和mqttclient开始工作。
syncDate
	参数：无。
	处理：
		跟服务器同步时间。
reset
	参数：无。
	处理：
		清空信息。
requestMqttToken
	参数：无。
	调用./login/request-mqtt-token.sh处理。
updateBasicInfo
	参数：无。
	处理：
		返回本机的sn号等设备信息。
resetSettings
	参数：无。
	处理：
		用cloudgw.request发送一个reset请求。
sendNLPConfirm
	参数：
		appId
		intent
		slot
		options
		attrs
	处理：
		cloudgw request请求。
```



## mqtt

对应文件mqtt/client.js

对外暴露的是class MqttClient。

构造方法：

```
接收的参数是CloudStore对象和一个option。

实例属性有：
payload
	有3个属性：username、token、expireTime。
options
_isOnline
_isConnecting
_rejectReconnect
_lastSubscribed
_mqttHandle
_messageHandle
_backoffTime
```

prototype方法有：

```
needRefresh
	username、token、expireTime无效都要refresh。
getChannelName
	返回字符串。
	是mqtt的主题。
	u/masterId/deviceType/xx/deviceId/yy/rc
	
setMessageHandler
	把函数赋值给_messageHandler
onmessage
	调用_messageHandler处理消息。
start
	返回一个Promise。
	
reconnect
	如果_isConnecting，则直接返回。
	
suspend
sendToApp

```



## cloudgw

对应代码packages\@yoda\cloudgw

这个对应的服务端代码没有开源。

也没有文档，从代码推算协议，看看能不能自己实现对应的服务端。

只做demo。

这个并没有多少东西，总共100多行代码。

就一个post请求。

# /etc/yoda/env.json

```
{
  "cloudgw": {
    "account": "device-account.rokid.com",
    "wss": "apigwws.open.rokid.com",
    "restful": "apigwrest.open.rokid.com"
  },
  "mqtt": {
    "registry": "wormhole-registry.rokid.com",
    "uri": "mqtts://wormhole.rokid.com:8885"
  },
  "speechUri": "wss://apigwws.open.rokid.com:443/api",
  "skills": {
    "alarmUri": "cas-alarm-pro.rokid.com"
  },
  "activation": {
    "defaultPath": "/opt/media/",
    "customPath": "/data/activation/media/"
  },
  "trace": {
    "uploadUrl": "https://das-tc-service-pro.rokid.com"
  }
}
```

分析一下这些服务端。

这里就涉及到一个api gw的概念。这里转去研究了一下express-gateway。





## mqtt部分

从名字看，有个wormhole，表示虫洞。

WormHole是“虫洞”意思。物理界解释为连接黑洞和白洞的时空隧道。它的结构和计算机网络中的网关类似，作为连接两个世界的枢纽。各管各，不用关心中间做了什么。

WormHole是一个简单、易用的api管理平台。目的是为了降低后端服务开发与前端调用的耦合性。通过WormHole这一层使整个项目的开发协作更加完善。客户端开发人员从管理平台查找需要的接口信息进行调用，服务端开发人员定义好接口后同步到管理平台中，管理平台可以统一对接口的访问设置等。

WormHole有两个版本，一个是基于SpringMVC框架、一个是基于原版改造为SpringBoot版本的。



https://gitee.com/deathearth/wormhole



# lifetime.js

runtime\lib\component\lifetime.js

对外接口是LaVieEnPile这个类。这个名字是法语，表示电池寿命。

内部有个AppSlots的类。

```
构造函数
	参数：cut、scene。
		都是bool类型，二选一。

```

prototype函数

```
addApp
	参数：
		appId
		isScene
	处理：
		如果是isScene，那么把appId赋值给this.scene
removeApp
	参数：
		appId
	处理：
		就是把cut或者scene赋值为null。
	返回：
		bool。
copy
	参数：无。
	处理：就是new AppSlot。
	返回：
		创建的AppSlots
toArray
	返回数组。

```

LaVieEnPile



```
构造函数
	参数：
		runtime
	处理：
		持有runtime
		new AppSlots	
		是EventEmitter的子类。
```



# 参考资料

1、

