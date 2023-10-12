---
title: gstreamer（1）
date: 2018-11-26 17:12:24
tags:
	- gstreamer
typora-root-url: ..\
---

--

gstreamer是gnome桌面环境推荐的流媒体应用框架。

基于插件和管道的设计风格。

基于glib进行开发，所以与一般的C语言写法有些不同。

gstreamer是一个创建流媒体应用程序的框架。

其基本设计思想来自于**俄勒冈研究生学院有关视频管道的创意**。

同时也借鉴了DirectShow的设计思想。



设计原则是：

```
1、结构清晰，功能强大。
2、面向对象的编程思想。
3、灵活的可扩展性。
4、高性能。
5、核心库与插件分离。
```



一个元件，由clock、pad、bus、state构成。

bin是箱子，用来装元件的。

pipeline是最上层的bin。

每一个pipeline都有一个默认的总线。这个总线会在一个mainloop里去检查消息。

并触发对应的callback。跟应用实现通信。

bus包含了一个队列。每次往队列里放消息，都会导致main context被唤醒。







# gstreamer核心

主要做的事情：

1、提供一些组件类型的基类的实现。以及这些组件之间的通信机制。

2、提供api。

核心不关心编码解码这些细节。它提供了一个蓝图。





# 元件GstElement

GstElement是最基础的元素，翻译为“元件”。

我们可以把它理解为一个黑盒子。这个盒子对外暴露的接口，叫连接点（link point）。

GSTElement根据作用，可以分为3种：

1、Source Element。只有输出接口。例如录音设备。

2、Filter Element。有输入和输出2种接口。例如编码模块。

3、Sink Element。只有输入接口。例如播放设备。

每个元件上的 每种接口可以有多个。

例如可以有多个输出接口。

创建一个GstElement的方法，只有一种，就是用GstElementFactory。

不同类型的元件，通过传递给工厂的名字来区分。



Gstreamer使用了跟GObject类似的机制来对属性进行管理。

```
GstObject
	GstElement

```



## 元件的连接

```
GstPad *srcpad, *sinkpad;
srcpad = gst_element_get_pad(element1, "src");
sinkpad = gst_element_get_pad(element2, "sink");
//连接
gst_pad_link(srcpad, sinkpad);
//断开
gst_pad_unlink(srcpad, sinkpad);
```

如果元件都只有一个sink pad和一个source pad，那么就可以简单地这样来连接。

```
gst_element_link(element1, element2);
```

## 元件状态

有4种状态：

1、NULL。

2、READY。

3、PAUSED。

4、PLAYING。

用gst_element_set_state来进行状态的切换。

状态变迁：

```
NULL->READY
	NULL是element的默认状态。
	在NULL状态下，没有分配任何的资源。也没有加载任何运行时库，显然这个时候不能处理任何内容。
	READY
	REDY状态下，一个element拥有所有的默认资源。
	但是跟流相关的东西还没有被分配。
	这个变化对应的枚举是：GST_STATE_CHANGE_NULL_TO_READY。
	
READY->PAUSED
	这个过程中做的事情是：
	激活pad，启动stream thread，直到sink pad收到first buffer，停住。
	PAUSED状态对数据机进行preroll。
	目的是为后续的PLAYING状态准备好数据。
	使得PLAYING启动的速度可以更快。
PAUSED->PLAYING
	大部分element忽略这个状态。
	同步时钟只在PLAYING时发生。
	sink pad不再阻塞buffer和event，开始render数据。
	对多少element来说，PAUSED状态跟PLAYING状态没有区别。
	只有sink element需要区分这2种状态。
	
PLAYING->PAUSED
	
```



参考资料

https://wenku.baidu.com/view/464fc6728e9951e79b892745.html?sxts=1576827823935

# task调度



# 衬垫pad

对应的英文是pad。

衬垫是指Element跟外部的连接通道。

对应的结构体是GstPad。

pad可以有两种被激活的模式。

1、push。上游element主动push到下游。

2、pull。下游主动从上游去pull。这个比较少用。

pad的有效性

1、永久型。Always。也叫static。在元件创建后就一直存在。gst-inspect-1.0 alsasink。

2、随机型。Sometimes。根据输入数据的不同而产生的pad。看gst-inspect-1.0  qtdemux的属性

3、请求型。On Request。

sink pad一般是永久型的。

而src pad一般是随机型的。

参考资料

http://blog.sina.com.cn/s/blog_53b7ddf00102v5sl.html

# 箱柜bin

箱柜的英文是bin。

是gstreamer里的容器元件。

它用来容纳其他的元件。它本身也是一个GstElement。

一般用到的箱柜有两种：

1、GstPipeline。

2、GstThread。这个用来提供音视频同步能力。

创建了bin之后，可以用gst_bin_add来添加元件到里面来。



# 精灵衬垫ghost pad

ghost pad。

bin作为一个整体，它没有属于自己的sink pad和source pad。

那么就没法跟其他的元件进行交互。

为了解决这个问题，就引入了ghost pad。

它是从bin里面的所有元件里推举出来的。



# GstPipeline

是一个特殊的GstBin。给所有的子元件提供clock。

**也提供一个顶级的bus。**

基于选择的clock计算running_time。

为管道里所有元素计算全局的延迟。



# 缓冲区Buffer

缓冲区包含了创建的pipeline里的数据流。

通常一个source element会创建一个新的buffer。

同时element会把buffer的数据传递给下一个element。

编写应用的时候，不需要关心buffer，框架给我们自动维护。

一个buffer由这些部分组成：

```
1、执行某个内存的指针。
2、内存的大小。
3、buffer的时间戳。
4、引用计数。
```

# 事件Event和查询Query

事件是gstreamer针对media定义的一些概念。

事件和缓冲区一样，在pipeline往上下游传输。

**event是绑定到pad的，**

通过 gst_pad_set_event_function来设置处理函数。

一般元件之间会用event相互传递事件。

应用程序用的event较少，比如seek。



GstQuery是向一个element或者pad查询信息，

比如当前位置，总时间等。

**和事件Event一样，它也是绑定到pad的。**

通过gst_pad_set_query_function来设置某一pad的处理函数。





参考资料

1、

https://blog.csdn.net/yuangc/article/details/119532651

# 简单的mp3播放器

需要使用mad解码插件，这个就需要依赖ugly的插件。



# 自动pipeline

```
#include <gst/gst.h>

int main(int argc, char **argv)
{
	GstElement *pipeline;
	GstBus *bus;
	GstMessage *msg;
	
	gst_init(&argc, &argv);
	//build pipeline
	pipeline = gst_parse_launch("playbin2 uri=http://docs.gstreamer.com/media/sintel_trailer-480p.webm", NULL);
	//start playing
	gst_element_set_state(pipeline, GST_STATE_PLAYING);
	//wait until error or EOS
	bus = gst_element_get_bus(pipeline);
	msg = gst_bus_timed_pop_filtered(bus, GST_CLOCK_TIME_NONE, GST_MESSAGE_ERROR | GST_MESSAGE_EOS);
	//free resource
	if(msg != NULL) {
		gst_message_unref(msg);
	}
	gst_object_unref(bus);
	gst_element_set_state(pipeline, GST_STATE_NULL);
	gst_object_unref(pipeline);
	return 0;
}

```

上面的代码，就是自动搭建了一个pipeline，那么如何手动用element来搭建pipeline呢？

# 手动创建pipeline

下面我们将要学习：

1、什么是element，如何建立一个element。

2、如何在element之间建立连接。

3、如何定制element的行为。

4、如何监视bus上的信息并处理。



gst_element_factory_make  的参数：

第一个是类型，不能随便写。第二个是名字，我们可以自己随便写。

# 动态pipeline

对于视频文件，一般有一路视频和2路音频。

所以需要demuxer来分离。这些蓝色的部分，属于叫做pad。

为什么需要动态的？因为在demuxer把文件解开之前，你不知道文件里有几路视频几路音频。

所以需要先打开文件，分析之后，才知道pipeline具体应该是怎样。





# 时间管理

下面看看如何进行时间管理。

主要是seek和查询。





# 带ui界面的播放器



# 可视化音频





https://gstreamer.freedesktop.org/src/gstreamer/

从这里看，gstreamer现在最新版本是1.16版本。源代码压缩包3.2M。

buildroot里用 的是1.12.4版本。

依赖这些：

```
host-bison \
	host-flex \
	host-pkgconf \
	libglib2 \
```



# 插件分析

看插件名字有4种：

base

good

bad

ugly

这四种名字代表的含义是什么？

0.9版以后的插件可被区分成三种类 (来自电影黄金三镖客"The Good, the Bad and the Ugly"的名字)

先在我的笔记本上编译安装gstreamer。看看会生成哪些库，能不能把这些库打包成一个。不然组织管理是个麻烦事情。

然后写基本的播放音乐的例子。

选择了1.14.4版本。因为当前我手里的buildroot里下载好了这个版本。

```
teddy@teddy-ThinkPad-SL410:~/work/test/gstreamer/code$ tree -L 1
.
├── gst-plugins-bad-1.14.4.tar.xz
├── gst-plugins-base-1.14.4.tar.xz
├── gst-plugins-good-1.14.4.tar.xz
├── gst-plugins-ugly-1.14.4.tar.xz
└── gstreamer-1.14.4.tar.xz
```

5个压缩包。

gstreamer-1.14.4下面有1100个文件左右。

编译：

```
./configure --prefix=/home/teddy/tools/install/gstreamer
make -j2
make install
```

编译只需要2分钟。

安装的目录下是这样：

```
teddy@teddy-ThinkPad-SL410:~/tools/install/gstreamer$ tree -L 2
.
├── bin
│   ├── gst-inspect-1.0
│   ├── gst-launch-1.0
│   ├── gst-stats-1.0
│   └── gst-typefind-1.0
├── include
│   └── gstreamer-1.0
├── lib
│   ├── gstreamer-1.0
│   ├── libgstbase-1.0.la
│   ├── libgstbase-1.0.so -> libgstbase-1.0.so.0.1404.0
│   ├── libgstbase-1.0.so.0 -> libgstbase-1.0.so.0.1404.0
│   ├── libgstbase-1.0.so.0.1404.0
│   ├── libgstcheck-1.0.la
│   ├── libgstcheck-1.0.so -> libgstcheck-1.0.so.0.1404.0
│   ├── libgstcheck-1.0.so.0 -> libgstcheck-1.0.so.0.1404.0
│   ├── libgstcheck-1.0.so.0.1404.0
│   ├── libgstcontroller-1.0.la
│   ├── libgstcontroller-1.0.so -> libgstcontroller-1.0.so.0.1404.0
│   ├── libgstcontroller-1.0.so.0 -> libgstcontroller-1.0.so.0.1404.0
│   ├── libgstcontroller-1.0.so.0.1404.0
│   ├── libgstnet-1.0.la
│   ├── libgstnet-1.0.so -> libgstnet-1.0.so.0.1404.0
│   ├── libgstnet-1.0.so.0 -> libgstnet-1.0.so.0.1404.0
│   ├── libgstnet-1.0.so.0.1404.0
│   ├── libgstreamer-1.0.la
│   ├── libgstreamer-1.0.so -> libgstreamer-1.0.so.0.1404.0
│   ├── libgstreamer-1.0.so.0 -> libgstreamer-1.0.so.0.1404.0
│   ├── libgstreamer-1.0.so.0.1404.0
│   └── pkgconfig
├── libexec
│   └── gstreamer-1.0
└── share
    ├── aclocal
    ├── bash-completion
    ├── gtk-doc
    ├── locale
    └── man
```

二进制文件：

```
├── bin
│   ├── gst-inspect-1.0
│   ├── gst-launch-1.0
│   ├── gst-stats-1.0
│   └── gst-typefind-1.0
```

对应的代码是：

```
./tools/gst-typefind.c
./tools/gst-inspect.c
./tools/gst-launch.c
./tools/gst-stats.c
```

现在编译base plugin。报了这个错误。

```
configure: Requested 'gstreamer-1.0 >= 1.14.4' but version of GStreamer is 1.8.3
configure: error: no gstreamer-1.0 >= 1.14.4 (GStreamer) found
```

需要这样设置一下。

```
export PKG_CONFIG_PATH=/home/teddy/tools/install/gstreamer/lib/pkgconfig
```

这个安装后，目录下的so文件就到了39个了。

在lib/gstreamer-1.0目录下增加了很多，可见这个目录下主要是放插件的。

```
libgstadder.so
libgstalsa.so
libgstapp.so
libgstaudioconvert.so
libgstaudiomixer.so
libgstaudiorate.so
libgstaudioresample.so
libgstaudiotestsrc.so
libgstcoreelements.so
libgstcoretracers.so
libgstencoding.so
libgstgio.so
libgstpbtypes.so
libgstplayback.so
libgstrawparse.so
libgstsubparse.so
libgsttcp.so
libgsttypefindfunctions.so
libgstvideoconvert.so
libgstvideorate.so
libgstvideoscale.so
libgstvideotestsrc.so
libgstvolume.so
```

安装了good plugin后。so数量到了87个。

这个安装后，播放wav可以了。但是播放mp3还是不行。所以还需要继续安装bad的。

但是bad的编译出错了。

我指定了PKG_CONFIG_PATH的。但是看错误，还是试图去系统目录下找。

```
/usr/include/gstreamer-1.0/gst/gl/gstglapi.h:24:32: fatal error: gst/gl/gstglconfig.h: 没有那个文件或目录
```

删掉bad目录，重新解压编译看看。

还是一样的错误。



现在编译的方式走不通。暂时不走了。



通过我写一个mp3界面播放的例子，用ldd查看，可以看出，只用到了libgstreamer-1.0.so这一个so文件。其余都没有用。



# gst-inspect-1.0

打印所有支持的特性。

```
gst-inspect-1.0 -a
总数:3 个插件, 28 个特性
输出内容有1800行左右。
```

查看某一项特性

```
gst-inspect-1.0 fakesrc
```

# gst-launch-1.0

这个是手动用命令来构造一个链路。

构建链路。

用playbin、playbin2、decodebin、decodebin2、uridecodebin这种上传的元件是最简单省事的。

例如，你想要播放一个1.flv文件。

可以这样：

```
gst-launch-1.0 filesrc location=/home/teddy/1.flv ! decodebin ! autovideosink
```

这里使用了3个元件：

1、filesrc。指定它的location属性。

2、decodebin。

3、autovideosink。

还可以用uridecodebin

````
gst-launch-1.0 uridecodebin uri=file:///home/teddy/1.flv ! decodebin ! autovideosink
````

还可以用playbin。

```
gst-launch-1.0 playbin uri=file:///home/teddy/1.flv
```



# 官方示例

在gstreamer-1.14.4/tests/examples目录下。

直接在examples目录下make就可以编译了。

```
.
├── adapter
├── controller
├── helloworld
├── memory
├── netclock
├── ptp
├── stepping
├── streamiddemux
└── streams
```

## HelloWorld

编译是没有报错。

但是运行有错误。无论是播放mp3还是wav，都提示错误。

```
Error: Your GStreamer installation is missing a plug-in.
```

所以我还是把所有的插件先都编译安装了吧。

安装了base和good后，播放wav文件可以了。

播放mp3还是不行。



# 官方教程

我现在使用apt-get安装的来测试gstreamer的基本使用。

这个安装的用gst-inspect-1.0查看

总数:72 个插件, 448 个特性

比我编译的要多一些。



教程地址在这里：

https://gstreamer.freedesktop.org/documentation/tutorials/basic/index.html?gi-language=c

## HelloWorld

这个是播放一个webm的文件。所以需要在图形界面下执行，不然会报错。

```
teddy@teddy-ThinkPad-SL410:~/work/test/gstreamer/test$ ./a.out 
Failed to connect to Mir: Failed to connect to server socket: 没有那个文件或目录
Unable to init server: 无法连接： 拒绝连接
```

图形界面下，可以正常播放一个视频。

看看代码内容。

在gstreamer里，一般情况下，你是需要手动组装各个元件。

但是如果管道逻辑很简单，而且不需要任何高级特性，你可以用这种简单的方式来做。

```
gst_parse_launch("");
```

playbin是一个特殊的元件，它同时是source和sink 元件。

如果你输入的文件不存在，或者有其他的错误，gstreamer会有通知提示。

## 相关概念

这个教程的目的是讲解相关的概念。

还是需要在图形界面下运行，播放窗口产生一些彩色条纹。

一般需要把所有的元件都包含在一个pipeline里面，由pipeline统一管理时钟和消息传递。







# 关于大量动态库的问题

我觉得是这样：

写代码链接的时候，只需要链接libgstreamer.so就够了。

其他的插件，是运行时才会去找的。所以只要在文件系统里放了就好了。我不需要过度关注那一大堆的动态库。



# avs里的使用分析

avs里使用了gstreamer，看看是怎么用的。



# GstClock

这个是用来实现同步机制的。

GstClock是精确到纳秒的计数。

怎么选择时钟源？

从最上游的元件选择。如果管道里所有的元件都不能提供时钟，那么就用系统时钟。

管道发布时钟的时机有：

```
1、管道进入到playing状态。
2、添加一个可以提供时钟的元件时。
3、
```

GStreamer提供了GstQuery的查询机制
用于查询Element或Pad的相应信息。例如：查询当前的播放速率，产生的延迟，是否支持跳转等。可查看GstQuery文档了解所支持的类型。

我们通过查询Pipeline是否支持跳转（seeking），如果支持跳转（有些媒体不支持跳转，例如实时视频），我们会在播放10秒后跳转到其他位置。

position和duration都是以ns为单位的。



# 怎样播放pcm

用gst-launch命令来进行播放。

这个代码是用来增加对pcm的支持的吗？

```
GstCaps* caps = gst_caps_new_empty_simple("audio/x-raw");
    if (!caps) {
        ACSDK_ERROR(LX("setupPipelineFailed").d("reason", "createCapabilityStructFailed"));
        return false;
    }
```

# caps协商

## 协商

Capabilities 协商是为 [GStreamer](https://so.csdn.net/so/search?q=GStreamer&spm=1001.2101.3001.7020) pipeline内的数据流决定适当格式的过程。

理想情况下，协商（也称为“capsnego”）将信息从pipeline中具有信息的那些部分传输到pipeline的那些易扩展的部分，

受pipeline中不易扩展部分的约束。

## 基本规则

必须遵循这些简单的规则：

1. 下游建议格式
2. 上游决定格式

caps协商中使用了 4 种 查询/事件（queries/events ）：

1. GST_QUERY_CAPS：获取可能的格式
2. GST_QUERY_ACCEPT_CAPS：检查格式是否可行
3. GST_EVENT_CAPS：配置格式（下游）
4. GST_EVENT_RECONFIGURE：通知上游可能的新caps



参考资料

1、

https://blog.csdn.net/zk5950886/article/details/118421374

# playbin

playbin是一个元件，可以让我们很快速地实现一个播放器。

playbin是老版本。已经不再维护了。

新的版本是playbin2 。

playbin是一个pipeline，需要一个Application来调用。gst-launch-1.0就是一个Application。

继承关系是：

```
  GObjectClass ->GstObjectClass->GstElementClass->GstBinClass->GstPipelineClass->GstPlayBinClass
```

是高级插件。使用了gstreamer的自动加载（auto plugging）机制。

可以自动根据媒体类型，选择不同的管道播放。

相当于是个万能的播放插件。



# 调试方法

输出环境变量

```
export GST_DEBUG=2
```

然后再执行你的程序，就可以看到相关的日志了。

级别：

```
0：none
1：ERROR
2：warning
3：fixme
4：info
5：debug
6：log
7：trace
8：memdump
```

你可以单独指定某个元件的日志级别。

```
export GST_DEBUG=2,audiotestsrc:6
```

还可以进行通配。

```
export GST_DEBUG=2,audio*:6
```

这样就表示audio开头的元件的日志级别都设置为6 。

```
gst-launch-1.0 --gst-debug-help 
```

这个可以查看有哪些东西可以设置日志的。

怎么自己在开发的时候添加日志呢？

用GST_ERROR这些宏来打印日志。



还有一个有用的调试手段是，把pipeline的图输出。



具体说明在这里。

https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html

# 自己写mp3播放器

代码放在这里：

https://github.com/teddyxiong53/c_code/tree/master/gstreamer_test/MediaPlayer

默认音量是100 。这个不受系统音量的控制好像。

用接口调节音量没用。

无论是在播放状态还是暂停状态。

不是，是我用了adjustVolume接口，传参为80，这个表示的含义是音量在当前的基础上增加80。

用setVolume就可以了。

默认音量是100，是这样定义的。

```
static constexpr uint8_t DEFAULT_VOLUME = 100;
```

# appsrc

这个是起什么作用？

官方说明在这里：

https://gstreamer.freedesktop.org/documentation/app/appsrc.html?gi-language=c#appsrc-page

# 实现视频直播

腾讯的视频基础业务

https://cloud.tencent.com/solution/video



# 资源收集

柳鲲鹏的csdn博客。排名377名。有一些gstreamer相关文章

https://blog.csdn.net/quantum7/column/info/31476



# 播放速度

一般播放速度是1.0，如果要快进，就让播放速度大于1，如果要满放，就让播放速度小于1 。

还可以倒着播放，就是让播放速度为负数。

gstreamer提供了2个事件来处理播放控制：step事件和seek事件。

step就是跳过一些帧。

step事件是一种实现控制播放速度的很方便的方式。但是有一些缺点。

所以现在我们先看seek方式的。



# 音视频同步



# GstStructure

这个是一组键值对。

key是GQuark类型。

value是任意的GType类型。

还有一个名字。

GstStructure被gstreamer很多地方都用到了。

因为它可以很灵活地存储信息。

这个结构体自己没有引用计数，它靠包含自己的类的引用计数来工作。

gst_structure_set_parent_refcount  靠这个函数来做。

字符串编码必须是ascii或utf-8的。其他的编码都不允许。



# 资源收集



https://github.com/jcaden/gst-dynamic-examples

https://github.com/sampleref/gstreamer-cpp-example



#　调试经验

载入libav出错。

```
ERROR: Caught a segmentation fault while loading plugin file:           
/usr/lib/gstreamer-1.0/libgstlibav.so                                   
                                                                        
Please either:                                                          
- remove it and restart.                                                
- run with --gst-disable-segtrap --gst-disable-registry-fork and debug. 
                                                                        
ERROR: Caught a segmentation fault while loading plugin file:           
/usr/lib/gstreamer-1.0/libgstlibav.so                                   
                                                                        
Please either:                                                          
- remove it and restart.                                                
- run with --gst-disable-segtrap --gst-disable-registry-fork and debug. 
```

用下面命令测试，也是这样的打印。

```
gst-inspect-1.0 libav
```

# 配置文件

我现在碰到问题，是gst-play就会导致crash。

发现我改默认的播放设备都没有起作用。

于是看gstalsa下面的代码，发现gst自己有一个配置文件。

gst-soundcard.conf。这个会指定gst使用的hw是哪个。

# 内存分配协商机制

在两个衬垫的caps协商完成之后，元件之间需要确认如何分配[buffer](https://so.csdn.net/so/search?q=buffer&spm=1001.2101.3001.7020)。

本文梳理Gstreamer 内存协商机制，

比如当某元件不能自己分配内存时，如何使用其他元件的分配器。

一般而言，内存分配的协商是在caps协商之后。

根据需求匹配到对应的参数，获取到分配器和内存池，然后才能开始数据传输。









参考资料

1、

https://blog.csdn.net/yuangc/article/details/122069594



# queue2

直接播放Internet上的文件而不在本地保存就被称为流播放。

我们在前面教程里已经这样做过了，使用了http://的URL。

本教程展示的是在播放流的时候需要记住的几个点，特别是：

   如何设置缓冲

   如何从打断中恢复（因为失去了时钟）

当在播放流的时候，

一旦从网络上取到媒体数据块就会进行解码和放入显示队列。

这意味着如果网络来的数据延迟了，那么显示队列就可能没有数据，播放就会停下来。

   解决这个问题的办法是建立缓冲，

这就是说，在开始播放前允许队列里已经存储了一些数据。

这样的话，播放虽然晚了一点开始，但如果网络有什么延时，那么还有一定的缓冲数据可以播放。



这个方案已经在GStreamer里面实现了，

但前面的教程中没有涉及到这个方面。

有些element，像在playbin2里面用到的queue2和multiqueue，

都可以建立自己的缓冲然后根据缓冲的等级发送消息到总线上。

一个应用如果希望能更好的适应各种网络环境，那么就该关注这些消息，当缓冲等级低到一定程度时就要暂停播放。



为了在多个sink中同步，我们使用了一个全局的时钟。

这个时钟是GStreamer在所有的可以提供时钟的element中选出来的。

在某些情况下，例如，一个RTP资源切换流或者更换输出设备，那么时钟就可能丢失。

这时就需要重新建立一个时钟，这个过程在本教程会解释一下。



当时钟丢失的时候，应用会从总线上得到一个消息。

要建立一个新的时钟，应用仅仅把pipeline设置到PAUSED状态然后重新置成PLAYING即可。



# 常用命令





参考资料

1、

https://blog.csdn.net/hyl999/article/details/121486320



# gstreamer vs ffmpeg

目前，很大部分音视频编解码应用开发都是基于ffmpeg框架。

ffmpeg API简单 上手快，也迅速成为了国内视频相关开发者的首选开源库。

而gstreamer由于其复杂难懂，学习成本高，似乎在国内使用的人越来越少.

于是乎， 有人认为 熟悉ffmpeg API就可以在音视频流媒体开发畅通无阻了。

个人认为，不是这样。

如果你只想写一个简单的音视频应用，那么也许ffmpeg再合适不过，

因为它的API封装了所有细节，很多时候几个API组装就完事了。

可是ffmpeg只在格式处理 编解码 转码作了比较好的封装，

但却不够模块化。

如果你想基于ffmpeg做一些人工智能、视频分析相关的高级前沿扩展，会显得力不从心。

而gstreamer不同，

它是高度模块化的管线驱动式的媒体框架，扩展性极强。

理论上，不只是媒体流，gstreamer可以扩展为处理任何一种数据流。

因此，架构上,gstreamer更强大，扩展性更强。

ffmpeg的核心转码功能也可以作为gstreamer的插件扩展，

可以认为gstreamer可以整合ffmpeg的功能，并大大超越ffmpeg所能做的范畴。



 AI时代，gstreamer依托于不断更新丰富的各种AI插件,大有可为。

一个典型的例子是英伟达公司基于gstreamer推出了业界首个视频分析系统框架:DeepStream







参考资料

1、Gstreamer被ffmpeg或其他媒体框架淘汰了吗？

https://blog.csdn.net/acs713/article/details/91406931

# preroll的概念

在 GStreamer 中，"preroll" 是指在开始播放媒体流之前进行的一些准备工作，包括填充数据缓冲区和启动管道中的元件。这是为了确保在用户开始观看或听取媒体之前，系统已经准备好了足够的数据以避免播放中断。

以下是 preroll 的一些关键概念：

1. **数据缓冲**：在播放媒体之前，必须先填充数据缓冲区，以便流畅地播放。这包括从文件、网络流或其他数据源中读取数据，并将其存储在内存中或传输到 GStreamer 管道中的适当位置。

2. **管道准备**：在启动 GStreamer 管道之前，必须确保所有的元件（例如解码器、解复用器、音频/视频渲染器）已经初始化并准备好接受数据。这可能包括打开文件、分配内存、建立网络连接等。

3. **时钟同步**：在 preroll 过程中，还需要确保管道中的各个元件都采用相同的时钟以保持时间同步。这对于音视频同步和播放控制非常重要。

4. **启动管道**：一旦 preroll 完成，管道就可以启动，媒体播放即可开始。这包括将数据流动起来，将数据传递给渲染器，以便用户可以观看或听取媒体。

Preroll 是为了确保在用户按下播放按钮或请求播放媒体时，系统不会出现播放中断或等待加载数据的情况。它在播放和流媒体应用中非常常见，以提供良好的用户体验。在 GStreamer 中，preroll 是一个重要的概念，用于处理数据准备和初始化管道的过程。

# gstregistry

`GstRegistry` 是 GStreamer 多媒体处理框架中的一个重要组件，

用于管理和维护各种 GStreamer 插件的注册信息。

GStreamer 是一个用于构建多媒体应用程序和流媒体处理的开源框架，它包括各种插件（如解码器、编码器、过滤器等），

**而 `GstRegistry` 负责跟踪这些插件的注册和状态。**

以下是 `GstRegistry` 的一些关键功能和用途：

1. **插件注册**：`GstRegistry` 负责注册和管理可用的 GStreamer 插件。插件可以是解码器、编码器、元件（elements）、效果、过滤器等。通过注册，GStreamer 可以知道哪些插件可供使用。

2. **插件发现**：`GstRegistry` 可以在系统中搜索并发现可用的插件。这使得 GStreamer 可以自动检测和利用在系统中安装的插件。

3. **版本控制**：`GstRegistry` 也跟踪每个插件的版本信息，以确保正确的插件版本被加载和使用。这对于确保兼容性非常重要。

4. **状态管理**：`GstRegistry` 跟踪每个插件的状态，包括已注册、已加载、已启用等状态。这有助于确定插件是否可以使用以及它们的加载状态。

5. **插件信息查询**：开发者可以查询 `GstRegistry` 以获取有关特定插件的信息，如插件的名称、描述、作者、版本等。这对于调试和配置插件非常有用。

6. **插件加载和卸载**：`GstRegistry` 允许开发者加载和卸载插件，以便将它们添加到 GStreamer 管道中或从中移除。

7. **多种后端支持**：`GstRegistry` 可以支持多种后端，包括文件系统、注册表、数据库等，以存储插件信息。

总之，`GstRegistry` 在 GStreamer 中扮演着重要的角色，使得多媒体应用程序能够动态地管理和利用各种插件。这有助于构建灵活、可扩展和高效的多媒体应用程序，而无需显式加载和管理每个插件。

# gststructure

`GstStructure` 是 GStreamer（一个用于处理多媒体数据的开源框架）中的一种数据结构，

==用于表示元数据信息或键值对的集合。==

它是一个灵活的方式来描述多媒体数据流的属性、配置和参数。

`GstStructure` 的主要特点包括：

1. **键值对**：`GstStructure` 是由键值对组成的集合，其中键是字符串，值可以是各种数据类型，如整数、浮点数、字符串等。

2. **嵌套结构**：`GstStructure` 可以包含嵌套的子结构，允许更复杂的数据结构表示。

3. **数据类型不限定**：每个键值对的值可以是任意数据类型，因此 `GstStructure` 可以用于表示各种多媒体属性和配置信息。

4. **可扩展性**：开发者可以根据需要动态添加或删除键值对，使其非常灵活。

5. **用途广泛**：`GstStructure` 通常用于描述多媒体数据流的参数、元数据、媒体格式信息等，以便在 GStreamer 管道中传递和配置。

使用 `GstStructure` 时，通常会通过以下步骤：

1. 创建一个新的 `GstStructure` 对象。

2. 添加键值对，其中键是字符串，值可以是各种数据类型。

3. 在 GStreamer 管道中使用或传递 `GstStructure` 对象，以描述和配置多媒体数据流的属性。

4. 根据需要访问、查询或修改 `GstStructure` 中的键值对。

下面是一个示例，演示如何创建一个 `GstStructure` 对象，并向其添加一些键值对：

```c
GstStructure *structure = gst_structure_new("video-info",
    "width", G_TYPE_INT, 1920,
    "height", G_TYPE_INT, 1080,
    "framerate", GST_TYPE_FRACTION, 30, 1,
    "codec", G_TYPE_STRING, "H.264",
    NULL);

// 访问键值对
gint width;
gint height;
gst_structure_get_int(structure, "width", &width);
gst_structure_get_int(structure, "height", &height);
```

在这个示例中，我们创建了一个名为 "video-info" 的 `GstStructure`，并添加了一些键值对，以描述视频流的属性，如宽度、高度、帧率和编解码器。后续可以根据需要访问这些键值对的值。

总之，`GstStructure` 是 GStreamer 中用于表示多媒体数据流属性和配置信息的通用数据结构。它在多媒体应用程序和流媒体处理中广泛使用。

# gstatomicqueue

`GstAtomicQueue` 是 GStreamer 中的一个线程安全的队列数据结构，

用于多线程环境下的数据传输和同步。

GStreamer 是一个用于多媒体处理的开源框架，而 `GstAtomicQueue` 为开发者提供了一个线程安全的方式来传递和共享数据。

`GstAtomicQueue` 的主要特点包括：

1. **线程安全**：`GstAtomicQueue` 被设计为可以安全地在多线程环境中使用。多个线程可以同时对队列进行入队和出队操作，而不会导致数据竞争或不一致性。

2. **先进先出（FIFO）**：队列遵循先进先出的原则，确保元素按照它们的入队顺序被出队。

3. **阻塞和非阻塞操作**：`GstAtomicQueue` 支持阻塞和非阻塞的入队和出队操作。这使得它适用于各种多线程场景，包括生产者-消费者问题的解决。

4. **用途广泛**：`GstAtomicQueue` 可用于多种多媒体数据传输和同步任务，如音频、视频、流媒体处理等。

以下是一个示例，展示如何在 GStreamer 中使用 `GstAtomicQueue`：

```c
GstAtomicQueue *queue = gst_atomic_queue_new();

// 在生产者线程中入队数据
gpointer data = some_data;
gst_atomic_queue_push(queue, data);

// 在消费者线程中出队数据
gpointer retrieved_data = gst_atomic_queue_pop(queue);
```

在这个示例中，我们创建了一个 `GstAtomicQueue` 对象，然后在生产者线程中使用 `gst_atomic_queue_push` 将数据入队，然后在消费者线程中使用 `gst_atomic_queue_pop` 出队数据。这可以安全地在多线程环境中传递数据。

总之，`GstAtomicQueue` 是 GStreamer 中用于线程安全数据传输和同步的队列数据结构。它允许多线程同时进行数据入队和出队操作，并遵循先进先出原则，使其适用于多媒体处理和流媒体应用程序中的多线程场景。

# gstminiobject

`GstMiniObject` 是 GStreamer 多媒体处理框架中的一个基本数据结构，

用于表示所有 GStreamer 对象的通用基类。

GStreamer 是一个开源多媒体框架，

用于构建多媒体应用程序和流媒体处理。

`GstMiniObject` 提供了 GObject 类型系统的一些功能，==但比完整的 GObject 更轻量和高效。==

以下是一些关键特点和概念，涉及到 `GstMiniObject`：

1. **基类**：`GstMiniObject` 是所有 GStreamer 对象的基类。这包括音频和视频数据流、媒体文件、媒体管道等。

2. **轻量**：相对于完整的 GObject，`GstMiniObject` 更轻量。这意味着它占用更少的内存和资源，适用于需要高性能的多媒体处理。

3. **引用计数**：`GstMiniObject` 支持引用计数，允许开发者跟踪对象的引用，确保在不再需要时正确释放资源。

4. **自定义类型**：每个 `GstMiniObject` 对象都有一个类型，用于确定其类别，例如视频流还是音频流。这有助于多媒体处理框架正确处理不同类型的对象。

5. **快速分配和释放**：相对于完整的 GObject，`GstMiniObject` 具有更快的分配和释放速度，这对于高性能多媒体处理至关重要。

6. **继承**：开发者可以使用 `GstMiniObject` 作为其他自定义对象的基类，以继承引用计数和其他功能。

在 GStreamer 中，开发者通常不会直接操作 `GstMiniObject` 对象，而是使用特定的 GStreamer 插件、元素和框架。这些插件和元素通常使用 `GstMiniObject` 作为它们的基类，以获得引用计数和资源管理的优势。

总之，`GstMiniObject` 是 GStreamer 多媒体处理框架中的一个基本数据结构，用于表示多媒体对象的通用基类。它支持引用计数和轻量级资源管理，适用于高性能多媒体处理应用程序。

# GstAllocator

`GstAllocator` 是 GStreamer 多媒体处理框架中的一个关键组件，

用于内存分配和管理。



`GstAllocator` 用于为多媒体数据（如音频、视频）分配内存，

并提供了一种标准化的方式来管理和共享内存。



以下是 `GstAllocator` 的一些关键特点和概念：

1. **内存分配**：`GstAllocator` 允许应用程序为多媒体数据分配内存。这些数据可以包括音频采样、视频帧等。

2. **内存管理**：`GstAllocator` 负责分配和管理内存块。它提供了一种标准化的方式来跟踪已分配内存的状态，以确保及时释放和回收内存。

3. **内存共享**：多个组件和线程可能需要访问相同的多媒体数据。`GstAllocator` 允许多个用户共享相同的内存块，而不需要多次复制数据。

4. **内存池**：`GstAllocator` 可以管理内存池，以提高内存分配和释放的效率。内存池允许多次分配和释放内存而不需要频繁地从系统内核分配新的内存块。

5. **自定义分配器**：开发者可以创建自定义的内存分配器，以满足特定的需求。这使得可以选择不同的内存分配策略，如物理内存分配或共享内存分配。

使用 `GstAllocator` 时，通常会涉及以下操作：

1. 创建 `GstAllocator` 对象，或者使用默认的内存分配器。

2. 使用分配器分配内存块，通常为多媒体数据。

3. 在适当的时候释放内存块，以防止内存泄漏。

4. 如果需要，共享内存块以避免数据复制和提高性能。

总之，`GstAllocator` 是 GStreamer 多媒体处理框架中的一个组件，用于内存分配和管理，以满足多媒体数据的需求。它提供了一种标准化的方式来分配、管理和共享内存，以支持高性能多媒体应用程序的开发。



# GstNetTimeProvider

`GstNetTimeProvider` 是 GStreamer 中的一个组件，用于处理时间同步和时钟管理。

 `GstNetTimeProvider` 用于==协调多个多媒体流或设备的时间==，以确保它们能够同步播放或录制。

以下是 `GstNetTimeProvider` 的一些关键特点和概念：

1. **时间同步**：在多媒体处理中，特别是在音频和视频流中，时间同步非常重要。`GstNetTimeProvider` 用于确保多个设备或多媒体流之间的时间同步，以便它们可以协调播放或录制操作。

2. **网络协议**：`GstNetTimeProvider` 可以使用网络协议来获取时间信息，例如 Network Time Protocol (NTP)。这允许多媒体设备或应用程序通过网络同步它们的时间。

3. **时间基准**：`GstNetTimeProvider` 可以为多媒体流或设备提供时间基准，使它们能够根据相同的时间线工作。

4. **GstClock 集成**：`GstNetTimeProvider` 通常与 GStreamer 中的 `GstClock` 一起使用，以提供时间信息。`GstClock` 用于管理时间和时钟，而 `GstNetTimeProvider` 可以与之协同工作，以确保时间同步。

5. **自定义实现**：开发者可以自定义实现 `GstNetTimeProvider`，以满足特定的时间同步需求。这使得它非常灵活，可以适应不同的应用场景。

使用 `GstNetTimeProvider` 通常涉及以下操作：

1. 创建或配置 `GstNetTimeProvider` 对象。

2. 获取或同步时间信息，通常通过网络协议。

3. 向 GStreamer 中的多媒体流或设备提供时间信息。

4. 协调多个多媒体流或设备，以确保它们在相同的时间线上运行。

总之，`GstNetTimeProvider` 是 GStreamer 多媒体处理框架中的一个组件，用于处理时间同步和时钟管理，以确保多媒体流或设备能够同步播放或录制。它在多媒体处理应用程序中非常有用，特别是在需要协调多个多媒体流或设备的场景中。

# GstStaticPadTemplate

`GstStaticPadTemplate` 是 GStreamer 多媒体处理框架中的一种数据结构，

用于定义元素（Element）的静态插孔模板。

GStreamer 是一个用于构建多媒体应用程序和流媒体处理的开源框架，

而 `GstStaticPadTemplate` 用于描述元素的输入和输出插孔（Pad），这些插孔用于数据流的连接。

以下是 `GstStaticPadTemplate` 的一些关键特点和概念：

1. **静态模板**：`GstStaticPadTemplate` 是一个静态的数据结构，它在元素的代码中定义，通常在编译时创建。这与动态插孔模板不同，后者可以在运行时创建和修改。

2. **插孔类型**：`GstStaticPadTemplate` 包含了插孔的名称、方向（输入或输出）、数据类型（数据流的类型）等信息。这有助于描述元素可以连接的插孔。

3. **插孔模板的用途**：`GstStaticPadTemplate` 用于定义元素的插孔模板，以使元素的输入和输出能够与其他元素的插孔匹配。这有助于构建多媒体处理管道，其中不同元素之间可以传递数据。

4. **复用和共享**：多个元素可以共享相同的插孔模板，这有助于提高元素的复用性和互操作性。

使用 `GstStaticPadTemplate` 通常涉及以下操作：

1. 在元素的代码中定义一个或多个 `GstStaticPadTemplate` 对象，描述元素的插孔模板。

2. 当连接多个元素以构建多媒体处理管道时，插孔模板用于确保插孔之间的数据流是兼容的。

3. 插孔模板也用于在 GStreamer 调度器中为数据流的传输提供指导，以确保数据正确流动。

总之，`GstStaticPadTemplate` 是 GStreamer 多媒体处理框架中的一个数据结构，用于定义元素的插孔模板，以支持多媒体数据流的连接和交换。这有助于构建复杂的多媒体处理管道和提高元素的复用性。

# GstEventType

`GstEventType` 是 GStreamer 多媒体处理框架中的一个枚举类型，用于表示不同类型的事件。 



`GstEventType` 枚举包含了一系列用于描述不同事件类型的常量值。

这些事件类型可以用于与多媒体数据流的处理和控制相关的操作。

以下是一些常见的 `GstEventType` 值和其对应的事件类型：

1. **GST_EVENT_EOS**：表示多媒体流已经结束，即到达了流的末尾（End of Stream）。

2. **GST_EVENT_FLUSH_START**：表示多媒体流的刷新操作即将开始，用于清空缓冲区。

3. **GST_EVENT_FLUSH_STOP**：表示多媒体流的刷新操作已经完成，数据流可以继续。

4. **GST_EVENT_SEEK**：表示进行媒体流的寻找（Seek）操作，用于跳转到流中的特定位置。

5. **GST_EVENT_CAPS**：表示多媒体流的格式或能力已经发生变化，需要重新协商流格式。

6. **GST_EVENT_SEGMENT**：表示多媒体流的特定部分（片段）即将被处理，用于指定处理流的范围。

7. **GST_EVENT_TAG**：表示多媒体流的元数据标签，用于携带流的附加信息，如标题、作者等。

8. **GST_EVENT_BUFFERSIZE**：表示多媒体流的缓冲区大小已发生变化，通常用于通知流的数据块大小。

9. **GST_EVENT_CUSTOM_UPSTREAM** 和 **GST_EVENT_CUSTOM_DOWNSTREAM**：表示自定义事件，可以用于特定应用程序或插件发送和接收事件。

这些事件类型允许应用程序或插件在多媒体处理过程中进行控制、通信和协商。通过发送和接收这些事件，可以实现多媒体流的管理、控制和协商，以满足不同应用场景的需求。

总之，`GstEventType` 是 GStreamer 多媒体处理框架中的一个枚举类型，用于表示不同类型的事件，这些事件允许控制和协商多媒体数据流的处理和行为。

# 参考资料

1、GStreamer基础教程01——Hello World

https://blog.csdn.net/sakulafly/article/details/19398257

7、Gstreamer 编译安装

https://blog.csdn.net/jintaofu/article/details/51744706

8、交叉编译gstreamer

https://blog.csdn.net/naaaa/article/details/25132047

9、gstreamer，vlc，ffmpeg比较

https://blog.csdn.net/rocvfx/article/details/51577322

10、用 GStreamer 简化 Linux 多媒体开发

https://www.ibm.com/developerworks/cn/linux/l-gstreamer/

11、gst-inspect-1.0

https://gstreamer.freedesktop.org/documentation/tools/gst-inspect.html

12、gstreamer插件指南

https://blog.csdn.net/sinat_28502203/article/details/46010485

13、GStreamer 编写一个简单的MP3播放器

https://blog.csdn.net/wangpengqi/article/details/8589645

14、

https://blog.csdn.net/chicher123/article/details/67640549

15、Read and write raw PCM using GStreamer

https://blog.csdn.net/brandon2015/article/details/50457900

16、深入浅出gstreamer开发

这个作者Smith先生的文章不错。值得看。

https://blog.csdn.net/acs713/article/details/7777946

17、Gstreamer之Caps协商

https://blog.csdn.net/hiccupzhu/article/details/17918045

18、GStreamer播放教程01——playbin2的使用

https://blog.csdn.net/sakulafly/article/details/22216775

19、gstreamer让playbin能够播放rtp over udp流数据

https://www.cnblogs.com/shakin/p/6142219.html

20、gst-launch & gst-inspect 介绍

https://www.cnblogs.com/testplay/archive/2013/01/27/2879047.html

21、中文翻译的教程。排版挺好的。

https://www.cnblogs.com/xleng/p/11008239.html

22、使用 GStreamer appsrc 等插件实现视频音频混流，录制和推流

http://www.mamicode.com/info-detail-2163963.html

23、

https://blog.csdn.net/quantum7/article/details/82250524

24、gstreamer简介

这篇文章很好。

https://blog.csdn.net/evsqiezi/article/details/82466267

25、Gstreamer的音视频同步

https://blog.csdn.net/maeom/article/details/7729840

26、gstreamer

这个的图不错。文章也不错。

https://www.jianshu.com/p/09b98a7e1395

27、这个是官方插件文档，组织地非常好。

https://www.freedesktop.org/software/gstreamer-sdk/data/docs/latest/gstreamer-plugins-0.10/index.html