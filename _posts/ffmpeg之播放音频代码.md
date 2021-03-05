---
title: ffmpeg之播放音频代码
date: 2018-11-26 11:06:25
tags:
	- 音频
---



用C语言写一个播放mp3文件的例子。

官方有提供例子。我们就以这个为入口分析。看看用到了哪些结构体和哪些函数。



# av_packet_alloc

从一个文件里读取一个packet的数据。是编码后的数据。例如aac的。

# avcodec_find_decoder

这个是查找并分配一个AVCodec结构体。

这些都是预定义好的。

```
static const AVCodec * const codec_list[] = {
    &ff_a64multi_encoder,
    &ff_a64multi5_encoder,
```



# av_parser_init

得到一个AVCodecParserContext结构体。参数是AVCodec的id。

这个也是预定义的。

```
static const AVCodecParser * const parser_list[] = {
    &ff_aac_parser,
    &ff_aac_latm_parser,
```

# avcodec_alloc_context3

分配一个context。这个要malloc了。

# avcodec_open2

参数是AVCodec和AVCodecContext。



然后就是打开文件，把数据读取到一个buffer里。



# av_frame_alloc

分配一个空间，存放解码后的数据。

# av_parser_parse2

解码。

avcodec_send_packet

avcodec_receive_frame





