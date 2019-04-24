---
title: ffmpeg常用命令
date: 2017-02-16 22:15:55
tags:
	- video
	- ffmpeg
---
下载windows版本的ffmpeg，在git bash行下执行，比较习惯bash的命令行风格。

# 基本命令
1、`./ffmpeg`。
可以看到版权信息和编译时打开的功能。
可以看到命令的基本格式是：`./ffmpeg [opt] [in opt] -i infile [out opt] outfile`。
用`./ffmpeg -h`。可以看到更多的帮助信息。

`./ffmpeg -h long`看到的帮助信息更加详细。

分析一下帮助信息，分为以下5种：
1）通用选项。
2）per file选项。
3）video选项。
4）audio选项。
5）subtitle选项。

2、查询性质的命令。
格式都是`./ffmpeg -xxx`。
xxx可能的取值是：
formats：查询支持的文件格式。
protocols：查询支持的协议。
colors：颜色。

`./ffmpeg -i test.mp4`。查询文件的信息。

# 实用命令

1、从mp4文件中提取h264码率。
`./ffmpeg -i test.mp4 -codec copy -bsf: h264_mp4toannexb -f h264 test.264`

h264有两种封装，一种是annexb模式，传统模式，有startcode，SPS和PPS是在ES中。一种是mp4模式，一般mp4 mkv会有，没有startcode，SPS和PPS以及其它信息被封装在Container中，每一个frame前面是这个frame的长度。
很多解码器只支持annexb这种模式，因此需要将mp4做转换，在ffmpeg中用`h264_mp4toannexb_filter`可以做转换。
3.5M的mp4文件得到的h264码流文件是2.8M。
得到的h264文件，可以用vlc播放器来播放。默认vlc不能播放。打开`工具--首选项--左下角选择全部显示设置--找到输入/编解码器--去复用器--去复用模块--选择H264视频去复用器`。再进行h264文件播放就可以了。
看媒体信息，可以看到只有视频流。
播放完之后，要把刚刚改的设置改回去，不然vlc就没法播放mp4文件了。

2、从mp4文件提取音频。
` ./ffmpeg.exe -i test.mp4 -vn test.aac`。

3、把aac和h264合并成mp4文件。
`./ffmpeg.exe -i test.aac -i test.264 test2.mp4`。
得到的文件比原来的test.mp4要小，只有800K左右。原来是3.5M左右。

4、把mp4文件分成图片。
`./ffmpeg.exe -i test.mp4 pic/test%d.jpg`。
应该是每一帧生成了一张图片。每张图片是40KB。

5、 把图片合并为一个mp4文件。
`./ffmpeg.exe -f image2 -i pic/test%d.jpg test3.mp4`。
得到的test3.mp4大小是1.5M左右。

6、从mp4文件中提取yuv数据。
`./ffmpeg.exe -i test.mp4 -vcodec rawvideo -an test.yuv`



# 音频相关命令

打印音频文件信息。

```
ffprobe -v quiet -print_format json -show_format -show_streams startup.wav  
```

pcm转wav

```
ffmpeg -f s16le -ar 16k -ac 1 -i data2.pcm data2.wav
```



wav转pcm

```
ffmpeg -i volume_new.wav -f s16le -acodec pcm_s16le volume_new.pcm
```

mp3转wav

```
ffmpeg  -i  input.mp3 output.wav
```

# 图片处理

