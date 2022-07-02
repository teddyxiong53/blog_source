---
title: gstreamer（1）
date: 2018-11-26 17:12:24
tags:
	- gstreamer
typora-root-url: ..\
---

1

gstreamer是gnome桌面环境推荐的流媒体应用框架。

基于插件和管道的设计风格。

基于glib进行开发，所以与一般的C语言写法有些不同。

gstreamer是一个创建流媒体应用程序的框架。

其基本设计思想来自于俄勒冈研究生学院有关视频管道的创意。

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





#元件GstElement

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



#衬垫pad

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

# 事件Event



# 简单的mp3播放器

需要使用mad解码插件，这个就需要依赖ugly的插件。



#自动pipeline

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

#手动创建pipeline

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

#实现视频直播

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