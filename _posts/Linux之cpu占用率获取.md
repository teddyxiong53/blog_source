---
title: Linux之cpu占用率获取
date: 2018-11-15 15:17:17
tags:
	- cpp

---



我是希望用C语言来获取的。其实不太想去分析proc文件系统。但是不知道有没有其他的函数可以用。

网上找了一下，都是用分析sys或者proc文件系统里的节点的方式的。



这里的代码写得比较好。也比较全。

https://rosettacode.org/wiki/Linux_CPU_utilization#C

试了一下，c++版本的比较好。就把c++版本的用起来。

是基于/proc/stat来做的，就分析第一行。

```
/ # cat /proc/stat
cpu  4344440 0 400449 33524102 13 0 5602 0 0 0
```

这些数字的含义，依次如下：

单位是节拍时间，一般就是10ms。

user：从系统启动到现在，处于用户态的运行时间。

nice：nice值为负数的进程的累计运行时间。

system：内核太累计运行时间。

idle：累计的等待时间。

irq：累计的中断时间。

```
#include <fstream>
#include <iostream>
#include <numeric>
#include <unistd.h>
#include <vector>
 
int main()
{
	std::ifstream proc_stat("/proc/stat");
	proc_stat.ignore(5, ' ');
	std::vector<size_t> times;
	for(size_t time; proc_stat >> time; times.push_back(time));
	for(int i=0; i<times.size(); i++) {
		std::cout << times[i] << std::endl;
	}
	
}
```

这样就把第一行的内容存到一个vector里了。



# 参考资料

1、Linux中通过/proc/stat等文件计算Cpu使用率

这篇文章特别好。

http://www.blogjava.net/fjzag/articles/317773.html