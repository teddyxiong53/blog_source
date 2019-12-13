---
title: cpp之内存泄漏分析
date: 2018-11-15 14:45:17
tags:
	- cpp

---



# valgrind

就用valgrind来测试一下。

```
std::string g_str;
void main()
{
    g_str = std::string(100, 'a');
}
```

这样并不会内存泄漏。因为g_str不是一个指针。

而且我没有用new。所以也就不需要delete，也无法delete。

# mtrace

用mtrace来做。这个是原理的给malloc和free加上了钩子函数。

不行。我写了一个测试的c文件，是可以的。

放弃mtrace。



# gperftools

这个是谷歌的工具。准确说是一组工具集。

使用了tcmalloc这个内存分配器。

主要有3个工具：

1、heap-profiler。内存监测。

2、heap-checker。检查内存泄漏。

3、cpu-profiler。cpu性能监测。

安装步骤

```
git clone https://github.com/gperftools/gperftools
cd gperftools
./autogen.sh
./configure
make -j8
sudo make install
```

```
git clone git://git.sv.gnu.org/libunwind.git
cd libunwind
./autogen.sh
./configure
make
make install
```

在代码里包含：

```
#include <google/profiler.h>
ProfilerStart("profiler");参数是文件名。随便写。
在适合的位置加上ProfilerStop();
连接加上-lprofiler。
```

然后执行程序，会生成一个profiler的文件。

执行下面的命令，生成统计图片。

```
pprof --gif ./dossos profiler > profiler.gif
```

需要先安装：

```
sudo apt-get install graphviz
```



内存泄漏检查

```
export PPROF_PATH=/usr/local/bin/pprof
```

```
sudo env HEAPCHECK=normal ./dossos
```



参考资料

1、警惕多线程环境string、vector、protobuf等自增长数据结构的隐性内存泄漏

https://blog.csdn.net/u011693064/article/details/72466171

2、google-gperftools分析代码时间分布

https://blog.csdn.net/oujiangping/article/details/77172802

3、gperftools工具检测内存泄漏

https://blog.csdn.net/zhengbin6072/article/details/80222639

4、tcmalloc安装与使用

https://blog.csdn.net/u011217649/article/details/77683126

5、tcmalloc使用的一点经验

http://blog.chinaunix.net/uid-20722087-id-5083864.html

6、C：使用mtrace、memwatch、dmalloc检测内存泄漏

https://my.oschina.net/letiantian/blog/754506