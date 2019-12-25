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



编译例子

make examples

用单步调试的方法，阅读下面的代码。

decode_audio.c这值得看一下。

现在我测试的材料是1.mp3文件。这个时长是1.8s。是我合成的一个文件。

单声道，16K，16bit有符号。

```
./decode_audio ./1.mp3 ./1.out
```

1.out可以有Audacity导入，选择原始数据。

1.mp3文件大小刚好是3600字节。

从打印看，一次是处理72个字节。

对应的parse函数是跳转到这里，mpegaudio_parse



demuxing_decoding

这个是解封装和解码。

我随便找一个mp4文件，改名为2.mp4。

```
./demuxing_decoding ./2.mp4 2-video 2-audio
```

我找的这个mp4文件是vscode里的演示视频。没有音频。

执行完成后，会提示你可以这样进行播放：

```
ffplay -f rawvideo -pix_fmt yuv420p -video_size 1596x1080 2-video
```

encode_audio

这个是随机生成了一些数据。然后编码得到文件。



```
AVPacket
	存放的是压缩的数据。
	由demuxer输出。
	然后传递给decoder。
	或者是从encoder输出，传递给muxer。
	对于video，它应该包含一个压缩的帧。
	对于audio，它包含多个压缩的帧。
	encoder可以输出空的packet。
	所谓空的packet，是指没有音视频数据，只有一些控制信息。AVPacketSideData
	AVPacket是一个比较特殊的结构体。
	里面内容并不多。
		AVBufferRef *buf
		pts
			pts必须大于等于dts。
			AV_NOPTS_VALUE 这个如果没有，就用这个值。
		dts
			d代表decompression，解压的意思。
			也可以用AV_NOPTS_VALUE。
		data指针
		size
		flags
		side_data
		duration
		pos
	配套的函数：
		av_packet_ref
		av_packet_unref
		
AVFrame
	这个结构体代表界面后的数据。
	必须用av_frame_alloc来进行分配。
	必须用av_frame_free进行释放。
	AVFrame一般只分配一次，然后多次使用。
	在这种使用情况下，av_frame_unref把AVFrame reset到初始状态。
	AVPacket也是这样用的。
	成员变量：
		width、height
			对于video。
		nb_samples
			对于audio。
			表示这个AVFrame里包含的音频帧的个数。
		format
			对于audio，是AVSampleFormat
			对于video，是AVPixelFormat
		key_frame
			1或者0
		pict_type
			I帧、B帧等。
		pts
		pkt_dts
		sample_rate
		channel_layout
		pkt_pos
		pkt_duration
		channels
		pkt_size
		
《一百万个可能》歌曲信息。
	Audio file with ID3 version 2.3.0, 
	contains: MPEG ADTS, layer III, v1, 128 kbps, 44.1 kHz, JntStereo
	
	Metadata:
    title           : 一百万个可能（温柔男声版）（Cover：Christine Welch）
    album           : 一百万个可能
    artist          : 黑崎子
  Duration: 00:03:56.70, start: 0.025057, bitrate: 128 kb/s
    Stream #0:0: Audio: mp3, 44100 Hz, stereo, s16p, 128 kb/s
    Metadata:
      encoder         : LAME3.99r
    Side data:
      replaygain: track gain - -4.800000, track peak - unknown, album gain - unknown, album peak - unknown, 
```



# 参考资料

1、FFMpeg框架代码阅读

https://www.cnblogs.com/azraelly/archive/2012/12/30/2840133.html

2、FFmpeg源代码结构图

https://www.cnblogs.com/x_wukong/p/4864863.html

3、多媒体文件格式探测⑨

https://www.cnblogs.com/tocy/p/media_container_9-probe-utility.html

4、如何在mac中使用VScode来调试ffmpeg、x264和x265

https://blog.csdn.net/xueyushenzhou/article/details/86736273