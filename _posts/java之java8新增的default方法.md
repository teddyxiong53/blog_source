---
title: java之java8新增的default方法
date: 2017-12-28 11:09:08
tags:
	- java

---



看java8的源代码里，有这种代码：

```
default void forEach(Consumer<? super T> action) {
}
```

default怎么能够用在这个位置呢？是什么东西呢？

网上查了下，这个是java8新增的default方法。

用途是：在接口中添加新功能特性，而且还不影响接口的实现类。

举例说明如下：

```
public class MyClass implements InterfaceA {
	@override 
	public void saySomething() {
		
	}
}

interface InterfaceA {
	public void saySomething();
}

```

上面这些代码里，MyClass类实现 了InterfaceA的saySomething方法。

现在如果InterfaceA新增了一个sayHi 的方法，这么做的话，MyClass是不能通过编译的，因为按照以前的做法，MyClass必须实现sayHi方法才行。这个其实是很不方便的。

现在的解决办法就是default方法。

具体做法是这样：

```
interface InterfaceA {
	public void saySomething();
	default public void sayHi() {
		System.out.println("Hi");
	}
}
```

这样MyClass就不需要做任何的修改了。

当然MyClass也可以自己实现sayHi。如果没有实现，就用interfaceA的sayHi。



上面讨论的是只实现了一个interface的情况，如果一个类实现了多个interface，就有可能出现这种情况。

InterfaceA和InterfaceB都实现了default的sayHi方法。如果MyClass同时实现了这2个interface，那么就会出现变异错误。如果MyClass自己实现了sayHi方法，则不会报错。



