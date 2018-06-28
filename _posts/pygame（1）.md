---
title: pygame（1）
date: 2018-06-28 20:32:20
tags:
	- pygame

---



pygame在Python3里跑不起来。

所以还是在Python2下面做。

先不管去管概念。我们先看一个例子。

```
import pygame
import sys
from pygame.locals import *
white = 255,255,255
blue = 0,0,200

pygame.init()
screen = pygame.display.set_mode((600,500))

myfont = pygame.font.Font(None, 60)

textImage = myfont.render('hello pygame', True, white)
while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    screen.fill(blue)
    screen.blit(textImage, (100,100))
    pygame.display.update()
```



1.3.2版本，在2018年4月13日发布，支持了Python3.7 。



官方文档

https://www.pygame.org/docs/

pygame是一个python库，基于SDL。

用来做游戏等多媒体应用的。

高度可移植。

官方承认并不是最好的，甚至不是排名靠前的，只是可用的状态。

pygame里把colour都写成color的。

pygame开始于2000年的夏天。

SDL是一个跟DirectX一个类型的东西。

作者写这个项目，就是想要把Python跟SDL结合起来。

他发现已经有个小项目在做这个事情了，就是PySDL。但是这个项目不久就夭折了。

作者就下定决定开始做pygame。

项目在2000年的十月正式开始。6个月以后，pygame1.0发布。

作者写了一个简单的演示程序，就是一个跳跳球的动画示例。

```
import pygame
import sys

size = width,height = 320,240
speed = [2,2]
black = 0,0,0
screen = pygame.display.set_mode(size)

ball = pygame.image.load('ball.bmp')
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]

    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
```

Python适合用来写游戏吗？

这个取决于游戏的类型。

在过去的这些年，游戏开发有一些有意思的发展趋势。就是往更高级的语言迁移。

一个游戏往往分为两部分。

1、游戏引擎。这个部分是越快越好。

2、游戏逻辑。

在2001年，《黑暗之刃》这块大型游戏，就是用Python写的游戏逻辑。

2001年三月，pygame作者发布了自己写的一个游戏，《SolarWolf》。



pygame的模块有：

1、cdrom。

2、cursors。

3、display。

4、draw。

5、event。

6、font。

7、image。

8、joystick。

9、key。

10、mouse。

11、sndarray。

12、surfarray。

13、time。

14、transform。

# import和初始化

pygame是把一些模块打包成了一个package。

一些模式是用C写的，一些是用Python写的。

这里有不少的例子。

C:\Python27\Lib\site-packages\pygame\examples



这里有个很好的集合。

https://github.com/ntasfi/PyGame-Learning-Environment

一个教程

https://github.com/kidscancode/pygame_tutorials

http://kidscancode.org/lessons/ 这个和上面教程配对的。



# 参考资料

1、Python游戏编程之旅（1）：初识pygame

http://python.jobbole.com/85785/