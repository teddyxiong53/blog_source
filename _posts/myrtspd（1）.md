---
title: myrtspd（一）
date: 2018-04-30 20:42:11
tags:
	- rtsp

---



参考的是：https://github.com/teddyxiong53/Linux-C-Examples/tree/master/rtsp

现在写了个框架。

运行报错。

```
[ERROR][rtspd.c][rtspd_rtp_init][93]: status is not right. status:0
```

这个是需要前面阻塞，等状态变成8 。

所以加入锁rtspd_lock[]。

rtp初始化，要等到有链接建立了才做。

我前面状态只处理了options方法。看来还不行。还得把其他的方法完善。

这个算是核心状态机了。要写完，需要加的代码不少。



另外rtspd_lock初始化的值，应该是0。



现在用ffplay来进行点播。

```
ffplay rtsp://192.168.190.137/1.h264
```

1.h264文件，跟rtspd这个可执行文件放在同一个目录下。



现在点播，没有反应，应该是listen那里没有收到东西。



加打印。看到有accept到连接。到这里没有问题。



我在Ubuntu下运行ffplay，不能 抓到包。所以我在windows下运行ffplay，点播Ubuntu下的rtspd。

这样就可以用tcpdump来抓包。



看正常的程序。是这样的包情况。

```
OPTIONS rtsp://192.168.190.137:554/1.h264 RTSP/1.0
CSeq: 1
User-Agent: Lavf57.38.102
```

```
 DESCRIBE rtsp://192.168.190.137:554/1.h264 RTSP/1.0
 Accept: application/sdp
 CSeq: 2
 User-Agent: Lavf57.38.102
```



```
[DEBUG][rtsp.c][parse_url][284]: url:rtsp://192.168.190.137:554/1.h264
describe command response       sucessfull
[DEBUG][rtsp.c][parse_url][284]: url:rtsp://192.168.190.137/1.h264/trackID=0
setup command response  sucessfull
[DEBUG][rtsp.c][parse_url][284]: url:rtsp://192.168.190.137/1.h264/
```



现在看好像是options过来，处理没有成功。

现在问题是 read那里，没有读取到数据。



read的fd是4 （这个是accept时分配的），listen的是3 。

问题是这里，fd居然是0 。

```
[DEBUG][rtsp.c][rtsp_proc][729]: before tcp read,fd:0
```

再多加一点打印。可以看出，顺序不对了。

```
[DEBUG][rtsp.c][rtsp_proc][729]: before tcp read,fd:0
[DEBUG][socket.c][socket_tcp_read][53]: before read
[DEBUG][socket.c][socket_really_proc_accept][26]: rb->cli_rtsp.cli_fd:4
[DEBUG][socket.c][socket_really_proc_accept][27]: [0]:4
[DEBUG][socket.c][socket_really_proc_accept][28]: [1]:0
```

正常的程序，在这里，有一个rtspd_cond来进行阻塞。

cond需要跟mutex配合工作。加上：

```
rtspd_cond
rtspd_mutex
```

只有accept连接后，才往下走，去读取分配的fd的内容。

现在基本上可以交互了。

但是还是出错。

我的构造的返回内容。这里有问题。

```
Date: 1525134642, 01 May 2018 08:30:
```

因为我打错了一个字符。我把%a写成了%s。

```
	strftime(buf+strlen(buf), 38, "Date: %a, %d %b %Y %H:%M:%S GMT"RTSP_EL, t);
```

这里我少了一个斜杠。不过这里不是关键。

```
Server: rtspd1.0
```

现在问题是，setup的时候，返回了406 错误。

```
RTSP/1.0 406 Not Acceptable
        CSeq: 3
```

```
[ERROR][rtsp.c][rtsp_proc_method][677]: setup fail
[ERROR][rtspd.c][rtspd_rtp_init][98]: status is not right. status:5
[ERROR][rtspd.c][main][347]: rtspd_rtp_init fail
```

是因为我把判断条件写反了。

改了继续。

现在跑挂了。应该是play的时候。

```
[DEBUG][rtsp.c][rtsp_proc][743]: method:4
Segmentation fault (core dumped)
```

gdb查看core文件，可以看到是在sscanf里。

```
#1  0x00007f19b50adbcc in __GI___isoc99_vsscanf (string=0x1e5f825 "Session: 0\r\n\r\n 3\r\nUser-Agent: Lavf57.38.102\r\n\r\n", format=0x409660 "%254s %d", 
    args=args@entry=0x7f19b483fcd8) at isoc99_vsscanf.c:43
#2  0x00007f19b50adb57 in __isoc99_sscanf (s=<optimized out>, format=<optimized out>) at isoc99_sscanf.c:31
#3  0x00000000004070c2 in rtsp_method_play (conn_num=0) at src/src/rtsp.c:579
```

是我漏写了一个参数。改了就好了。



```
[DEBUG][rtspd.c][rtspd_rtcp_create_socket][120]: fd:7
[ERROR][rtp_h264.c][rtp_send_packet][138]: fopen fail
```

这里也是我条件写反了。



现在没有明显报错了。

但是还是没有发送出来。

看windows上的错误提示。

```
[h264 @ 0000000000325cc0] Invalid NAL unit 0, skipping.  0B f=0/0
    Last message repeated 1 times
[rtsp @ 0000000000321da0] decoding for stream 0 failed   0B f=0/0
Input #0, rtsp, from 'rtsp://192.168.190.137/1.h264':
  Metadata:
    title           : RTSP Session
    comment         : rtspd 1.0 Streaming Server
  Duration: N/A, bitrate: N/A
    Stream #0:0: Video: h264 (Constrained Baseline), yuv420p, 720x576, 90k tbr, 90k tbn, 180k tbc
[h264 @ 00000000003cdfe0] Invalid NAL unit 0, skipping.
    nan M-V:    nan fd=   0 aq=    0KB vq=    0KB sq=    0B f=0/0
```

看正常的程序。

```
[h264 @ 0000000000475cc0] Invalid NAL unit 0, skipping.  0B f=0/0
[h264 @ 0000000000475cc0] Invalid NAL unit 0, skipping.  0B f=0/0
Input #0, rtsp, from 'rtsp://192.168.190.137/1.h264':    0B f=0/0
  Metadata:
    title           : RTSP Session
    comment         : rtspd 1.0 Streaming Server
  Duration: N/A, start: 0.160000, bitrate: N/A
    Stream #0:0: Video: h264 (Constrained Baseline), yuv420p, 720x576, 25 fps, 25 tbr, 90k tbn, 180k tbc
[h264 @ 0000000004595020] Invalid NAL unit 0, skipping.
  11.08 M-V:  0.024 fd=   0 aq=    0KB vq=  242KB sq=    0B f=0/0
```



seqno的分析。



rtsp的2个线程，分别是做什么？
1、一个阻塞在accept。这个叫A。A去创建B比较合适。
2、一个阻塞在read。这个叫B。

rtp和rtcp的4个port和4个fd。
1、rtp_cli_port。
这个是从客户端通过url传递过来。

```
SETUP rtsp://192.168.190.137/1.h264/trackID=0 RTSP/1.0
Transport: RTP/AVP/UDP;unicast;client_port=23614-23615//就是这里。依次是rtp_cli_port和rtcp_cli_port。
CSeq: 3
User-Agent: Lavf57.38.102
```

服务端回复给客户端的：

```
Transport: RTP/AVP;unicast;client_port=23614-23615192.168.190.13723615;server_port=14309-14310;ssrc=772018775;ttl=32
```

server_port是通过client_port运算得到的。

```
(cli_port-5004)/2+cli_port
```

这样4个port都清楚了。

现在看看4个fd。





有个写法很奇怪。

定义了2个sockaddr_in。rtp_bind和rtp_addr。

服务端的rtp_ser_port通过connect连接到客户端的rtp_cli_port 。这个是是反向连接的。

为什么要这么做呢？我觉得没什么问题。

rtp_video_fd跟rtp_bind进行绑定。

对应的port是rtp_ser_port。



rtcp是udp的。

rtp也是udp的。



当前默认只支持了UDP的方式。

```
strcat(rtsp[cur_conn_num]->out_buffer, "Transport: RTP/AVP;unicast;client_port=");
```

