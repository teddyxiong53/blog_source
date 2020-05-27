---
title: cpp之操作符重载
date: 2018-11-22 17:23:19
tags:
	- cpp

---



看看一个简单的等于和不等于的重载。

```
bool DeviceInfo::operator==(const DeviceInfo& rhs) {
    if (getClientId() != rhs.getClientId()) {
        return false;
    }
    if (getProductId() != rhs.getProductId()) {
        return false;
    }
    if (getDeviceSerialNumber() != rhs.getDeviceSerialNumber()) {
        return false;
    }

    return true;
}

bool DeviceInfo::operator!=(const DeviceInfo& rhs) {
    return !(*this == rhs);
}
```

有这么几点是我之前没有认识到的。

1、不等于是对等于的调用。只是把结果取反一下而已。

2、要用对象来调用，所以this是一个指针，要进行指针取值操作。



# new操作符的重载

```
A a = new A;
```

上面这一行语句，实际的执行步骤有：

1、分配内存。

2、调用A()构造函数。

分配内存的操作是靠operator new(size_t)来完成的。

类A可以选择自己是否对new这个操作符进行重载。

如果要重载，这样写：

```
void* operator new(size_t size) {
    //...
}
```

不过一般我们都是不重载的，那么就是调用全局的new。

```
::operator new(size_t)
```

全局的new，由C++运行时默认提供。



c++里的new有两种，一个是关键字new，一个是操作符new。

关键字new的行为就是 ：先调用操作符new分配内存，然后调用构造函数初始化对象。

关键字new不存在重载的概念。



在c++里，类的对象有两种建立方式。

1、静态方式。例如A a。

2、动态方式。A a = new A

可以通过一些方式，来限制只能建立静态的对象或者动态的对象。

要让类只能建立动态对象，可以通过把析构函数设置为protected来做。

因为栈上的对象，出了作用范围就要自动调用析构函数。但是我们把析构函数没有对外暴露。这样编译器就会报错的。

但是我们的动态对象，也没法析构了。这就需要另外定义一个destroy函数来帮助我们进行析构操作。

但是new来产生对象，却用destroy来释放对象，挺奇怪的。

我们可以做一下对称封装，如下。

```
class A {
protected:
	A();
	~A();
public:
	static A* create() {
        return new A();
	}
	void destroy() {
        delete this;
	}
	
};
```

如果要限制为只允许在栈上建立对象呢？

重载操作符new为私有的就可以了。

重载了操作符new，就需要同时把delete也重载了。

```
class A{
private:
	void* operator new(size_t size) {}
	void operator delete(void *ptr){}
public:
	A();
	~A();
};
```



参考资料

1、C++ 内存分配(new，operator new)详解

<https://www.cnblogs.com/raichen/p/5808766.html>