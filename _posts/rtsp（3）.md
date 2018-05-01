---
title: rtsp（3）
date: 2017-02-25 21:46:50
tags:
	- linux
	- rtsp
---
先了解一下live555。live555是用C++实现的用于流媒体传输的开源库。支持的流媒体传输协议有RTP、RTSP、SIP等。它被很多的播放器采用来实现流媒体播放功能，例如VLC。
代码在这里：`https://github.com/xanview/live555`。这个不是官方发布地址，只是镜像。我比较习惯从github上下载代码。
把代码放到Ubuntu虚拟机上，解压后，进行编译。先要生成Linux下的Makefile。然后再make。
```
# ./genMakefiles linux
# make 
```
编译完成后，在mediaServer目录下，有个叫live555MediaServer的可执行文件。
启动后的打印如下：
```
LIVE555 Media Server
        version 0.89 (LIVE555 Streaming Media library version 2017.01.26).
Play streams from this server using the URL
        rtsp://192.168.17.129:8554/<filename>
where <filename> is a file present in the current directory.
Each file's type is inferred from its name suffix:
        ".264" => a H.264 Video Elementary Stream file
        ".265" => a H.265 Video Elementary Stream file
        ".aac" => an AAC Audio (ADTS format) file
        ".ac3" => an AC-3 Audio file
        ".amr" => an AMR Audio file
        ".dv" => a DV Video file
        ".m4e" => a MPEG-4 Video Elementary Stream file
        ".mkv" => a Matroska audio+video+(optional)subtitles file
        ".mp3" => a MPEG-1 or 2 Audio file
        ".mpg" => a MPEG-1 or 2 Program Stream (audio+video) file
        ".ogg" or ".ogv" or ".opus" => an Ogg audio and/or video file
        ".ts" => a MPEG Transport Stream file
                (a ".tsx" index file - if present - provides server 'trick play' support)
        ".vob" => a VOB (MPEG-2 video with AC-3 audio) file
        ".wav" => a WAV Audio file
        ".webm" => a WebM audio(Vorbis)+video(VP8) file
See http://www.live555.com/mediaServer/ for additional documentation.
```
从上面的打印我们可以看到，这个server支持的文件类型是有限的，至少mp4文件我们没有看到支持的。
我们在这个目录下放一个test.mp3的文件。
然后我们在windows下打开vlc播放器。选择打开网络串流。填入地址：`rtsp://192.168.17.129:8554/test.mp3`。然后就可以用rtsp来播放文件了。
我们也可以用ffmpeg把mp4文件里的264码流抽取出来，放在这个目录下进行点播。
我们现在可以用wireshark来抓包分析rtsp的点播过程。
我的windows地址是192.168.17.1（下面称为client），Ubuntu的地址是192.168.17.129（下面称为server） 。
抓包我们过滤rtsp的包。据此来分析rtsp协议。
第一步：client发给server。这一步是用来查询server支持的方法有哪些的。
```
OPTIONS rtsp://192.168.17.129:8554 /test.mp4 RTSP/1.0 
CSeq: 2
User-Agent: LibVLC/2.2.4
```

第二步：server回复，告诉client自己支持的方法。
```
RTSP/1.0 200 OK
CSeq: 2
Date: Sat, Feb 25 2017 14:03:02 GMT
Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE, GET_PARAMETER, SET_PARAMETER

```
第三步：client发给server，请求媒体描述信息。sdp是Session Description Protocol的缩写。
```
DESCRIBE rtsp://192.168.17.129:8554/test.mp3 RTSP/1.0
CSeq: 3
User-Agent: LibVLC/2.2.4
Accept: application/sdp
```
第四步：server回复sdp信息。
```
RTSP/1.0 200 OK
CSeq: 3
Date: xxx
Content-Base: rtsp://192.168.17.129:8554/test.mp3
Content-type: application/sdp
Content-length: 394
\r\n
SDP内容。
```
第五步：client要求server建立连接。
```
SETUP rtsp://192.168.17.129:8554/test.mp3/track1 RTSP/1.0
CSeq: 4
User-Agent: LibVLC/2.2.4
Transport: RTP/AVP;unicast;client_port=64366-64367
```
第六步：server回复建立连接成功。
```
RTSP/1.0 200 OK
CSeq: 4
Date: xxx
Transport: RTP/AVP;unicast;destination=192.168.17.1;source=192.168.17.129;client_port=64366-64367;serverport=6970-6971
Session: 963558E3;timeout=65
```
第七步：client调用Play方法。
```
PLAY  rtsp://192.168.17.129:8554/test.mp3/ RTSP/1.0
CSeq: 5
User-Agent: LibVLC/2.2.4
Session: 963558E3
Range: npt=0.000-
```
第八步：server回复ok。
```
RTSP/1.0 200 OK
CSeq: 5
Date: xxx
Range: npt=0.000-
Session: 963558E3
RTP-Info: url=rtsp://192.168.17.129:8554/test.mp3/track1;seq=10814;rtptime=2442558152

```
第九步：get parameter。
```
GET_PARAMETER rtsp://192.168.17.129:8554/test.mp3/ RTSP/1.0
CSeq: 6
User-Agent: LibVLC/2.2.4
Session: 963558E3

```
第十步：回复。
```
RTSP/1.0 200 OK
CSeq: 6
Date: xxx
Session: 963558E3
Content-length: 10
\r\n
2017.01.26
```
第十一步：client调用tear down方法。
```
TEARDOWN rtsp://192.168.17.129:8554/test.mp3/ RTSP/1.0
CSeq: 7
User-Agent: LibVLC/2.2.4
Session: 963558E3
```
第十二步：server回复ok。
```
RTSP/1.0 200 OK
CSeq: 7
Date: xxx
```
到这里，一个完整的流程分析完了。


