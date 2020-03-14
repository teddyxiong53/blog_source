---
title: cpp之boost库
date: 2018-10-09 17:47:51
tags:
	- cpp

---

1

boost库包括了哪些内容？



从buildroot里的boost的配置来看。

在targeted packages --> libraries --> others里面。

有这些内容：

```
[*] boost                      
      Layout (system)  --->    
[ ]   boost-atomic             
[ ]   boost-chrono             
[ ]   boost-container          
[ ]   boost-date_time          
[ ]   boost-exception          
[ ]   boost-fiber              
[ ]   boost-filesystem         
[ ]   boost-graph              
[ ]   boost-graph_parallel     
[ ]   boost-iostreams          
[ ]   boost-locale             
[ ]   boost-log                
[ ]   boost-math               
[ ]   boost-mpi                
[ ]   boost-program_options    
[ ]   boost-random             
[ ]   boost-regex              
[ ]   boost-serialization      
[ ]   boost-signals            
[ ]   boost-stacktrace         
[ ]   boost-system             
[ ]   boost-test               
[ ]   boost-thread             
[ ]   boost-timer              
[ ]   boost-type_erasure       
[ ]   boost-wave               
```



官网：https://www.boost.org/

```
Boost provides free peer-reviewed portable C++ source libraries.
```

当前最新版本是1.72.0版本的。

buildroot里当前是1.66版本的。还算比较新的。

全部是头文件。



自己在Ubuntu下编译安装boost。

1、解压。

2、执行脚本：

```
./bootstrap.sh
```

3、然后会提示你执行：

```
./b2 
./b2 headers
```

编译还比较慢。

b2的参数有：

```
stage/install
	stage表示只生成库。
	install还会生成include目录。
	
```

```
./b2 install --prefix=/usr
```

最后需要注意，如果安装后想马上使用boost库进行编译，还需要执行一下这个命令：

```
sudo ldconfig
```



测试安装是否成功：

```
#include <string>
#include <iostream>
#include <boost/version.hpp>
#include <boost/timer.hpp>
using namespace std;
int main()
{
    boost::timer t;
    cout << "max timespan: " << t.elapsed_max() / 3600 << "h" << endl;
    cout << "min timespan: " << t.elapsed_min() << "s" << endl;
    cout << "now time elapsed: " << t.elapsed() << "s" << endl;
    cout << "boost version" << BOOST_VERSION << endl;
    cout << "boost lib version" << BOOST_LIB_VERSION << endl;
    return 0;
}
```

编译：

```
g++ test.cpp
```

运行输出：

```
max timespan: 2.56205e+09h
min timespan: 1e-06s
now time elapsed: 0.000177s
boost version107200
boost lib version1_72
```

可见生效了。



参考资料

1、boost

https://baike.baidu.com/item/boost/69144?fr=aladdin

2、boost为什么仅包含头文件就能用？

https://www.zhihu.com/question/275966715

3、完全编译安装boost

https://blog.csdn.net/q_l_s/article/details/53934036

4、Linux编译和安装boost库

https://blog.csdn.net/this_capslock/article/details/47170313

5、Boost.Build 简明教程

https://www.cnblogs.com/yaoyu126/p/5552495.html