---
title: tkinter（1）
date: 2023-01-02 10:20:30
tags:
	- python
---

--

# 资源收集

官方文档

https://docs.python.org/zh-cn/3.6/library/tkinter.html

这个教程不错。

https://www.jiyik.com/w/tkinter/tkinter-label

# 基本信息

Tcl/Tk集成到Python中已经有一些年头了。

Python程序员可以通过 [`tkinter`](https://docs.python.org/zh-cn/3.6/library/tkinter.html#module-tkinter) 包和它的扩展， [`tkinter.tix`](https://docs.python.org/zh-cn/3.6/library/tkinter.tix.html#module-tkinter.tix) 模块和 [`tkinter.ttk`](https://docs.python.org/zh-cn/3.6/library/tkinter.ttk.html#module-tkinter.ttk) 模块，来使用这套鲁棒的、平台无关的窗口工具集。

[`tkinter`](https://docs.python.org/zh-cn/3.6/library/tkinter.html#module-tkinter) 包使用面向对象的方式对Tcl/Tk进行了一层薄包装。

使用 [`tkinter`](https://docs.python.org/zh-cn/3.6/library/tkinter.html#module-tkinter) ，你不需要写Tcl代码，但可能需要参考Tk文档，甚至Tcl文档。

 [`tkinter`](https://docs.python.org/zh-cn/3.6/library/tkinter.html#module-tkinter) 使用Python类，对Tk的窗体小部件（Widgets）进行了一系列的封装。

除此之外，内部模块 `_tkinter` 针对Python和Tcl之间的交互，**提供了一套线程安全的机制。**

[`tkinter`](https://docs.python.org/zh-cn/3.6/library/tkinter.html#module-tkinter) 最大的优点就一个字：快，再一个，是Python自带的。

尽管官方文档不太完整，但有其他资源可以参考，比如Tk手册，教程等。

 [`tkinter`](https://docs.python.org/zh-cn/3.6/library/tkinter.html#module-tkinter) 也以比较过时的外观为人所知，但在Tk 8.5中，这一点得到了极大的改观。

除此之外，如果有兴趣，还有其他的一些GUI库可供使用。

更多信息，请参考 [其他图形用户界面（GUI）包](https://docs.python.org/zh-cn/3.6/library/othergui.html#other-gui-packages) 小节。





# HelloWorld

```
import tkinter as tk
root_window = tk.Tk()
root_window.title('test')
root_window.mainloop()
```

# 增加一个label和一个button

```
import tkinter as tk
root_window = tk.Tk()
root_window.title('test')
root_window.geometry('450x300')
root_window['background'] = '#c9c9c9'
text = tk.Label(root_window, text='label test', bg='yellow', fg='red', font=('Times', 20, 'bold italic'))
text.pack()
button = tk.Button(root_window, text='close', command=root_window.quit)
button.pack(side='bottom')
root_window.mainloop()

```

# pack表示了什么

## 简而言之，就是相对位置布局

`pack` 是 Tkinter 中的一个布局管理器，用于将控件放置在父容器中。

`pack` 方法是每个可包装（packable）控件的实例方法，它用于将控件放置在父容器中的适当位置。

```python
widget.pack(options)
```

在 `pack` 方法中，你可以指定一些选项来控制控件的布局和放置。以下是一些常用的选项：

- `side`：控件相对于父容器的放置位置，可以是 `"top"`、`"bottom"`、`"left"` 或 `"right"`。
- `fill`：控件沿着其所在方向填充可用空间，可以是 `"x"`（水平填充）、`"y"`（垂直填充）或 `"both"`（水平和垂直填充）。
- `expand`：控件是否在父容器中扩展，可以是 `True` 或 `False`。
- `padx` 和 `pady`：控件相对于周围空间的水平和垂直填充值。

以下是一个示例，演示如何使用 `pack` 方法将两个按钮控件放置在一个框架中：

```python
import tkinter as tk

root = tk.Tk()

frame = tk.Frame(root)
frame.pack()

button1 = tk.Button(frame, text="Button 1")
button1.pack(side="left", padx=10, pady=5)

button2 = tk.Button(frame, text="Button 2")
button2.pack(side="right", padx=10, pady=5)

root.mainloop()
```

在上面的示例中，我们首先创建一个根窗口 `root`。然后，创建一个框架 `frame` 并将其使用 `pack` 方法放置在根窗口中。最后，创建两个按钮 `button1` 和 `button2`，并使用 `pack` 方法将它们分别放置在框架中的左侧和右侧。

`pack` 方法的调用顺序决定了控件的放置顺序和位置。根据需要，你可以在父容器中嵌套多个框架和控件，并使用 `pack` 方法将它们放置在合适的位置。

**请注意，`pack` 布局管理器对于简单的布局需求非常方便，**

但对于更复杂的布局需求，例如网格布局，你可能需要使用 `grid` 或 `place` 布局管理器来实现更精确的控件放置。



`pack()` 方法用来对主控件里面的小控件来进行布局分布。它有如下的参数列表，

| pack() 方法                         | 描述                         |
| ----------------------------------- | ---------------------------- |
| after=widget                        | 打包widget后打包             |
| anchor=NSEW (or subset)             | position widget according to |
| before=widget                       | 在打包小部件之前打包它       |
| expand=bool                         | 如果父级大小增加则扩展小部件 |
| fill=NONE or X or Y or BOTH         | 如果小部件增长，则填充小部件 |
| in=master                           | 使用 master 来包含这个小部件 |
| in_=master                          | 请参阅“in”选项说明           |
| ipadx=amount                        | 在x方向添加内部填充          |
| ipady=amount                        | 在y方向添加内部填充          |
| padx=amount                         | 在x方向添加填充              |
| pady=amount                         | 在y方向添加填充              |
| side=TOP or BOTTOM or LEFT or RIGHT | 在哪里添加这个小部件。       |

通过更改 `pack()` 的参数，你可以获取不同的控件布局。

# tkinter里的frame用途

在Tkinter中，Frame是一个容器控件，用于组织和管理其他控件。它可以用作其他控件的父容器，以便将它们组织成逻辑上的单元或者实现复杂的布局。

以下是一些Frame控件的常见用途：

1. **布局管理器的容器**：Frame可以用作其他控件的容器，例如放置按钮、标签、输入框等控件的容器。通过在Frame中使用布局管理器（如pack、grid或place），可以更好地控制这些控件的放置方式和位置。

2. **分组控件**：Frame可以用于将相关的控件组合在一起，形成一个逻辑上的单元或者功能块。通过将相关的控件放置在同一个Frame中，可以提高代码的可读性和维护性，并使代码结构更清晰。

3. **边框和装饰**：Frame可以用于添加边框、背景色、装饰和样式等效果，以增强界面的外观。通过设置Frame的relief、borderwidth和background等属性，可以为其中的控件提供可视化的边界和视觉分隔。

4. **页面切换**：Frame可以用于实现多个页面或视图之间的切换。通过在Frame中放置不同的控件组合，可以根据需要显示和隐藏特定的Frame，以实现用户界面的动态切换和导航。

5. **复杂布局**：Frame可以嵌套使用，形成层次化的布局结构。通过将多个Frame嵌套在一起，可以实现复杂的布局，并按照需要组合和组织控件。

总的来说，Frame是一个非常有用的控件，用于组织和管理其他控件，实现更好的布局和界面组织。它提供了一种组织控件的方式，并为其他控件提供容器和装饰功能。

## frame切换页面的例子

```
import tkinter as tk

class Page(tk.Frame):
    def __init__(self, parent, name):
        tk.Frame.__init__(self, parent)
        self.name = name

    def show(self):
        self.lift()

class PageManager(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pages = {}

    def add_page(self, page):
        self.pages[page.name] = page
        page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)

    def show_page(self, name):
        page = self.pages.get(name)
        if page:
            page.show()

# 创建根窗口
root = tk.Tk()

# 创建页面管理器
page_manager = PageManager(root)
page_manager.pack(fill="both", expand=True)  # 将页面管理器放置在根窗口上

# 创建页面1
page1 = Page(page_manager, "Page 1")
label1 = tk.Label(page1, text="This is Page 1", font=("Helvetica", 24))
label1.pack()

# 创建页面2
page2 = Page(page_manager, "Page 2")
label2 = tk.Label(page2, text="This is Page 2", font=("Helvetica", 24))
label2.pack()

# 添加页面到页面管理器
page_manager.add_page(page1)
page_manager.add_page(page2)

# 创建按钮控件
button1 = tk.Button(root, text="Page 1", command=lambda: page_manager.show_page("Page 1"))
button1.pack(side="left")

button2 = tk.Button(root, text="Page 2", command=lambda: page_manager.show_page("Page 2"))
button2.pack(side="left")

# 显示初始页面
page_manager.show_page("Page 1")

# 运行主循环
root.mainloop()

```



# 控件类型

有15种控件

```
Button
Canvas
Checkbutton
Entry
Frame
Label
LabelFrame
ListBox
Menu
MenuButton
Message
MessageBox
OptionMenu
PanedWindow
RadioButton
Scale
Spinbox
Scrollbar
Text
Toplevel
```

控件的基本属性：

```
anchor
bg
bitmap
borderwidth
command
cursor
font
fg
height
image
justify
padx/pady
relief
text
state
width

```

## Label

## Button

按钮回调函数示例：

```
import tkinter as tk

app = tk.Tk()
labelExample = tk.Button(app, text="0")

def change_label_number():
    counter = int(str(labelExample['text']))
    counter += 1
    labelExample.config(text=str(counter))

buttonExample = tk.Button(app, text="Increase", width=30,
                          command=change_label_number)

buttonExample.pack()
labelExample.pack()
app.mainloop()

```

回调函数带参数，靠partial函数。下面的效果是每次点击一下加2 。

```
import tkinter as tk
from functools import  partial
app = tk.Tk()
labelExample = tk.Button(app, text="0")

def change_label_number(num):
    counter = int(str(labelExample['text']))
    counter += num
    labelExample.config(text=str(counter))

buttonExample = tk.Button(app, text="Increase", width=30,
                          command=partial(change_label_number, 2))

buttonExample.pack()
labelExample.pack()
app.mainloop()

```

## 布局

有三种布局：

pack、grid、place（固定位置布局）

## Entry 文本输入

## Combobox下来列表

## Radiobutton 单选

## Checkbutton 多选





# window

主窗口控件（window）是一切控件的基础，它好比是一台高速运转的机器，而其他控件则相当于这台机器上的部件，比如齿轮、链条、螺丝等等。

由此我们知道，主窗口是一切控件的基础，所有的控件的都需要通过主窗口来显示。

创建一个空白的窗口

```
# 导入tk
from tkinter import *
# 创建一个主窗口对象
window = Tk()
# 调用mainloop()显示主窗口
window.mainloop()
```

window的常用方法

```
title
resizable
geometry
quit
update
mainloop
iconbitmap
config
minsize
maxsize
attributes
state
withdraw
iconify
deiconify
winfo_screenwidth
winf_screenheight
protocol
```

# ttkbootstrap

https://blog.csdn.net/qq_59142194/article/details/123937365

# 参考资料

1、

http://c.biancheng.net/tkinter/the-first-tkinter.html