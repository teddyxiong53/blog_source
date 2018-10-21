---
title: Python之画地图
date: 2018-10-20 15:46:08
tags:
	- Python
	- 地图

---



最近对地图产生了兴趣，所以就想用Python来画地图。

# 安装环境

这个在anaconda环境下来安装环境是最简单的。

我之前的电脑出了点问题，我的Python环境也有问题了。

所以现在索性只用anaconda这个环境了。

网上找了一篇教程，发现需要安装basemap模块。

```
conda install basemap
```

这种方式是最简单的了。

# 最简单的代码

```
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

plt.figure(figsize=(16,8))
m = Basemap()
m.drawcoastlines()

plt.show()
```

运行报错。

```
  File "D:\Anaconda3\lib\site-packages\mpl_toolkits\basemap\__init__.py", line 155, in <module>
    pyproj_datadir = os.environ['PROJ_LIB']
  File "D:\Anaconda3\lib\os.py", line 669, in __getitem__
    raise KeyError(key) from None
KeyError: 'PROJ_LIB'
```

根据参考资料1进行解决。

输入这一行，又提示要安装一堆的东西。这个不对，这个是创建了一个虚拟环境，名字叫TEST。

```
conda create --name TEST python=3.6 basemap
```

实际的解决方法是，新建一个环境变量，叫PROJ_LIB。指向的目录是：

```
D:\Anaconda3\Library\share
```

然后再运行就可以了。

这段代码的效果，就是得到一张世界地图。

再加上一行：

```
m.drawcounties(linewidth=1.5) #画出国家
```

运行报错了。看这个提示，是需要安装另外的库才行。这个库大概100M。

```
OSError: Cannot find D:\Anaconda3\Library\share\basemap\UScounties.shp
You can install it with`conda install basemap-data-hires`
```

下面看看怎样画中国地图。

就是给Basemap传递几个参数进去就好了。

```

```

这样画出来的地图，看起来有点变形，因为没有使用投影参数。Basemap提供了24种投影参数。

比较常用的是兰勃特投影。

# Basemap

上面我们已经看到了Basemap的一些简单使用。

那么Basemap是什么呢？

Basemap 是Matplotlib 的一个扩展，使得Matplotlib更方便处理地理数据。



# Catorpy

这个是跟Basemap类似的一个库。

Basemap用起来比较繁琐一些。



# 参考资料

1、KeyError 'PROJ_LIB' #419

https://github.com/matplotlib/basemap/issues/419

