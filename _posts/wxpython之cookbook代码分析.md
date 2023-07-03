---
title: wxpython之cookbook代码分析
date: 2023-07-01 15:01:51
tags:
	- wxpython

---

--

# 代码地址

https://github.com/driscollis/wxpythoncookbookcode

为了方便后续我自己复用代码，我自己用自己的代码风格照着写了一遍，地址在：

https://github.com/teddyxiong53/wxpython_cookbook

# 01 动态添加删除控件

这个的关键是这几句。在界面元素变化时，需要调用frame的sizer的Layout和frame的Fit函数。

```
        self.widget_sizer.Add(new_button, 0, wx.ALL, 5)
        self.frame.sizer.Layout()
        self.frame.Fit()
```

## Layout函数的作用

它的作用是重新计算和布置所有已添加到 sizer 中的控件，以确保它们以正确的位置和大小显示在窗口中。

## Fit函数的作用

 `Fit` 函数，它的作用是根据窗口中已添加的控件和布局规则，自动调整窗口的大小和位置，以确保所有控件都能够完全显示在窗口中。

## 对我的用途

我可以用在根据配置动态生成界面元素的情况。

# 02 截屏

主要是ScreenDC和MemoryDC的使用。

调用打印机的部分不管。我工作中基本不涉及打印机的。

学了也没有什么用。

## ScreenDC

`wx.ScreenDC()` 是 wxPython 中的一个函数，用于获取当前屏幕的设备上下文（Device Context）。**设备上下文是一个抽象的概念，表示了与设备相关的绘图环境和属性，可以用于绘制图形、文本和图像等。**

具体来说，`wx.ScreenDC()` 函数会根据当前屏幕的分辨率和显示属性，创建一个设备上下文对象，并返回该对象的引用。**可以使用返回的设备上下文对象来绘制当前屏幕的内容，例如截屏、屏幕录制等。**

以下是一个简单的示例代码，演示了如何使用 `wx.ScreenDC()` 函数来获取当前屏幕的设备上下文，并将屏幕内容绘制到一个 wxPython 窗口中：

```python
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')

        # 获取当前屏幕的设备上下文
        dc = wx.ScreenDC()

        # 获取当前屏幕的宽度和高度
        width, height = dc.GetSize()

        # 创建一个和屏幕大小相同的位图对象
        bitmap = wx.Bitmap(width, height)

        # 将屏幕内容绘制到位图对象中
        memdc = wx.MemoryDC(bitmap)
        memdc.Blit(0, 0, width, height, dc, 0, 0)

        # 将位图对象显示在窗口中
        self.bitmap = wx.StaticBitmap(self, bitmap=bitmap)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
```

在这个例子中，我们使用 `wx.ScreenDC()` 函数来获取当前屏幕的设备上下文。然后，我们使用 `GetSize()` 方法获取当前屏幕的宽度和高度，并使用这些值创建一个和屏幕大小相同的位图对象。接下来，我们使用 `wx.MemoryDC` 类来创建一个内存设备上下文对象，并使用 `Blit()` 方法将屏幕内容绘制到位图对象中。最后，我们将位图对象显示在一个 wxPython 窗口中，以便用户查看屏幕截图。

总之，`wx.ScreenDC()` 函数是 wxPython 中用于获取当前屏幕设备上下文的方法，可以用于屏幕截图、屏幕录制等应用场景。

# 03 嵌入图像

在这里看到怎么给应用程序设置图标。

## img2py 脚本用法

`img2py` 是 wxPython 中的一个命令行工具，用于将图像文件转换为 Python 代码，以便在程序中使用。使用 `img2py` 可以方便地将图像文件嵌入 Python 代码中，避免在程序运行时需要读取外部图像文件，从而提高程序的可移植性和运行效率。

`img2py` 命令行工具的用法如下：

```
img2py [options] inputfile outputfile
```

其中，`inputfile` 是要转换为 Python 代码的图像文件，可以是 BMP、JPEG、PNG、GIF 等格式；`outputfile` 是输出的 Python 代码文件，可以是任意合法的 Python 文件名。`options` 是一些可选的参数，用于控制转换过程的行为，包括输出格式、压缩选项、图像尺寸等。

以下是一些常用的 `img2py` 命令行选项：

- `-i, --icon`：将图像文件转换为 wxPython 中的 `wx.Icon` 对象。
- `-b, --bitmap`：将图像文件转换为 wxPython 中的 `wx.Bitmap` 对象。
- `-a, --agw`：将图像文件转换为 `agw` 包中的 `AGWImage` 对象。
- `-n, --name`：指定生成的 Python 代码中的对象名称，默认为图像文件的文件名。
- `-c, --compress`：启用压缩选项，将生成的 Python 代码压缩以减小文件大小。
- `-z, --size`：指定生成的 Python 代码中图像的尺寸，格式为 `width,height`。

以下是一个示例命令，演示了如何使用 `img2py` 将一个 PNG 格式的图像文件转换为 Python 代码，并输出到一个名为 `myimage.py` 的 Python 文件中：

```
img2py -b myimage.png myimage.py
```

在上面的命令中，`-b` 选项表示将图像文件转换为 `wx.Bitmap` 对象，`myimage.png` 是要转换的图像文件，`myimage.py` 是输出的 Python 代码文件。

转换完成后，`myimage.py` 文件中会生成一个名为 `myimage` 的 `wx.Bitmap` 对象，可以在程序中直接使用。

## ico文件和png文件区别

ICO 文件和 PNG 文件都是常见的图像文件格式，但它们有一些不同之处。

**ICO 文件是 Windows 系统中常用的图标文件格式，用于表示应用程序、文件夹、文件等的图标**。ICO 文件可以包含多个图标，每个图标都有不同的尺寸和颜色深度。ICO 文件通常用于 Windows 系统中的界面设计和图标制作，可以通过 Windows 图库编辑器等工具进行编辑和制作。ICO 文件支持的颜色深度较少，通常只支持 1、4、8 和 24 位色。

PNG 文件是一种无损压缩的图像文件格式，支持透明度和高色彩深度。PNG 文件通常用于 Web 设计、图像处理、游戏开发等领域，可以通过 Photoshop、GIMP 或其他图像编辑软件进行编辑和制作。PNG 文件支持的颜色深度较多，可以支持 1、2、4、8、16、24 和 32 位色。PNG 文件还支持 alpha 通道和透明度，可以实现半透明效果和透明背景。

在实际应用中，ICO 文件通常用于 Windows 系统中的图标设计和制作，PNG 文件通常用于 Web 设计、游戏开发和图像处理等领域。如果需要在 Python 程序中使用图像，可以将 PNG 文件转换为 wxPython 中的 `wx.Bitmap` 对象或 `wx.Image` 对象，或者将 ICO 文件转换为 `wx.Icon` 对象。

# 04 背景图片

给应用程序设置背景图片。

这个还是有点用途的。

## hSizer.Add((1,1), 1, wx.EXPAND)

`hSizer.Add((1,1), 1, wx.EXPAND)` 是 wxPython 中用于添加布局元素的方法之一。**这个方法的作用是在水平方向上添加一个空白元素**，用于调整布局中各个元素之间的间距和位置。

具体来说，`hSizer` 是一个水平布局器（`wx.BoxSizer(wx.HORIZONTAL)`），用于管理一组水平方向上的窗口元素。`Add()` 方法用于向布局器中添加元素，其中**第一个参数 `(1, 1)` 表示要添加的元素的大小，这里是一个元组，表示宽度和高度都为 1 个像素。**第二个参数 `1` 表示该元素占据的空间权重，这里设置为 1，**表示该元素在布局中占据的空间和其他元素一样**。第三个参数 `wx.EXPAND` 表示该元素在布局中应该如何扩展，这里设置为 `wx.EXPAND`，表示该元素可以在水平方向上扩展以填充布局中的空白区域。

总之，`hSizer.Add((1,1), 1, wx.EXPAND)` 是 wxPython 中用于添加水平布局元素的方法之一，用于添加一个空白元素来调整布局中元素之间的间距和位置。

## h_sizer.Add(sizer, 0, wx.TOP, 100)

`h_sizer.Add(sizer, 0, wx.TOP, 100)` 是 wxPython 中用于添加布局元素的方法之一。这个方法的作用是在水平方向上添加一个子布局器 `sizer`，并在**该子布局器上方添加一个垂直方向上的空白区域，上边距为 100 个像素。**

具体来说，`h_sizer` 是一个水平布局器（`wx.BoxSizer(wx.HORIZONTAL)`），用于管理一组水平方向上的窗口元素。`Add()` 方法用于向布局器中添加元素，其中第一个参数 `sizer` 表示要添加的子布局器对象；**第二个参数 `0` 表示该元素占据的空间权重，这里设置为 0，表示该元素在布局中不占据额外的空间；**第三个参数 `wx.TOP` 表示该元素应该放置在子布局器 `sizer` 的上方；第四个参数 `100` 表示该元素与子布局器 `sizer` 之间的上边距为 100 个像素。

总之，`h_sizer.Add(sizer, 0, wx.TOP, 100)` 是 wxPython 中用于添加水平布局元素的方法之一，用于添加一个子布局器，并在子布局器上方添加一个垂直方向上的空白区域，上边距为 100 个像素，以调整布局中元素之间的间距和位置。

# 05 改变背景颜色

没有什么特别的。

# 06 黑夜模式

这个不管。

# 07 pubsub

wx.lib.pubsub 这里的这个通信模块已经不再推荐使用了。

但是还可以用。不会报错 。

这个用来在不同的Frame之间通信。

## wx.lib.pubsub 主要使用场景

`wx.lib.pubsub` 是 wxPython 中用于实现发布-订阅模式的一个第三方库，它允许不同组件之间进行消息传递和通信。主要使用场景包括以下几个方面：

1. 解耦组件之间的关系：使用发布-订阅模式可以将组件之间的依赖关系解耦，使得组件之间可以独立地进行开发和维护。

2. 简化组件之间的通信：使用发布-订阅模式可以通过简单的消息传递机制实现组件之间的通信，避免了复杂的回调函数和事件处理机制。

3. 提高组件之间的灵活性：使用发布-订阅模式可以使得组件之间的通信更加灵活和动态，不需要在代码中硬编码组件之间的关系，而是通过订阅特定的消息来进行通信。

4. 支持多种消息类型：`wx.lib.pubsub` 支持多种消息类型，包括字符串、整数、浮点数、列表、字典等，可以满足不同场景下的消息传递需求。

总之，使用 `wx.lib.pubsub` 可以在 wxPython 应用程序中实现组件之间的消息传递和通信，从而提高应用程序的灵活性和可维护性。它适用于需要解耦组件之间的关系、简化组件之间的通信、提高组件之间的灵活性和支持多种消息类型的应用场景。

# 08 pydispatcher

跟pubsub接口都是兼容的。

# 09 wizard写法

