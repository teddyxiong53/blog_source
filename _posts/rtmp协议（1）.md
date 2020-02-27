---
title: rtmp协议（1）
date: 2020-02-19 14:54:51
tags:
	- 音视频

---

1

nginx做直播服务器，有个模块是nginx-rtmp。这个是用得很多的。

所以我选择rtmp来做我的项目。

需要对rtmp进行一些了解。



rtmp和rtsp的关系是什么？



HLS不适合直播，只适合点播。是基于http的。延时变化大。

RTSP定义流格式，RTP传输流数据。

RTSP的实时性最好，但是实现复杂，适合视频聊天和视频监控。

RTMP优势在于浏览器支持好，加载flash插件后就可以播放。



流媒体相关协议

传统的流媒体协议

```
RTMP
RTSP

从这里看，rtsp和rtmp是两种不同的协议。
传统的，最适合这种场景：
	通过服务器向不多的观众传输。
	
rtmp的延迟在5秒左右。算是比较大的了。
而rtsp的延迟在2秒左右。

一般会用rtmp再转码成http数据，这样可以做到比较好的通用性。
```

基于http的协议

```
HLS
其他
```

新技术

```
webrtc
```



# rtmp延时大

我现在用阿里云服务器和本地笔记本做rtmp服务器，测试得到的延时都比较大。

局域网表现并没有比公网服务器更好。

采集端，我已经尽量缩小缓存了。



# srs软件

https://github.com/ossrs/srs/wiki/v1_CN_SampleRTMP

```
cd trunk
./configure && make
./objs/srs -c conf/rtmp.conf
```





参考资料

1、基于 Nginx 搭建视频直播服务器

https://zhangshuqiao.org/2018-01/%E5%9F%BA%E4%BA%8ENginx%E6%90%AD%E5%BB%BA%E8%A7%86%E9%A2%91%E7%9B%B4%E6%92%AD%E6%9C%8D%E5%8A%A1%E5%99%A8/

2、使用FFmpeg将rtsp流摄像头视频转码为rtmp播放

https://zhuanlan.zhihu.com/p/62021755

3、HLS，RTSP，RTMP的区别

https://www.jianshu.com/p/70c9a2fd918b

4、Streaming Protocols: Everything You Need to Know

https://www.wowza.com/blog/streaming-protocols

5、通过live555实现H264 RTSP直播

https://blog.csdn.net/firehood_/article/details/16844397

6、

https://blog.csdn.net/fantasy_ARM9/article/details/78150804