---
title: ffmpeg之调试方法
date: 2020-02-26 09:47:40
tags:
	- 视频

---

1

gdb调试方法

目前的问题是，我另外安装了ffmpeg，自动会去连接系统目录下的动态库。

而很多代码都是在动态库里的。

我当然是希望优先连接当前目录下编译出来的动态库。

或者简单点，让生成的ffmpeg，完全进行静态链接。

```
teddy@teddy-ThinkPad-SL410:~/work/ffmpeg-compile/ffmpeg-4.2.2$ ldd ./ffmpeg_g
        linux-vdso.so.1 =>  (0x00007ffd5acd6000)
        libavdevice.so.58 => /usr/local/ffmpeg/lib/libavdevice.so.58 (0x00007fcd76ee2000)
```

手动在Makefile里加-static选项，会链接不过。

用下面命令配置一下看看。

```
./configure --extra-ldexeflags="-static"
```

这样编译是好的。可以用来调试了。

直接用打印的方式来调试还方便点。

修改后，直接make，就可以把修改编译进来。

目前编译有优化，在单步执行的时候，跳转很没有规律。

在ffbuild/config.mak里，搜索"-O"，可以看到默认是O3 的，改成O0的。

再touch一下example的例子。make examples。这样就可以直接生效了。

但是如果改动了库里面的代码，则会编译所有的examples。也比较耗时。

可以在config.mak里，把不需要的example的配置项改成no。



现在需要用ffmpeg通过C代码打开alsa设备进行录音操作。

但是这样代码不行：

```
 AVInputFormat *ifmt=av_find_input_format("alsa");  
 if(avformat_open_input(&a_ifmtCtx,"default",ifmt,NULL)!=0){  
     printf("Couldn't open input stream.default\n");  
     return -1;  
 }  
```

首先alsa就找不到。

configure查看可用的输入设备有这些。

是因为我没有配置进来导致的。

因为用我本地编译的不行，提示找不到alsa格式。

```
./ffmpeg -f alsa -i hw:0,0 1.wav
```

而用apt-get安装的，则可以。

用ffmpeg -buildconf  查看比较一下。

还是多了不少的配置项。我觉得有影响的，可能是这个

```
    --enable-gpl
```





总结一下配置

```
./configure --disable-doc --extra-ldexeflags="-static" \
	--disable-asm \
	--enable-gpl \
	--enable-indevs  \
    --enable-alsa    \
    --enable-outdevs \
	--enable-debug \
	 --enable-pic \
	 --enable-nonfree 
```

但是会打印这个：

```
ERROR: alsa requested but not found
```

```
Enabled indevs:
fbdev                   lavfi                   oss                     v4l2

Enabled outdevs:
fbdev                   oss                     v4l2
```

把默认安装的ffmpeg的configure选项完全拷贝过来执行，可以看到。

```
Enabled indevs:
alsa                    fbdev                   lavfi                   oss                     v4l2                    xcbgrab

Enabled outdevs:
alsa                    fbdev                   oss                     v4l2                    xv
```

一切都是--extra-ldexeflags="-static"  这个导致的。去掉这个就可以看到alsa的了。

通过指定LD_LIBRARY_PATH来做保证链接本地的库吧。

```
export FF_DIR=/home/teddy/work/ffmpeg-compile/ffmpeg-4.2.2
export LD_LIBRARY_PATH=${FF_DIR}/libavcodec/:${FF_DIR}/libavdevice/:${FF_DIR}/libavfilter/:${FF_DIR}/libavformat/:${FF_DIR}/libavresample/:${FF_DIR}/libswresample/:${FF_DIR}/libavutil/:${FF_DIR}/libpostproc
```

感觉禁用掉asm，编译的过程会快很多。



我写代码时，有一个错误，居然编译没有报错。

```
avcodec_parameters_from_context(stream->codecpar, codec_context );
函数的第二个参数，是一个codec_context类型的，但是我传递了AVCodec的指针，也编译过了。
```

估计是动态库链接方式的问题。



```
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <inttypes.h>

#include <libavutil/channel_layout.h>
#include <libavutil/common.h>
#include <libavutil/frame.h>
#include <libavutil/samplefmt.h>

#include "libavdevice/avdevice.h"
#include "libavformat/avio.h"
#include "libavutil/time.h"
#include "libavcodec/avcodec.h"
#include "libavformat/avformat.h"
#include <unistd.h>
#include "mylog.h"

AVFormatContext *inputContext;
AVFormatContext *outputContext;

int64_t lastReadPacketTime;
int64_t packetCount = 0;
int interrupt_cb(void *arg);
int openInput(char *input_url);
int initDecodeContext(AVStream *inputStream);

int initEncoderCodec(AVStream *inputStream, AVCodecContext **encodeContext);


int interrupt_cb(void *arg)
{
    int timeout = 3;
    if(av_gettime() - lastReadPacketTime > timeout*1000*1000) {
        return -1;
    }
    return 0;
}
int openInput(char *input_url)
{
    inputContext = avformat_alloc_context();
    lastReadPacketTime = av_gettime();
    inputContext->interrupt_callback.callback = interrupt_cb;
    AVInputFormat *ifmt = av_find_input_format("alsa");
    if(!ifmt) {
        mylogd("can not find format for input:%s\n", "alsa");
        return -1;
    }
    AVDictionary *options = NULL;//这个后面再加选项。
    int ret;
    ret = avformat_open_input(&inputContext, input_url, ifmt, NULL);
    if(ret < 0) {
        mylogd("open %s fail\n", input_url);
        return -1;
    }
    ret = avformat_find_stream_info(inputContext, NULL);
    if(ret < 0) {
        mylogd("find stream info fail\n");
        return -1;
    }
    mylogd("open input ok\n");
    return 0;
}

int initDecodeContext(AVStream *inputStream)
{
    enum AVCodecID codecId =  inputStream->codec->codec_id;
    AVCodec *codec =  avcodec_find_decoder(codecId);
    if(!codec) {
        mylogd("can not find decoder\n");
        return 1;
    }
    //打开
    int ret = avcodec_open2(inputStream->codec, codec, NULL);
    if(ret < 0) {
        mylogd("open codec fail\n");
        return -1;
    }
    return 0;
}
int initEncoderCodec(AVStream *inputStream, AVCodecContext **encodeContext)
{
    AVCodec *codec;
    codec = avcodec_find_encoder(AV_CODEC_ID_AAC);
    if(!codec ) {
        mylogd("find mp3 encoder fail\n");
        return -1;
    }
    *encodeContext = avcodec_alloc_context3(codec);
    if(!(*encodeContext)) {
        mylogd("alloc context fail\n");
        return -1;
    }
    (*encodeContext)->codec_id = codec->id;
    (*encodeContext)->time_base.den = 16000;
    (*encodeContext)->time_base.num = 1;
    (*encodeContext)->sample_fmt = AV_SAMPLE_FMT_S16;
    (*encodeContext)->sample_rate = 16000;
    (*encodeContext)->channels = 1;
    (*encodeContext)->channel_layout = av_get_default_channel_layout(1);
    (*encodeContext)->bit_rate = 16000;
    
    (*encodeContext)->strict_std_compliance = FF_COMPLIANCE_EXPERIMENTAL;
    int ret = 0;
    ret = avcodec_open2(*encodeContext, codec, NULL);
    if(ret < 0) {
        mylogd("open codec fail\n");
        return -1;
    }
    ret = avcodec_parameters_from_context(inputStream->codecpar, (*encodeContext));
    if(ret < 0) {
        mylogd("set param fail\n");
        return -1;
    }
    return 0;
}
int openOutput(char *outurl, AVCodecContext *encodeContext);

int openOutput(char *outurl, AVCodecContext *encodeContext)
{
    int ret = 0;
    int i = 0;
    ret = avformat_alloc_output_context2(&outputContext, NULL, "wav", outurl);
    if(ret < 0) {
        mylogd("alloc output context fail\n");
        goto error;
    }
    ret = avio_open2(&outputContext->pb, outurl, AVIO_FLAG_WRITE, NULL, NULL);
    if(ret < 0) {
        mylogd("avio open fail\n");
        goto error;
    }
    //创建输出stream。
    AVStream *stream = avformat_new_stream(outputContext, encodeContext->codec);
    ret = avcodec_copy_context(stream->codec, encodeContext);
    if(ret < 0) {
        mylogd("copy context fail\n");
        goto error;
    }
    //写文件头部。
    mylogd("");
    ret = avformat_write_header(outputContext, NULL);
    mylogd("");
    if(ret < 0) {
        mylogd("write file header fail, %s\n", av_err2str(ret));
        goto error;
    }
    mylogd("open output ok\n");
    return 0;
error:
    if(outputContext) {
        for(i=0; i<outputContext->nb_streams; i++) {
            avcodec_close(outputContext->streams[i]->codec);
        }
        avformat_close_input(&outputContext);
    }
    return -1;
}
AVPacket * readPacketFromSource();

AVPacket * readPacketFromSource()
{
    AVPacket *pkt = av_packet_alloc();
    av_init_packet(pkt);
    lastReadPacketTime = av_gettime();
    int ret = av_read_frame(inputContext, pkt);
    if(ret < 0) {
        return NULL;
    }
    return pkt;
}
int decodePacket(AVStream *stream, AVPacket *pkt, AVFrame *frame);

int decodePacket(AVStream *stream, AVPacket *pkt, AVFrame *frame)
{
    return 0;
}
void initFfmpeg();

void initFfmpeg()
{
    av_register_all();
	avformat_network_init();
	avdevice_register_all();
	av_log_set_level(AV_LOG_DEBUG);
}

void closeInput()
{

}

void closeOutput()
{

}

int main()
{
    int ret;
    initFfmpeg();
    ret = openInput("default");
    if(ret < 0) {
        mylogd("open input fail\n");
        goto error;
    }
    //只有一路，是音频的，就取这一路。
    ret = initDecodeContext(inputContext->streams[0]);
    if(ret < 0) {
        mylogd("init decode context fail\n");
        goto error;
    }
    AVFrame *audioFrame = av_frame_alloc();
    AVCodecContext *encodeContext = NULL;
    ret = initEncoderCodec(inputContext->streams[0], &encodeContext);
    if(ret < 0) {
        goto error;
    }
    ret = openOutput("1.wav", encodeContext);
    if(ret < 0) {

        mylogd("open output fail\n");
        goto error;
    }
    while(1) {
        //读取输入
        
        //发去编码
        //获取编码后的数据，写入
        sleep(1);
    }
    
    return 0;
error:
    closeInput();
    closeOutput();
    return -1;
}
```



参考资料 

1、

https://github.com/zimbatm/ffmpeg-static/blob/master/build.sh

2、

https://blog.csdn.net/momo0853/article/details/78043903