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



# tkinter介绍

Tkinter是Python中内置的图形用户界面（GUI）库，用于创建桌面应用程序的用户界面。

它基于Tk GUI工具包，是Tkinter的Python接口。

Tkinter提供了一组用于创建窗口、标签、按钮、文本框等GUI组件的工具，

使得开发者能够创建直观且交互性强的用户界面。

以下是一些Tkinter的主要特点和概念：

1. **跨平台性：** Tkinter是Python标准库的一部分，因此可以在几乎所有支持Python的平台上运行，包括Windows、Linux和macOS。

2. **组件：** Tkinter提供了各种GUI组件，如窗口、标签、按钮、文本框、滚动条等，可以通过这些组件来构建用户界面。

3. **事件驱动：** Tkinter是事件驱动的，即用户与界面交互时，程序会响应相应的事件，例如按钮点击、鼠标移动等。

4. **布局管理：** Tkinter提供了不同的布局管理器，如`pack`、`grid`和`place`，以帮助开发者更灵活地安排界面上的组件。

5. **绑定与回调：** 使用Tkinter，您可以将事件（如按钮点击）与特定的函数关联起来，这样当事件发生时，相关的函数将被调用，实现特定的功能。

6. **标准对话框：** Tkinter提供了一些标准对话框，如文件选择对话框、消息框等，方便开发者处理常见的交互。

以下是一个简单的Tkinter示例，展示了如何创建一个简单的窗口：

```python
import tkinter as tk

# 创建主窗口
root = tk.Tk()

# 创建标签
label = tk.Label(root, text="Hello, Tkinter!")

# 将标签放置在窗口中
label.pack()

# 启动事件循环
root.mainloop()
```

这只是一个简单的入门示例，Tkinter还有很多其他功能和选项，可以根据项目的需要进行更复杂的界面设计。

## Tk GUI工具包

Tk是一个用于创建图形用户界面（GUI）的工具包，最初是为Tcl编程语言设计的。

Tk提供了一组用于构建窗口、按钮、标签等GUI组件的工具，

使得开发者能够创建直观且交互性强的用户界面。Tk的Python接口就是Tkinter。

以下是Tk工具包的一些关键特点：

1. **跨平台性：** Tkinter是Tk的Python接口，而Tk本身是一个独立的工具包，可以在多个平台上运行，包括Windows、Linux和macOS。

2. **简单易学：** Tkinter提供了一个相对简单的API，容易学习和使用。这使得它成为Python初学者和快速原型开发的理想选择。

3. **组件丰富：** Tkinter提供了各种常用的GUI组件，如窗口、标签、按钮、文本框、滑块等。这些组件可以通过简单的调用进行创建和配置。

4. **布局管理：** Tkinter支持多种布局管理器，例如`pack`、`grid`和`place`，允许开发者以不同的方式安排和组织界面元素。

5. **事件处理：** Tkinter是事件驱动的，可以通过绑定函数到特定的事件来响应用户的交互。例如，单击按钮时触发的事件可以与相应的函数关联起来。

6. **可扩展性：** Tkinter可以与其他Python库和工具集成，使得开发者可以利用Python丰富的生态系统来增强应用程序的功能。

在Python中，Tkinter是使用Tk工具包创建GUI的主要方式。虽然Tkinter在功能上较为基础，但对于许多小到中型的GUI应用程序，它是一个简单而有效的选择。如果需要更复杂的GUI功能，也可以考虑使用其他GUI库，如PyQt、wxPython等。

# tkinter程序的基本结构

Tkinter程序的基本结构通常包括创建主窗口、定义和布局GUI组件、设置事件处理函数以及启动主循环。以下是一个简单的Tkinter程序的基本结构示例：

```python
import tkinter as tk

# 创建主窗口
root = tk.Tk()

# 定义函数（可用于事件处理）
def button_click():
    label.config(text="Button Clicked!")

# 创建组件
label = tk.Label(root, text="Hello, Tkinter!")
button = tk.Button(root, text="Click Me", command=button_click)

# 布局管理
label.pack(pady=10)
button.pack(pady=10)

# 启动事件循环
root.mainloop()
```

这个简单的程序包括以下几个关键步骤：

1. **导入Tkinter模块：** 使用`import tkinter as tk`语句导入Tkinter模块，通常将其重命名为`tk`以简化代码。

2. **创建主窗口：** 使用`tk.Tk()`创建一个主窗口对象，这是GUI应用程序的顶层窗口。

3. **定义函数：** 可以定义与按钮点击等事件相关的函数，这些函数将在事件发生时被调用。

4. **创建组件：** 使用Tkinter提供的组件类（例如`Label`和`Button`）创建GUI组件。

5. **布局管理：** 使用布局管理器（例如`pack`、`grid`、`place`）将组件放置在主窗口中，以便在界面上进行适当的排列。

6. **设置事件处理：** 将事件与相应的函数关联，例如将按钮点击事件与`button_click`函数关联。

7. **启动主循环：** 使用`root.mainloop()`启动Tkinter的主事件循环，使应用程序保持运行，等待用户交互。

这只是一个简单的例子，Tkinter还提供了许多其他组件和选项，以及更复杂的布局和功能。您可以根据项目的需求扩展和定制这个基本结构。

# tkinter的布局管理逻辑

Tkinter提供了三种主要的布局管理器：`pack`、`grid`和`place`。这些布局管理器允许您灵活地安排和定位GUI组件。以下是每个布局管理器的基本逻辑：

1. **`pack` 布局管理器：**
   
   - `pack` 布局管理器将组件按照添加的顺序一个接一个地放置在父容器中。
   - 使用 `side` 参数指定组件相对于父容器的位置，例如 `side='top'` 表示在顶部，`side='left'` 表示在左侧等。
- 可以使用 `fill` 参数控制组件在其可用空间内的填充方式，`fill='both'` 表示填充水平和垂直方向。
   
   示例：
   ```python
   label.pack(side='top', fill='both', pady=10)
```
   
2. **`grid` 布局管理器：**
   - `grid` 布局管理器通过指定行和列的索引来放置组件。
   - 使用 `row` 和 `column` 参数指定组件所在的行和列，可以使用 `rowspan` 和 `columnspan` 来指定组件跨越的行数和列数。
   - 可以使用 `sticky` 参数来指定组件在其格内的对齐方式。

   示例：
   ```python
   button.grid(row=0, column=1, sticky='e', padx=10, pady=10)
   ```

3. **`place` 布局管理器：**
   - `place` 布局管理器允许您以绝对坐标的方式放置组件。
   - 使用 `x` 和 `y` 参数指定组件左上角的坐标，以像素为单位。
   - 可以使用 `relx` 和 `rely` 参数以相对于父容器的比例来指定组件的位置。

   示例：
   ```python
   entry.place(x=50, y=20)
   ```

在实际应用中，通常会根据布局的需求选择适当的管理器。有时，也可以混合使用这些布局管理器，以实现更复杂的界面布局。布局的选择通常取决于个人偏好、项目需求以及开发者对每个管理器的熟悉程度。

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

# tkinter缺失哪些高级功能

尽管Tkinter是Python的标准GUI库，但在某些高级功能方面相对较简单，缺少一些现代GUI框架所提供的一些功能。以下是Tkinter相对较简单的一些方面以及缺失的一些高级功能：

1. **外观和主题：** Tkinter的外观和主题相对较为基础，用户定制化的选项有限。一些现代GUI框架提供更灵活的外观定制和主题支持。

2. **现代控件：** Tkinter的控件集合相对有限，缺少一些现代GUI框架提供的一些复杂和高级的控件，如树状列表、表格、富文本编辑器等。

3. **绑定到数据模型：** 一些现代GUI框架提供了更强大的数据绑定机制，可以轻松地将界面控件与数据模型同步。在Tkinter中，这通常需要手动编写代码来处理数据更新和界面更新之间的关系。

4. **MVVM（Model-View-ViewModel）架构：** Tkinter缺少对MVVM架构的内建支持，这是一种在许多现代GUI框架中广泛使用的设计模式，有助于分离界面逻辑和业务逻辑。

5. **动画和过渡效果：** Tkinter在处理动画和过渡效果时相对简单。一些现代GUI框架提供了更丰富的动画支持，允许开发者创建更吸引人的用户界面。

6. **复杂布局：** 尽管Tkinter提供了几种布局管理器，但在处理复杂的自定义布局时，可能需要编写更多的代码。一些现代GUI框架提供更灵活的布局选项和工具。

尽管Tkinter可能缺少一些高级功能，但它在编写简单到中等复杂度的GUI应用程序时仍然是一个强大而方便的工具。对于更复杂的需求，开发者可能需要考虑使用其他GUI框架，如PyQt、wxPython等，这些框架提供了更多现代GUI应用程序开发所需的功能。

# 参考资料

1、

http://c.biancheng.net/tkinter/the-first-tkinter.html