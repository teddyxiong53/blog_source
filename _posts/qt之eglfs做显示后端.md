---
title: qt之eglfs做显示后端
date: 2021-07-19 19:32:33
tags:
	- gui

---

--

现在在评估qt的二维绘图硬件加速方案。

directfb问题不少，而且不再继续维护了。

所以看看其他的方案。在src/plugins/platforms下，按字母顺序，首先觉得值得评估的是eglfs。

# eglfs

EGLFS是一个Qt5的平台插件，

它的作用就是让QT应用直接运行在EGL和OpenGL ES 2.0上（关于EGL和OpenGL ES 2.0的介绍具体可以看这篇文章）。

说白了，就是能让你绕过图形桌面，直接从显卡输出Qt图像到屏幕。





egl是opengl和本地window system的接口。

eglfs是一个插件，用来支持在egl和opengl 2.0上运行qt程序。

不需要一个X11来做底层。

eglfs被推荐使用，尤其是在有gpu的嵌入式板子上。

eglfs强制顶层窗口全屏显示。

相关环境变量

```
QT_QPA_EGLFS_INTEGRATION
QT_QPA_EGLFS_FB
	默认是/dev/fb0
QT_QPA_EGLFS_DEBUG
```

在树莓派上，配置是这样：

```
QPA backends:
EGLFS ................................ yes
EGLFS details:
  EGLFS i.Mx6 ........................ no
  EGLFS i.Mx6 Wayland ................ no
  EGLFS EGLDevice .................... no
  EGLFS GBM .......................... no
  EGLFS Mali ......................... no
  EGLFS Rasberry Pi .................. yes
  EGL on X11 ......................... no
```

在buildroot里的配置项是这样：

```
ifeq ($(BR2_PACKAGE_QT5BASE_EGLFS),y)
QT5BASE_CONFIGURE_OPTS += -eglfs
QT5BASE_DEPENDENCIES   += libegl
else
QT5BASE_CONFIGURE_OPTS += -no-eglfs
endif
```



EGL 是 OpenGL ES 渲染 API 和本地窗口系统(native platform window system)之间的一个中间接口层，它主要由系统制造商实现。EGL提供如下机制：

- 与设备的原生窗口系统通信
- 查询绘图表面的可用类型和配置
- 创建绘图表面
- 在OpenGL ES 和其他图形渲染API之间同步渲染
- 管理纹理贴图等渲染资源

为了让OpenGL ES能够绘制在当前设备上，我们需要EGL作为OpenGL ES与设备的**桥梁**。



# 参考资料

1、

https://doc.qt.io/qt-5/embedded-linux.html

2、

https://zhuanlan.zhihu.com/p/74006499

3、

https://blog.csdn.net/pengjiaqi1028/article/details/111476742