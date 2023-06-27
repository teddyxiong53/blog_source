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

# c++的std 发展历史

C++的标准库（std）是C++语言中提供的一组常用库，包含了许多数据结构、算法、输入/输出、多线程、时间处理等功能。下面是C++标准库的发展历史的主要里程碑：

1. C++98：最初的C++标准（通常称为C++98或C++03）引入了最基本的标准库。它包含了`<iostream>`、`<vector>`、`<string>`等头文件，并定义了`std`命名空间和一些常用的类和函数。

2. C++11：C++11引入了许多对标准库的改进和扩展。它添加了新的容器类，如`<array>`、`<unordered_map>`和`<unordered_set>`，以及新的算法和迭代器支持，如`<algorithm>`中的Lambda表达式、范围基于for循环和智能指针类`<memory>`。

3. C++14：C++14对标准库进行了一些小的改进和增强。它添加了新的数值类型`std::make_unique`、`std::integer_sequence`和`std::exchange`等，并对一些库组件进行了修订和改进。

4. C++17：C++17对标准库进行了一系列改进和扩展。它引入了一些新的头文件和类，如`<optional>`、`<variant>`和`<filesystem>`，并对`<algorithm>`、`<string>`等进行了改进和增强。

5. C++20：C++20是C++标准库的最新版本，于2020年发布。它引入了一些重要的新特性，如概念（Concepts）、范围（Ranges）、协程（Coroutines）和模块（Modules），并对现有的库组件进行了改进和扩展。

每个C++标准的发布都带来了对标准库的改进和增强，以提供更强大、更灵活和更高效的功能。标准库的发展历史反映了C++语言本身的演进和不断改进的需求，以满足开发人员在不同领域和应用中的需求。开发人员可以根据所使用的C++标准版本来选择适当的标准库功能，以获得最佳的开发体验和性能。

# std的头文件分类

C++标准库（std）中的头文件可以分为以下几个分类，每个分类提供了一组相关的功能和类：

1. 输入/输出（I/O）相关头文件：
   - `<iostream>`：提供基本的输入和输出操作，包括输入输出流、输入输出操作符等。
   - `<fstream>`：提供文件输入和输出操作，包括文件读写、文件流等。

2. 容器类和算法相关头文件：
   - `<vector>`：提供动态数组容器。
   - `<list>`：提供双向链表容器。
   - `<deque>`：提供双端队列容器。
   - `<map>`：提供键值对映射容器。
   - `<set>`：提供有序集合容器。
   - `<algorithm>`：提供各种算法操作，如排序、查找、变换等。

3. 字符串和字符处理相关头文件：
   - `<string>`：提供字符串操作和处理。
   - `<cstring>`：提供C风格字符串操作函数。
   - `<cctype>`：提供字符分类和转换函数。

4. 数值和数学相关头文件：
   - `<cmath>`：提供数学函数，如三角函数、指数函数、对数函数等。
   - `<random>`：提供随机数生成器。
   - `<numeric>`：提供数值计算相关的算法。

5. 内存管理和智能指针相关头文件：
   - `<memory>`：提供智能指针和内存管理功能，如`shared_ptr`、`unique_ptr`等。
   - `<new>`：提供内存分配和释放操作。

6. 时间和日期处理相关头文件：
   - `<chrono>`：提供时间点和时间间隔的计算和处理。
   - `<ctime>`：提供时间和日期的处理函数。

7. 异常处理相关头文件：
   - `<exception>`：提供异常处理相关的类和函数。

这些是C++标准库中的一些常用头文件分类及其相关头文件的示例。需要根据具体需求选择适当的头文件来使用其中的功能和类。

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

就是把this指针也变成一个shared_ptr。就这么简单。

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