---
title: opencv（二）windows环境搭建
date: 2018-04-08 10:29:30
tags:	
	- opencv

---



因为我的usb摄像头在虚拟机Ubuntu总是不能正常工作。我决定还是在windows下面来做。



# 下载安装

1、下载地址在这里。

https://opencv.org/releases.html#

选择windows版本下载，目前最新的是3.4.1的。

2、安装。注意安装路径不要有空格就好。路径都用英文。

它这个实际上就是一个解压，并不需要安装。

我就解压到D:\work\video\opecv这个目录。解压后大概780M。

```
D:\work\video\opecv\opencv
λ ls
LICENSE.txt  LICENSE_FFMPEG.txt  README.md.txt  build/  sources/
```

就2个目录，一个build，是已经编译好的，sources里面放的就是源代码。

3、配置环境变量。

现在需要把build目录下的bin目录加入到环境表里。

D:\work\video\opecv\opencv\build\x64\vc14\bin

# visual studio工程

现在vs也有免费的社区版本了。不需要再去破解了。只是需要用你的windows账号进行登陆。微软也在慢慢走向开源免费的路子。

登陆比较慢。

1、建立一个空的工程。test_opencv

2、设置工程包含头文件的目录。

右键工程 ，然后点击属性，然后vc++目录。包含目录。

加入这3个路径：

```
D:\work\video\opecv\opencv\build\include
D:\work\video\opecv\opencv\build\include\opencv
D:\work\video\opecv\opencv\build\include\opencv2
```

3、设置库目录。

把vc14/lib目录添加进来。

这就是windows下的不方便之处，各种地方点来点去，不如linux下面直接写文件来得直观统一。

4、添加依赖的库文件名字。

属性，链接器，输入，附加依赖项，加入opencv_world341d.lib。

5、我们新建一个test.cpp文件。并且把这个文件添加到工程里。

代码如下：

```
#include <opencv2/opencv.hpp>
#include <iostream>
using namespace std;
using namespace cv;

int main()
{
	Mat image = imread("D:\\work\\vs\\test_opencv\\test_opencv\\1.jpg");
	imshow("show image", image);
	waitKey(0);
	return 0;
}
```

build，然后运行。就可以看到图片显示出来了。

整个过程是非常顺利而且简单的。



# 看看usb摄像头的

我们直接把D:\work\video\opecv\opencv\sources\samples\cpp\example_cmake这个目录下的文件内容拷贝到test.cpp里，然后编译运行。就可以很顺利地看到图像了。



# 参考资料

1、拜小白教你OpenCV3.2.0+VS2017开发环境配置

https://blog.csdn.net/sinat_36264666/article/details/73135823?ref=myread

