---
title: cpp之chrono
date: 2018-09-29 17:25:51
tags:
	- cpp

---

---

chrono是一个时间库，来自于boost。现在已经是c++的标准。

需要包含头文件`<chrono>`

是一个模板库。

跟其他的标准库略有不同的是，这个的类，都是在std::chrono命名空间下，而不是之间在std命名空间。



主要涉及3个概念：

1、duration。表示时间段。例如：1分钟。1小时。

2、time_point。表示时间点。

3、clock。表示时间戳。



类有这些：

时间段和时间点。

```
template <class Rep, class Period = ratio<1> >
class duration;

template <class Clock, class Duration = typename Clock::duration>
class time_point;
```

clock

```
system_clock
steady_clock
high_resolution_clock
```

函数有：

```
duration_cast
time_point_cast
```

为了便于使用的类实例化typedef

```
hours
minutes
seconds
```

# 解决什么问题

`<chrono>` 头文件提供了 C++ 标准库中处理时间、时钟和计时的功能，它解决了以下一些常见问题：

1. 跨平台时间处理： `<chrono>` 提供了跨平台的时间处理功能，可以在不同的操作系统和编译器中使用一致的时间表示和计算方式。

2. 时间点和时间间隔的表示： `<chrono>` 定义了不同类型的时间点（time point）和时间间隔（duration），使得可以方便地进行时间的表示、计算和比较。

3. 时间转换和格式化： `<chrono>` 提供了时间点和时间间隔的转换函数，可以将它们与其他时间表示形式（如时间戳）进行相互转换。同时，可以根据需要将时间点格式化为各种日期和时间字符串。

4. 计时和延时操作： `<chrono>` 允许精确地测量代码的执行时间，包括纳秒、微秒、毫秒和更长时间间隔的计时。此外，还提供了延时等待功能，可用于控制程序的执行速度或定时操作。

5. 高分辨率时钟： `<chrono>` 中定义的 `std::chrono::high_resolution_clock` 提供了一个高精度的时钟，可用于测量代码执行时间或实现需要更精确计时的应用程序。

通过提供统一的时间处理接口和功能，`<chrono>` 解决了在不同平台上处理时间的复杂性，简化了时间相关操作的实现，并提供了更高精度的计时功能。它是 C++ 中处理时间的推荐方式，使开发人员能够更方便地进行时间相关的编程。

# 使用chrono封装一些常用功能

以下是使用 `<chrono>` 头文件封装一些常用功能的示例代码：

```cpp
#include <iostream>
#include <chrono>

int main() {
    // 获取当前时间点
    std::chrono::system_clock::time_point now = std::chrono::system_clock::now();

    // 将时间点转换为时间戳
    std::time_t timestamp = std::chrono::system_clock::to_time_t(now);
    std::cout << "当前时间戳：" << timestamp << std::endl;

    // 将时间戳转换为时间点
    std::chrono::system_clock::time_point timePoint = std::chrono::system_clock::from_time_t(timestamp);

    // 计算时间间隔
    std::chrono::system_clock::duration duration = now - timePoint;
    std::cout << "时间间隔：" << duration.count() << " 秒" << std::endl;

    // 延时等待
    std::chrono::seconds delay(3);
    std::cout << "开始等待 " << delay.count() << " 秒..." << std::endl;
    std::this_thread::sleep_for(delay);
    std::cout << "等待结束" << std::endl;

    // 测量代码执行时间
    auto start = std::chrono::high_resolution_clock::now();
    // 执行一些操作
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "代码执行时间：" << duration.count() << " 毫秒" << std::endl;

    return 0;
}
```

上述代码演示了使用 `<chrono>` 头文件进行常见功能的封装。其中包括获取当前时间点、时间戳转换、计算时间间隔、延时等待以及测量代码执行时间。请根据具体需求和场景进行适当的调整和使用。

# duration

是一个类模板。

```
template <class Rep, class Period = ratio<1>>
class duration;
```

Period表示单位，默认是秒数。如果是1000，则表示1毫秒。表示的是切分关系。

Rep表示单位的个数，例如10秒，10分钟。

ratio就是表示分数值的意思。

```
ratio<3600, 1>                hours
ratio<60, 1>                    minutes
ratio<1, 1>                      seconds
ratio<1, 1000>               microseconds
ratio<1, 1000000>         microseconds
ratio<1, 1000000000>    nanosecons
```



预定义的值有：

```
typedef ratio<1, 1000000000> nano;
typedef ratio<1, 1000000> micro;
typedef ratio<1, 1000> milli;
typedef duration<long long, nano> nanoseconds;      //纳秒
typedef duration<long long, micro> microseconds;    //微秒
typedef duration<long long, milli> milliseconds;    //毫秒
typedef duration<long long> seconds;                //秒
typedef duration<int, ratio<60> > minutes;          //分钟
typedef duration<int, ratio<3600> > hours;          //小时
```

看一个简单的例子。

```
int main()
{
	typedef std::chrono::duration<int> seconds_type;
	typedef std::chrono::duration<int, std::milli> milliseconds_type;
	typedef std::chrono::duration<int, std::ratio<60*60>> hours_type;
	
	hours_type h_oneday(24);
	seconds_type s_oneday(24*60*60);
	
	std::cout << s_oneday.count() << " seconds in a day" << "\n";
	return 0;
	
}
```



# steady_clock和system_clock

steady_clock就是单独递增的时间。就像体育老师手里的秒表。一般用来统计函数的耗时。

system_clock，就是系统时间。

high_resolution_clock。相当于steady_clock的高精度版本。

```
using namespace std::chrono;
int main()
{
    steady_clock::time_point t1 = steady_clock::now();
    sleep(1);
    steady_clock::time_point t2 = steady_clock::now();
    duration<double> diff = duration_cast<duration<double>>(t2-t1);
    printf("time:%f\n", diff);
    return 0;
}
```

## system_clock

```
内部类型
rep
period
duration
time_point

成员常量
is_steady
	bool类型。
static成员函数
now()
to_time_t()
from_time_t()
```

函数串起来用，如下：

```
int main()
{
    using std::chrono::system_clock;
    std::chrono::duration<int, std::ratio<60*60*24>> one_day;
    system_clock::time_point today = system_clock::now();
    system_clock::time_point tomorrow = today+one_day;
    std::time_t tt;

    tt = system_clock::to_time_t(today);
    std::cout << "today is :" << ctime(&tt) << " \n";
    return 0;
}
```



# 参考资料

1、C++11 std::chrono库详解

https://www.cnblogs.com/jwk000/p/3560086.html

2、c++11时间相关库(chrono)

https://www.cnblogs.com/geloutingyu/p/8529239.html