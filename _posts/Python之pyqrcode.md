---
title: Python之pyqrcode
date: 2017-11-23 11:44:00
tags:
	- Python
	- 二维码

---



# 二维码

二维码简称QRCode，是Quick Response Code的缩写，学名为快速响应矩阵码。是二维条码的一种。

由日本的Denso Wave公司在1994年发明。



# 简单例子

```
import pyqrcode
import sys
url = pyqrcode.create('http://uca.edu')
url.svg(sys.stdout, scale=1)
url.svg('uca.svg', scale=4)
number = pyqrcode.create(123456789012345)
number.png('big-number.png')
```

从这个例子里，我们可以看到，二维码可以封装网址，可以封装数字。

可以生成svg文件（一种矢量图，可以用浏览器打开），可以生成普通的png文件。

还可以直接在命令行上把二维码打印出的。如下：

```
import pyqrcode
import sys
number = pyqrcode.create(123456789012345)
number.png('big-number.png')
print number.terminal(quiet_zone=1)
```

