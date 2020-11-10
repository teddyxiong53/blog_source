---
title: opencv（一）Ubuntu环境搭建
date: 2018-04-02 10:47:26
tags:
	- opencv

---



# 什么是opencv

1、是一个基于bsd协议开源的跨平台计算机视觉库。

2、提供了C语言、Python、matlab等的接口。

3、实现了很多计算机视觉方面的通用算法。

4、opencv主要是用c++写的。

5、这个项目开始于1999年，Intel发起的。

6、目前最新版本是3.4，是2017年12月发布的。

# opencv应用领域

1、人机互动。

2、物体识别。

3、图像分割。

4、人脸识别。

5、动作识别。

6、运动跟踪。

7、机器人。

8、运动分析。

9、机器视觉。

10、结构分析。

11、汽车安全驾驶。

# 编译安装

1、安装必要的编译工具。

```
sudo apt-get install cmake build-essential libgtk2.0-dev libavcodec-dev libavformat-dev libjpeg.dev libtiff4.dev libswscale-dev libjasper-dev
```

2、下载opencv3的源代码。

https://github.com/opencv/opencv/releases

源代码大概80M。

3、配置编译。

```
cd opencv3
mkdir build  #不能在源代码目录下进行cmake。会报错。
cd build
cmake ../   
make -j4 #make也还是在新建的build目录下来做。
sudo make install #安装。
```

cmake用来生成Makefile的。

比较好。因为编译有进度提示。

编译大概10分钟。

# 测试

opencv自带了测试程序。

进入到`ddy-ubuntu:~/work/opencv/opencv-3.4.1/samples/cpp/example_cmake`这个目录下，make。

得到opencv_exmaple文件。运行。

报错了。

```
./opencv_example: error while loading shared libraries: libopencv_highgui.so.3.4: cannot open shared object file: No such file or directory
```

解决办法如下：

1、编辑/etc/ld.so.conf文件。

加上一行：

```
include /usr/local/lib
```

然后运行`sudo ldconfig`来使得修改生效。

2、修改/etc/bash.bashrc文件。

```
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig 
export PKG_CONFIG_PATH 
```

然后运行：`source /etc/bash.bashrc`使得修改生效。

运行得到的opencv_exmaple文件。

报错。原因应该是我的usb摄像头没有数据进入到Ubuntu里来。

但是在windows下是好的。这个摄像头在树莓派下也是好的。

那是为什么？





# 参考资料

1、ubuntu16.04搭建opencv3环境

https://www.cnblogs.com/dragonyo/p/6754599.html