---
title: tkinter（1）
date: 2023-01-02 10:20:30
tags:
	- python
---

--

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

# window

主窗口控件（window）是一切控件的基础，它好比是一台高速运转的机器，而其他控件则相当于这台机器上的部件，比如齿轮、链条、螺丝等等。由此我们知道，主窗口是一切控件的基础，所有的控件的都需要通过主窗口来显示。

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



# 参考资料

1、

http://c.biancheng.net/tkinter/the-first-tkinter.html