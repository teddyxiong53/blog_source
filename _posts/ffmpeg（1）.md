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