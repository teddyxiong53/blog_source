---
title: gstreamer之多线程
date: 2019-12-20 10:56:19
tags:
	- 视频
---

--

gstreamer是一个支持多线程的框架。

如果有必要，它会自动在内部创建和销毁线程。

如果是在四核的cpu上运行，会自动创建4个线程来进行解码。

下面的代码，参考文章里，有几点需要修改：

1、ffmpegcolorspace，目前已经被调整为videoconvert。

2、pad template那里，"src%d"目前需要调整为"src_%u"。这个信息，可以从gst-inspect-1.0看到。

以qtdemux的为例，查看：

```
Pad Templates:
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/quicktime
      video/mj2
      audio/x-m4a
      application/x-3gp

  SRC template: 'video_%u'
    Availability: Sometimes
    Capabilities:
      ANY

  SRC template: 'audio_%u'
    Availability: Sometimes
    Capabilities:
      ANY

  SRC template: 'subtitle_%u'
    Availability: Sometimes
    Capabilities:
      ANY
```



```
#include <gst/gst.h>

int main()
{
    GstElement *pipeline, *audio_source, *tee, *audio_queue,\
        *audio_convert, *audio_resample, *audio_sink;
    GstElement *video_queue, *visual, *video_convert, *video_sink;
    GstBus *bus;
    GstMessage *msg;

    GstPadTemplate *tee_src_pad_template;
    GstPad *tee_audio_pad, *tee_video_pad;
    GstPad *queue_audio_pad, *queue_video_pad;

    gst_init(NULL, NULL);
    audio_source = gst_element_factory_make("audiotestsrc", "audio_source");
    g_print("line:%d, %p\n", __LINE__, audio_source);
    tee = gst_element_factory_make("tee", "tee");
    g_print("line:%d, %p\n", __LINE__, tee);
    audio_queue = gst_element_factory_make("queue", "audio_queue");
    g_print("line:%d, %p\n", __LINE__, audio_queue);
    audio_convert = gst_element_factory_make("audioconvert", "audio_convert");
    g_print("line:%d, %p\n", __LINE__, audio_convert);
    audio_resample = gst_element_factory_make("audioresample", "audio_resample");
    g_print("line:%d, %p\n", __LINE__, audio_resample);
    audio_sink = gst_element_factory_make("autoaudiosink", "audio_sink");
    g_print("line:%d, %p\n", __LINE__, audio_sink);

    video_queue = gst_element_factory_make("queue", "video_queue");
    g_print("line:%d, %p\n", __LINE__, video_queue);
    visual = gst_element_factory_make("wavescope", "visual");
    g_print("line:%d, %p\n", __LINE__, visual);
    video_convert = gst_element_factory_make("videoconvert", "csp");
    g_print("line:%d, %p\n", __LINE__, video_convert);
    video_sink = gst_element_factory_make("autovideosink", "video_sink");
    g_print("line:%d, %p\n", __LINE__, video_sink);


    pipeline = gst_pipeline_new("test-pipeline");
    g_print("line:%d, %p\n", __LINE__, pipeline);
    if(
        !(pipeline && audio_source && tee && audio_queue && audio_convert &&
            audio_resample && audio_sink && video_queue && visual && video_convert && video_sink)
    )
    {
        // g_print("line:%d, %p\n", __LINE__, pipeline);
        // g_print("line:%d, %p\n", __LINE__, audio_source);
        // g_print("line:%d, %p\n", __LINE__, tee);
        // g_print("line:%d, %p\n", __LINE__, audio_queue);
        // g_print("line:%d, %p\n", __LINE__, audio_convert);
        // g_print("line:%d, %p\n", __LINE__, audio_resample);
        // g_print("line:%d, %p\n", __LINE__, audio_sink);
        // g_print("line:%d, %p\n", __LINE__, video_queue);
        // g_print("line:%d, %p\n", __LINE__, visual);

        // g_print("line:%d, %p\n", __LINE__, video_convert);
        // g_print("line:%d, %p\n", __LINE__, video_sink);

        g_print("some element is null\n");
        //return -1;
    }
    g_object_set(audio_source, "freq", 215.0f, NULL);
    //g_object_set(visual, "shader", 0, "style", 3, NULL);

    gst_bin_add_many(GST_BIN(pipeline), audio_source, tee, audio_queue,
        audio_convert, audio_resample, audio_sink,
        video_queue, visual, video_convert, video_sink, NULL);

    if(gst_element_link_many(audio_source, tee, NULL) != TRUE
        || gst_element_link_many(audio_queue, audio_convert, audio_resample ,audio_sink, NULL) != TRUE
        || gst_element_link_many(video_queue, visual, video_convert, video_sink, NULL) != TRUE
        )
    {
        g_print("not all element can be linked\n");
        gst_object_unref(pipeline);
        return -1;
    }
    tee_src_pad_template = gst_element_class_get_pad_template(GST_ELEMENT_GET_CLASS(tee), "src_%u");
    g_print("tee template:%p\n", tee_src_pad_template);
    tee_audio_pad = gst_element_request_pad(tee, tee_src_pad_template, NULL, NULL);
    g_print("get request pad for audio branch:%s\n", gst_pad_get_name(tee_audio_pad));
    queue_audio_pad = gst_element_get_static_pad(audio_queue, "sink");

    tee_video_pad = gst_element_request_pad(tee, tee_src_pad_template, NULL, NULL);
    g_print("get request pad for video branch:%s\n", gst_pad_get_name(tee_video_pad));
    queue_video_pad = gst_element_get_static_pad(video_queue, "sink");

    if(gst_pad_link(tee_audio_pad, queue_audio_pad) != GST_PAD_LINK_OK
        || (gst_pad_link(tee_video_pad, queue_video_pad) != GST_PAD_LINK_OK))
    {
        g_print("tee can not be linked\n");
        gst_object_unref(pipeline);
        return -1;
    }
    gst_object_unref(queue_audio_pad);
    gst_object_unref(queue_video_pad);

    gst_element_set_state(pipeline, GST_STATE_PLAYING);

    bus = gst_element_get_bus(pipeline);
    msg = gst_bus_timed_pop_filtered(bus,
        GST_CLOCK_TIME_NONE, GST_MESSAGE_ERROR | GST_MESSAGE_EOS);

    gst_element_release_request_pad(tee, tee_audio_pad);
    gst_element_release_request_pad(tee, tee_video_pad);
    gst_object_unref(tee_audio_pad);
    gst_object_unref(tee_video_pad);

    if(msg) {
        gst_message_unref(msg);
    }
    gst_object_unref(bus);
    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(pipeline);

    return 0;
}

```



参考资料

1、GStreamer基础教程07——多线程和Pad的有效性

https://blog.csdn.net/sakulafly/article/details/21318313

2、gst_element_class_get_pad_template does not return pud_template

https://stackoverflow.com/questions/25700666/gst-element-class-get-pad-template-does-not-return-pud-template