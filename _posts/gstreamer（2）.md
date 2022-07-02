---
title: gstreamer（2）
date: 2020-01-06 13:58:08
tags:
	- gstreamer

---

1

# core api

## 运行和调试gstreamer应用

环境变量

```
GST_PLUGIN_SYSTEM_PATH
GST_PLUGIN_SYSTEM_PATH_1_0
GST_PLUGIN_PATH 
GST_DEBUG
	从0到9
	0 ： none
	1：error
	2：warning
	5：debug
GST_DEBUG_COLOR_MODE
	on
	off
	auto == on
	disable == off
	unix
GST_DEBUG_OPTIONS
GST_DEBUG_DUMP_DOT_DIR
GST_REGISTRY

```

## gstreamer初始化相关api

就关注gst_init就够了。

## GstObject

作为gstreamer库的root object。

目前仅仅是GInitialUnowned的简单包装。



## GstMiniObject

是一个简单的结构体，用来实现引用计数类型。



## GstAllocator

这个是用来分配内存的方式。其实没有用。是用系统默认的方式进行分配的。

这个是第一个正式的类。

从这里可以看出文档的组织方式：

```
结构体
	1、继承关系图。
	2、成员变量
	3、对应的class结构体
	4、methods
		method是相当于类的方法。
		特点是第一个参数是Xxx *指针。
	5、functions
		参数第一个不是Xxx*指针。
	6、virtual methods
		是指在对应的class结构体里的函数指针。
	7、函数宏。
		GST_XXX_CAST这种。
	8、枚举。
	9、宏定义。
	10、构造函数。
		就是返回Xxx*指针的函数。一般以new作为后缀。
```

## GstBin

GstBin是一个特殊的element，它是一个容器，可以放入其他的element。并且把放入的element作为一个group来看待。

子element的pad可以被ghost到bin上，这样就可以提供一个更高层次的抽象。

一个GstBin通过gst_bin_new来创建。

如果你要创建一个顶层bin，那么你就需要用GstPipeline。因为一个普通的bin，没有bus。

在bin创建后，你可以用gst_bin_add往里面放入element。

通过gst_bin_remove来移除element。

可以通过gst_bin_get_by_name来从bin里拿到。

可以用gst_bin_iterate_elements来遍历所有的element。

在一个element被添加到bin的时候，bin就是发出一个element-added的signal。

类似的，在一个element从bin里被移除的是，bin会发出一个element-removed的signal。



GstBin后拦截子element发出的GstMessage。并对下面这些message进行了默认实现。

```
EOS
	这个消息是被playing状态的sinks发出。如果所有的sinks都发出了这个消息，那么bin就会把EOS对外抛出。
SEGMENT_START
	只是收集，从来不对外抛出。
SGETMENT_DONE
DURATION_CHANGED
CLOCK_LOST
CLOCK_PROVIDE
OTHERS
	直接对外抛出。
```

GstBin接收这些query。

```
duration 
position
```



## GstBuffer

GstBuffer是gstreamer的数据传输的基本单元。

包括了时间、offset以及其他的metadata，这些都跟GstMemory有关系。

通过gst_buffer_new创建。创建后，一般是接着分配一块内存给它。

这么做：

```
GstBuffer *buffer;
GstMemory *memory;
int size, w, h, bpp;
size = w*h*bpp;
buffer = gst_buffer_new();
memory = gst_allocator_alloc(NULL, size, NULL);
gst_buffer_insert_memory(buffer, -1, memory);
```

GstBuffer包括一个GstMemory的链表。

可以通过gst_buffer_n_memory来查看这个链表的长度。

一个buffer，一般具有时间戳、duration，但都不是必须的。

时间戳和duration都是以ns为单位的。

一个buffer的dts，表示buffer应该被界面的时机。一般是单调递增的。

而pts这个时间戳，表示buffer内容被presentation的时机。不总是单调递增的。

一个buffer可能有start和end的offset。

这个是跟媒体类型相关的。

对于video类型，start offset一般是frame number。

对于audio类型，start offset一般是指已经产生的采样数。

对于压缩数据，start offset则表示字节偏移。

start和end 都可以被设置为GST_BUFFER_OFFSET_NONE。

## GstBus

GstBus通过fifo的方式传递消息。从GstTask传递到应用层。

提供基于GSource的通知支持。这样就可以在mainloop里处理率消息了。

可以用gst_bus_async_signal_func来把消息转成signal。

```
gst_bus_post
	发出消息。
gst_bus_peek和gst_bus_pop
	获取消息。
gst_bus_poll
	查询消息。
	
```

GstBus结构体定义很简单，就继承GstObject，然后一个私有数据指针。

## GstCaps

结构体很简单，就包装了GstMiniObject。

```
struct _GstCaps {
  GstMiniObject mini_object;
};
```

用来描述媒体类型。

是由GstStructure数组组成的。

不能嵌套，只能一层GstCaps结构体。

构造函数有多个：

```
gst_caps_new_any()
	any表示兼容任意媒体类型。
gst_caps_new_simple 
	一般用这个。
```



## GstStructure

这个表示键值对容器。

key是GQuark的，value是任意的GType的。

还有一个name属性。

被广泛使用，用来存储各种信息。灵活也有扩展性。

没有引用计数，不单独存在，都是嵌入在其他的结构体里。



## GstClock

gstreamer使用一个global的clock来同步一个pipeline里的所有element。

GstClock返回一个单调递增的时间，通过gst_clock_get_time函数。

一般是讨论相对时间，所以一个时间值是没有意义的。

所有的renderers通过buffer的时间戳来同步clock。



## GstElement



## GstElementFactory

这个定义是在gst_private.h里。

继承自GstPluginFeature。

用来创建element实例。

可以被添加到GstPlugin，因为它继承了GstPluginFeature。



## GstEvent

提供了工厂方法用来构造event去send，以及解析收到的event。

有的事件只能upstream，有的事件只能downstream。有的两个方向都可以。

大部分的事件api，都是被plugin内部使用的，应用只需要使用一个接口：gst_event_new_seek。

一个例子：

```
GstEvent *event;
gboolean result;
event = gst_event_new_seek(
	1.0,  GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH,
	GST_SEEK_TYPE_SET, 2*GST_SECOND, 
	GST_SEEK_TYPE_SET, 5*GST_SECOND
);
result = gst_element_send_event(pipeline, event);
if(!result) {
	printf("send fail\n");
}
```



## GstFormat

向gstreamer注册一个新的format。

format可以用来seek或者查询。

GstFormat是一个枚举。

有bytes、time、buffers、percent这些类型。



## GstMemory

一个简单的引用技术对象，包装了一块内存。



## GstPad

pad可以有template，也可以没有。

```
有template，用gst_pad_new_from_template
没有template，用gst_pad_new
```

要让数据可以流动，需要gst_pad_set_active。



## GstPadTemplate

template描述一个pad可以处理的媒体类型。

pad和template通过GstCaps联系起来。



## GstPipeline

GstPipeline是GstBin的子类。

多了clock和bus这2个东西。



# 功能库api

## 音频相关

属于base插件，libgstaudio.so。

base目录下的gst-libs下面。



# 手册

gstreamer 是一个非常强大且万能的框架，用来插件流媒体应用。

gstreamer的优点来自它的模块化。

可以集成大量的新的模块。

模块化带来了设计的复杂性，让写代码不那么容易。

这个手册的目的就是让你理解gstreamer的框架，从而能够基于它编写应用。

第一章会聚焦在开发一个简单的audio player。用来帮助你理解相关的概念。

主要分为下面4个部分：

```
关于gstreamer
	概览。讨论设计哲学。
构建应用。
高级概念。
	
高级接口
	playbin
	decodebin
```

```
#include <gst/gst.h>
#include <glib.h>


static void on_pad_added(GstElement *element, GstPad *pad, gpointer data)
{
	GstPad *sinkpad;
	GstElement *decoder = (GstElement *)data;
	g_print("dynamic pad created, link demuxer and decoder\n");
	sinkpad = gst_element_get_static_pad(decoder, "sink");
	gst_pad_link(pad, sinkpad);
	gst_object_unref(sinkpad);
}

int main(int argc, char **argv)
{
	GMainLoop *mainloop;
	GstElement *pipeline, *source, *demuxer, *decoder, *conv, *sink;
	GstBus *bus;
	guint bus_watch_id;

	gst_init(NULL, NULL);
	mainloop = g_main_loop_new(NULL, FALSE);
	if(argc != 2) {
		g_error("usage: %s filename", argv[0]);
		return -1;
	}
	pipeline = gst_pipeline_new("audio-player");
	printf("pipeline:%p\n", pipeline);
	source = gst_element_factory_make("filesrc", "file-source");
	printf("source:%p\n", source);
	demuxer = gst_element_factory_make("oggdemux", "ogg-demuxer");
	printf("demuxer:%p\n", demuxer);
	decoder = gst_element_factory_make("vorbisdec", "vorbis-decoder");
	printf("decoder:%p\n", decoder);
	conv = gst_element_factory_make("audioconvert", "converter");
	printf("conv:%p\n", conv);
	sink = gst_element_factory_make("autoaudiosink", "audio-output");
	printf("sink:%p\n", sink);
	if(!pipeline || !source || !demuxer || !decoder || !conv || !sink) {
		g_error("one element is null\n");
		return -1;
	}
	g_object_set(G_OBJECT(source), "location", argv[1], NULL);
	gst_bin_add_many(GST_BIN(pipeline), source, demuxer, decoder, conv, sink, NULL);
	gst_element_link(source, demuxer);
	gst_element_link_many(decoder, conv, sink, NULL);
	g_signal_connect(demuxer, "pad-added", G_CALLBACK(on_pad_added), decoder);

	g_print("now playing ...\n");
	gst_element_set_state(pipeline, GST_STATE_PLAYING);

	g_main_loop_run(mainloop);
}
```





# 参考资料

1、

https://gstreamer.freedesktop.org/documentation/gstreamer/gi-index.html?gi-language=c