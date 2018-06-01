---
title: Python之PIL使用
date: 2018-06-01 22:53:31
tags:
	- Python

---



最近写一个小工具，从一些图片里提取一些RGB值。用到了PIL这个库。

觉得这个库功能强大，使用简单。

所以现在把这个库系统学习一下。



PIL

Python Imaging Library。是Python平台事实上的图像处理标准库。



安装方法

```
sudo apt-get install python-imaging
```



对文件进行缩放。这里可以体现出Python的简洁。只需要几行代码就可以达到目的。

如果用C来做，就很麻烦。

```
#!/usr/bin/python 

from PIL import Image

im = Image.open("./HappyFish.jpg")
w,h = im.size
print w,h

im.thumbnail((w/2,h/2))
im.save("./thumb.jpg", 'jpeg')
```

模糊效果

```
#!/usr/bin/python 

from PIL import Image, ImageFilter

im = Image.open("./HappyFish.jpg")
w,h = im.size
im2 = im.filter(ImageFilter.BLUR)
im2.save('./HappyFish_blur.jpg', 'jpeg')
```



下面看一个很实用的用途。生成图片验证码。

```
#!/usr/bin/python 

from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random
#get random char
def rndChar():
	return chr(random.randint(65,90))
	
def rndColor():
	r = random.randint(64,255)
	g = random.randint(64,255)
	b = random.randint(64, 255)
	return (r,g,b)
	


def rndColor2():
	r = random.randint(32,127)
	g = random.randint(32,127)
	b = random.randint(32,127)
	return (r,g,b)
	
width = 240
height = 60

image = Image.new('RGB', (width, height),(255,255,255))
font = ImageFont.truetype('Ubuntu-B.ttf', 36)
draw = ImageDraw.Draw(image)

for x in range(width):
	for y in range(height):
		draw.point((x,y), fill=rndColor())
		
for t in range(4):
	draw.text((60*t+10, 10), rndChar(), font=font, fill=rndColor2())
	
image  = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')
```





# 参考资料

1、PIL

https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140767171357714f87a053a824ffd811d98a83b58ec13000