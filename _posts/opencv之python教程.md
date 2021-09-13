---
title: opencv之python教程
date: 2019-09-29 16:06:48
tags:
	- python

---

--

教程是基于python2.7的。我就用anaconda，结合pycharm来进行环境的搭建。

打开pycharm，创建一个conda环境。

进入解释器配置，安装依赖：

```
opencv
numpy
matplotlib
```

新建一个test.py，写入下面的内容：

```
import cv2
print cv2.__version__
```

当前我的电脑上打印是3.2.0。

# 图片处理

学习3个函数：imread、imshow、imwrite

```
import cv2
import numpy as np
img = cv2.imread('./1.jpg', cv2.IMREAD_GRAYSCALE)
k = cv2.imshow('my image show', img)
k = cv2.waitKey(0)&0xff
if k == 27: # esc key
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('./1_gray.png', img)
    cv2.destroyAllWindows()
```

上面的代码做了这些：

```
1、把一个jpg图片，读取灰度图到内存。然后显示出来。
2、等待2个按键，esc直接退出，s的话，则保存灰度图到磁盘。
```

opencv里载入的图片，是BGR模式的。而不是RGB。

而matplotlib里是RGB格式的。

所以用opencv载入的彩色图片，直接用matplotlib显示是不正常的。

用matplotlib显示灰度图。

```
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./1.jpg', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray', interpolation='bicubic')
plt.xticks([]), plt.yticks([])
plt.show()
```

imread返回的对象是一个numpy的ndarray对象。

它的维度是(w,h,depth)

```
#coding: utf-8
from __future__ import print_function
import numpy as np
import cv2

img = cv2.imread('./1.jpg', cv2.IMREAD_COLOR)
print(type(img))
print(img.shape)
```

输出是这样：

```
<type 'numpy.ndarray'>
(222L, 180L, 3L)
```

# 重新再来

现在研究npu相关的东西。用到一些opencv的东西。

所以先通过python版本的来快速了解opencv的常见用法。

现在对docker和jupyter比较喜欢。搭建环境快速。就用这个来重新搭建环境。

我就在jupyter TensorFlow的基础上安装一下opencv就好了。

```
!pip install opencv-python -i https://pypi.douban.com/simple/
```

当前的最新版本是 opencv-python-4.5.3.56

”cv2”中的”2”并不表示OpenCV的版本号。

 OpenCV是基于C/C++的，

”cv”和”cv2”表示的是底层C API和C++API的区别，

”cv2”表示使用的是C++API。这主要是一个历史遗留问题，是为了保持向后兼容性。



图片的读取、显示、写入操作

```
import numpy as np
import cv2
import imutils

gray_img = cv2.imread('1080p.bmp', cv2.IMREAD_GRAYSCALE)  #加载灰度图像
rgb_img = cv2.imread('1080p.bmp', cv2.IMREAD_COLOR)   #加载RGB彩色图像

cv2.imshow('origin image', imutils.resize(rgb_img, 800))
```



# 参考资料

1、官方教程

https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html#install-opencv-python-in-windows

2、OpenCV 中图像坐标系统与Python中NumPy Arrays之间的关系

https://blog.csdn.net/lz0499/article/details/80978433

3、为什么OpenCV3在Python中导入名称是cv2

https://blog.csdn.net/mid_Faker/article/details/105653181