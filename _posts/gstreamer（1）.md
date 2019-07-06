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



#元件

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



#衬垫

对应的英文是pad。

衬垫是指Element跟外部的连接通道。

对应的结构体是GstPad。



# 箱柜

箱柜的英文是bin。

是gstreamer里的容器元件。

它用来容纳其他的元件。它本身也是一个GstElement。

一般用到的箱柜有两种：

1、GstPipeline。

2、GstThread。这个用来提供音视频同步能力。

创建了bin之后，可以用gst_bin_add来添加元件到里面来。



# 精灵衬垫

ghost pad。



# 简单的mp3播放器



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

```
#include <gst/gst.h>

int main(int argc, char **argv)
{
	GstElement *pipeline, *source, *sink;
	GstBus *bus;
	GstMessage *msg;
	GstStateChangeReturn ret;
	gst_init(&argc, &argv);
	source = gst_element_factory_make("videotestsrc", "source");
	sink = gst_element_factory_make("autovideosink", "sink");
	pipeline = gst_pipeline_new("test-pipeline");
	
	if(!source || !sink || !pipeline) {
		return -1;
	}
	gst_bin_add_many(GST_BIN(pipeline), source, sink, NULL);
	if(gst_element_link(source, sink) != TRUE) {
		return -1;
	}
	g_object_set(source, "pattern", 0, NULL);
	int ret = gst_element_set_state(pipeline, GST_STATE_PLAYING);
	bus = gst_element_get_bus(pipeline);
	msg = gst_bus_timed_pop_filtered(bus, GST_CLOCK_TIME_NONE, GST_MESSAGE_ERROR | GST_MESSAGE_EOS);
	if(msg) {
		gst_message_unref(msg);
	}
	gst_object_unref(bus);
	gst_element_set_state(pipeline, GST_STATE_NULL);
	gst_object_unref(pipeline);
	return 0;
}
```

gst_element_factory_make  的参数：

第一个是类型，不能随便写。第二个是名字，我们可以自己随便写。

# 动态pipeline

对于视频文件，一般有一路视频和2路音频。

所以需要demuxer来分离。这些蓝色的部分，属于叫做pad。

![](./images/gstreamer之视频pipeline.png)



```
#include <gst/gst.h>

typedef struct _CustomData {
	GstElement* pipeline;
	GstElement* source;
	GstElement* convert;
	GstElement* sink;
} CustomData;

static void pad_added_handle(GstElement* src, GstPad *pad, CustomData* data);

int main(int argc, char **argv)
{
	CustomData data;
	GstBus *bus;
	GstMessage *msg;
	GstStateChangeReturn ret;
	
	gboolean terminate = FALSE;
	gst_init(&argc, &argv);
	
	data.source = gst_element_factory_make("uridecodebin", "source");
	data.convert = gst_element_factory_make("audioconvert", "convert");
	data.sink = gst_element_factory_make("autoaudiosink", "sink");
	data.pipeline = gst_pipeline_new("test-pipeline");
	
	gst_bin_add_many(GST_BIN(data.pipeline), data.source, data.convert, data.sink);
	gst_element_link(data.convert. data.sink);
	g_object_set(data.source, "uri", "http://docs.gstreamer.com/media/sintel_trailer-480p.webm", NULL);
	g_signal_connect(data.source, "pad-added", G_CALLBACK(pad_added_handle), &data);
	gst_element_set_state(data.pipeline, GST_STATE_PLAYING);
	
	bus = gst_element_get_bus(data.pipeline);
	do {
		msg = gst_bus_timed_pop_filtered(bus, GST_CLOCK_TIME_NONE, GST_MESSAGE_ERROR | GST_MESSAGE_EOS | GST_MESSAGE_STATE_CHANGED);
		if(msg) {
			switch(GST_MESSAGE_TYPE(msg)) {
				case GST_MESSAGE_ERROR:
				case GST_MESSAGE_EOS:
					terminate = true;
					break;
				case GST_MESSAGE_STATE_CHANGED:
					//this is the msg we are interested in 
					if(GST_MESSAGE_SRC(msg) == GST_OBJECT(data.pipeline)) {
						GstState old_state, new_state, pending_state;
						gst_message_parse_state_changed(msg, &old_state, &new_state, &pending_state);
					}
					break;
				default:
					break;
			}
		}
		gst_message_unref(msg);
		
	} while(!terminate);
	gst_object_unref(bus);
	gst_element_set_state(data.pipeline, GST_STATE_NULL);
	gst_object_unref(data.pipeline);
	
	return 0;
}

static void pad_added_handle(GstElement* src, GstPad *new_pad, 
CustomData* data) {
	GstPad *sink_pad = gst_element_get_static_pad(data->convert, "sink");
	GstPadLinkReturn ret;
	GstCaps *new_pad_caps = NULL;
	GstStructure *new_pad_struct = NULL;
	gchar *new_pad_type = NULL;
	if(gst_pad_is_linked(sink_pad)) {
		printf("we are already linked, ignore it\n");
		goto exit;
	}
	new_pad_caps = gst_pad_get_caps(new_pad);
	new_pad_struct = gst_pad_get_structure(new_pad);
	new_pad_type = gst_structure_get_name(new_pad_struct);
	if(!g_str_has_prefix(new_pad_type, "audio/x-raw")) {
		printf("type is not raw audio, it is [%s]\n", new_pad_type);
		goto exit;
	}
	ret = gst_pad_link(new_pad, sink_pad);
	
exit:
	if(new_pad_caps != NULL) {
		gst_caps_unref(new_pad_caps);
	}
	gst_object_unref(sink_pad);
}
```



# 时间管理

下面看看如何进行时间管理。

主要是seek和查询。

```
#include <gst/gst.h>

typedef struct _CustomData {
	GstElement *playbin;
	gboolean playing;
	gboolean terminate;
	gboolean seek_enabled;
	gboolean seek_done;
	gint64 duration;
} CustomData;

static void handle_message(CustomData *data, GstMessage *msg);

int main(int argc, char **argv)
{
	CustomData data;
	GstBus *bus;
	GstMessage *msg;
	GstStateChangeReturn ret;
	data.playing = FALSE;
	data.terminate = FALSE;
	data.seek_enabled = FALSE;
	data.seek_done = FALSE;
	data.duration = GST_CLOCK_TIME_NONE;
	gst_init(&argc,&argv);
	data.playbin = gst_element_factory_make("playbin", "playbin");
	g_object_set(data.playbin, "uri", "https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel-480.webm", NULL);
	ret = gst_element_set_state(data.playbin, GST_STATE_PLAYING);
	
	bus = gst_element_get_bus(data.playbin);
	do {
		msg = gst_bus_timed_pop_filtered(bus, 100*GST_MSECOND, GST_MESSAGE_STATE_CHANGED | GST_MESSAGE_EOS | GST_MESSAGE_ERROR | GST_MESSAGE_DURATION);
		if(msg != NULL) {
			handle_message(&data, msg);
		} else {
			//no msg ,means timeout
			gint64 current = -1;
			gst_element_query_position(data.playbin, GST_FORMAT_TIME, &current);
			if(!GST_CLOCK_TIME_IS_VALID(data.duration)) {
				gst_element_query_duration(data.playbin, GST_FORMAT_TIME, &data.duration);
			}
			printf("position:%d, duration:%d\n", current, data.duration);
			if(data.seek_enabled && !data.seek_done && current>10*GST_SECOND) {
				printf("reach 10s, perform seek\n");
				gst_element_seek_simple(data.playbin, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_KEY_UNIT, 30*GST_SECOND);
				data.seek_done = TRUE;
			}
		}
		
	} while(!data.terminate);
	gst_object_unref(bus);
	gst_element_set_state(data.playbin, GST_STATE_NULL);
	gst_object_unref(data.playbin);
	return 0;
}

static void handle_message(CustomData *data, GstMessage *msg)
{
	GError *err;
	gchar *debug_info;
	switch(GST_MESSAGE_TYPE(msg)) {
		case GST_MESSAGE_ERROR:
		case GST_MESSAGE_EOS:
			data->terminate = TRUE;
			break;
		case GST_MESSAGE_DURATION:
			data->duration = GST_CLOCK_TIME_NONE;
			break;
		case GST_MESSAGE_STATE_CHANGED:
			GstState old_state, new_state, pending_state;
			gst_message_parse_state_changed(msg, &old_state, &new_state, &pending_state);
			if(GST_MESSAGE_SRC(msg) == GST_OBJECT(data->playbin)) {
				data->playing = (new_state == GST_STATE_PLAYING);
			}
			if(data->playing) {
				GstQuery *query ;
				gint64 start, end;
				query = gst_query_new_seeking(GST_FORMAT_TIME);
				if(gst_element_query(data->playbin, queyr)) {
					gst_query_parse_seeking(query, NULL, &data->seek_enabled, &start, &end);
					if(data->seek_enabled) {
						printf("seek is enabled from %ld to %ld\n", GST_TIME_ARGS(start), GST_TIME_ARGS(end));
					} else {
						printf("seek is not enabled\n");
					}
						
				} else {
					printf("seek query failed\n");
				}
			}
			break;
		default:
			printf("msg not right\n");
			break;
	}
	gst_message_unref(msg);
}

```



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





参考资料

1、GStreamer基础教程01——Hello World

https://blog.csdn.net/sakulafly/article/details/19398257

2、GStreamer基础教程02——GStreamer概念

https://blog.csdn.net/lengkunbit/article/details/76723932

3、GStreamer基础教程03——动态pipeline

https://blog.csdn.net/sakulafly/article/details/20936067

4、gstreamer基础教程4-Time management

https://blog.csdn.net/knowledgebao/article/details/82688834

5、GStreamer基础教程05——集成GUI工具

https://blog.csdn.net/fireroll/article/details/51498685

6、GStreamer播放教程06——可视化音频

https://blog.csdn.net/sakulafly/article/details/22695577

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