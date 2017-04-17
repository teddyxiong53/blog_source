---
title: 树莓派上使用usbcam
date: 2017-04-15 22:27:59
tags:
	- 树莓派
	- uvc
---
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






