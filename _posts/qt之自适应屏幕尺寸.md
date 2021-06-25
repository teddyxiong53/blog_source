---
title: qt之自适应屏幕尺寸
date: 2021-06-25 17:07:33
tags:
	- qt

---

--

我看qt的例子在我的720x720这样一个不怎么常见的屏幕上，都是正常的铺满屏幕的。

是怎么做到对屏幕尺寸的自适应的呢？

以wearable这个为例，它在wearable.qml里写的尺寸是：

```
QQC2.ApplicationWindow {
    id: window
    visible: true
    width: 320
    height: 320
```

在main函数里写的：

```
int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
```

AA_EnableHighDpiScaling 这个的作用是：

设置环境变量 `QT_AUTO_SCREEN_SCALE_FACTOR=1`  可以起到相同的作用。

参考资料

1、

https://doc.qt.io/archives/qt-5.6/qtlabscontrols-highdpi.html

2、Qt5和PyQt5中设置支持高分辨率屏幕自适应的方法

https://blog.csdn.net/u010579736/article/details/108852326