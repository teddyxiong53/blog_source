---
title: python之mixin模式
date: 2020-05-05 12:22:51
tags:
	- Python
---

python为什么要有mixin模式？

是因为python没有类似java的接口。而又要避免多重继承的问题。

java的接口实现方式：

```
public abstract class Vehicle {

};
public interface Flyable {
    public void fly();
}

public FlyableImpl implements Flyable {
    public void fly() {
        System.out.println("fly");
    }
}
public class Airplane extends Vehicle implements Flyable {
    private Flyable flyable;
    public Airplane() {
        flyable = new FlyableImpl();
    }
    public void fly() {
        flyable.fly();
    }
}
```

而用python来实现的这样：

```
class Vehicle(object):
    pass
class PlaneMixin(object):
    def fly(self):
        print("fly")

class Airplane(Vehicle, PlaneMixin):
    pass
```

**实际上还是一种多继承。名字里带mixin，只是为了表明，这个类只是给对方添加一些功能，而不是作为父类。**

功能类似java的接口。

实现mixin来做多继承的时候，需要非常小心：

1、首先是是表示一种功能。而不是一种物品。

2、必须功能单一。如果有多种功能，那么就做多个mixin类。

3、子类即使没有继承这个mixin类，也可以工作。只是缺失部分功能。





参考资料

1、关于Python的Mixin模式

<https://www.cnblogs.com/aademeng/articles/7262520.html>