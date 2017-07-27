---
title: 树莓派之picamera
date: 2017-07-27 23:37:36
tags:

	- 树莓派

	- video

---

网上找到一个简单的代码段。但是这个对USB摄像头不能用。

```
#!/usr/bin/env python
import picamera
import time

with picamera.PiCamera() as camera:
	camera.resolution = (1024,576)
	camera.start_preview()
	time.sleep(2)
	camera.capture("1.jpg")
```

又找到一段新的代码：

```
#!/usr/bin/env python
import pygame
import pygame.camera
from pygame.locals import *

# initialize
pygame.init()
pygame.camera.init()

# capture a image
camera = pygame.camera.Camera("/dev/video0", (640, 480))
camera.start()
image = camera.get_image()
pygame.image.save(image, "image.jpg")
camera.stop()
```

这个就需要安装pygame。安装提示sdl-config没有。就安装sdl的东西。

```
wget http://www.libsdl.org/release/SDL-1.2.14.tar.gz
tar -xzvf SDL-1.2.14.tar.gz
cd SDL-1.2.14
./configure 
sudo make all
sudo make install
```

做完上面的步骤，现在再安装pygame，如下：

```
 Hunting dependencies...
    SDL     : found 1.2.14
    FONT    : not found
    IMAGE   : not found
    MIXER   : not found
    PNG     : not found
    JPEG    : found
    SCRAP   : not found
    PORTMIDI: not found
    PORTTIME: not found
    FREETYPE: found 2.6.0
    Missing dependencies
```

谷歌搜索一下，想办法把这些依赖给安装上。

```
 sudo apt-get update && apt-get upgrade -y  
 sudo apt-get build-dep python-pygame
```

现在还是好了一点，但是还不行：

```
    Hunting dependencies...
    SDL     : found 1.2.14
    FONT    : not found
    IMAGE   : not found
    MIXER   : not found
    PNG     : not found
    JPEG    : found
    SCRAP   : not found
    PORTMIDI: found
    PORTTIME: found
    FREETYPE: found 2.6.0
    Missing dependencies
```











