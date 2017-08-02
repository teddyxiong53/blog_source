---
title: 树莓派上使用usbcam
date: 2017-04-15 22:27:59
tags:
	- 树莓派
	- uvc
---
网上说树莓派支持的usb摄像头不是很多。我在淘宝上选了便宜的，才20几块钱，今贵S9的。虽然分辨率比较低，但是使用完全没有问题。我觉得现在Linux对USB摄像头支持应该是很好了的。

# 1. fswebcam
插入usb摄像头之后，`ls /dev/video*`，看看能否识别到摄像头。识别之后，我们可以安装一些软件来使用摄像头。
安装：
`sudo apt-get install fswebcam`。
使用：
`fswebcam --no-banner -r 640x480 test.jpg`
这样我们就得到一张照片。
fswebcam的github地址是：`https://github.com/fsphil/fswebcam`。我们把代码下载下来，简单学习一下。


# 2. raspvid和ffmpeg
```
# 用ffmpeg采集摄像头数据直接输出
ffmpeg -f v4l2 -i /dev/video0 -c libx264 -profile:v main -preset:v fast \
-b:v 300k -s 640x480 -r 25 -an -f flv -y rtmp://127.0.0.1/live/livestream

# 用raspvid编码后，在用ffmpeg封装输出
raspvid -f1 -t 0 -w 640 -h 480 -b 1200000 -fps 15 \
	-pf baseline -o - | ffmpeg -f h264 -i - \
	-c copy -an -f flv -y rtmp://127.0.0.1/live/livestream
```
# 3. motion
motion是Linux下的开源的视频动态监控软件。
我们用apt-get来安装就好了。对应的配置文件在`/etc/motion/motion.conf`里。
可以改动下面的几点：
```
daemon off
locate_motion_mode on
videodevice /dev/video0
width 640
height 480
target_dir /var/lib/motion #拍摄照片存放的位置
threshold 3000 #3000像素，越小，则越容易触发动作。
```
为了避免权限问题，最好`sudo motion`来运行。
运行之后，用手在摄像头前面晃动一下，可以看到出现如下的打印：
```
[1] [NTC] [EVT] event_new_video FPS 16
[1] [NTC] [EVT] event_newfile: File of type 8 saved to: /var/lib/motion/01-20170416150801.avi
[1] [NTC] [ALL] motion_detected: Motion detected - starting event 1
[1] [NTC] [EVT] event_newfile: File of type 1 saved to: /var/lib/motion/01-20170416150801-13.jpg
[1] [NTC] [EVT] event_newfile: File of type 1 saved to: /var/lib/motion/01-20170416150802-03.jpg
[1] [NTC] [EVT] event_newfile: File of type 1 saved to: /var/lib/motion/01-20170416150802-07.jpg
[1] [NTC] [ALL] motion_loop: End of event 1
```
# 4. mjpg-streamer

下载源代码。这个apt-get不能安装。

wget [https://github.com/jacksonliam/mjpg-streamer/archive/master.zip](http://jump.bdimg.com/safecheck/index?url=rN3wPs8te/r8jfr8YhogjfUWFoMgIRa83KqgVswSQ4m6yARY42pFziTvIV8F84f9vo06e7Xl/yNiZHzCcc+SIMMx4hMSb96TpkIhMmUefkbWV5cxFm4v0m/r+n902d2/VI4TdC/RH4eTCg6iKEVBFj/uLDrhMxCTAx0kOLvwKWRhKHoBncgUV/MCbnyhLl0YU9LI4CCJvs4wPGbuJnYGNA==)

编译：

```
make USE_LIBV4L2=true clean 
make USE_LIBV4L2=true  all 
sudo make install
```

我的cmake没有安装，装上。

运行：

```
./mjpg_streamer -i "input_uvc.so" -o "output_http.so -p 8090 -w /www" 
```

用搜狗浏览器打开地址：`http://192.168.0.101:8090/?action=stream`。就可以看到视频了。

用vlc来打开这个地址，也是可以看到的。



# 5. uvcdynctrl

这个工具是用来查看系统支持的图片的格式。

```
pi@raspberrypi:~/work/fswebcam$ uvcdynctrl -f
Listing available frame formats for device video0:
Pixel format: YUYV (YUYV 4:2:2; MIME type: video/x-raw-yuv)
  Frame size: 640x480
    Frame rates: 30, 15
  Frame size: 352x288
    Frame rates: 30, 15
  Frame size: 320x240
    Frame rates: 30, 15
  Frame size: 176x144
    Frame rates: 30, 15
  Frame size: 160x120
    Frame rates: 30, 15
pi@raspberrypi:~/work/fswebcam$ sudo uvcdynctrl -l
Listing available devices:
  video0   USB2.0 PC CAMERA
    Media controller device: /dev/media0
    Entity 1: USB2.0 PC CAMERA. Type: 65537, Revision: 0, Flags: 1, Group-id: 0, Pads: 1, Links: 0
      Device node
      Entity: 1, Pad 0, Flags: 1
    Entity 2: Processing 2. Type: 131072, Revision: 0, Flags: 0, Group-id: 0, Pads: 2, Links: 1
      Subdevice:       Entity: 2, Pad 0, Flags: 1
      Entity: 2, Pad 1, Flags: 2
      Out link: Source pad { Entity: 2, Index: 1, Flags: 2 } => Sink pad { Entity: 1, Index: 0, Flags: 1 }
    Entity 3: Camera 1. Type: 131072, Revision: 0, Flags: 0, Group-id: 0, Pads: 1, Links: 1
      Subdevice:       Entity: 3, Pad 0, Flags: 2
      Out link: Source pad { Entity: 3, Index: 0, Flags: 2 } => Sink pad { Entity: 2, Index: 0, Flags: 1 }
```



# 6 音频相关工具

arecord命令可以做录音。



