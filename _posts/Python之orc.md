---
title: Python之orc
date: 2018-06-18 22:17:08
tags:
	- Python

---



现在有个需求，需要从一些图片里提取出文字信息。

1、安装

```
pip install pytesseract
```

这个需要依赖tesseract包。

```
sudo apt-get install tesseract-ocr
```



```
#!/usr/bin/python

import pytesseract
from PIL import Image

def main():
	image = Image.open('1.jpg')
	text = pytesseract.image_to_string(image)
	print text
	
if __name__ == '__main__':
	main()
```

这个处理很简单的图片是可以的。

弄成灰度图的。



```
#!/usr/bin/python

import pytesseract
from PIL import Image

def get_bin_table(threshold = 230):
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)
	return table
	
def main():
	image = Image.open('1.jpg')
	imgry = image.convert('L')
	imgry.save('2.jpg', 'JPEG')
	table = get_bin_table()
	out = imgry.point(table, '1')
	text = pytesseract.image_to_string(out, config='digits')
	fil = filter(str.isdigit, text)
	new_text = ''
	for i in fil:
		print i
	
if __name__ == '__main__':
	main()
	
```



https://www.jianshu.com/p/365f91aea667

我使用的 Python 版本是 3.6， 而标准库 PIL 不支持 3.x。所以需要使用 Pillow 来替代。Pillow 是专门兼容 3.x 版本的 PIL 的分支。使用 pip 包管理工具安装 Pillow 是最方便快捷的。



这个对于我的情况，识别太差了，根本识别不出来。所以希望借助网络上的看看。

https://ai.baidu.com/docs#/ImageClassify-Python-SDK/top

看看百度的。



训练。

https://www.cnblogs.com/cnlian/p/5765871.html

pytorch

https://blog.csdn.net/sunqiande88/article/details/80089941



在线的ocr识别。不太好。

http://www.ocrmaker.com/

安卓实现扫一扫识别。

https://juejin.im/entry/59b89ffd6fb9a00a4f1b0a91



腾讯的识别。表现比百度的好。

https://ai.qq.com/product/ocr.shtml#handwrite

# 参考资料

1、

http://www.inimei.cn/archives/297.html