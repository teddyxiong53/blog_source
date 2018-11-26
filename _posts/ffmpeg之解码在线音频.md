---
title: ffmpeg之解码在线音频
date: 2018-11-26 11:57:25
tags:
	- 音频
---



总体上分为3步：

1、解封装。输入是mp3文件。

2、解码。mp3编码。

3、pcm数据重采样。

解封装的过程
1、调用av_register_all，注册所有的封装器和解封装器。

2、调用avformat_open_input函数，打开一个文件，参数可以是一个文件名，也可以是一个url。

3、调用avformat_find_stream_info，查找流信息，把信息存入到AVFormatContext里。

4、在AVFormatContext里搜索，找到音频流的索引值codec_id。

5、根据codec_id，用avcodec_find_decoder，取得对应的AVCodec* 

6、使用avcodec_open2打开解码器。

写成代码是这样：

```
#include <libavutil/frame.h>
#include <libavcodec/avcodec.h>
#include <libavforamt/avformat.h>
#include <libavutil/dict.h>

int main()
{
	int filename = "./1.mp3";
	AVFrame *avFrame = av_frame_alloc();
	AVFormatContext * formatContext ;
	int ret;
	//1. format process
	//1.1 register all fromat
	av_register_all();
	//1.2 open file
	avformat_open_input(&formatContext, filename, NULL, NULL);
	//1.3 find audio stream
	avformat_find_stream_info(formatContext, NULL);
	//1.4 find audio codec_id
	int streamsCount = formatContext->nb_streams;
	AVDictionaryEntry *tag = NULL;
	while(tag = av_dict_get(formatContext->metadata, "", tag, AV_DICT_IGNORE_SUFFIX)) {
		char *key = tag->key;
		char *value = tag->value;
		printf("key:%s, value:%s\n", key,value);
	}
	int audio_id = -1;
	for(int i=0; i<streamsCount; i++) {
		if(formatContext->streams[i]->codec->codec_type == AVMEDIA_TYPE_AUDIO) {
			audio_id = i;
			break;
		}
	}
	if(audio_id < 0) {
		return -1;
	}
	//1.5 find decoder
	AVCodecContext *codecContext;
	codecContext = formatContext->streams[audio_id]->codec;
	AVCodec *codec = avcodec_find_decoder(codecContext->codec_id);
	
	//1.6 open decoder
	avcodec_open2(codecContext, codec, NULL);
	
	
}
```



参考资料

1、使用FFMpeg 解码音频文件

https://blog.csdn.net/douzhq/article/details/82937422





