---
title: wxpython之各种sizer布局器分析
date: 2023-07-01 15:11:51
tags:
	- wxpython

---

--

在 wxPython 中，Sizer 是一种布局管理器，用于控制窗口中各个控件的大小和位置。Sizer 可以自动处理控件的布局，使得窗口在不同平台和不同分辨率下都能呈现出一致的效果。

wxPython 中提供了几种不同类型的 Sizer，包括：

1. `wx.BoxSizer`：BoxSizer 是最常用的 Sizer 类型之一，用于将控件按照水平或垂直方向排列。可以通过设置 `wx.HORIZONTAL` 或 `wx.VERTICAL` 参数来指定水平或垂直方向。

2. `wx.GridSizer`：GridSizer 用于将控件按照网格布局排列。可以通过设置行数和列数来指定网格的大小。

3. `wx.FlexGridSizer`：FlexGridSizer 与 GridSizer 类似，但可以设置每个单元格的大小和对齐方式。

4. `wx.StaticBoxSizer`：StaticBoxSizer 用于将控件按照分组排列，并在每个分组周围**添加一个静态框。**

5. `wx.WrapSizer`：WrapSizer 用于将控件按照水平或垂直方向排列，并自动换行。

6. `wx.GridBagSizer`：**GridBagSizer 是最灵活的 Sizer 类型之一**，可以将控件按照网格布局排列，并自由设置每个单元格的大小、位置和对齐方式。

7. `wx.BoxSizer(wx.HORIZONTAL)` 和 `wx.BoxSizer(wx.VERTICAL)`：这两种 Sizer 是 BoxSizer 的简化版本，用于将控件按照水平或垂直方向排列。

# BoxSizer例子

```python
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        
        # 创建控件
        label1 = wx.StaticText(self, label='Label 1')
        label2 = wx.StaticText(self, label='Label 2')
        button1 = wx.Button(self, label='Button 1')
        button2 = wx.Button(self, label='Button 2')
        
        # 创建 Sizer 并添加控件
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label1, 0, wx.ALL, 5)  # 添加 Label 1
        sizer.Add(label2, 0, wx.ALL, 5)  # 添加 Label 2
        
        sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer.Add(button1, 0, wx.ALL, 5)  # 添加 Button 1
        sub_sizer.Add(button2, 0, wx.ALL, 5)  # 添加 Button 2
        
        sizer.Add(sub_sizer, 0, wx.CENTER)  # 添加 Button 1 和 Button 2 的水平 BoxSizer，并在窗口中心对齐

        self.SetSizer(sizer)
        self.Fit()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
```

在这个例子中，我们使用了 `wx.BoxSizer` 和 `wx.HORIZONTAL` 和 `wx.VERTICAL` 参数来创建水平和垂直方向的 BoxSizer。我们还使用了 `wx.ALL` 参数来指定控件与 Sizer 之间的边距。在最后，我们使用 `self.SetSizer(sizer)` 将 Sizer 应用到窗口中，并使用 `self.Fit()` 调整窗口大小以适应其内容。

# GridSizer的例子

构造方法这样就够了：

```
GridSizer(rows, cols, vgap, hgap)
```

例子：

```
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        self.panel = wx.Panel(self)

        # 创建一个 2 行 3 列的网格布局
        grid = wx.GridSizer(rows=2, cols=3, vgap=10, hgap=10)

        # 向网格中添加三个按钮
        button1 = wx.Button(self.panel, label='Button 1')
        button2 = wx.Button(self.panel, label='Button 2')
        button3 = wx.Button(self.panel, label='Button 3')
        grid.Add(button1, 0, wx.EXPAND)
        grid.Add(button2, 0, wx.EXPAND)
        grid.Add(button3, 0, wx.EXPAND)

        # 将网格应用到 panel 上
        self.panel.SetSizer(grid)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
```

以下是一些适合使用 `wx.GridSizer` 的场景：

- 创建一个包含多个按钮、文本框、复选框等控件的表单或面板。
- 在一个窗口中排列多个图像或图表。
- 创建一个包含多个文本标签和输入框的表格或列表。
- 在一个窗口中排列多个媒体文件，如音频、视频等。

# WrapSizer例子

`wx.WrapSizer` 是 wxPython 中的一个 Sizer 类，用于创建一个自动换行的布局，可以在窗口大小改变时自动调整控件的位置和大小。`wx.WrapSizer` 可以使控件更加灵活和自适应，特别是当需要在一个窗口中放置多个控件时，不需要手动计算控件的位置和大小。

以下是一个使用 `wx.WrapSizer` 创建一个简单布局的示例代码：

```python
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        self.panel = wx.Panel(self)

        # 创建一个自动换行的布局
        sizer = wx.WrapSizer(wx.HORIZONTAL)

        # 向布局中添加多个按钮
        for i in range(10):
            button = wx.Button(self.panel, label=f'Button {i+1}')
            sizer.Add(button, 0, wx.ALL, 10)

        # 将布局应用到 panel 上
        self.panel.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
```

在这个例子中，我们创建了一个自动换行的布局，并向其中添加了十个按钮。我们使用 `wx.WrapSizer` 来创建一个自动换行的布局，并使用 `wx.HORIZONTAL` 参数指定水平方向的自动换行。我们还使用 `wx.ALL` 标志来指示按钮应该在四个方向上添加相同的空隙。最后，我们将布局应用到了 `wx.Panel` 上。

运行这个示例代码后，应该会看到一个自动换行的布局，其中按钮被自动调整为适合窗口大小的大小，并在窗口大小改变时自动调整其位置和大小。`wx.WrapSizer` 可以使控件更加灵活和自适应，特别是当需要在一个窗口中放置多个控件时，不需要手动计算控件的位置和大小。

# GridBagSizer

适合用来做表单布局。

`wx.GridBagSizer` 是 wxPython 中的一个 Sizer 类，用于创建一个灵活的网格布局，可以在不同的单元格中放置不同大小和位置的控件，并可以调整单元格之间的间距和比例。`wx.GridBagSizer` 可以使控件更加灵活和自适应，特别是当需要在一个窗口中放置多个相关控件时。

以下是一个使用 `wx.GridBagSizer` 创建一个简单布局的示例代码：

```python
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        self.panel = wx.Panel(self)

        # 创建一个灵活的网格布局
        sizer = wx.GridBagSizer(hgap=5, vgap=5)

        # 向网格布局中添加多个控件
        label1 = wx.StaticText(self.panel, label='Name:')
        textctrl1 = wx.TextCtrl(self.panel)
        label2 = wx.StaticText(self.panel, label='Age:')
        textctrl2 = wx.TextCtrl(self.panel)
        button1 = wx.Button(self.panel, label='OK')
        button2 = wx.Button(self.panel, label='Cancel')

        sizer.Add(label1, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(textctrl1, (0, 1), flag=wx.EXPAND)
        sizer.Add(label2, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(textctrl2, (1, 1), flag=wx.EXPAND)
        sizer.Add(button1, (2, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(button2, (2, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

        # 将网格布局应用到 panel 上
        self.panel.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
```

在这个例子中，我们创建了一个灵活的网格布局，并向其中添加了四个标签、两个文本框和两个按钮。我们使用 `wx.GridBagSizer` 来创建一个灵活的网格布局，并使用 `hgap` 和 `vgap` 参数指定单元格之间的水平和垂直间距。我们使用 `Add` 方法将控件添加到网格布局中，并使用元组 `(row, col)` 来指定控件所在的行和列。我们还使用 `wx.ALIGN_CENTER_VERTICAL` 和 `wx.EXPAND` 标志来指示控件应该垂直居中并填充其单元格。最后，我们将网格布局应用到了 `wx.Panel` 上。

运行这个示例代码后，应该会看到一个包含四个标签、两个文本框和两个按钮的网格布局，其中控件被自动调整为适合窗口大小的大小，并可以在不同的单元格中放置不同大小和位置的控件。`wx.GridBagSizer` 可以使控件更加灵活和自适应，特别是当需要在一个窗口中放置多个相关控件时。



# sizer的各种flag

```
wx.TOP
wx.BOTTOM
wx.LEFT
wx.RIGHT
wx.ALL

这5个是说控件会被放在sizer的上下左右哪一侧。

wx.EXPAND 这个说填满。
wx.SHAPED 这个是等比例放大

wx.FIXED_MINSIZE 最小尺寸限制。

wx.RESERVE_SPACE_EVEN_IF_HIDDEN
保存空间，即使控件被隐藏。


```

通常wx.Sizers将使用wx.Window.GetEffectiveMinSize来确定窗口项的最小尺寸应该是多少，并使用该尺寸来计算布局。这允许在项目发生变化且其最佳尺寸发生变化时调整布局。如果您希望窗口项保持其开始时的大小，则使用 wx.FIXED_MINSIZE。

# sizer的主要方法

```
Add
AddMany
AddSpacer 添加空白

Clear 清除所有的控件。

Fit
FitInside

GetItem
GetItemById

Insert
Prepend
Show

```

## BoxSizer的方法

这个就没有多少。

```
AddSpacer
SetOrientation ：主要就是这个设置方向的。
```

# Add方法的参数

```
Add (self, window, flags)

Add (self, window, proportion=0, flag=0, border=0, userData=None)

Add (self, sizer, flags)

Add (self, sizer, proportion=0, flag=0, border=0, userData=None)

Add (self, width, height, proportion=0, flag=0, border=0, userData=None)

Add (self, width, height, flags)

Add (self, item)
```

这些Add函数，按照参数，分为4类：

window：这一个是最常见的。就是把一个空间往里面放。

sizer

宽高

item

proportion 这个参数的意思是什么？一般给0，表示不会根据窗口变化而缩放。

比例 (int) – 尽管该参数的含义在 wx.Sizer 中未定义，但它在 wx.BoxSizer 中用于指示 sizer 的子级是否可以在 wx.BoxSizer 的主方向上更改其大小 - 其中 0 代表不可更改且大于零的值被解释为相对于同一 wx.BoxSizer 的其他子项的值。例如，您可能有一个带有三个子级的水平 wx.BoxSizer，其中两个子级应该使用 sizer 来更改其大小。然后，两个可拉伸窗口将分别获得 1 的值，以使它们随着 sizer 的水平尺寸均匀地增长和收缩。