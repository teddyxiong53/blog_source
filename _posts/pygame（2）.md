---
title: pygame（2）
date: 2018-06-29 23:26:02
tags:
	- pygame

---



现在我们做一个太空射击游戏。

教程地址在这里。

http://kidscancode.org/lessons/

我们在上一篇文章的模板的基础进行修改。

1、游戏的名字改为shmup。是Shoot Them Up的缩写。是一个类型的游戏的统称。

2、FPS改为60，

3、窗口尺寸改为480宽，600高。

重点是加入按键的控制。

我们是在Player里的update方法里加这些代码。

```
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx += -5
        if keystate[pygame.K_RIGHT]:
            self.speedx += 5

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.speedx
```



# 加入敌机

我们称之为Mob。这个也是游戏的术语。

https://en.wikipedia.org/wiki/Mob_(gaming)

```
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,8)
            
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
```

现在可以看到基本效果。但是现在敌机还是只能沿着Y轴移动，我们在X轴上也要加上随机速度。



# 碰撞检测和子弹



# 加入图片

这位画家，Kenny，画了不少的画。

http://opengameart.org/content/space-shooter-redux

我们就下载这个图片包。

1、替换背景图片。

```
background = pygame.image.load(os.path.join(img_folder, 'purple.png')).convert()
background_rect = background.get_rect()

在循环里：
#render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
```

2、替换组件的图片。

Player，Mob，Bullet的都要替换。

这里就涉及到一个问题，就是图片的尺寸，跟我们程序里的尺寸对不上。

怎么处理？两种方法：

1、把图片资源修改为跟程序要求的一样。

2、在代码里进行缩放。

我们现在用第二种方式。

```
self.image = pygame.transform.scale(player_img, (50, 38))
```

# 改进碰撞检测

我们现在的图片都不是规则形状，而碰撞检测是按矩形检测的，所以就会出现，明明看起来没有碰到，实际上已经产生了碰撞时间。这个肯定会影响游戏体验的 。

这种基于矩形的碰撞检测是简单的方式。叫做AABB。Axis-Align Bounding Box。

可以改成圆形检测。

只修改Player和Mob的。

```
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
```

对应代码：https://github.com/teddyxiong53/Python/pygame/shmup/v5

# 加入动画

现在所有的敌机都是一样的，看起来没劲。

我们要达到把敌机的大小随机产生，而且会旋转。

http://kidscancode.org/blog/2016/08/pygame_shmup_part_6/



# 显示分数



# 声音和音乐



# 加入血量值

现在Player是一碰就死，这样不好，应该加入血量。



# 爆炸效果



# Player爆炸



# Player战斗力增强

Player应该可以获得道具，可以加强自身的战斗力。



# GameOver界面

