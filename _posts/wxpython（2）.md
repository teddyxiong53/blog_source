---
title: wxpython（2）
date: 2018-06-03 22:00:38
tags:
	- wxpython

---



上一篇文章，把基本的界面内容写完了。

现在看一点高级的东西。

# 加入PyCrust

PyCrust的Crust是壳的意思，跟shell含义是一样的。只是因为PyShell这个名字已经被占用了。

这个东西看起来挺强大的。但是不是我现在需要的，我先跳过。



#设计代码的方法

重构的一些原则：

1、不要重复。

2、一次做一件事情。

3、嵌套的层数要少。

4、避免魔数。



我们先看一个例子。这个是一个写得不好的。是我们马上要进行重构的对象。

```
import wx

class RefactorExample(wx.Frame):
    def __init__(self, parent, id ):
        wx.Frame.__init__(self, parent, id, 'refactor example', size=(320,100))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")
        prevButton = wx.Button(panel, -1, "<<prev", pos=(80,0))
        self.Bind(wx.EVT_BUTTON, self.OnPrev, prevButton)
        nextButton = wx.Button(panel, -1, "next>>", pos=(160,0))
        self.Bind(wx.EVT_BUTTON, self.OnNext, nextButton)

        firstButton = wx.Button(panel, -1, "first", pos=(0,0))
        self.Bind(wx.EVT_BUTTON, self.OnFirst, firstButton)
        lastButton = wx.Button(panel, -1, "last", pos=(240,0))
        self.Bind(wx.EVT_BUTTON, self.OnNext, lastButton)

    def OnFirst(self, event):
        pass
    def OnLast(self, event):
        pass
    def OnPrev(self, event):
        pass
    def OnNext(self, event):
        pass

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = RefactorExample(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
```

上面代码存在的问题。

1、构造函数写得有点长。我们可以把里面的内容提取成一个函数。

2、代码有重复。生成按钮的代码。

函数提取。

```
    def __init__(self, parent, id ):
        wx.Frame.__init__(self, parent, id, 'refactor example', size=(320,100))
        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour("White")
        self.createButtonBar(self.panel)

    def createButtonBar(self, panel):
        firstButton = self.buildOneButton(panel, "first", self.OnFirst, pos=(0,0))
        prevButton = self.buildOneButton(panel, "<<prev", self.OnPrev, pos=(80,0))

    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return  button
```

然后是数据内容的提取，位置坐标这种信息，不要分散在代码里。修改不方便。

把数据集中起来。

```
import wx

class RefactorExample(wx.Frame):
    def __init__(self, parent, id ):
        wx.Frame.__init__(self, parent, id, 'refactor example', size=(320,100))
        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour("White")
        self.createButtonBar(self.panel)

    def buttonData(self):
        return(("first", self.OnFirst),
               ("<<prev", self.OnPrev),
               ("next>>", self.OnNext),
               ("last", self.OnLast)
        )

    def createButtonBar(self, panel, yPos=0):
        xPos = 0
        for label,handler in self.buttonData():
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, label, handler, pos)
            xPos += button.GetSize().width

    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return  button


    def OnFirst(self, event):
        pass
    def OnLast(self, event):
        pass
    def OnPrev(self, event):
        pass
    def OnNext(self, event):
        pass

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = RefactorExample(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
```

# MVC模式

对于桌面程序，View和Controller往往是在一起的。

因为一般你显示数据的窗口组件，本身也需要显示在屏幕上。

而对于web应用，View和Controller很好分离，因为Controller在服务器后台。



