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



http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/

这个系列教程写得挺好的。

game loop

每个游戏的核心都是一个循环。叫做game loop。

每一次循环就是一帧，frame。

每一次循环，可以做的事情有：

1、处理输入。

2、更新数据。

3、渲染。

另外，还有一个重要的因素，就是clock。



我们先写一个pygame的模板。

1、引入相关的模块。定义基础变量。

```
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30
```

2、打开游戏窗口。

```
pygame.init()
pygame.mixer.init() #for sound
screen = pygame.display.setmode((WIDTH,HEIGHT))
pygame.display.set_caption("mygame")
clock = pygame.time.Clock()
```

3、创建循环。

```
running = True
while running:
    #process input
    #update
    #render
```

4、我们定义一些有用的颜色。

```
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
在while循环里。
    #render
    screen.fill(BLACK)
    pygame.display.flip()
```

pygame.display.flip()则是由于双缓冲的原因，需要将整个display的surface对象更新到屏幕上去。所以，循环的最后一般都是调用flip，如果你在flip之后做处理，就没有效果。

现在我们的代码可以运行出来一个窗口了。

5、加入事件处理。

因为当前不能直接关闭窗口。是因为没有加入事件处理。

```
    #process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
```

6、控制帧率。

```
在循环里，
clock.tick(FPS)
```

7、其他。

现在我们在循环体的外面加一行：

```
pygame.quit()
做退出时的处理。
```

完整的程序是：

```
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
pygame.mixer.init() #for sound
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("mygame")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    #process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update
    
    #render
    screen.fill(BLACK)
    pygame.display.flip()

pygame.quit()
```

上面的步骤看起来很简单。

我们继续。

这里引入一个术语，sprite。我们就不翻译了。大概的含义是精灵的意思。

表示的是屏幕上任何能够移动的物体。

我们上面的模板里，update这个部分还是空的。

一个游戏里的sprite可能很多，pygame给我们提供了管理工具。

```
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
```

```
    #update
    all_sprites.update()
    #render
    screen.fill(BLACK)
    all_sprites.draw(screen)
```

现在我们来创建我们的第一个sprite。

```
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
```

然后添加：

```
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
```

现在运行，得到的效果，就是黑色屏幕里中间有一个绿色的方块。

现在我们要让这个方块动起来。

我们在循环里的update部分，调用了：

```
all_sprites.update()
```

我们需要让Player里，定义一个update方法，这样就会自动被调用到的。

```
def update(self):
        self.rect.x += 5
```

再运行，看到的效果就是绿色方块移动到最右边消失了。

我们希望这个方块再从左边出来。

```
def update(self):
        self.rect.x += 5
        if self.rect.right > WIDTH:
            self.rect.right = 0
```

接下来，我们要加入更多的sprite。

我们现在只是简单的方块，如果要得到漂亮的图片素材，你怎么办？

1、自己画。

2、网上找。

http://opengameart.org/

这个网站提供了免费的资源。没有版权风险的。

我们就下载这个包的。大概6M。图片很实用。

https://opengameart.org/content/platformer-art-complete-pack-often-updated

我们看看如何管理我们的游戏资源。

```
import pygame
import random
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()

```

上面的convert函数，是为了让画图更加快。

然后，我们修改Player里的；

```
def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
```

现在我们允许，就可以看到一个小人在屏幕上跑动了。

但是现在还是有问题，就是图片在一个非黑色的背景上，就可以看到矩形的黑色部分。

我们可以这样解决。

```
self.image = player_img
self.image.set_colorkey(BLACK) #加上这一行。
self.rect = self.image.get_rect()
```

到这里，我们可以算是完成了一个简单的游戏雏形了。

完整的代码是这样。总共50行代码左右。

```
import pygame
import random
import os


WIDTH = 360
HEIGHT = 480
FPS = 30

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
    def update(self):
        self.rect.x += 5
        if self.rect.right > WIDTH:
            self.rect.right = 0
pygame.init()
pygame.mixer.init() #for sound
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("mygame")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True



while running:
    clock.tick(FPS)
    #process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update
    all_sprites.update()
    #render
    screen.fill(BLUE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
```

# pygame绘制太阳系运行动画

```
import pygame
import math

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸和标题
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("太阳系运动动画")

# 定义颜色
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (127, 127, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置时钟对象
clock = pygame.time.Clock()

# 行星类
class Planet:
    def __init__(self, name, radius, distance, speed, color):
        self.name = name
        self.radius = radius
        self.distance = distance
        self.speed = speed
        self.color = color
        self.angle = 0

    def update(self):
        self.angle += self.speed

    def draw(self):
        x = width // 2 + math.cos(math.radians(self.angle)) * self.distance
        y = height // 2 + math.sin(math.radians(self.angle)) * self.distance
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)

# 创建行星对象
sun = Planet("Sun", 50, 0, 0, YELLOW)
mercury = Planet("Mercury", 10, 100, 1, GRAY)
venus = Planet("Venus", 15, 150, 0.8, RED)
earth = Planet("Earth", 20, 200, 0.6, BLUE)
mars = Planet("Mars", 15, 250, 0.4, RED)

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏
    screen.fill(BLACK)

    # 绘制行星
    sun.draw()
    mercury.update()
    mercury.draw()
    venus.update()
    venus.draw()
    earth.update()
    earth.draw()
    mars.update()
    mars.draw()

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出程序
pygame.quit()

```

# pygame除了游戏之外，还有哪些妙用

除了游戏开发之外，Pygame 还可以应用于其他领域，下面是一些 Pygame 的其他妙用示例：

1. 可视化工具：Pygame 提供了绘图、图像处理和交互功能，可以用于创建各种可视化工具，例如数据可视化、图形绘制、图像处理等。

2. 交互式图形界面：借助 Pygame 的绘图和事件处理功能，可以创建交互式的图形用户界面（GUI），用于构建应用程序、工具或演示。

3. 模拟和仿真：Pygame 的绘图和物理引擎功能可用于创建各种模拟和仿真场景，例如物理模拟、粒子系统、汽车驾驶模拟等。

4. 教育和学习工具：Pygame 可以用于开发教育工具和学习资源，例如交互式数学教学、物理实验模拟、编程学习等。

5. 图像处理和计算机视觉：Pygame 提供了处理图像和视频的功能，可以用于计算机视觉应用，例如图像识别、目标跟踪、图像处理等。

6. 艺术和创意项目：Pygame 的绘图和动画功能可以用于艺术和创意项目，例如生成艺术图像、交互式艺术展示、音乐可视化等。

7. 物理实验和控制：结合外部硬件接口（如 Arduino），Pygame 可以用于物理实验和控制项目，例如机器人控制、传感器数据采集等。

这些只是一些示例，Pygame 的灵活性和可扩展性使其适用于许多其他领域和项目。您可以根据自己的需求和创意，发挥 Pygame 的优势，应用于各种有趣和实用的场景。

# 基于pygame的gui演示

下面是一个简单的基于 Pygame 的 GUI 演示示例，其中使用按钮、文本框和标签等元素：

```python
import pygame
import pygame_gui

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸和标题
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GUI 演示")

# 设置 GUI 管理器
manager = pygame_gui.UIManager((width, height))

# 创建按钮
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 100), (100, 50)),
                                     text="点击我",
                                     manager=manager)

# 创建文本框
text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 200), (300, 30)),
                                               manager=manager)

# 创建标签
label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 250), (300, 30)),
                                    text="",
                                    manager=manager)

# 主循环
running = True
while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 处理 GUI 事件
        manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    label.set_text("按钮被点击了")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                label.set_text("输入的文本是：" + text_box.text)

    # 更新 GUI
    manager.update(time_delta)

    # 清屏
    screen.fill((255, 255, 255))

    # 绘制 GUI
    manager.draw_ui(screen)

    # 刷新屏幕
    pygame.display.flip()

# 退出程序
pygame.quit()
```

这个示例使用 Pygame 和 Pygame GUI 库来创建一个简单的 GUI 界面。其中包含一个按钮、一个文本框和一个标签。点击按钮会在标签中显示相应的消息，同时在按下回车键后会将文本框中的内容显示在标签中。

您可以根据自己的需求和创意，添加更多的 GUI 元素、布局和交互功能，以创建更复杂和丰富的 GUI 应用程序。

# pygame 物理模拟仿真示例

下面是一个使用 Pygame 实现简单物理模拟仿真的示例，其中模拟了一个小球的自由落体运动：

```python
import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸和标题
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("物理模拟仿真")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 小球类
class Ball:
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y
        self.velocity = 0

    def update(self):
        # 更新小球的位置和速度
        self.y += self.velocity
        self.velocity += 0.1

        # 检查小球是否碰到地面
        if self.y + self.radius >= height:
            self.y = height - self.radius
            self.velocity *= -0.9

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# 创建小球对象
ball = Ball(30, width // 2, 0)

# 设置时钟对象
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏
    screen.fill(WHITE)

    # 更新和绘制小球
    ball.update()
    ball.draw()

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出程序
pygame.quit()
```

在这个示例中，一个小球从顶部开始自由落体运动，通过模拟重力和碰撞来更新小球的位置和速度。小球在碰到地面时会有一定的反弹，并逐渐减缓运动。

您可以根据需要修改小球的初始位置、速度和半径等参数，以及调整重力和碰撞的模拟规则，来实现不同的物理仿真效果。例如，可以模拟更复杂的碰撞、添加其他物体等。

# 参考资料

1、Python游戏编程之旅（1）：初识pygame

http://python.jobbole.com/85785/

2、pygame中几个重要模块

https://blog.csdn.net/qq_27717921/article/details/53231762