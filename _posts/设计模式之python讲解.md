---
title: 设计模式之python讲解
date: 2019-10-29 15:38:49
tags:
	- 设计模式

---

1

我现在用python来重新梳理软件知识点。

python比较简洁，让描述可以专注问题本身。

设计模式分为三大类：

```
创建型
	6种。
	3个工厂：简单工厂、工厂方法、抽象工厂。
	builder模式、原型模式、单例模式。
结构型
	7种。
	适配器
	代理
	装饰器
	桥
	组合
	外观
	享元
行为型
	11种。
	观察者。典型的订阅发布。
	状态模式。
	策略模式。
	责任链模式。
	命令模式。
	访问者模式。
	调停者模式。
	备忘录模式。
	迭代器模式。
	监视器模式。
	目标模式。
```



# 简单工厂

```
class Shape(object):
    def draw(self):
        raise NotImplementedError

class Circle(Shape):
    def draw(self):
        print("draw circle")

class Rectangle(Shape):
    def draw(self):
        print("draw rectangle")

class ShapeFactory(object):
    def create(self, shape):
        if shape == 'Circle':
            return Circle()
        elif shape == 'Rectangle':
            return Rectangle()
        else:
            return None

fac = ShapeFactory()
o1 = fac.create('Circle')
o1.draw()
```

简单工厂其实不算GoF总结的23中设计模式之一。

优点：

客户端不需要修改代码。

缺点：

需要增加新的类的时候，要改动工厂类，违反了开闭原则。

# 工厂方法模式

跟简单工厂的区别是，工厂方法模式是每一种产品对应一个工厂。

```
class ShapeFactory(object):
    def getShape(self):
        return self.shape_name

class Circle(ShapeFactory):
    def __init__(self):
        self.shape_name = "Circle"
    def draw(self):
        print('draw circle')

class Rectangle(ShapeFactory):
    def __init__(self):
        self.shape_name = 'Rectangle'

    def draw(self):
        print("draw rectangle")

class ShapeInterfaceFactory(object):
    def create(self):
        raise NotImplementedError

class ShapeCircle(ShapeInterfaceFactory):
    def create(self):
        return Circle()

class ShapeRectangle(ShapeInterfaceFactory):
    def create(self):
        return Rectangle()

shape_interface = ShapeCircle()
o1 = shape_interface.create()
print(o1.getShape())
o1.draw()
```

# 抽象工厂模式

每一种模式都是针对一种特定问题的解决方案。

抽象工厂模式跟工厂方法模式的区别是：

工厂方法模式针对的是一个产品等级。

抽象工厂模式需要面对多个产品等级。

在学习抽象工厂模式之前，应该明白2个重要的概念：产品族和产品等级。

AMD的主板、cpu、芯片组属于AMD产品族。

Intel的主板、cpu、芯片组属于Intel的产品族。

而主板、cpu、芯片组分别属于3个产品等级。





参考资料

1、Python之23种设计模式

https://blog.csdn.net/burgess_zheng/article/details/86762248