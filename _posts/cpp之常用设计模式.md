---
title: cpp之常用设计模式
date: 2018-05-12 20:48:27
tags:
	- cpp
typora-root-url: ..\
---



# 单例模式

单例模式适用的场景：

1、工具性质的类，本身不用存储太多跟自身有个的数据。

2、所以没有必要每次都去new，这样开销太大。

3、所以我们只需要一个实例就好了。

4、但是，如果用全局变量，这样会影响封装性。



实现单例模式的代码技巧：

1、把构造函数设为private的，这样外部就没法new了。



单例模式的分类：

1、饿汉单例。java这样的纯面向对象的才能实现。就是在静态区初始化好。getInstance的时候直接返回。

2、懒汉单例。在getInstance里构造。



代码原型：

```
Singleton * getInstance() {
	if(instance == NULL) {
		lock();
		if(instance() == NULL) {
			intance = new Singleton();
		}
		unlock();
	}
	return instance;
}
```

这样的写法，保证了在多线程的情况下也能正常工作。



# 观察者模式 

我看到很多dueros里很多应用了观察者模式。

什么是观察者模式？

定义对象之间的一对多的依赖关系。

当一个对象发生变化的时候，所有依赖它的对象都会得到通知并且被自动更新。

这个就是一种发布订阅模式。

大家都盯着公布栏的，一旦有通知贴上去，观察者就知道了。

具体的uml图是这样的。

![](/images/cpp之常用设计模式-观察者模式.png)

示例代码。

```
#include <iostream>
#include <list>
using namespace std;

class Observer {
public:
	virtual void update(int) = 0;
};

class Subject {
public:
	virtual void attach(Observer *) = 0;
	virtual void detach(Observer *) = 0;
	virtual void notify() = 0;
};


class ConcreteObserver : public Observer {
public:
	ConcreteObserver(Subject *pSubject): m_pSubject(pSubject) {

	}
	void update(int val) {
		cout << "concrete observer get update, new val: " << val << endl;
	}
private:
	Subject *m_pSubject;
};


class ConcreteObserver2 : public Observer {
public:
	ConcreteObserver2(Subject *pSubject): m_pSubject(pSubject) {

	}
	void update(int val) {
		cout << "concrete observer2 get update, new val: " << val << endl;
	}
private:
	Subject *m_pSubject;

};

class ConcreteSubject : public Subject {
public:
	void attach(Observer *pObserver);
	void detach(Observer *pObserver);
	void notify();
	void setState(int state) {
		m_iState = state;
	}
private:
	std::list<Observer *> m_ObserverList;
	int m_iState;
};

void ConcreteSubject::attach(Observer *pObserver) 
{
	m_ObserverList.push_back(pObserver);
}

void ConcreteSubject::detach(Observer *pObserver)
{
	m_ObserverList.remove(pObserver);
}

void ConcreteSubject::notify()
{
	std::list<Observer *>::iterator it = m_ObserverList.begin();
	while(it != m_ObserverList.end()) {
		(*it)->update(m_iState);
		it++;
	}
}


int main(int argc, char const *argv[])
{
	ConcreteSubject *pSubject = new ConcreteSubject();

	Observer *pObserver = new ConcreteObserver(pSubject);
	Observer *pObserver2 = new ConcreteObserver2(pSubject);

	pSubject->setState(1);

	pSubject->attach(pObserver);
	pSubject->attach(pObserver2);

	pSubject->notify();

	pSubject->detach(pObserver);
	pSubject->setState(2);
	pSubject->notify();

	delete pObserver;
	delete pObserver2;
	delete pSubject;

	return 0;
}
```

```
teddy@teddy-ubuntu:~/work/test/cpp$ ./a.out 
concrete observer get update, new val: 1
concrete observer2 get update, new val: 1
concrete observer2 get update, new val: 2
```



# 代理模式

代理模式跟装饰器模式比较类似。

但是二者的目的是不一样的。

代理模式是为了控制对象的访问。

一个现实生活的例子，

男生A想要追求女生B，但是A不认识B，但是A认识C，C跟B认识。

所以A希望通过C给B送礼物。

示例代码：

```
#include <iostream>
#include <list>
using namespace std;

//定义女孩类。
class Girl {
public:
	Girl(char *name= "") :m_name(name) {

	}
	char *getName() {
		return m_name;
	}
private:
	char *m_name;
};
//定义送礼物接口。
class GiveGift {
public:
	virtual void giveFlower() = 0;
	virtual void giveDoll() = 0;
};


class BoyA : public GiveGift {
public:
	BoyA(Girl g) : m_girl(g) {

	}

	void giveDoll() {
		cout << "boya give " << m_girl.getName() << " doll" << endl;

	}
	void giveFlower() {
		cout << "boya give " << m_girl.getName() << " flower" << endl;
	}
private:
	Girl m_girl;
};

class BoyC : public GiveGift {
public:
	BoyC(Girl g) {
		ba = new BoyA(g);
	}
	void giveDoll() {
		ba->giveDoll();
	}
	void giveFlower() {
		ba->giveFlower();
	}
private:
	BoyA* ba;
};


int main(int argc, char const *argv[])
{
	Girl mm("ccc");
	BoyC boyc(mm);
	boyc.giveDoll();
	boyc.giveFlower();
	return 0;
}
```



# 监听者模式



# 参考资料

1、单例模式及C++实现代码

https://www.cnblogs.com/cxjchen/p/3148582.html

2、设计模式之观察者模式（c++）

https://www.cnblogs.com/carsonzhu/p/5770253.html

3、代理模式(Proxy)C++实现

https://www.cnblogs.com/wrbxdj/p/5267370.html