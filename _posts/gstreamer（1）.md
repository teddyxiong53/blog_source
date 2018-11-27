---
title: gstreamer（1）
date: 2018-11-26 17:12:24
tags:
	- gstreamer
typora-root-url: ..\
---



还是系统地学习一遍。

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