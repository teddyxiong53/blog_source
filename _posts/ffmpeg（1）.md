---
title: ffmpeg（1）
date: 2018-08-11 15:11:40
tags:
	- 视频

---

--

# 代码经验

free的时候，很多都是二级指针，如果传递一级指针，就会段错误。

```

static void save_gray_frame(unsigned char *buf, int wrap, int xsize, int ysize, char *filename)
{
    FILE *f;
    int i;
    f = fopen(filename, "w");
    fprintf(f, "P5\n\%d %d\n%d\n", xsize, ysize, 255);
    for(i=0;i <ysize; i++) {
        fwrite(buf + i*wrap, 1, xsize, f);
    }
    fclose(f);
        
}

static int decode_packet(AVPacket *pPacket, AVCodecContext *pCodecContext, AVFrame *pFrame)
{
    int response = avcodec_send_packet(pCodecContext, pPacket);
    if(response < 0) {
        printf("send packet fail\n");
        return -1;
    }
    while(response >= 0) {
        response = avcodec_receive_frame(pCodecContext, pFrame);
        if(response == AVERROR(EAGAIN) || response == AVERROR_EOF) {

            break;
        } else if(response < 0) {
            printf("fatal error:%s\n", av_err2str(response));
            return response;
        }
        if(response >= 0) {
            char frame_filename[1024];
            snprintf(frame_filename, sizeof(frame_filename), "%s-%d.pgm", "frame", pCodecContext->frame_number);
            save_gray_frame(pFrame->data[0], pFrame->linesize[0], pFrame->width, pFrame->height, frame_filename);
        }
    }
    return 0;
}
int main(int argc, char **argv)
{
    if(argc < 2) {
        printf("you need to specify a filename\n");
        return -1;
    }
    AVFormatContext *pFormatContext = avformat_alloc_context();
    char *filename = argv[1];
    avformat_open_input(&pFormatContext, filename, NULL, NULL);
    
    avformat_find_stream_info(pFormatContext, NULL);
    AVCodec *pCodec = NULL;
    AVCodecParameters *pCodecParameters;
    int video_stream_index = -1;
    int i =0;
    for(i=0; i<pFormatContext->nb_streams; i++) {
        AVCodecParameters *pLocalCodecParameters = NULL;
        pLocalCodecParameters = pFormatContext->streams[i]->codecpar;

        AVCodec *pLocalCodec;
        pLocalCodec = avcodec_find_decoder(pLocalCodecParameters->codec_id);
        if(pLocalCodec == NULL) {
            printf("can not find codec\n");
            return -1;
        }

        if(pLocalCodecParameters->codec_type == AVMEDIA_TYPE_VIDEO) {
            if(video_stream_index == -1) {
                video_stream_index = i;
                pCodec = pLocalCodec;
                pCodecParameters = pLocalCodecParameters;
            }
        } else if(pLocalCodecParameters->codec_type == AVMEDIA_TYPE_AUDIO) {
            printf("find audio stream\n");
        }
        
    }
    AVCodecContext *pCodecContext = avcodec_alloc_context3(pCodec);
    avcodec_parameters_to_context(pCodecContext, pCodecParameters);

    avcodec_open2(pCodecContext, pCodec, NULL);
    AVFrame *pFrame = av_frame_alloc();
    AVPacket *pPacket = av_packet_alloc();
    int response = 0;
    int how_many_packets_to_process = 8;
    while(av_read_frame(pFormatContext, pPacket) >= 0) {
        if(pPacket->stream_index == video_stream_index) {
            printf("pts:%"PRId64"\n", pPacket->pts);
            response = decode_packet(pPacket, pCodecContext, pFrame);
            if(response < 0) {
                break;
            }
            if(--how_many_packets_to_process <= 0) {
                break;
            }
        }
        av_packet_unref(pPacket);
    }
    printf("release all resource\n");
    avformat_close_input(&pFormatContext);
    avformat_free_context(pFormatContext);
    av_packet_free(&pPacket);
    av_frame_free(&pFrame);
    avcodec_free_context(&pCodecContext);
    return 0;
}
```



# 简介

下面是关于FFmpeg的简介：

| 名称     | FFmpeg                                                       |
| -------- | ------------------------------------------------------------ |
| 类型     | 跨平台的多媒体处理工具和库                                   |
| 特点     | - 支持多种音频、视频和多媒体格式<br>- 提供了丰富的音视频处理功能<br>- 可以用于格式转换、编解码、流媒体处理等 |
| 主要组件 | - ffmpeg：用于命令行操作的主要工具<br>- ffplay：用于播放音视频的简单播放器<br>- ffprobe：用于检查多媒体文件信息的工具 |
| 开发语言 | C语言                                                        |
| 许可证   | 大多数情况下采用LGPL或GPL许可证                              |

FFmpeg是一个非常强大的工具，被广泛用于视频处理、转码、流媒体等应用场景。



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

# 发展历史

以下是FFmpeg的主要发展历史：

| 时间段 | 重要事件                                                     |
| ------ | ------------------------------------------------------------ |
| 2000年 | - FFmpeg项目由Fabrice Bellard创建<br>- 最初版本发布          |
| 2003年 | - 项目由Michael Niedermayer接管<br>- FFmpeg开始支持更多的编解码器和格式 |
| 2011年 | - FFmpeg与Libav分道扬镳，形成两个独立的项目                  |
| 2015年 | - FFmpeg回归原始开发者Michael Niedermayer的领导下            |
| 2020年 | - FFmpeg发布版本4.3，增加了对新的编解码器和格式的支持<br>- 持续改进性能和稳定性 |
| 未来   | - FFmpeg项目预计将继续发展，支持更多新的编解码器和多媒体格式<br>- 可能会持续改进性能和优化代码 |

FFmpeg经历了多个版本和领导层的变动，但一直保持着对多媒体处理领域的贡献和领导地位。

# 代码架构

FFmpeg的代码架构相当庞大，主要由多个模块组成，包括但不限于：

1. **libavcodec**: 实现了音视频编解码器的库，支持多种编码和解码算法。
2. **libavformat**: 实现了音视频格式的封装和解封装功能，支持多种容器格式。
3. **libavfilter**: 提供了音视频过滤器的库，可以进行音视频的处理和过滤。
4. **libavutil**: 包含一些常用的工具函数和数据结构，为其他模块提供支持。
5. **libswscale**: 提供了图像格式转换和缩放的功能，用于处理视频帧。
6. **ffmpeg/ffplay/ffprobe**: 命令行工具，用于进行音视频处理、播放和信息查看。
7. **doc**: 文档目录，包含了FFmpeg的官方文档和使用手册。
8. **tests**: 包含了用于测试和验证FFmpeg功能的测试代码。
9. **compat**: 兼容性模块，用于处理不同操作系统和平台之间的差异。

整个代码库结构清晰，模块化程度高，使得开发人员可以方便地定位和修改相关功能。

# 写一个简单的mp3播放器

以下是一个简单的使用FFmpeg库实现的MP3音频播放器的C语言版本示例代码：

```c
#include <stdio.h>
#include <libavformat/avformat.h>
#include <libavutil/opt.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    const char *file_path = argv[1];
    av_register_all();

    // 打开输入文件
    AVFormatContext *format_ctx = NULL;
    if (avformat_open_input(&format_ctx, file_path, NULL, NULL) != 0) {
        printf("无法打开输入文件\n");
        return 1;
    }

    // 查找音频流信息
    if (avformat_find_stream_info(format_ctx, NULL) < 0) {
        printf("无法获取音频流信息\n");
        avformat_close_input(&format_ctx);
        return 1;
    }

    // 查找第一个音频流
    int audio_stream_index = -1;
    for (int i = 0; i < format_ctx->nb_streams; i++) {
        if (format_ctx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_AUDIO) {
            audio_stream_index = i;
            break;
        }
    }

    if (audio_stream_index == -1) {
        printf("未找到音频流\n");
        avformat_close_input(&format_ctx);
        return 1;
    }

    // 分配音频解码器上下文
    AVCodecContext *codec_ctx = avcodec_alloc_context3(NULL);
    if (!codec_ctx) {
        printf("无法分配解码器上下文\n");
        avformat_close_input(&format_ctx);
        return 1;
    }

    // 填充音频解码器参数
    if (avcodec_parameters_to_context(codec_ctx, format_ctx->streams[audio_stream_index]->codecpar) < 0) {
        printf("无法填充解码器参数\n");
        avcodec_free_context(&codec_ctx);
        avformat_close_input(&format_ctx);
        return 1;
    }

    // 查找解码器
    AVCodec *codec = avcodec_find_decoder(codec_ctx->codec_id);
    if (!codec) {
        printf("找不到解码器\n");
        avcodec_free_context(&codec_ctx);
        avformat_close_input(&format_ctx);
        return 1;
    }

    // 打开解码器
    if (avcodec_open2(codec_ctx, codec, NULL) < 0) {
        printf("无法打开解码器\n");
        avcodec_free_context(&codec_ctx);
        avformat_close_input(&format_ctx);
        return 1;
    }

    // 读取音频帧并播放
    AVPacket packet;
    av_init_packet(&packet);
    while (av_read_frame(format_ctx, &packet) >= 0) {
        if (packet.stream_index == audio_stream_index) {
            AVFrame *frame = av_frame_alloc();
            int ret = avcodec_send_packet(codec_ctx, &packet);
            if (ret < 0) {
                printf("发送音频数据包时出错\n");
                break;
            }
            ret = avcodec_receive_frame(codec_ctx, frame);
            if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
                av_frame_free(&frame);
                continue;
            }
            if (ret < 0) {
                printf("从解码器接收音频帧时出错\n");
                break;
            }
            printf("播放音频帧...\n");

            av_frame_free(&frame);
        }
        av_packet_unref(&packet);
    }

    // 释放资源
    avcodec_free_context(&codec_ctx);
    avformat_close_input(&format_ctx);
    return 0;
}
```

这个C语言版本的播放器使用了FFmpeg的C API，打开输入文件并查找音频流信息。然后，它找到音频流并为其分配解码器上下文。最后，它循环读取音频帧并播放。你需要在编译时链接FFmpeg库。

# 主要的api介绍

以下是FFmpeg主要API的简要介绍：

1. **libavformat**：这个库提供了音视频容器格式的封装和解封装功能。你可以使用它来读取和写入各种音视频格式的文件，以及处理流媒体数据。常用的函数包括：
   - `avformat_open_input()`：打开输入文件。
   - `avformat_find_stream_info()`：获取音视频流信息。
   - `avformat_write_header()`：写入文件头。
   - `av_read_frame()`：读取音视频帧数据。

2. **libavcodec**：这个库提供了音视频编解码器的功能。你可以使用它来解码、编码各种音视频数据。常用的函数包括：
   - `avcodec_find_decoder()`：查找解码器。
   - `avcodec_find_encoder()`：查找编码器。
   - `avcodec_open2()`：打开解码器或编码器。
   - `avcodec_send_packet()`：发送音视频数据包。
   - `avcodec_receive_frame()`：接收解码后的音视频帧。

3. **libavfilter**：这个库提供了音视频过滤器的功能，用于处理和修改音视频流。常用的函数包括：
   - `avfilter_graph_alloc()`：创建一个过滤器图。
   - `avfilter_graph_parse2()`：解析过滤器图的描述字符串。
   - `avfilter_graph_config()`：配置过滤器图。
   - `av_buffersrc_write_frame()`：向输入过滤器发送音视频帧。
   - `av_buffersink_get_frame()`：从输出过滤器获取处理后的音视频帧。

4. **libavutil**：这个库包含了一些常用的工具函数和数据结构，为其他模块提供支持。常用的函数包括：
   - `av_malloc()`：分配内存。
   - `av_freep()`：释放内存。
   - `av_gettime()`：获取当前时间。

5. **libswscale**：这个库提供了图像格式转换和缩放的功能，用于处理视频帧。常用的函数包括：
   - `sws_getContext()`：创建图像转换上下文。
   - `sws_scale()`：进行图像转换和缩放。

这些API提供了丰富的功能，使得开发人员可以进行各种复杂的音视频处理操作。

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

## 常用选项

```
-c :指定编码器
-c copy: 直接赋值，不经过重新编码。这样比较快。
-c:v 指定视频编码器。
-c:a 指定音频编码器。
-an： 去掉音频。
-vn：去掉视频。
-preset：
	指定输出的视频质量。
	有这些值：
	ultrafast
	superfast
	veryfast
	faster
	fast
	medium
	slow
	slower
	veryslow
	
```



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



**AVPacket的大小是public ABI的一部分。这样的结构体在ffmpeg里很少。**

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
2、P1和P2的data指针指向不同的内存。
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

`AVDictionary`是FFmpeg中用于表示字典（键值对）的数据结构。它用于存储元数据、选项和参数等信息。`AVDictionary`结构的定义如下：

```c
typedef struct AVDictionary AVDictionary;
```

每个`AVDictionary`结构都包含了零个或多个键值对，每个键值对由一个键（key）和一个值（value）组成，都是字符串类型。在FFmpeg中，`AVDictionary`常用于传递选项和元数据，例如编码器的参数、文件的元数据等。

以下是一些常用的`AVDictionary`相关的函数：

- `av_dict_set()`: 用于向`AVDictionary`中添加或更新键值对。
- `av_dict_get()`: 用于从`AVDictionary`中获取指定键对应的值。
- `av_dict_count()`: 返回`AVDictionary`中键值对的数量。
- `av_dict_free()`: 释放`AVDictionary`及其所有的键值对。

`AVDictionary`在FFmpeg中广泛用于传递和管理参数和选项，对于处理音视频流时，特别是编解码和封装时，经常会用到。

# AVClass

这个结构体的作用是什么？

用vscode在ffmpeg的代码里搜索`static const AVClass`。

可以找到所有定义选项的地方。

例如mp3的：

```
static const AVClass libmp3lame_class = {
    .class_name = "libmp3lame encoder",
    .item_name  = av_default_item_name,
    .option     = options,
    .version    = LIBAVUTIL_VERSION_INT,
};
```

它的options有这些：

```
static const AVOption options[] = {
    { "reservoir",    "use bit reservoir", OFFSET(reservoir),    AV_OPT_TYPE_BOOL, { .i64 = 1 }, 0, 1, AE },
    { "joint_stereo", "use joint stereo",  OFFSET(joint_stereo), AV_OPT_TYPE_BOOL, { .i64 = 1 }, 0, 1, AE },
    { "abr",          "use ABR",           OFFSET(abr),          AV_OPT_TYPE_BOOL, { .i64 = 0 }, 0, 1, AE },
    { NULL },
};
```



https://blog.csdn.net/qq_35044535/article/details/77862183

# AVOption

# AVDiscard

一个枚举。

有7种值。

表示是否丢弃某些数据。

例如丢弃非参考帧，丢弃所有帧。

在ffplay的代码里有用到。



【FFmpeg小点记】AVDiscard的作用

https://segmentfault.com/a/1190000019742659

# avformat_find_stream_info

这个函数的作用：

读取一部分的音视频数据，从中分析得到相关信息。

有一些文件格式没有头，比如说MPEG格式的，这个时候，这个函数就很有用，因为它可以从读取到的包中获得到流的信息。





ffmpeg源码分析5-avformat_find_stream_info()

https://www.jianshu.com/p/f840e27fc5f8



# av_audio_fifo_alloc

这个一般的用法是这样，先申请一个字节的。

后面再realloc。

初始化fifo的时候这样：

```
av_audio_fifo_alloc(codec_context->sample_fmt, codec_context->channels, 1);//1个字节。
```

要填入数据的时候。

```
av_audio_fifo_realloc(fifo, av_audio_fifo_size(fifo)+frame_size);

av_audio_fifo_write(fifo, (void **)converted_input_samples, frame_size);
```

存储到fifo后，我们需要判断该fifo中是否有一帧数据，如果有，则从fifo中取出，也有可能fifo中含有多帧，

所以从fifo中取出数据的时候，需要用到while循环。

在取出fifo中的数据前，同样需要先申请一帧音频帧的空间：



大多用audiofifo做音频转码，并没有用avfilter，**当然相比较来说，AVFilter更加简单，适合无脑上手**。不过其实它底层也是用fifo实现。

示例提供了一个“解封装->解码->filtering->编码->封装”的处理流程。

编码之前的音频数据经过AVAudioFifo处理，用于满足音频编码器对frame size的要求。

**否则音频编码为AAC的时候，会报more samples than frame size的错误。**AVAudioFifo提供了一个先入先出的音频缓冲队列。



参考资料

https://blog.csdn.net/lichen18848950451/article/details/78518439

https://www.jianshu.com/p/f04e0028dd14

# AVFMT_NOFILE

这个对于设备是需要设置的。



# AVFMT_GLOBALHEADER

如果AVCodecContext中设置了AV_CODEC_FLAG_GLOBAL_HEADER标志，对于生成的视频文件（如mp4），在windows操作系统下，并以图标的方式查看该视频文件时，视频文件的图标将是视频文件的第一帧，从而起到预览的作用





https://blog.csdn.net/a812073479/article/details/79856262

https://blog.csdn.net/passionkk/article/details/75528653



#  时间戳pts/dts

没有封装格式的裸流（例如H.264裸流）是不包含PTS、DTS这些参数的。

在发送这种数据的时候，需要自己计算并写入AVPacket的PTS，DTS，duration等参数。

H264裸流加时间戳

```
AVRational time_base1=ifmt_ctx->streams[videoindex]->time_base;
			printf("time base, %d/%d\n", time_base1.num, time_base1.den);
			//Duration between 2 frames (us)
			int64_t calc_duration=(double)AV_TIME_BASE/av_q2d(ifmt_ctx->streams[videoindex]->r_frame_rate);
			printf("cacl_duration:%lld, frame_rate:%d\n", calc_duration,av_q2d(ifmt_ctx->streams[videoindex]->r_frame_rate ));
			//Parameters
			pkt.pts=(double)(frame_index*calc_duration)/(double)(av_q2d(time_base1)*AV_TIME_BASE);
			pkt.dts=pkt.pts;
			printf("pts:%d\n", pkt.pts);
			pkt.duration=(double)calc_duration/(double)(av_q2d(time_base1)*AV_TIME_BASE);
			printf("duration:%lld\n", pkt.duration);
```

# 解码后延时发送



# av_rescale_q

av_rescale_q用于计算Packet的PTS。av_rescale_q的返回值是一个很大的整数，

且每次计算的结果间隔很大。

在进行存储视频流的时候，必须将avpacket里的pts设置好，否则会出现视频过快或过慢的情况，在此主要用到ffmpeg里的av_rescale_rnd函数

ffmepg中的时间戳，是以微秒为单位，关乎timebase变量，它是作为dts、pts的时间基准粒度，数值会很大。



 如果视频里各帧的编码是按输入顺序（也就是显示顺序）依次进行的，那么解码和显示时间应该是一致的。可事实上，在大多数编解码标准（如H.264或HEVC）中，编码顺序和输入顺序并不一致。 于是才会需要PTS和DTS这两种不同的时间戳。



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



# 常用格式

```
v4l2
x11grab
video4linux2,v4l2
wav
sdl
rtp
rtsp
rawvideo
mp3
mp4
jack
h264
hevc
flac
```



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



# ff_libmp3lame_encoder

一个codec的分析

# 基于ffmpeg的项目有哪些

基于 FFmpeg 的项目非常多样，涵盖了音视频处理、多媒体应用、流媒体服务等多个领域。以下是一些基于 FFmpeg 的项目示例：

1. **视频编辑和转码软件**：许多视频编辑软件和转码工具使用 FFmpeg 作为核心引擎，提供视频剪辑、转码、滤镜效果等功能，如 HandBrake、FFmpegGUI、Shotcut 等。

2. **流媒体服务器**：一些流媒体服务器使用 FFmpeg 作为处理音视频流的引擎，用于实时编码、转码和传输音视频数据，如 NGINX RTMP Module、Wowza Streaming Engine 等。

3. **媒体播放器**：一些媒体播放器使用 FFmpeg 解码和渲染音视频数据，提供多种格式的媒体播放支持，如 VLC、MPlayer、MPV 等。

4. **音视频分析工具**：一些工具利用 FFmpeg 的能力来分析音视频文件，提取元数据、检测编码信息、生成波形图等，如 MediaInfo、ffprobe 等。

5. **实时音视频通信**：一些实时音视频通信应用（如视频会议、直播）使用 FFmpeg 来处理和传输音视频数据，如 WebRTC 库、Jitsi Meet 等。

6. **音视频编解码库**：一些项目专注于构建基于 FFmpeg 的高层封装或接口，使开发者更容易使用 FFmpeg 进行音视频编解码操作，如 LibAV、pydub 等。

7. **音频处理工具**：一些工具专注于音频处理领域，利用 FFmpeg 来处理和转换音频文件，如 Audacity、SoX 等。

8. **游戏开发**：一些游戏开发项目使用 FFmpeg 来处理游戏中的音频和视频资源，实现游戏内的音视频播放效果。

9. **媒体框架**：一些媒体处理框架使用 FFmpeg 来处理音视频数据，为开发者提供丰富的媒体操作功能，如 GStreamer、OpenCV 等。

需要注意的是，这只是一小部分基于 FFmpeg 的项目示例。由于 FFmpeg 是一个强大且灵活的多媒体框架，它在不同领域有着广泛的应用。如果你对特定领域的项目有兴趣，可以在开源社区或代码托管平台上寻找更多的项目示例。

# ffmpeg主要结构体分析

FFmpeg 中有许多重要的结构体，用于存储和管理音视频数据、参数、上下文等信息。这些结构体是实现各种功能的基础，以下是一些主要的 FFmpeg 结构体：

1. **AVFormatContext（封装格式上下文）**：用于管理音视频文件的封装格式信息，包括文件名、格式、流信息、封装器和解封装器等。

2. **AVCodecContext（编解码器上下文）**：用于管理音视频编解码器的参数和状态，包括编码器类型、编码参数、解码参数、位率等。

3. **AVFrame（音视频帧）**：用于存储音视频数据的帧，包括图像数据、音频数据、时间戳、采样率等。

4. **AVPacket（音视频数据包）**：用于存储编码后的音视频数据，包括压缩数据、时间戳、数据大小等。

5. **AVFilterContext（过滤器上下文）**：用于管理音视频过滤器的参数和状态，包括输入输出连接、滤镜链等。

6. **AVIOContext（输入输出上下文）**：用于管理自定义的输入输出操作，包括读取、写入、定位等。

7. **AVDictionary（字典）**：用于存储键值对的数据结构，用于传递和存储元数据、选项等信息。

8. **AVRational（有理数）**：表示一个有理数，用于处理时间戳、帧率等。

9. **AVStream（音视频流）**：用于存储音视频流的信息，如流索引、编解码器信息、时基等。

10. **AVFilterGraph（过滤器图）**：用于管理音视频过滤器的图结构，包括过滤器链和连接。

11. **AVCodec（编解码器）**：用于描述音视频编解码器的信息，如名称、类型、支持的格式等。

这些结构体相互关联，构成了 FFmpeg 的核心数据结构，用于处理音视频数据的读取、编解码、转换、过滤等各个方面。在使用 FFmpeg 进行音视频处理时，你会涉及到操作这些结构体来进行数据的传递和管理。每个结构体都具有特定的功能和属性，需要根据具体的任务进行使用和配置。

# ffmpeg 重采样

FFmpeg 提供了 `libswresample` 库，用于实现音频的重采样（resampling）。重采样是将音频数据从一个采样率和格式转换为另一个采样率和格式的过程，常用于将音频适应不同的播放设备或处理需求。

以下是使用 FFmpeg 进行音频重采样的基本步骤：

1. **初始化 `SwrContext`：** 首先，你需要初始化一个 `SwrContext` 结构，该结构包含了重采样的参数和状态。

```c
SwrContext *swr_ctx = swr_alloc();
```

2. **设置参数：** 设置重采样的输入和输出参数，包括输入采样率、输出采样率、输入样本格式、输出样本格式等。

```c
av_opt_set_int(swr_ctx, "in_channel_layout", in_channel_layout, 0);
av_opt_set_int(swr_ctx, "in_sample_rate", in_sample_rate, 0);
av_opt_set_sample_fmt(swr_ctx, "in_sample_fmt", in_sample_fmt, 0);

av_opt_set_int(swr_ctx, "out_channel_layout", out_channel_layout, 0);
av_opt_set_int(swr_ctx, "out_sample_rate", out_sample_rate, 0);
av_opt_set_sample_fmt(swr_ctx, "out_sample_fmt", out_sample_fmt, 0);
```

3. **初始化重采样上下文：** 根据设置的参数，初始化重采样上下文。

```c
swr_init(swr_ctx);
```

4. **循环重采样：** 对输入的音频数据进行重采样，将结果写入输出缓冲区。

```c
int nb_samples = ...; // 输入样本数
uint8_t *in_data[AV_NUM_DATA_POINTERS] = {in_samples_data}; // 输入样本数据
int in_linesize[AV_NUM_DATA_POINTERS] = {in_samples_linesize}; // 输入样本行大小

int out_samples = ...; // 输出样本数
uint8_t *out_data[AV_NUM_DATA_POINTERS] = {out_samples_data}; // 输出样本数据
int out_linesize[AV_NUM_DATA_POINTERS] = {out_samples_linesize}; // 输出样本行大小

swr_convert(swr_ctx, out_data, out_samples, (const uint8_t **)in_data, nb_samples);
```

5. **释放资源：** 最后，记得释放分配的资源。

```c
swr_free(&swr_ctx);
```

这只是一个简单的示例，实际的重采样过程可能会涉及更多的参数和设置。重采样过程需要根据具体的需求和情况进行调整。你可以参考 FFmpeg 的文档和示例来了解更多关于 `libswresample` 的用法和详细步骤。

# ffmpeg怎样保证ABI兼容

为了保证 FFmpeg 的 ABI（Application Binary Interface）兼容性，即确保不同版本的 FFmpeg 库能够与已编译的应用程序二进制文件正确链接并运行，FFmpeg 团队采取了一系列策略和实践：

1. **版本号管理：** FFmpeg 使用了版本号规则，其中包括主版本号、次版本号和修订版本号。当 API 或 ABI 发生不兼容性更改时，主版本号会增加。次版本号增加表示有新功能的引入，但不影响 ABI 兼容性。修订版本号增加表示只有兼容性修复的变更。

2. **符号版本控制：** FFmpeg 使用符号版本控制（Symbol Versioning）来标识库中的符号（函数和变量），以指定它们的版本和兼容性。这有助于确保应用程序链接的是正确版本的符号，从而保持 ABI 兼容性。

3. **二进制兼容性测试：** FFmpeg 团队在每个主要发布版之前进行二进制兼容性测试，以验证新版本是否与先前版本保持兼容。这有助于捕获潜在的兼容性问题并进行修复。

4. **API/ABI 文档和声明：** FFmpeg 提供详细的 API 和 ABI 文档，以指导开发者正确地使用和链接 FFmpeg 库。API 文档描述了每个公共函数的用法，而 ABI 文档描述了符号版本控制的规则和库之间的兼容性。

5. **废弃和移除策略：** 当不再需要某些旧 API 或 ABI 时，FFmpeg 会首先将其标记为已废弃，并在后续版本中移除。这使得开发者在迁移代码时有足够的时间进行适应。

6. **稳定分支：** FFmpeg 维护一个稳定分支，用于维护和修复旧版本的问题。这有助于确保旧版本的 ABI 兼容性。

7. **API 扩展：** FFmpeg 的 API 扩展通常在较新的版本中引入，以保持较旧版本的 ABI 兼容性。新功能会在次版本号增加时引入。

总之，FFmpeg 通过版本管理、符号版本控制、文档、测试等多种方式来保证 ABI 兼容性，以确保开发者能够稳定地使用不同版本的 FFmpeg 库进行开发。开发者在使用 FFmpeg 时应该参考相关的文档和指南，以确保正确链接和使用库的版本。



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

FFmpeg音频解码

https://www.jianshu.com/p/d77718947e21