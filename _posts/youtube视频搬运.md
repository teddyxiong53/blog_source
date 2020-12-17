---
title: youtube视频搬运
date: 2020-12-11 11:11:30
tags:
	- 自媒体
---

1

我定一个基本规则：

1、~~只下载1080P的。如果没有，下载720P的。其余不考虑。~~实际上，youtube默认只让你下载720P的。720P的尺寸小多了。清晰度可以接收。就用720P。

2、视频格式，只要MP4，音频只要aac。但是看了一下，音频经常是只有m4a。那就已m4a为主。（音频这个也不用管，720P的默认音视频是一起的）

3、字幕，只下载中文的。因为我是从国外往国内搬运。（这个实际上，只有部分的有英文字幕，下载中文字幕，想多了）

我把下载命令整理成脚本了。

https://gitee.com/teddyxiong53/youtube_translate







# 摸索过程

下面我已一期great scott的视频为例子，来测试命令看看。

## 下载一个视频

视频地址是这个：

https://www.youtube.com/watch?v=6LxRnf6sQNQ

完整的是这样：

https://www.youtube.com/watch?v=6LxRnf6sQNQ&t=27s&ab_channel=GreatScott%21

t=27s，这个是广告时长。

我用git bash来进行操作。这个命令行比windows命令行要好用。

```
# 为了方便后面的操作，把url定义为video变量。
export video="https://www.youtube.com/watch?v=6LxRnf6sQNQ"
./youtube-dl.exe --list-formats $video
```

可以看到有这些格式：

```
[youtube] 6LxRnf6sQNQ: Downloading webpage
[info] Available formats for 6LxRnf6sQNQ:
format code  extension  resolution note
249          webm       audio only tiny   53k , opus @ 50k (48000Hz), 3.54MiB
250          webm       audio only tiny   70k , opus @ 70k (48000Hz), 4.39MiB
140          m4a        audio only tiny  130k , m4a_dash container, mp4a.40.2@128k (44100Hz), 9.02MiB
251          webm       audio only tiny  140k , opus @160k (48000Hz), 8.11MiB
278          webm       256x144    144p   97k , webm container, vp9, 25fps, video only, 5.30MiB
160          mp4        256x144    144p  105k , avc1.4d400c, 25fps, video only, 3.11MiB
242          webm       426x240    240p  224k , vp9, 25fps, video only, 6.97MiB
133          mp4        426x240    240p  225k , avc1.4d4015, 25fps, video only, 5.39MiB
243          webm       640x360    360p  408k , vp9, 25fps, video only, 12.00MiB
134          mp4        640x360    360p  476k , avc1.4d401e, 25fps, video only, 9.95MiB
244          webm       854x480    480p  749k , vp9, 25fps, video only, 17.63MiB
135          mp4        854x480    480p  978k , avc1.4d401e, 25fps, video only, 14.65MiB
247          webm       1280x720   720p 1509k , vp9, 25fps, video only, 30.20MiB
136          mp4        1280x720   720p 2072k , avc1.4d401f, 25fps, video only, 23.93MiB
248          webm       1920x1080  1080p 2648k , vp9, 25fps, video only, 85.57MiB
137          mp4        1920x1080  1080p 4166k , avc1.640028, 25fps, video only, 89.37MiB
18           mp4        640x360    360p  425k , avc1.42001E, 25fps, mp4a.40.2@ 96k (44100Hz), 29.63MiB
22           mp4        1280x720   720p 1451k , avc1.64001F, 25fps, mp4a.40.2@192k (44100Hz) (best)

```

可以看到1080P的视频是80M左右，而720P的视频是20M左右。

音频，m4a的只有一个，有9M。比较大。

那我不如选择webm格式，最小的那个。

默认下载：

```
$ ./youtube-dl.exe $video
[youtube] 6LxRnf6sQNQ: Downloading webpage
[download] Destination: DIY LiPo Supercharger! (Charge, Protect, 5V_12V Boost V2)-6LxRnf6sQNQ.mp4
[download] 100% of 101.06MiB in 01:39

Administrator@doss MINGW64 /d/tools/youtube-dl-dir
$ ls
'DIY LiPo Supercharger! (Charge, Protect, 5V_12V Boost V2)-6LxRnf6sQNQ.mp4'   youtube-dl.exe*

```

## 查看视频信息

用vlc播放器查看。

是下载了720P的。音频格式是m4a的。

![image-20201211140910642](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201211140910642.png)

默认是匹配的best。就是这个。

```
22           mp4        1280x720   720p 1451k , avc1.64001F, 25fps, mp4a.40.2@192k (44100Hz) (best)
```

好吧，这么看，默认的best策略是符合我的需求的。

接近10分钟的视频，100M左右。

那么就可以理解为1分钟数据是10M左右。

我需要了解这个，来评估我的梯子够不够用。





请注意，YouTube采取了某种保护措施，以防止下载工具下载（甚至看不到）1080p版本，但是您仍然可以下载所有其他分辨率，包括720p以下。



加上这个选项，表示自动选择可以下载的最高分辨率。

```
-f best 
```

这些命令将确保您从视频中下载最高质量的mp4视频和m4a音频作为单个文件，或者将它们合并回单个mp4（`ffmpeg`在我的情况下使用）。



如果`ffmpeg`或`avconv`不可用，`youtube-dl`应回退到单个文件`-f best option`而不是默认文件。



我当前并没有安装ffmpeg，但是还是成功产生了一个文件。

应该是720P的，音视频就是一个文件，没有分开的。



## 下载字幕文件

当前下载下来没有字幕。

看看这样能不能把中英文字幕都下载下来。

```
./youtube-dl.exe --write-auto-sub --sub-lang en,cn -f 18 $video
```

为了加快测试的速度，我选择18号的格式，这个提交比较小。

还是没有字幕。

查看一下字幕。

```
./youtube-dl.exe --list-subs $video
```

只有英文的。

```
Language formats
en       vtt, ttml, srv3, srv2, srv1
```

试一下这个

```
./youtube-dl.exe --write-sub --skip-download --sub-lang zh-Hans -f 18 $video 
```

提示没有中文字幕。

```
$ ./youtube-dl.exe --write-sub --skip-download --sub-lang zh-Hans -f 18 $video
[youtube] 6LxRnf6sQNQ: Downloading webpage
WARNING: zh-Hans subtitles not available for 6LxRnf6sQNQ
```

把zh-Hans改成cn，也不行。

这样可以把英文的字幕下载下来。

```
./youtube-dl.exe --write-sub --skip-download --all-subs -f 18 $video
```

文件是

```
'DIY LiPo Supercharger! (Charge, Protect, 5V_12V Boost V2)-6LxRnf6sQNQ.en.vtt'
```

vtt文件，可以用notepad++打开。





![image-20201211143251336](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201211143251336.png)

## 字幕自动翻译工具

说实话，翻译比较耗时。看看有没有办法直接对vtt进行机器翻译。

有工具。

https://www.appinn.com/tern-subtitle-file-translator/

tern这个工具，有windows和macos 2个版本。

对于个人用户来说，每个月 Tern 自带的 100 万字符免费额度，加翻译平台的免费额度，完全足够免费使用。

我要处理的视频，应该大部分都是这种情况，需要联网单独下载字幕文件，然后翻译。

## 播放列表下载

播放列表在这里。

https://www.youtube.com/c/greatscottlab/playlists

先选一个感兴趣的主题。

例如这个，电子基础知识。这个就不错。

播放列表的url是这样的：

https://www.youtube.com/playlist?list=PLAROrg3NQn7dGPxb9CFtxwbgzLNaaj1Oe

youtube-dl怎么下载播放列表？

先查看列表里有哪些文件。

```
$ export list="https://www.youtube.com/playlist?list=PLAROrg3NQn7dGPxb9CFtxwbgzLNaaj1Oe"
$ ./youtube-dl.exe --flat-playlist $list
[youtube:tab] PLAROrg3NQn7dGPxb9CFtxwbgzLNaaj1Oe: Downloading webpage
[download] Downloading playlist: Electronics Projects
[youtube:tab] Downloading page 1
[youtube:tab] playlist Electronics Projects: Downloading 140 videos
[download] Downloading video 1 of 140
[download] Downloading video 2 of 140
[download] Downloading video 3 of 140
[download] Downloading video 4 of 140
[download] Downloading video 5 of 140
```

然后可以下载整个列表。不知道有多大。

可以选择先下载前面10个。

同时还把对应的字幕文件一起下载下来。

## 批量下载字幕文件

下面的单独下载字幕的。

下载这一步，没有什么特别的。就一次性的。

```
./youtube-dl.exe --write-sub --all-subs --yes-playlist --skip-download --playlist-start 1 --playlist-end 2 $list 
```

加入下载完成了，有140个vtt文件。

怎么提交一次性翻译？

先下载工具，工具还有点大，有100多M。

界面是基于electron写的，所以可以跨平台。

总体的原理是后台调用腾讯云等翻译服务。需自己填入appkey等信息。

![image-20201211151339682](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201211151339682.png)

## 批量翻译字幕文件

这个工具也是可以批量加入文件进行翻译的。

140个也可以一次性翻译完成。

## 合成视频和字幕

140个文件，每个大小在100M左右。那么就是14G左右。这点流量还是有的。

下载视频。把原始字幕和翻译字幕放进去看看效果。

```
./youtube-dl.exe  --yes-playlist --playlist-start 1 --playlist-end 2 $list 
```

当前这样下载，默认就把字幕都嵌入到视频文件了。

我可以再把翻译后中文字幕再拖入到vlc里。

看到的效果就是这样，这样就最好了。达到了中英文双语字幕的效果了。非常好。

![image-20201211153526629](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201211153526629.png)

![image-20201211154353403](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201211154353403.png)

就是不知道上传到B站会是什么效果。

## 上传B站试一下

试一下就知道了。

不行。不能直接上传字幕文件。那么最好的方法，还是我本地来完成视频和字幕的合成。

然后再上传。本地看到的，要就是最后的效果。

那就需要用ffmpeg来完成字幕的集成。

## 做字幕（软字幕不行）

当前视频里是没有字幕的。

之前显示英文字幕，是因为我把英文字幕跟视频文件放在同一个目录下。

中文字幕，是因为我把文件拖放到vlc里。

现在把字幕文件放到其他位置，然后重新打开视频。可以看到没有任何字幕。

那么接下来，就看用ffmpeg怎么来集成了。然后再加上我的个人水印。

最好字幕不是称为视频上的部分，而是在容器里的一部分。这就是所谓软字幕。

相对应的就是硬字幕。

```
ffmpeg -i input.mkv -i subtitles.srt -c copy output.mkv
```

试一下。

这个没有用。一个字幕都没有弄进去。

```
./ffmpeg.exe -i "DIY ESP32 AC Power Meter (with Home Assistant_Automation Integration)-PSzkaSy5lHY.mp4" -i "DIY ESP32 AC Power Meter (with Home Assistant_Automation Integration)-PSzkaSy5lHY.en.vtt" -i "[tencent-en-zh] DIY ESP32 AC Power Meter (with Home Assistant_Automation Integration)-PSzkaSy5lHY.en.vtt" -c copy  output.mp4
```

先弄一个看看。

```
./ffmpeg.exe -i "DIY ESP32 AC Power Meter (with Home Assistant_Automation Integration)-PSzkaSy5lHY.mp4"  -i "[tencent-en-zh] DIY ESP32 AC Power Meter (with Home Assistant_Automation Integration)-PSzkaSy5lHY.en.vtt" -c copy  output.mp4

```

也不行。

由于mp4容器，不像MKV等容器有自己的字幕流。

是MP4的格式问题。

像MKV这种容器的视频格式中，会带有一个字幕流，可以在播放中，控制字幕的显示与切换，也可以通过工具或命令，将字幕从视频中分离出来。

而MP4格式的容器，是不带字幕流的。所以如果要将字幕集中进去，就需要将字幕文件烧进视频中去。烧进去的视频，不能再分离出来，也不能控制字幕的显示与否。

为了方便测试，我把文件改名如下：输入input.mp4、中文字幕cn.vtt、英文字幕en.vtt、输出文件output.mp4。

上面的说法不对。实际上可以的。

用下面的命令就可以。

```
./ffmpeg -i "input.mp4" -i cn.vtt -i en.vtt -map 0:v -map 0:a -map 1 -map 2  -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=chn -metadata:s:s:1 language=eng "output.mp4"

```

这里用到的参数较多。需要说明一下。

-map是轨道参数，如果只有一个字幕，就不需要这个参数。

在这个例子中，

-map 0:v表示第一个文件输入视频轨道，

-map 0:a 表示第二个轨道是第一个文件输入的音频轨道，

-map 1建立第三个轨道，

-map 2建立第四个轨道。

如果添加map参数，默认就只有一个字幕轨道，第二个英文字幕会覆盖第一个中文字幕轨道。



-c:s mov_text 字幕轨道采用mov_text的格式。

**这种格式是直接将srt或者vvt文件添加到视频文件中，但是不是直接渲染到视频中**。

这样的好处是添加速度快，

缺点是如果播放器不支持就不会显示字幕（手机上qq自带的和windows player之类的都不能正确显示），但是一般的PC播放器、手机上的mplayer、vlc、potplayer之类的主流播放器都可以显示。

如果要做到视频里面去就要用其他参数，还要设置好字体、字号、颜色等等。

> 当前我在vlc上播放，默认就是没有显示字幕的。不知道在B站上进行播放的时候，会不会默认显示双语字幕？

metadata:s:s:0 language=chn 这是设置第一条字幕的参数，如设置语言为中文。

请注意，这个语言不能写错或自定义，只能设置成固定的缩写。

如将这个写成zh-CN显示成 数字1之类的。

-metadata:s:s:1 language=eng 第二条字幕的语言设置为英文。

> 我用windows Media Player播放，并不能显示字幕。所以字幕要做成硬字幕。



```
ffmpeg -i input.mp4 -vf "subtitles=input.srt:force_style='FontName=Source Han Sans SC,Fontsize=27,PrimaryColour=&H88FFFFFF&'" -c:a copy -preset fast -crf 22 output.mp4
```

## 做硬字幕（可以）

由于mp4格式并不支持字幕流，

简单解决办法就是将字幕流烧写在视频流中，

因此也被称为是硬压制，压制过程需要重新解码编码的视频流



vtt的好像不行，我需要先统一把vtt转成ass字幕。

再进行操作。

这样就需要重新生成视频。慢是会慢一些的。

CPU占有率也非常高。

```
./ffmpeg.exe -i cn.vtt cn.ass 
./ffmpeg.exe -i en.vtt en.ass

./ffmpeg.exe -y -i input.mp4 \
-filter_complex "[0:v]ass=en.ass[tmp];[tmp]ass=cn.ass[sub]" \
-map [sub] -map 0:1 \
output.mp4
```



视频会变大一倍。

不过确实效果可以。没有乱码。格式可以接受。

就用这种方式。

网上可以开着电脑转码。10分钟的720P视频，我估计用了3到4分钟左右。

有些地方中英文字幕重叠了。

打开中文字幕文件，发现里面就已经是保留了英文的。

所以，我只需要放中文字幕文件，就已经是双语的效果了。

```
./ffmpeg.exe -y -i input.mp4 \
-filter_complex "[0:v]ass=cn.ass[sub]" \
-map [sub] -map 0:1 \
output.mp4
```



流程清楚了。接下来就是写脚本了。

就写在git bash下可以正常运行的bash脚本。

我觉得，可以用4位数的数字前缀来进行编号。

这样方便跟踪和梳理great scott的视频顺序。

我下载，也采用从老的到新的顺序来进行。



分析一下文件名的规律。

```
'DIY ESP32 AC Power Meter (with Home Assistant_Automation Integration)-PSzkaSy5lHY.mp4'
'DIY LiPo Supercharger! (Charge, Protect, 5V_12V Boost V2)-6LxRnf6sQNQ.mp4'
```

xx (yy)-zz.mp4

xx：本来的文件名。

yy：本领了文件名的说明部分。

zz：视频在youtube的id。

这个文件名已有可以不变动。

我在最前面加上0001-这样5个字符。

来依次给所有视频编号。

youtube-dl按时间从逆序下载。

用字幕下载来做实验。这样下载比较快。

## youtube-dl 输入文件名模板

这个对于整理文件是很有用的。

就在github帮助文档里搜索。

https://github.com/ytdl-org/youtube-dl#output-template



```
没有特别说明的，都是string类型
id  	视频id
title	
url		
ext 	扩展名
alt_title 第二个title
display_id 	另外一个id
uploader 	上传折的名字。全名。
license		视频采用的许可证。
creator 	视频的创造者
release_date 发布时间 YYYYMMDD格式。
timestamp   视频可以被访问的时间戳。numeric类型。
upload_date  上传时间
upload_id    上传者的昵称。
location      视频的拍摄地址
duration     时长。numeric类型。
view_count   观看数。
like_count   点赞数。
dislike_count  不喜欢的数目。
repost_count  repost的数量。转发的意思。
average_rating 平均分。
comment_count  评论数。
age_limit 年龄限制。
is_alive 视频是否直播。
start_time 视频真正开始的地方，除去前面的广告时间的。
end_time 视频真正结束的地方。
format 格式。
format_id  格式id
format_note  格式信息。
width 视频宽度
height 视频高度
resolution  分辨率
tbr  音频和视频平均码率
abr  音频的码率
acodec  音频的编码器
asr  音频采样率
vbr  视频的码率
fps  帧率
vcodec
container 视频容器
filesize  如果提前可以知道的文件大小
filesize_approx  估算的文件大小
protocol 下载协议
epoch  创建文件的unix时间戳
autonumber  这个是自动根据下载顺序创建的索引号，从0开始。5位的，00000开始。
playlist 
playlist_index
playlist_id
playlist_title
playlist_uploader
playlist_uploader_id

对于有章节的视频，还有这些可以用。
chapter
chapter_number
chapter_id
series
season   第几季
season_number
season_id
episode   第几集
episode_number
episode_id
```

## 指定视频质量

```
best
worst
bestvideo
worstvideo
bestaudio
worstaudio
```

可以这样：

```
-f best #最好的音频和视频
-f bestaudio 
-f bestvideo+bestaudio
-f 'bestvideo+bestaudio'
# 还可以加条件
-f "best[height<=480]" # 视频高度小于480里的最好的。
# 还可以组合
# 这个表示下载best，视频高度不大于480
-f 'bestvideo[height<=480]+bestaudio/best[height<=480]'
```



# 一次完成字幕和水印

这两个命令都可以。

但是是图片方式的。我只有文本水印就够了。

```
ffmpeg -i input.mkv -threads 0 -c:v -preset fast \
-vf "movie=watermark.png[wm];[in][wm]overlay=0:0,subtitles=subtitle.srt[out]" \
output.mp4

ffmpeg -i input.mkv -i watermark.png -threads 0 -c:v libx264 -crf 28 -preset veryslow \
-filter_complex "[0:v][1:v]overlay=0:0,subtitles=subtitle.srt[out]" \
-map "[out]" -map 0:a output.mp4
```

文本方式可以这样：

```
ffmpeg -i input.mp4 -vf "drawtext=fontfile=simhei.ttf: text='熊汉良翻译':x=1200:y=80:fontsize=24:fontcolor=white:shadowy=2" output.mp4
```

但是二者不能直接融合。

模式不一样，前者是complex filtergraph。后者是simple filtergraph。

我还是对命令不够熟练。

图片就图片吧。

网上做了一个签名。生成透明图片。

可以看到在左上角。这个可以。就这样。

![image-20201212174259469](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201212174259469.png)

https://superuser.com/questions/612635/ffmpeg-watermark-logo-with-hardcode-subtitle

## 最终的处理命令

可以一次性把水印和硬字幕做好。

```
ffmpeg -i input.mp4 -i watermark.png -threads 0 preset fast \
-filter_complex "[0:v][1:v]overlay=0:0,subtitles=subtitle.ass[out]" \
-map "[out]" -map 0:a output.mp4
```



# 没有字幕文件

1、上传到Youtube自动翻译

经常看Youtube的人都知道，Youtube上几乎所有的视频都有翻译字幕，这是Youtube会使用AI自动为用户上传的视频添加字幕，可以利用它的这个特性，为自己的视频添加字幕

我们可以在Youtube Studio中上传私享视频，视频上传后等待一段时间，Youtube就会自动生成英文字幕了，你可以直接用英文字幕，或者翻译成中文或者其他的语言。

这个对我来说没有可操作性。

因为需要上传后台。太麻烦了。



## 尝试脚本下载字幕

这个是下载视频字幕的。

https://github.com/1c7/Youtube-Auto-Subtitle-Download

这里下载油猴脚本。

https://greasyfork.org/zh-CN/scripts/5368-youtube-subtitle-downloader-v28

但是对于没有字幕文件的，还是不行。

![image-20201214114540404](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201214114540404.png)



## 只能自己配字幕

怎样自动翻译英文视频并添加字幕，几个免费工具交给你

https://zhuanlan.zhihu.com/p/142234424



## 网易见外平台

试用一下网易见外这个平台。看看翻译的效果怎么样。
上传速度不快。
只有400K左右的速度。
这个限制比较大。

处理也慢，也估计是把视频播放，实时语音识别。

自动化做的部分，应该就是把识别结果跟时间轴进行结合了。

上传了一个视频测试一下，效果还不错。

![image-20201214171030667](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201214171030667.png)

## python加字幕

我看看自己能不能做一个类似的离线版本。

或者脚本之类的。

谷歌一下“python 字幕”。

确实可以找到相关的软件。

工具叫做autosub。

autosub是由麻省理工学院创作，用于自动语音识别和字幕生成的实用程序。

原理是基于使用ffmpeg和调用Google语音识别API实现视频或音频转写字幕的操作。

目前试过在Ubuntu和windows10_64位均能正常运行，

原版的autosub需要python3环境并且未在Windows系统上提供可视化操作，

代码在这里。

https://github.com/agermanidis/autosub

显示是不再维护了。

上一次的更新是2年前。

争取把这个跑起来。这样搞不定，再考虑在线平台。



下载autosub代码。

```
sudo python3 setup.py install
```

或者你这样安装也可以。

```
sudo python3 -m pip install autosub
```

得到的是一个命令行工具：autosub。

查看支持的字幕文件格式：

```
teddy@thinkpad:~/work/autosub$ autosub --list-formats
List of formats:
srt
vtt
json
raw
```

查看支持的语言，基本都支持。

```
autosub --list-languages 
```

支持中文。

```
zh-CN   Chinese (Simplified)
```

测试一下，因为我需要翻译，所以需要谷歌翻译的apikey。-K参数就是。

但是申请需要信用卡。

我先不用翻译，只识别看看效果。

```
autosub -F vtt -S en -D zh-CN -K xxx input.mp4
```

只识别。

```
autosub -F vtt input.mp4
```

我找一个有字幕文件的，这样方便对比看看识别的准确性。

只要可以识别，我可以自己手动翻译。

![image-20201214174457857](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201214174457857.png)

识别卡住。

应该还是调用了在线服务的。

代码就3个文件，不多。看一下。

```
    recognizer = SpeechRecognizer(language=src_language, rate=audio_rate,
                                  api_key=GOOGLE_SPEECH_API_KEY)
```

```
GOOGLE_SPEECH_API_KEY = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
GOOGLE_SPEECH_API_URL = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang={lang}&key={key}" # pylint: disable=line-too-long
```

是这个key失效了吗？

很有可能。

我可以改成调用国内的相关服务看看。

因为语音识别都是类似的调用。

我不太清楚的是各种字幕格式。

就用百度的语音识别。

看到这个音频文件转写的demo。

![image-20201214175325133](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201214175325133.png)

```
DEFAULT_SUBTITLE_FORMAT = 'srt'
DEFAULT_CONCURRENCY = 10
DEFAULT_SRC_LANGUAGE = 'en'
DEFAULT_DST_LANGUAGE = 'en'
```



# youtube-dl帮助文档

youtube-dl官网

https://yt-dl.org/

是命令行工具。windows版本7M左右。

```
Usage: youtube-dl.exe [OPTIONS] URL [URL...]
```

支持的网站

https://ytdl-org.github.io/youtube-dl/supportedsites.html

常用选项：

```
通用选项
-U , --update
	更新到最新版本。
-i, --ignore-errors
	忽略错误。
	在下载多个视频的时候，如果某一个出错了，不影响后面的下载。
--abort-on-errors
	出错退出，后面的不继续下载。
--dump-user-agent
	显示当前的User Agent信息。
--list-extractors
	列出支持的网站。
--flat-playlist                  列出列表视频但不下载
网络选项
--proxy url
	设置代理。一般就这样：socks://127.0.0.1:1080
--source-address IP
	指定本机从哪个网卡走。
位置相关
    主要是避免区域限制。
    默认是跟这proxy的走。
视频选择
	--playlist-start NUMBER 播放列表的开始，默认是1
	--playlist-end NUMBER 播放列表的结束，默认是last。
	--playlist-items 1,2,5,8 指定下载这几个。
	--match-title REGEX 只下载符合规则的。
	--reject-title REGEX 过滤规则。
	--max-downloads NUMBER 下载这个数量后退出。
	--min-filesize SIZE 小于这个的不下载。
	--max-filesize SIZE 大于这个的不下载。
	--date DATE 只下载这一天上传的。
	--datebefore DATE
	--dateafter DATE
	--match-filter FILTER 这个规则可以写得比较复杂。
	--no-playlist 如果一个url指向了一个视频，同时指向了一个playlist，那么只下载视频。
	--yes-playlist 跟上面相反
	
下载选项
	-r, --limit-rate RATE 限制下载速度。50K 4.2M 这样写。
	-R, --retries RETRIES 出错后尝试。默认10次。
	--playlist-reverse 反序下载。
	--playlist-random 下载顺序随机。
	
文件选项
	-a, --batch-file FILE 指定一个txt文本，例如一行一个url。
	-o, --output TEMPLATE 输出模板。
	--autonumber-start NUMBER 编号。
	--restrict-filenames 规范名字。不要有&和空格。
	-w, --no-overwrites 不要覆盖同名文件。
	-c, --continue 继续下载没有完成的文件。
	--no-continue 这个是没有下载完成的，重新下载。
	
缩略图
	--write-thumbnail 把缩略图写入磁盘。
	--list-thumbnails 列出所有缩略图格式
	
其他
	-q, --quiet 安静模式
	-s, --simulate 模拟下载，调试用，看看规则是不是符合自己的需求。
	
```



# webm和m4a

因为使用 YouTube 所以接触到了 WebM 格式，这个格式 Google 开源的一个媒体容器格式，

常见的文件后缀名是 `.webm`，他设计的目标是为了给 HTML5 提供视频和音频。

Google 发起的 WebM 项目还有一个姊妹项目 WebP 是提供图像编码的。

其实 webm 格式就是 Matroska 容器的一层“皮”，`mkv` 格式也是 Matroska 容器的。

WebM 容器是 Matroska 一种特殊的 profile，可以封装 VP8 视频编码， Vorbis 音频编码。在 2013 年支持了 VP9 视频编码，和 Opus 音频编码。



参考资料

1、在线下载youtube视频和字幕-包括双语字幕

https://zhuanlan.zhihu.com/p/33150267

2、一个YouTube视频搬运工的教训

https://www.jianshu.com/p/c094164d3daf

3、怎样下载 Youtube 的字幕？

https://www.zhihu.com/question/19647719

4、如何从youtube-dl中选择视频质量？

https://qastack.cn/ubuntu/486297/how-to-select-video-quality-from-youtube-dl

5、youtube-dl下载最高画质 音频 内嵌字幕 MP4 m4a合并 视频列表 教程

https://blog.csdn.net/qq_43041976/article/details/104136199

6、

https://p3terx.com/archives/add-captions-to-your-videos-with-ffmpeg.html

7、通过 FFMPEG，将字幕“烧进”MP4视频中

https://blog.csdn.net/ufocode/article/details/75475539

8、ffmpeg 给视频加硬字幕的命令

https://www.v2ex.com/t/611035

9、国外视频课搬运方法整理

https://www.bilibili.com/read/cv2017604/

10、用Python实现自动化给视频实时加字幕，效率极高

https://www.pythonf.cn/read/95639