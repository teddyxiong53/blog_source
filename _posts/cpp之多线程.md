---
title: cpp之多线程
date: 2018-10-10 19:33:51
tags:
	- cpp

---



下面讨论的都是c++11版本之后的。

在C语言里，用pthread这个库来做多线程。

而到了c++里，可以在语言层来做多线程了。

好处就是程序的可移植性得到很大的提高。

c++11引入了5个头文件来支持多线程编程

1、atomic。声明了2个类，std::atomic和std::atomic_flag。

2、thread。主要声明了类std::thread类。

3、mutex。

4、condition_variable

5、future。主要声明了std::promise和 std::package_task这2个provider类。以及std::future/std::shared_future这2个future类。



最简单的例子。

```
#include <iostream>
#include <thread>

void t1_func() {
	std::cout << "hello thread" << std::endl;
}
int main()
{
	std::thread t1(t1_func);
	t1.join();
	return 0;
}
```



# std::thread详解

## 构造函数

```
//默认构造函数
thread() noexcept; 
//初始化构造函数
template <class Fn, class... Args>
explicit thread(Fn&& fn, Args&&... args);
//拷贝构造函数
被delete了。就是不可用被拷贝构造。
//move构造函数
thread(thread&& x) noexcept;
```

测试各种构造函数

```

#include <iostream>
#include <thread>
#include <chrono>

void f1(int n){
    for(int i=0 ;i<5; i++) {
        std::cout << "thread " << n << " is executing\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

void f2(int& n) {
    for(int i=0; i<5; i++) {
        std::cout << "thread 2 is executing\n";
        n++;
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

int main ()
{
    int n = 0;
    std::thread t1;
    std::thread t2(f1, n+1);
    std::thread t3(f2, std::ref(n));
    std::thread t4(std::move(t3));

    t2.join();
    t4.join();
    std::cout << "the value of n is: " << n << std::endl;
}

```



```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test 
thread 2 is executing
thread 1 is executing
thread 2 is executing
thread 1 is executing
thread 2 is executing
thread 1 is executing
thread 2 is executing
thread 1 is executing
thread 1 is executing
thread 2 is executing
the value of n is: 5
```



# std::mutex

mutex头文件内容：

4种mutex：

1、mutex。

2、recursive_mutex。递归mutex。

3、time_mutex。定时mutex。

4、recursive_timed_mutex。递归定时mutex。

还有两个lock类。

1、lock_guard。

2、unique_lock。

其他类型：

1、once_flag。

2、adopt_lock_t。

3、defer_lock_t。

4、try_to_lock_t。

函数：

1、try_lock。

2、lock。

3、call_once。

## 构造函数

不允许拷贝构造。不允许move拷贝。





# condition_variable

返回是这样的类型：

```
enum class cv_status {
    no_timeout,
    timeout   
};
```

0表示正常返回，1表示超时。

wait_for函数，里面的lambda表达式，要返回true，函数才算是满足条件。





# 参考资料

1、C++11 并发指南一(C++11 多线程初探)

这个系列文章都不错。

http://www.cnblogs.com/haippy/p/3235560.html

2、当前标签: 多线程

https://www.cnblogs.com/haippy/tag/%E5%A4%9A%E7%BA%BF%E7%A8%8B/

