---
title: cpp之std疑问
date: 2018-05-13 21:04:40
tags:
	- cpp

---



这篇文章就逐渐把碰到的std的内容整理起来。

pair

lock_guard

enable_shared_from_this



# pair

https://www.cnblogs.com/lvchaoshun/p/7769003.html

pair是把2个数据组合成一个数据。

pair实质上是一个结构体。

两个成员变量是first和second。

产生一个pair，有两种方法：

1、用构造函数。

2、用make_pair函数。

```
std::pair<int, float>(1, 1.1);
std::make_pair(1, 1.1);
```

需要包含头文件。

```
#include <utility>
```



#lock_guard

这个出现就是为了应对加锁和开锁不匹配的情况导致的死锁问题。

cpp引入lock_guard就是进行了一次很薄的封装，可以实现自动配对。

我看是以大括号为作用范围。



参考资料

 C++11 std::unique_lock与std::lock_guard区别及多线程应用实例 

https://blog.csdn.net/tgxallen/article/details/73522233

C++11多线程之std::lock_guard

https://blog.csdn.net/nirendao/article/details/50890486



# enable_shared_from_this

实际上是一个模板类。在头文件memory里。

原型是：

```
template <class T> class enable_shared_from_this;
```

如果一个类继承了enable_shared_from_this，那么就会拥有一个成员函数：shared_from_this。

而进行`std::shared_ptr<T>`定义时，就会调用到这个函数。

使用智能指针的目的就是为了方便资源管理，如果智能指针和裸指针混用，很容易破坏智能指针的语义，从而产生各种错误。





参考资料

https://blog.csdn.net/caoshangpa/article/details/79392878

C++中基类继承 enable_shared_from_this 之后派生类无法使用 shared_from_this() 的解决方法

https://blog.csdn.net/u013745174/article/details/52900870

# shared_ptr

也是一个模板类。

```
template < class T>
class shared_ptr;
```

例子。

```
struct Base {
	Base() {
		std::cout << "Base::Base()\n" ;
	}
	~Base() {
		std::cout << "Base::~Base()\n";
	}
};
struct Derived: public Base {
	Derived() {
		std::cout << "Derived::Derived()\n";
	}
	~Derived() {
		std::cout << "Derived::~Derived()\n";
	}
	
};
void thr(std::shared_ptr<Base> p)
{
	std::this_thread::sleep_for(std::chrono::seconds(1));
	std::shared_ptr<Base> lp = p;
	{
		static std::mutex io_mutex;
		std::lock_guard<std::mutex> lk(io_mutex);
		std::cout << "local pointer in a thread:\n"
			<< "lp.get() = " << lp.get()
			<< ", lp.use_count() = " << lp.use_count() << "\n";
	}
}
int main()
{
	std::shared_ptr<Base> p = std::make_shared<Derived>();
	std::cout << "create a shared Derived (as a pointer to Base)\n"
		<< "p.get() = " << p.get()
		<< ", p.use_count() = " << p.use_count() << "\n";
	std::thread t1(thr ,p), t2(thr, p), t3(thr, p);
	p.reset();
	std::cout << "shared ownership between 3 threads and released\n"
		<< "ownership from main:\n"
		<< "p.get() = " << p.get()
		<< ", p.use_count() = " << p.use_count() << "\n";
	t1.join();
	t2.join();
	t3.join();
	std::cout << "finish" << "\n";
	return 0;
}
```

输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./xxx 
Base::Base()
Derived::Derived()
create a shared Derived (as a pointer to Base)
p.get() = 0x233dc30, p.use_count() = 1
shared ownership between 3 threads and released
ownership from main:
p.get() = 0, p.use_count() = 0
local pointer in a thread:
lp.get() = 0x233dc30, lp.use_count() = 6
local pointer in a thread:
lp.get() = 0x233dc30, lp.use_count() = 4
local pointer in a thread:
lp.get() = 0x233dc30, lp.use_count() = 2
Derived::~Derived()
Base::~Base()
finish
```

# make_shared

make_shared实际上可以看做为了完全封装new而给shared_ptr的一个factory。



# memory头文件

这个头文件是动态内存管理的一部分。

主要内容有：

1、智能指针。4个

```
unique_ptr
shared_ptr
weak_ptr
auto_ptr：c++17移除了这个。
```

2、辅助类。4个

```

```

3、分配器。

4、



参考资料

https://zh.cppreference.com/w/cpp/header/memory