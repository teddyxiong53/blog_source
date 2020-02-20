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

# 视频处理

## 从mp4文件中提取h264码流。

```
ffmpeg -i test.mp4 -codec copy -bsf: h264_mp4toannexb -f h264 test.264
```

h264有两种封装，一种是annexb模式，传统模式，有startcode，SPS和PPS是在ES中。一种是mp4模式，一般mp4 mkv会有，没有startcode，SPS和PPS以及其它信息被封装在Container中，每一个frame前面是这个frame的长度。
很多解码器只支持annexb这种模式，因此需要将mp4做转换，在ffmpeg中用`h264_mp4toannexb_filter`可以做转换。
3.5M的mp4文件得到的h264码流文件是2.8M。
得到的h264文件，可以用vlc播放器来播放。默认vlc不能播放。打开`工具--首选项--左下角选择全部显示设置--找到输入/编解码器--去复用器--去复用模块--选择H264视频去复用器`。再进行h264文件播放就可以了。
看媒体信息，可以看到只有视频流。
播放完之后，要把刚刚改的设置改回去，不然vlc就没法播放mp4文件了。

## 从mp4文件提取音频。

```
ffmpeg.exe -i test.mp4 -vn test.aac
```

vn表示no video的意思。

可以指定格式：

```
ffmpeg -i input.mp4 -f mp3 output.mp3
```

指定输出的详细参数：

```
ffmpeg -i input.mp4 -vn -ar 16000 -ac 1 -ab 320 -f mp3 output.mp3
```

## 把声音合成到视频里

```
ffmpeg -i input_music.mp3 -i input_video.mp4 output.mp4
```



## 把aac和h264合并成mp4文件。

```
ffmpeg.exe -i test.aac -i test.264 test2.mp4
```

得到的文件比原来的test.mp4要小，只有800K左右。原来是3.5M左右。



## 把图片合并为一个mp4文件

```
ffmpeg.exe -f image2 -i pic/test%d.jpg test3.mp4
```

得到的test3.mp4大小是1.5M左右。

## 把视频切分为图片

```
ffmpeg -i input.mp4 frames/frame%03d.png
```



## 从mp4文件中提取yuv数据

`./ffmpeg.exe -i test.mp4 -vcodec rawvideo -an test.yuv`

## 格式转化

直接靠后缀名就可以了。

```
ffmpeg -i input.mp4 output.avi
```

还可以指定详细一点。

```
ffmpeg -i input.flv -vcodec copy -acodec copy output.mp4
```

上面命令是把flv转为mp4，只是改了封装。音频和视频直接拷贝过去的。

更加详细指定参数。

```
ffmpeg -y -i input_video.mp4 -bitexact -vcodec h263 -b 128 -r 15 -s 176x144 -acodec aac -ac 2 -ar 22500 -ab 24 -f 3gp output.3gp
```

## 从视频中剪切一段

```
ffmpeg -i input.mp4 -ss 00:01:45 -t 10 output.mp4
```

上面命令表示从视频的1分45秒处，剪切10秒的视频出来。

## 视频加速

```
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" output.mp4
```

## 视频减速

```
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" output.mp4
```

## 视频截图

```
ffmpeg -i input.mp4 -f image2 -t 0.001 -ss 10 -s 1920x1080 output.jpg
```

上面命令表示，在10秒的位置，截取一张1920x1080的图片。

也可以这样：

```
ffmpeg -i  input.mp4 -vframes 1 -ss 00:00:06.000 output.jpg
```

## 视频转gif

```
ffmpeg -i input.mp4 -vframes 30 -f gif output.gif
```

上面命令表示把视频的前面30帧转成gif。

## gif转视频

```
ffmpeg -i input.gif 
```





# 音频处理

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

降低mp3文件的码率

```
ffmpeg -i dudu.mp3 -b:a 16k dudu_out.mp3
```

MP3转pcm

```
ffmpeg -i input.mp3 -acodec pcm_s16le -f s16le -ac 1 -ar 16000 output.pcm
```

调节音量

```
ffmpeg -i input.mp3 -af volume=-3dB output.mp3
```



录音

```

```



# 图片处理

批量缩放图片。

```
#!/bin/sh
in_dir=in
out_dir=out
files=`ls $in_dir`
for f in $files; do
	ffmpeg -i $in_dir/$f -f scale=320:249 $out_dir/$f
donef in $files; do
	ffmpeg -i $in_dir/$f -f scale=320:249 $out_dir/$f
done
```



# rtsp相关



参考资料

1、ffmpeg入门笔记

http://einverne.github.io/post/2015/12/ffmpeg-first.html

2、How to specify audio and video bitrate

https://superuser.com/questions/319542/how-to-specify-audio-and-video-bitrate

3、

https://blog.csdn.net/u013010310/article/details/52371440