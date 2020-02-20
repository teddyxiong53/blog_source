---
title: ffmpeg（1）
date: 2018-08-11 15:11:40
tags:
	- 视频

---

1

ffmpeg是包括：

1、录制。

2、转换。

3、音视频编解码。

是一个完整的开源解决方案。

支持40多种编码，90多种解码。

包括：

```
libavformat
	音视频文件的封装和解封装。
libavdevice
	对输入输出设备的支持。
libavcodec
	编解码。
libavutil
	工具函数。
libswscale
	缩放。
libpostproc
	后期效果处理。
libavresample
	重采样。
libswresample
	
```



AVPacket：解码前的数据，例如AAC、H264数据。

AVFrame：解码后的数据，例如RGB、pcm数据。



下载代码，编译。

```
git clone https://git.ffmpeg.org/ffmpeg.git
```



```
./configure 
```

提示：

```
nasm/yasm not found or too old. Use --disable-x86asm for a crippled build.
```

安装nasm就好了。



用vscode来调试

我在Linux下来做。

```
./configure --enable-debug
```

生成的ffprobe_g，带调试信息的版本后面会_g后缀。



# 帮助信息

```
ffmpeg {1} {2} -i {3} {4} {5}
1：全局选项
2：input选项
3、input url
4、output选项
5、output url
```



```
-f 格式
	f表示force format。
	例如ffmpeg -f alsa
```

可以有多个input，多个output。

所以有per-file选项。

选项分为3种，全局的、input的，output的。

另外还有查询信息的选项。

全局的参数

```
基本的：
-v x
	设置日志级别。
-y
-n
	是否覆盖文件。
高级的；
-vsync
	视频同步方法 。
-async
	音频同步方法。
-copyts
	拷贝时间戳。
	
```

per-file的主要选项

```
-f fmt
	指定格式。
-c codec
	指定codec名字。
-t
	时长。

```

per-file高级选项

```
-re
-profile

```

视频选项

```
-r
	帧率
-s
	frame size。
-aspect
	宽高比。
-vn
	禁止视频。
	
```

高级视频选项

```
-pix_fmt 
	指定像素格式。

```

音频选项

```
-aframes
	音频帧数量。
-aq
	音频质量。
-ar
	音频采样率，hz为单位。
-an
	禁止音频。
-vol
	256为默认。
	
```

AVCodecContext选项

```

```

其他要注意的点：

```
-ab bitrate         audio bitrate (please use -b:a)
-b bitrate          video bitrate (please use -b:v)
```

从这里可以得到-b:a是一个完整的选项，而并不是冒号的特别用法。



# AVPacket

这个数据结构在ffmpeg里很重要。

保存了解复用（demuxer）之后，解码之前的数据以及一些附加的信息。

例如：

显示时间戳pts

解码时间戳dts

时长duration

所在流媒体的索引。stream_index。

对于视频来说，一个AVPacket通常包含一个压缩的Frame。

而对于音频来说，一个AVPacket包含多个压缩的Frame。

一个AVPacket也可能是空的。不包含任何压缩数据，只包含side data。



AVPacket的大小是public ABI的一部分。这样的结构体在ffmpeg里很少。

这也侧面说明了这个结构体的重要性。

除非libavcodec和libavformat有很大的改动，AVPacket里不能进行成员变量的增加和删除。



AVPacket的成员变量可以分为两部分：

1、数据的缓存及管理

2、数据的属性。



先看数据的属性。

```
pts
dts
size：data的大小。
stream_index：
flags：
	关键帧、损坏的数据、丢弃的数据。
side_data_elems：
	边缘数据个数。
duration
pos

```

数据缓存

```
AVPacket本身只是一个容器，不直接包含数据。
而是通过数据缓存的指针来引用数据。
包含两种数据。
uint8_t *data;//指向保存压缩数据的指针。这个就是AVPacket的实际数据。
AVPacketSideData *side_data;
AVBufferRef *buf;//用来管理data指针引用的数据缓存。
```

从一个AVPacket创建另外一个AVPacket的时候，有两种情况：

```
1、P1和P2的data指针是指向同一块内存。
2、P1和P2的data指针指向不通的内存。
```

情况2是简单的。但是这样无疑是有空间浪费的。拷贝也有性能开销。

对于情况1，采用引用计数来进行管理。

情况1，使用2个函数来进行访问：

```
av_packet_ref
av_packet_unref
```

AVBufferRef 这个结构体就是用来做引用计数管理的。





参考资料

FFMPEG结构体：AVPacket解析

https://www.jianshu.com/p/bb6d3905907e



# AVDictionary

本质是键值对，键值都是char *类型。

这个在http_multiclient.c这个例子里有进行使用。

```
AVDictionary *options = NULL;
av_dict_set(&options, "listen", 2, 0);//最后一个参数是flags。
然后这个options可以传递给其他函数进行使用。

```



# AVClass

这个结构体的作用是什么？



https://blog.csdn.net/qq_35044535/article/details/77862183

# AVOption



# 音频格式

新的ffmpeg3里，audio增加了planar格式（平面格式）。

sdl播放音频是不支持平面格式的。

所以ffmpeg解码出来的数据不能直接发送给sdl进行播放。

需要先进行格式化转换。

以前的音频解码api：avcodec_decode_audio4在新版本里废弃了。统一为avcodec_send_packet和avcodec_receive_frame接口。

音频格式分为两种：

1、packed格式。

2、planar格式。

在AVSampleFormat枚举里，

```
AV_SAMPLE_FORMAT_S16 
AV_SAMPLE_FORMAT_S16P ：后面有P后缀的，表示planar格式。
```

packed模式，就是交叉保存各个声道的数据的。

planar格式，是分开保存的，这样数据看起来就没有那么杂乱。





# api分析

av_frame_get_buffer

```
给frame分配buffer。
举例：
	ret = av_frame_get_buffer(frame, 0);
	返回值小于0表示出错。
```



# 编译例子

make examples

用单步调试的方法，阅读下面的代码。

AVCodec和AVCodecFormat的关系

```
AVCodec
	主要是函数指针。
	不设计太多具体参数。
AVCodecFormat
	具体参数。
	例如采样率这些。
```



## decode_audio

decode_audio.c这值得看一下。

现在我测试的材料是1.mp3文件。这个时长是1.8s。是我合成的一个文件。

单声道，16K，16bit有符号。

```
./decode_audio ./1.mp3 ./1.out
```

涉及的数据结构和函数有：

```
AVCodec
	这个用了一个ID_MP2的解码器。
	通过avcodec_find_decoder来找。并不是alloc出来的。
	所以解码器是默认就分配好的。
	avcodec_open2
		还需要打开才能用。
		在拿到上下文和codec之后，就可以进行打开操作。
AVCodecContext
	根据AVCodec来alloc得到。存放解码器的工作状态。
	avcodec_alloc_context3
AVCodecParserContext
	这个parser是起什么作用呢？
	也是一直存在的，av_parser_init(codec->id);通过这个初始化一下就好。
	av_parser_parse2
		解析一段数据，得到AVPacket的data和size。
		就是解析AVPacket的。
AVPacket
	用av_packet_alloc分配。
	av_parser_parse2把数据填充到这个结构体里。
	avcodec_send_packet
		发送给解码器去进行界面。
AVFrame
	av_frame_alloc
		也是分配一次就可以了，反复使用。
	avcodec_receive_frame
		在avcodec_send_packet后，就可以avcodec_receive_frame拿到界面后的数据。
	frame->data
		这个就可以往输出文件里写了。
```

使用parser是解析音频数据的两种方式之一。



## encode_audio

设计到的数据结构和函数有：

```
AVCodecContext
	这个跟解码例子的不同，在于avcodec_open2打开codec之前。
	需要对codec上下文进行参数填充赋值。
	
```

这个的数据是通过数学方式生成的。直接把数据写入音频文件，先编码再写入的。



## decode_video

基本跟界面音频的流程一样。

## encode_video

也是用数学方式生成的视频数据。

流程跟编码音频的类似。



## demuxing_decoding

这个是解封装和解码。

前面的例子，都没有涉及到解封装的。

现在这里开始涉及到解封装的函数。



我随便找一个mp4文件，改名为2.mp4。

```
./demuxing_decoding ./2.mp4 2-video 2-audio
```

我找的这个mp4文件是vscode里的演示视频。没有音频。

执行完成后，会提示你可以这样进行播放：

```
ffplay -f rawvideo -pix_fmt yuv420p -video_size 1596x1080 2-video
```

avformat_open_input

这个通过二级指针，来获得一个AVFormatContext实例。需要的材料是一个文件。

开始引入AVStream。这个代表解封装后得到的音频流和视频流对象。



这个例子用的函数，是比较老的。





# 参考资料

1、FFMpeg框架代码阅读

https://www.cnblogs.com/azraelly/archive/2012/12/30/2840133.html

2、FFmpeg源代码结构图

https://www.cnblogs.com/x_wukong/p/4864863.html

3、多媒体文件格式探测⑨

https://www.cnblogs.com/tocy/p/media_container_9-probe-utility.html

4、如何在mac中使用VScode来调试ffmpeg、x264和x265

https://blog.csdn.net/xueyushenzhou/article/details/86736273

5、FFmpeg学习4：音频格式转换

https://www.cnblogs.com/wangguchangqing/p/5851490.html

6、

这个教程挺好的。

https://github.com/leandromoreira/ffmpeg-libav-tutorial