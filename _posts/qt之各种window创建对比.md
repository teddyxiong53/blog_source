---
title: qt之各种window创建对比
date: 2021-06-10 10:13:11
tags:
	- qt

---

--

对比这么几个例子：



```
默认生成的代码：新建默认的widget Application。
	class MainWindow : public QMainWindow
	就是继承QMainWindow
	用的是QApplication app。
	QApplication : public QGuiApplication
默认生成的qml代码：新建qml Application
	这个是QGuiApplication。
	QQmlApplicationEngine engine;
	main.qml里是ApplicationWindow。
	
slide的代码：是一个全屏的相册应用。特点是全屏。
	class MainWindow : public QMainWindow
	这个可以看出是新建的默认的widget工程。
	用的是QApplication app。
	
analogclock的代码：是一个时钟应用。特点是动态绘图。
	QGuiApplication app
	class AnalogClockWindow : public RasterWindow
	class RasterWindow : public QWindow
	这个就是直接用的QWindow了。
	
```

**1.处理重绘事件的函数**
QWindow的重绘与QWidget重绘有点不一样，QWindow的没有提供PaintEvent相关的函数，这个时候可以重写下面的虚函数，在里面对Paint事件进行处理：

```
[virtual protected] bool QWindow::event(QEvent *ev)
```

**2.重绘的Painter**
在QWindow中，获取一个QPainter对象可以通过QBackingStore.paintDevice进行获取；
实例如下：



参考资料

1、QWindow重绘、避免闪烁

https://www.pianshen.com/article/4562135309/