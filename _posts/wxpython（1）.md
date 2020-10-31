---
title: wxpython（1）
date: 2018-06-03 16:35:41
tags:
	- wxpython
typora-root-url:..\
---



现在通过写一系列的文章，来学习wxpython的软件编写方法。

先看最简单的一个程序的写法。

开发环境：windows 7 ，PyCharm。

主要参考《wxPython in Action》这本书。

# 最简单程序

新建一个test.py文件。内容如下。

```
import wx

class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(parent=None, title="hello wxpython")
        frame.Show()
        return True

app = App()
app.MainLoop()
```

这个运行的效果就是一个空白的串口。

可以看到涉及的主要类是：App和Frame。这就类似Android下面的Application和Activity了。

一个App由一个或者多个Frame组成。

然后有一个事件循环，在等待你的鼠标键盘事件。

# 扩展上面的最简单程序

```
import wx

class MyFrame(wx.Frame):
    pass

class App(wx.App):
    def OnPreInit(self):
        self.frame = MyFrame(parent=None, title="myapp")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()
```

我们做了这几点改动：

1、增加了MyFrame类，集成了Frame。

2、设置了顶层窗口。

3、加入了main函数。

# 进一步完善

```
import wx

class MyFrame(wx.Frame):
    def __init__(self, image, parent=None, id=-1, pos=wx.DefaultPosition, title="hello,wx"):
        temp = image.ConvertToBitmap()
        size = temp.GetWidth(), temp.GetHeight()
        wx.Frame.__init__(self, parent, id, title, pos, size)
        self.bmp = wx.StaticBitmap(parent=self, bitmap=temp)

    pass
class App(wx.App):
    def OnPreInit(self):
        image = wx.Image('test.jpg', wx.BITMAP_TYPE_JPEG)
        self.frame = MyFrame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()
if __name__ == '__main__':
    main()
```

改动点：

1、加入了图片显示。

2、main函数提取。

# 创建wx.App的子类

你需要做的事情有：

1、定义子类。

2、重写OnInit方法。

3、创建子类的实例。

4、调用子类实例的MainLoop方法。

我们上面就是这么干的。



wx提供了PySimpleApp这个简单的子类。对于简单场景绰绰有余了。

```
import wx

def main():
    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None)
    frame.Show()
    app.MainLoop()
if __name__ == '__main__':
    main()
```



# 重定向输出

```
import wx,sys

class Frame(wx.Frame):
    def __init__(self, parent, id, title):
        print "Frame __init__"
        wx.Frame.__init__(self, parent, id, title)

class App(wx.App):
    def __init__(self, redirect=True, filename=None):
        print "App __init__"
        wx.App.__init__(self, redirect, filename)

    def OnPreInit(self):
        print "OnPreInit"
        self.frame = Frame(parent=None, id=-1, title="wx")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        print>>sys.stderr,"A pretend error message"
        return True

    def OnExit(self):
        print "OnExit"

if __name__ == '__main__':
    app =App(redirect=True)
    print "before MainLoop"
    app.MainLoop()
    print "after MainLoop"
```

运行，可以看到弹出了2个窗口。

因为我们没有给文件名，所以stdout和stderr都是单独输出到窗口里了。

上面加的打印，只有一条是在控制台打印出来的。

```
C:\Python27\python.exe D:/work/pycharm/py_test/test.py
App __init__
```

最后关闭的时候，控制台会打印“after MainLoop”。

![](/images/wxpython（1）重定向.png)·



我们改一下，

```
app =App(redirect=True, filename="./xx.log")
```

这样就只会弹出一个窗口了。日志会写入到xx.log文件里。

# 程序的退出

正常的退出方法是点击右下角的关闭按钮。

但是也可以用代码进行退出。

```
app.ExitMainLoop()
```

这个函数可以进行退出。

还有一个

```
wx.Exit()
```



# 顶层窗口

顶层窗口一般是程序的主界面。

顶层窗口的特点是Parent是None。



# 组件ID

所有组件都有一个ID来进行标识。

在一个Frame里，每个组件的ID要是唯一。

但是处于保险起见，我们最好是让App里的每一个组件的ID都唯一。

## 预定义的ID

有些标准的，已经被系统预定义了。

wx.ID_OK

wx.ID_CANCEL

## 创建ID的方法

1、明确给一个正整数值。

2、用wx.NewId()函数生成一个。

3、给-1 。还是让系统自己去设值。

# Frame的样式

默认样式是

wx.DEFAULT_FRAME_STYLE

```
wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
```

这些意思都很明显。



# 给窗口增加部件

我们前面的窗口都是空白的，什么都没有。

现在我们看看如何给窗口增加一个按钮。

```
import wx,sys

class InsertFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Frame with button', size=(300,100))
        panel = wx.Panel(self)
        button = wx.Button(panel, label="click me", pos=(125,10),size=(50,50))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)

    def OnCloseMe(self, event):
        self.Close(True)

if __name__ == '__main__':
    app  = wx.PySimpleApp()
    frame = InsertFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
```

从上面代码，我们指定了button的大小和位置，这种信息写在代码里，是非常不好的。

非常繁琐，而且不便于调整。

Android里有Layout布局。wx里也有类似的机制。叫做sizer。

# 增加menu、toolbar、status bar

书的内容，跟现在的wx已经不一样了。需要做下面的修改。

```
将原来的import images 替换成wx.py.images as images 原来的getNewBitmap 替换成getPyBitmap
```

```
import wx,sys
import wx.py.images as images

class ToolbarFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "toolbar", size=(300,200))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('White')
        statusBar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(wx.NewId(), images.getPyBitmap(),
                              "New", "Long help for 'new'")
        toolbar.Realize()
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menuBar.Append(menu1, "&File")
        menu2 = wx.Menu()
        menu2.Append(wx.NewId(), '&Copy', "Copy in status bar")
        menu2.Append(wx.NewId(), "C&ut", "")
        menu2.Append(wx.NewId(), "Paste", "")
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(), "&Options...", "Display Options")

        menuBar.Append(menu2, "&Edit")
        self.SetMenuBar(menuBar)


if __name__ == '__main__':
    app  = wx.PySimpleApp()
    frame = ToolbarFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
```

现在得到的界面已经有点样子了。

![](/images/wxpython（1）带菜单栏的界面.png)



# wx.Event

常用的事件有：

CloseEvent。

CommandEvent。

```
有28种。
EVT_BUTTON
```

KeyEvent。

MouseEvent。

```
一共14种。
敲击类的有9种。左中右3个键，分别有down、up、dclick（双击）。
EVT_LEFT_DOWN
EVT_LEFT_UP
EVT_LEFT_DCLICK
另外5种是：
EVT_MOTION
EVT_ENTER_WINDOW：这个如果是button来设置，就进入button范围。
EVT_EXIT_WINDOW
EVT_MOUSE_WHEEL：滚轮。
EVT_MOUSE_EVENTS：包括上面所有情况。
```

PaintEvent。

SizeEvent。

TimerEvent。



```
import wx,sys
import wx.py.images as images

class DoubleEventFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "frame with button", size=(300,100))
        self.panel = wx.Panel(self, -1)
        self.button = wx.Button(self.panel, -1, "click me", pos=(100,15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)
        #注意下面这个是button.Bind，上面是frame.Bind
        self.button.Bind( wx.EVT_LEFT_DOWN, self.OnMouseDown)

    def OnMouseDown(self, event):
        self.button.SetLabel("Again")
        event.Skip()
    def OnButtonClick(self, event):
        self.panel.SetBackgroundColour("Green")
        self.panel.Refresh()

if __name__ == '__main__':
    app  = wx.PySimpleApp()
    frame = DoubleEventFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
```



# Frame类

wxFrame对象是最常用的顶层窗口。它是从 wxWindow 类派生的。

wxFrame窗口可以包含任何帧(frame)而不只是一个对话或另一个帧(frame)。

wxFormBuilder是一个开源，跨平台的所见即所得的图形用户界面生成器，可以翻译wxWidget GUI设计成C++，Python和PHP或XML格式。 

Frame类的成员函数

```
CreateStatusBar()
CreateToolBar()
# MenuBar没有对应的Create函数，需要构造一个，然后setMenuBar设置过来。
GetMenuBar()
GetStatusBar()
SetToolBar() #也可以构造，然后设置过来。
SetStatusBar()
# 设置状态栏的文字
SetStatusText()
# 设置窗口大小
SetSize()
# 设置位置
SetPosition()
# 设置标题
SetTitle()
```

Frame绑定的事件

```
EVT_CLOSE
EVT_MENU_OPEN
EVT_MENU_CLOSE
EVT_MENU_HIGHLIGHT
```

# Panel类

Panel就相当于html里的div。没有也可以。但是有了，我们就操作起来更加方便。

而且我们一般是作为布局的基本元素来用。



小构件，如按钮，文本框等被放置在面板窗口。 

wx.Panel类通常是被放在一个wxFrame对象中。

**这个类也继承自wxWindow类。**

虽然控件可以手动放置在面板指定屏幕坐标的位置，建议使用合适的布局方案，称为大小测定器(sizer)

在wxPython中，为更好地控制布局和解决调整大小的问题。

在wxPanel构造，父参数是wx.Frame对象，在面板中放置。

id参数的默认值是wx.ID_ANY，而默认的样式参数是wxTAB_TRAVERSAL。

# Sizer

```
BoxSizer
	可设置水平或垂直布局，当控件超出窗体后不会自动换行
StaticBoxSizer
	在BoxSizer外面加了一个静态的边框以及标签，
	他可以独立的存在也可以放到其他布局管理器中进行嵌套：
FlexGridSizer
	网格布局，特点是可以设置网格之间的显示比例
```



# 布局

下面的代码，都在这个基础上进行添加。

```
import wx

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="xx", size=wx.Size(800,600))
app = wx.App()
frame = MyFrame(None)
frame.Show(True)
app.MainLoop()
```



## 绝对布局

```
class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="xx", size=(800,600))
        panel = wx.Panel(self)
        panel1 = wx.Panel(panel, pos=(0,0), size=(250, wx.EXPAND))
        panel1.SetBackgroundColour("yellow")
        panel2 = wx.Panel(panel, pos=(255,0), size=(wx.EXPAND, wx.EXPAND))
        panel2.SetBackgroundColour("green")
```

效果是这样：

![image-20201031114126972](/images/random_name/image-20201031114126972.png)



## 使用Sizer进行布局

![img](/images/random_name/2020011314571712.png)







# 改动UI及时刷新

因为我的调用是阻塞了ui线程的。

所以调用过程中改动了ui元素，是不能马上显示出来的。

怎么办？调用一下wx.Yield()就可以了。让ui有机会调度刷新一下。



# 参考资料

1、这个系列教程不错

https://www.yiibai.com/wxpython/wxpython_hello_world.html

2、wxPython各个布局的简单案例

https://blog.csdn.net/lyhDream/article/details/103957751