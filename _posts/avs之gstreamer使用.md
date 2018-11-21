---
title: avs之gstreamer使用
date: 2018-11-19 16:24:28
tags:
	 - avs

---



看avs里，用到了哪些gstreamer的接口，分别起到了什么作用。

先看MediaPlayer里。

```
GstAppSrc
GstElement
gst_init_check
g_main_loop_new 这个是glib的函数。用来处理空闲任务的。
gst_element_factory_make("audioconvert", "converter");
gst_element_factory_make("volume", "volume");
gst_element_factory_make(audioSinkElement.c_str(), "audio_sink");
gst_caps_new_empty_simple("audio/x-raw");
gst_caps_set_simple(caps, it.first.c_str(), it.second, std::stoi(value), NULL);
gst_pipeline_new("audio-pipeline");
GstBus* bus = gst_pipeline_get_bus(GST_PIPELINE(m_pipeline.pipeline));
m_busWatchId = gst_bus_add_watch(bus, &MediaPlayer::onBusMessage, this);

```

MediaPlayer靠glib的g_idle_add来实现异步的。

例如play函数里的handlePlay。



gst_bus_add_watch 这个总线起什么作用？

