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