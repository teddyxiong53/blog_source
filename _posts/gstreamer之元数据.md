---
title: gstreamer之元数据
date: 2020-01-15 09:09:19
tags:
	- gstreamer
---

1

什么是元数据？

在媒体文件里，通常包含歌手、专辑、编码类型这些描述性的数据。这些数据就叫元数据。

我们可以怎样使用这些元数据？

1、进行归类操作，例如同一个歌手的归为一类。同一种风格的归为一类。

2、播放的时候，可以在界面上进行显示。



gstreamer是可以处理这些元数据的。具体如何处理呢？

gstreamer把元数据分为了两种：

```
1、流信息。
	描述流的属性。例如：编码类型、分辨率、采样率。
	通过Pipeline的所有的GstPad来获取。
2、流标签。
	描述非技术性的信息。例如作者、标题、专辑。
	gstreamer通过监听GstBus，监听GST_MESSAGE_TAG消息，从消息里获取信息。
	需要注意的是，gstreamer可能触发多次GST_MESSAGE_TAG，应用可以通过gst_tag_list_merge来合并
	多个标签。再在合适的时候显示。
	在切换媒体文件的时候，需要清空缓存的数据。
	
```

一个简单的例子如下。

```
#include <gst/gst.h>

void print_one_tag (const GstTagList * list,
                      const gchar * tag,
                      gpointer user_data)
{
	// g_print("tag:%s\n", tag);
	int i,num;
	num = gst_tag_list_get_tag_size(list, tag);
	// printf("tag:%s, size:%d\n", tag, num);
	for(i=0; i<num; i++) {
		const GValue *val;
		val = gst_tag_list_get_value_index(list, tag, i);
		if(G_VALUE_HOLDS_STRING(val)) {
			g_print("%s : %s\n", tag, g_value_get_string(val));
		} else if(G_VALUE_HOLDS_UINT(val)) {
			g_print("%s : %d\n", tag, g_value_get_int(val));
		} else if(G_VALUE_HOLDS_DOUBLE(val)) {
			g_print("%s: %f\n", tag, g_value_get_double(val));
		}
	}
}
void on_new_pad(GstElement *dec, GstPad *pad, GstElement* sink)
{
	GstPad *sinkpad;
	sinkpad = gst_element_get_static_pad(sink, "sink");
	if(!gst_pad_is_linked(sinkpad)) {
		gst_pad_link(pad, sinkpad);
	}
	gst_object_unref(sinkpad);

}

int main(int argc, char **argv)
{
	GstElement *pipeline, *dec, *sink;
	if(argc < 2) {
		g_print("usage: %s filename\n", argv[0]);
		return -1;
	}
	gst_init(NULL, NULL);
	gchar *uri = NULL;
	if(gst_uri_is_valid(argv[1])) {
		uri = g_strdup(argv[1]);
	} else {
		uri = gst_filename_to_uri(argv[1], NULL);
	}
	dec = gst_element_factory_make("uridecodebin", "dec");
	if(!dec) {
		g_print("dec is null\n");
		return -1;
	}
	g_object_set(G_OBJECT(dec), "uri", uri, NULL);
	sink = gst_element_factory_make("fakesink", "sink");
	if(!sink) {
		g_print("sink is null\n");
		return -1;
	}

	pipeline = gst_pipeline_new("pipe");
	if(!pipeline) {
		g_print("pipe is null\n");
		return -1;
	}
	gst_bin_add(GST_BIN(pipeline), dec);
	gst_bin_add(GST_BIN(pipeline), sink);
	g_signal_connect(dec, "pad-added", on_new_pad, sink);
	gst_element_set_state(pipeline, GST_STATE_PAUSED);


	GstMessage *msg;
	while(1) {
		msg = gst_bus_timed_pop_filtered(GST_ELEMENT_BUS(pipeline), GST_CLOCK_TIME_NONE, GST_MESSAGE_ERROR | GST_MESSAGE_TAG | GST_MESSAGE_ASYNC_DONE);
		if(GST_MESSAGE_TYPE(msg) != GST_MESSAGE_TAG) {
			g_print("message is not tag, is %d\n", GST_MESSAGE_TYPE(msg));//GST_MESSAGE_ASYNC_DONE  靠这个消息退出的。
			break;
		}
		GstTagList *tags;
		gst_message_parse_tag(msg, &tags);
		g_print("got tags from element:%s\n", GST_OBJECT_NAME(msg->src));
		gst_tag_list_foreach(tags, print_one_tag, NULL);
		g_print("xxxxxxxxxxx\n");

	}
	g_print("end of code\n");
	g_free(uri);
	return 0;
}
```

使用了fakesink，fakesink的特点跟/dev/null一样，直接把收到的数据丢掉。

从上面看，我们要获取一个媒体的信息，需要构造一个pipeline来打开这个媒体文件。

有点大费周章了，而获取媒体信息这个功能是一个基础功能，使用也较多。

所以gstreamer给我们提供了一个更简单的方式。

# GstDiscoverer

首先看工具的使用。

```
teddy@teddy-ThinkPad-SL410:~/work/test/gstreamer/test$ gst-discoverer-1.0 ./UrlPlayer.mp3 
Analyzing file:///home/teddy/work/test/gstreamer/test/./UrlPlayer.mp3
Done discovering file:///home/teddy/work/test/gstreamer/test/./UrlPlayer.mp3

Topology:
  unknown: ID3 tag
    audio: MPEG-1 Layer 3 (MP3)

Properties:
  Duration: 0:03:56.695510204
  Seekable: yes
  Tags: 
      标题: 一百万个可能（温柔男声版）（Cover：Christine Welch）
      艺术家: 黑崎子
      专辑: 一百万个可能
      流派: Blues
      容器格式: ID3 tag
      ID3v2 frame: buffer of 38 bytes
      has crc: false
      channel mode: joint-stereo
      音频编码: MPEG-1 Layer 3 (MP3)
      比特率: 128000
```

代码的使用：

```

```



参考资料

1、GStreamer基础教程06 - 获取媒体信息

https://www.cnblogs.com/xleng/p/11277397.html