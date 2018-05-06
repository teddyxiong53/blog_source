---
title: fswebcam代码分析
date: 2017-04-22 21:08:07
tags:
	- video
---
先把代码拷贝到树莓派上，配置编译。出现如下错误：
```
configure: error: GD graphics library not found
```
是需要安装GD库。
安装方法：
```
sudo apt-get install libgd2-xpm-dev
```
安装总是不成功。我直接下载源代码进行编译安装。
源代码下载地址：
```
https://github.com/libgd/libgd/releases
```
默认配置，编译完，安装好。
再看fswebcam的编译。
```
configure: error: GD does not have JPEG support!
```

安装成功了。

# 代码目录分析

```
teddy@teddy-ubuntu:~/work/fswebcam/fswebcam-master$ tree
.
├── config.h
├── dec_bayer.c：这些dec_xx文件，里面都只有一个函数。
├── dec_grey.c
├── dec.h
├── dec_jpeg.c
├── dec_png.c
├── dec_rgb.c
├── dec_s561.c
├── dec_yuv.c
├── effects.c：就是实现旋转，缩放这些功能。
├── effects.h
├── example.conf
├── fswebcam.1
├── fswebcam.c：入口文件。
├── fswebcam.h
├── log.c
├── log.h
├── Makefile
├── parse.c
├── parse.h
├── README
├── src.c：这些src_xx文件，是指视频数据的来源。
├── src_file.c
├── src.h
├── src_raw.c
├── src_test.c
├── src_v4l1.c
├── src_v4l2.c
├── videodev2.h
├── videodev.h
└── videodev_mjpeg.h
```

总的来说，代码很简单。

我当前的使用场景是在树莓派上插着usb cam的。

所以视频来源是src_v4l2.c。

```
pi@raspberrypi:~$  fswebcam -d /dev/video0  ./`date "+%Y-%m-%d_%H-%M-%S"`.jpg -v
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
src_v4l2_get_capability,87: /dev/video0 information:
src_v4l2_get_capability,88: cap.driver: "uvcvideo"
src_v4l2_get_capability,89: cap.card: "USB2.0 PC CAMERA: USB2.0 PC CAM"
src_v4l2_get_capability,90: cap.bus_info: "usb-3f980000.usb-1.2"
src_v4l2_get_capability,91: cap.capabilities=0x84200001
src_v4l2_get_capability,92: - VIDEO_CAPTURE
src_v4l2_get_capability,103: - STREAMING
No input was specified, using the first.
src_v4l2_set_input,181: /dev/video0: Input 0 information:
src_v4l2_set_input,182: name = "Camera 1"
src_v4l2_set_input,183: type = 00000002
src_v4l2_set_input,185: - CAMERA
src_v4l2_set_input,186: audioset = 00000000
src_v4l2_set_input,187: tuner = 00000000
src_v4l2_set_input,188: status = 00000000
src_v4l2_set_pix_format,520: Device offers the following V4L2 pixel formats:
src_v4l2_set_pix_format,533: 0: [0x56595559] 'YUYV' (YUYV 4:2:2)
Using palette YUYV
Adjusting resolution from 384x288 to 352x288.
src_v4l2_set_mmap,672: mmap information:
src_v4l2_set_mmap,673: frames=4
src_v4l2_set_mmap,722: 0 length=202752
src_v4l2_set_mmap,722: 1 length=202752
src_v4l2_set_mmap,722: 2 length=202752
src_v4l2_set_mmap,722: 3 length=202752
--- Capturing frame...
Captured frame in 0.00 seconds.
--- Processing captured image...
Writing JPEG image to './2018-05-05_13-45-40.jpg'.
pi@raspberrypi:~$ 
```



打开dev/video0之后，

1、get cap。

2、set input。

3、set control。

4、set pix fmt。

5、set fps

6、set mmap。



```
	config->width = 384;
	config->height = 288;
```



先抓出一张图片，用select，ioctl DQBUF，放到src->img里。这个是yuv格式的。

abitmap = calloc(config->width * config->height * 3, sizeof(avgbmp_t));

分配的这个空间，比较大。是用来做中间处理用的。

然后fswc_add_image_yuyv。这一步得到的是rgb的数据。

然后创建一个gdImage。真彩色的。

```
/* Copy the average bitmap image to a gdImage. */
	original = gdImageCreateTrueColor(config->width, config->height);
```

把rgb的数据，运算一下，赋值到gdImage里。

```
	for(y = 0; y < config->height; y++)
		for(x = 0; x < config->width; x++)
		{
			int px = x;
			int py = y;
			int colour;
			
			colour  = (*(pbitmap++) / config->frames) << 16;
			colour += (*(pbitmap++) / config->frames) << 8;
			colour += (*(pbitmap++) / config->frames);
			
			gdImageSetPixel(original, px, py, colour);
		}
```

然后把original这个复制一份。

```
/* Make a copy of the original image. */
	image = fswc_gdImageDuplicate(original);
```

最后是把复制的这一份，写入banner。然后写入到文件。



# 参考资料

1、

https://github.com/fsphil/fswebcam/issues/4