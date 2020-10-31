---
title: wxpython（3）写一个画图程序
date: 2018-06-03 22:53:47
tags:
	- wxpython

---



# 初始版本的程序

放在这里了：https://github.com/teddyxiong53/Python/tree/master/wxpython/wxpython_in_action/sketch/v1

这个实现了一个空白的窗口，可以画一些线条了。



# 增加窗口修饰

常用的窗口修饰有：status bar、menu、toolbar。

## 状态栏

我们先增加一个状态栏，可以显示当前鼠标的位置。

只需要增加这么一点代码就够了。

```
class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "sketch frame", size=(800,600))
        self.sketch = SketchWindow(self, -1)
        self.sketch.Bind(wx.EVT_MOTION, self.OnSketchMotion)
        self.statusbar = self.CreateStatusBar()

    def OnSketchMotion(self,event):
        self.statusbar.SetStatusText(str(event.GetPositionTuple()))
        event.Skip()
```

我们是加在Frame上，而不是Window上。

我们可以增加多个状态栏信息。

```
class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "sketch frame", size=(800,600))
        self.sketch = SketchWindow(self, -1)
        self.sketch.Bind(wx.EVT_MOTION, self.OnSketchMotion)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1,-2,-3])

    def OnSketchMotion(self,event):
        self.statusbar.SetStatusText("Pos:%s" %str(event.GetPositionTuple()), 0)
        self.statusbar.SetStatusText("Cur Pts:%s" %len(self.sketch.curLine), 1)
        self.statusbar.SetStatusText("Line Count:%s" %len(self.sketch.lines), 2)
        event.Skip()
```

## 菜单

把菜单栏加好的代码在这里：

https://github.com/teddyxiong53/Python/tree/master/wxpython/wxpython_in_action/sketch/v2



当前菜单的功能函数还没有实现。

我们下面实现save和open的函数。



wxpython程序在pycharm里运行，看不到打印，FileDialog也出不来。

在cmd下面就可以的。

功能验证正常。保存。https://github.com/teddyxiong53/Python/tree/master/wxpython/wxpython_in_action/sketch/v3

## 加入颜色选择器

1、在File，Color里加上一个Other Color的选项。



加好了。解决了一些代码上的小问题。

https://github.com/teddyxiong53/Python/tree/master/wxpython/wxpython_in_action/sketch/v4



## 进行布局调整

给程序加入一个在侧边进行颜色和线宽选择的面板。

使用了GridSizer和BoxSizer这2个布局器。

https://github.com/teddyxiong53/Python/tree/master/wxpython/wxpython_in_action/sketch/v5



## 加入About窗口

https://github.com/teddyxiong53/Python/tree/master/wxpython/wxpython_in_action/sketch/v6

## 增加启动画面

