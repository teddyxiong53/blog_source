---
title: pyside（1）
date: 2023-05-28 11:00:11
tags:
	- python
---

--

pyqt的应用还是比wxpy更多。所以还是有必要研究一下pyside。

# pyqt和pyside区别

pyqt是第三方的，要钱的。

pyside是qt官方的，不要钱的。

二者的接口基本一样。

所以用pyside就可以了。

# pyside的版本区别

PySide是Qt的Python绑定，它有几个主要版本，主要包括：

### 1. PySide (PySide 1)
- **基于 Qt 4**。
- 初始发布于 2010 年。
- 功能较为基础，支持的模块和功能较少。

### 2. PySide2
- **基于 Qt 5**。
- 发布于 2018 年。
- 引入了许多新特性，如支持 Qt Quick、改进的信号与槽、以及对现代 C++ 的更好支持。
- 使用 `Qt for Python` 的命名。

### 3. PySide6
- **基于 Qt 6**。
- 发布于 2020 年。
- 进一步改进了性能和功能，支持最新的 Qt 特性。
- 适用于更现代的应用开发，提供了新的模块和 API。

### 版本选择建议
- **新项目**：建议使用 PySide6，因为它支持最新的 Qt 特性，并且有更好的性能和可维护性。
- **旧项目**：如果你有现有项目使用 PySide 或 PySide2，考虑升级到 PySide6，但需要评估兼容性。

如果你需要更详细的信息或比较特定版本的功能，请告诉我！

# 环境搭建

```
pip install PySide6
```

我总是安装不成功。

包在这里，

https://pypi.org/project/PySide6/

我看看通过源代码编译的方式来安装。

我本地已经是安装了qt6的环境的。

其实不用这么麻烦。我的qtcreator里默认就可以创建pyside6的项目的。

也是要安装pyside6。但是安装很顺利。

```
C:\Python39\python.exe -m pip install PySide6 --user
```



# macos安装pyside6

```
# 创建这个环境，python3.12之后，安装pip包都需要一个venv。我创建这个环境，专门用来跑pyside的程序。
python3.12 -m venv pyside6-venv
激活环境
然后pip install pyside6
```

```
Installing collected packages: shiboken6, PySide6-Essentials, PySide6-Addons, pyside6
```



# 资源

就看官网的教程就好了。

https://doc.qt.io/qtforpython-6/tutorials/basictutorial/widgets.html

# 官方例子

快速把官方的例子过一遍。

## HelloWorld

```
import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Hello World!")
label.show()
app.exec()
```

## 信号与槽

简单来说，就是event和handler。事件和对应的处理函数。

```
import  sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Slot

@Slot()
def say_hello():
    print('button click')

app = QApplication(sys.argv)
button = QPushButton('click me')
# 
button.clicked.connect(say_hello)
button.show()
app.exec()
```

## 对话框

```
import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    # Greets the user
    def greetings(self):
        print(f"Hello {self.edit.text()}")

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
```

## table显示数据

```
import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem

colors = [
    ('red', '#ff0000'),
    ('green', '#00ff00'),
    ('blue', '#0000ff')
]
app = QApplication()
table = QTableWidget()
table.setRowCount(len(colors))
table.setColumnCount(len(colors[0]) + 1)
table.setHorizontalHeaderLabels(["Name", "Hex Code", "Color"])

def get_rgb_from_hex(code):
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

for i, (name, code) in enumerate(colors):
    item_name = QTableWidgetItem(name)
    item_code = QTableWidgetItem(code)
    item_color = QTableWidgetItem()
    item_color.setBackground(get_rgb_from_hex(code))
    table.setItem(i, 0, item_name)
    table.setItem(i, 1, item_code)
    table.setItem(i, 2, item_color)

table.show()
sys.exit(app.exec())

```

## tree显示数据

```
import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
data = {"Project A": ["file_a.py", "file_a.txt", "something.xls"],
        "Project B": ["file_b.csv", "photo.jpg"],
        "Project C": []}

app = QApplication()
tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["Name", "Type"])

items = []
for key, values in data.items():
    item = QTreeWidgetItem([key])
    for value in values:
        ext = value.split(".")[-1].upper()
        child = QTreeWidgetItem([value, ext])
        item.addChild(child)
    items.append(item)

tree.insertTopLevelItems(0, items)

tree.show()
sys.exit(app.exec())


```

## 使用designer设计xml文件

有两种方式，一种是输出为py文件来使用，一种是直接使用ui文件。

# qt-material

https://github.com/UN-GCPDS/qt-material

# 官方文档

https://doc.qt.io/qtforpython-6/

Qt 提供了两种技术来构建用户界面：

Qt Widgets，一种自 Qt 诞生以来就存在的命令式编程和设计方法，使其成为 UI 应用稳定可靠的技术。

Qt Quick，一种声明式编程和设计方法，允许您通过描述简单元素来创建流畅的 UI。

两种技术都为您提供使用拖放工具创建界面的可能性。pyside6-designer 用于 Qt Widgets（在安装 pyside6 时包含），和 Qt Design Studio 用于 Qt Quick（在这里获取）。

 pyside6-project 工具，以了解如何自动创建项目而无需手动编写所有代码。

该工具包含几个子命令。使用以下命令并传递项目名称（目录）可以创建新项目：

- *new-ui 新界面*

  Creates a new QtWidgets project with a *Qt Widgets Designer*-based main window. 创建一个新的 QtWidgets 项目，具有基于 Qt Widgets Designer 的主窗口。

- *new-widget 新插件*

  Creates a new QtWidgets project with a main window. 创建一个新的 QtWidgets 项目，包含主窗口。

- *new-quick 新快速*

  Creates a new QtQuick project. 创建一个新的 QtQuick 项目。



对于使用 PySide6 的 widget 应用，您必须始终从 PySide6.QtWidgets 模块导入适当的类。

导入完成后，创建一个 QApplication 实例。

由于 Qt 可以从命令行接收参数，您可以将任何参数传递给 QApplication 对象。

通常，您不需要传递任何参数，因此可以保持原样，或者使用以下方法：

```
app = QApplication([])
```

创建应用对象后，我们创建了一个 QLabel 对象。QLabel 是一个可以呈现文本（简单或丰富，类似于 html）以及图片的控件：

```
# This HTML approach will be valid too!
label = QLabel("<font color=red size=40>Hello World!</font>")
```

QML 和 QWidget 的差异

- **声明性 vs. 命令式**：QML 是声明式的，强调结构和样式，而 QWidget 是命令式的，通常需要编写更多的代码来设置和管理控件。
- **界面流畅性**：QML 更适合现代、动态用户界面，支持动画和触摸事件。
- **性能**：对于图形密集型应用，QML 通常性能更好。

所有继承自 `QObject` 或其子类（如 `QWidget` ）的类都可以包含信号和槽。

当对象的状态以可能对其他对象感兴趣的方式改变时，信号由对象发出。

这是对象通信所做的一切。

它不知道或不关心是否有任何东西在接收它发出的信号。

这是真正的信息封装，确保对象可以作为软件组件使用。



槽可以用于接收信号，但它们也是正常的成员函数。

正如对象不知道是否有任何接收其信号一样，槽也不知道是否有任何信号连接到它。

**这确保了可以使用 Qt 创建真正独立的组件。**

你可以将任意多的信号连接到单个槽中，一个信号也可以连接到你需要的任意多的槽中。甚至有可能将一个信号直接连接到另一个信号上。（每当第一个信号发出时，第二个信号就会立即发出。）

Qt 的控件有很多预定义的信号和槽。

例如， `QAbstractButton` （Qt 中的按钮基类）有一个 `clicked()` 信号，

 `QLineEdit` （单行输入字段）有一个名为 `clear()` 的槽。

因此，可以通过在 `QLineEdit` 右侧放置一个 `QToolButton` 并将其 `clicked()` 信号连接到槽 `clear()` 来实现一个带有清除文本按钮的文本输入字段。

这是通过信号的 `connect()` 方法完成的：

```
button = QToolButton()
line_edit = QLineEdit()
button.clicked.connect(line_edit.clear)
```

`connect()` 返回一个 `QMetaObject.Connection` 对象，可以使用 `disconnect()` 方法断开连接。

信号也可以连接到自由函数：



我们建议使用 `@QtCore.Slot()` 标记器标记所有由信号连接使用的 方法。

不这样做会导致运行时开销，

因为在创建连接时方法会被添加到 `QMetaObject` 中。

这对于使用 QML 注册的 `QObject` 类尤其重要，缺少标记器可能会引入错误。

```
import sys
from PySide6.QtWidgets import  QApplication, QPushButton
from PySide6.QtCore import QObject, Signal, Slot

class Communicate(QObject):
    speak = Signal((int,), (str,))
    def __init__(self, parent=None):
        super().__init__(parent)
        self.speak[int].connect(self.say)
        self.speak[str].connect(self.say)

    @Slot(int)
    @Slot(str)
    def say(self, arg):
        if isinstance(arg, int):
            print('get int:', arg)
        elif isinstance(arg, str):
            print('get str:', arg)

app = QApplication(sys.argv)
someone = Communicate()
someone.speak.emit(10)
someone.speak[str].emit('hello')

```



```
pyside6-uic mainwindow.ui -o ui_mainwindow.py
```

我们将所有命令输出重定向到名为 `ui_mainwindow.py` 的文件中，该文件将直接导入：

```
from ui_mainwindow import Ui_MainWindow
```

```
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
```

`QUiLoader` 允许我们动态加载 ui 文件并立即使用它：

```
ui_file = QFile("mainwindow.ui")
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
window = loader.load(ui_file)
window.show()
```

# 使用 `.qrc` 文件（ `pyside6-rcc` ）

Qt 资源系统是一种机制，用于在应用程序中存储二进制文件。

文件将被嵌入到应用程序中，并可由 `QFile` 类和 `QIcon` 类、 `QPixmap` 类的构造函数访问，使用以 `:/` 开头的特殊文件名，通过提供文件名。

在运行任何命令之前，请将资源信息添加到 `.qrc` 文件中。在以下示例中，请注意资源是如何在 `icons.qrc` 中列出的。

```
<!DOCTYPE RCC><RCC version="1.0">
<qresource>
    <file>icons/play.png</file>
    <file>icons/pause.png</file>
    <file>icons/stop.png</file>
    <file>icons/previous.png</file>
    <file>icons/forward.png</file>
</qresource>
</RCC>
```

现在 `icons.qrc` 文件准备好了，使用 `pyside6-rcc` 工具生成包含资源二进制信息的 Python 类
为了做到这一点，我们需要运行：

```
pyside6-rcc icons.qrc -o rc_icons.py
```

使用生成的文件，请在主 Python 文件的顶部添加以下导入：

```
import rc_icons
```

# QSS样式

