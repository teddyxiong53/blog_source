---
title: cpp之chrono
date: 2018-09-29 17:25:51
tags:
	- cpp

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