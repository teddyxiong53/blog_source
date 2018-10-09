---
title: cpp之chrono
date: 2018-09-29 17:25:51
tags:
	- cpp

---



chrono是一个时间库，来自于boost。现在已经是c++的标准。

需要包含头文件<chrono>

是一个模板库。

主要涉及3个概念：

1、duration。表示时间段。

2、time_point。表示时间点。

3、clock。表示时间戳。

# duration

是一个类模板。

```
template <class Rep, class Period = ratio<1>>
class duration;
```

Period表示单位，默认是秒数。如果是1000，则表示1毫秒。表示的是切分关系。

Rep表示单位的个数，例如10秒，10分钟。

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





#参考资料

1、C++11 std::chrono库详解

https://www.cnblogs.com/jwk000/p/3560086.html

2、c++11时间相关库(chrono)

https://www.cnblogs.com/geloutingyu/p/8529239.html