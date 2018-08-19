---
title: php之面向对象
date: 2018-08-18 18:53:22
tags:
	- php

---



构造函数

```
void __constructor($x, $y) {
  
}
```

析构函数

```
void __destruct(void) {
  
}
```

继承

```
class A extends B {
  
}
```

重写方法

```
不需要特别声明什么，直接定义同名函数就好了。
```

访问控制

```
public
private
protected
```

接口

```
interaface A {
  
}
```

类的常量

可以把类里面保持不变的内容定义为常量，定义和使用的时候，都可以不用美元符。

```
class A {
  const var1 = "const_var1";
  
}
```

抽象类

```
abstract class A {
  
}
```

static关键字

```

```

final关键字

```

```

调用父类构造方法

```
parent::__contruct();
```



# 参考资料

1、PHP 面向对象
http://www.runoob.com/php/php-oop.html