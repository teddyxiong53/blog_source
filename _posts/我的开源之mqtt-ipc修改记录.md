mqtt-ipc是我的一个开源项目。

这个项目的目标是以mqtt作为系统的消息总线。

之前也简单做了一次。但是当前没有想清楚client向server get一个数据，怎么精确等待这个消息的回复。

今天想清楚了方法：

就是临时生成一个带id信息的主题，client发送之前先自己要发送的消息的id为主题进行订阅。server收到处理后，pub一个消息id的topic。这个消息只有发送的client才订阅了。

另外，client在发送后，进行一个阻塞等待回复。等待有个超时时间。

这样就完美结局这个问题了。

另外，关于我一直很纠结的主题设计，我觉得可以采取topic就一层，非常简单的做法。

把消息的层次放到content里的json里。

这样就跟我的之前的经验匹配上了。

为了便于定制，顺便深入理解一下mqtt broker。

我需要找一个精简的mqtt broker，如果可能，自己写一遍。加深理解。

这个项目就认真点做，文档注释都用英文来写。

# 找一个mqtt broker代码

之前star了这个

https://github.com/emqx/nanomq

这个也是来自于emqx的作品。

现在到这个topic下面看看。

https://github.com/topics/mqtt-broker

基于C语言的只有26个。都看一遍。

这个是在esp8266上跑的。但是代码看起来也不少。

https://github.com/martin-ger/uMQTTBroker

这个看起来也不是很大。（可以考虑）

https://github.com/codepr/sol

看起来这个作者也写了一个简单的eventloop方案，可以看一下。

https://github.com/codepr/ev

下面对比一下

| 名字        | 分析                                                         |
| ----------- | ------------------------------------------------------------ |
| nanomq      | 有建立一个官网，看起来是认真经验的一个项目。但是可能就是太完备了，有了很多我不需要的东西。可以研究一下。但是不打算用。 |
| uMQTTBroker | 偏向单片机风格。代码风格也不完全统一。再决定不用sol后，这个变得可以考虑。 |
| sol         | 我看了作者的ev.h这个eventloop项目，觉得很喜欢作者这种精致的小型库。代码风格也是我喜欢的。但是看了代码，作者也是不推荐在正式项目里使用的。 |

还是放弃集成一个不成熟的mqtt broker的做法。

就用mosquitto。

到这里看看有哪些可以选择的。

https://mqtt.org/software/



看来看去，还是决定了，就全部基于mosquitto来做。

broker用它，client api也用它。

不再搞那么多了。

先把它的api研究一下。

把mosquitto的源代码快速读了一遍。是比较工程化的写法，没有特别花哨的技巧，就是踏踏实实的那种写法。

读起来很舒服。

mosquitto项目并不复杂。文件较多，主要是划分比较细。很多文件只有几个函数。



## libmosquitto API

# 目录规划

就mipc.c和mipc.h这2个文件就够了。

```
struct mipc_handle
	持有一个mosquitto的handle。
	有个名字。
	
mipc_create
	把共性的消息注册进来。
还有有接口，可以自由注册关注的消息。
mipc_destroy()
mipc_run()
mipc_send
mipc_notify

```

然后examples

```
bgservice.c
uiapp.c
	他们都持有一个mipc_handle。
	对于mipc来说，他们没有区别。
	都是broker的client。
```

尽量在mipc的使用者那里，感受不到mqtt的存在。

