---
title: Python之matplotlib
date: 2018-06-01 23:44:01
tags:
	 - python
---

--

# pylot api

这是一组命令样式函数，使matplotlib的工作方式类似于matlab。

每个pylot函数对图形进行一些修改。

例如：创建图形、在图形中创建绘图区域、在绘图区域里绘制一些线、使用标签装饰绘图。

# 面向对象的api

matplotlib的核心是面向对象的。

如果要对plots进行更多控制和自定义，建议使用对象的方式。





我先只看pylot api的。因为我只是简单使用。

```
import matplotlib.pyplot as plt

plt.plot([1,2,3,4])
plt.ylabel('值', fontproperties = 'SimHei')
plt.show()
```

fontproperties必须要，不然中文显示不出来。

![image-20210107095050201](../images/playopenwrt_pic/image-20210107095050201.png)

可以看到，x轴是从0到3，而y轴是1到4 

因为如果你只给plot函数提供一个list，那么就被当成y轴数据。

然后另外单独给你生成x轴的数据。

plot()函数是一个多用途的函数。

可以接收多个参数。

例如这样：

```
x_data = [1,2,3,4]
y_data = [1,4,9,16]
plt.plot(x_data, y_data)
```

设置你的图形的风格

除了x、y轴数据，后面还可以有一个参数，用来指定图形的风格。

这个风格跟matlab里类似。

默认的风格是`b-`，表示的是蓝色的实线。

如果你想要改成红色的点，那么这样：

```
plt.plot(x_data, y_data, 'ro')
```

在一个图里，画多个图形。

```
import matplotlib.pyplot as plt

names = ['group_a', 'group_b', 'group_c']
values = [1,10,100]

plt.figure(figsize=(9,3))

plt.subplot(131)
plt.bar(names, values)

plt.subplot(132)
plt.scatter(names, values)

plt.subplot(133)
plt.plot(names, values)

plt.suptitle('all title')
plt.show()
```

![image-20210107100203797](../images/playopenwrt_pic/image-20210107100203797.png)



subplot函数

它的参数怎样理解？

```
# plot a line, implicitly creating a subplot(111)
plt.plot([1, 2, 3])
```

默认plot的，那么对应的subplot是subplot(111)

其实是可以分开成3个参数(1,1,1)

```
subplot(nrows, ncols, index, **kwargs)
```

第一个数字：行数。

第二个数字：列数。

第三个数字：索引值。

index从左上角的为1，往右边递增。

index还可以是一个元组(1,2)这样。这样就占据2/3的宽度。



我现在要画4个子图。

那就是两行两列。

```
subplot(2,2,1)
subplot(2,2,2)
subplot(2,2,3)
subplot(2,2,4)
```



```
import numpy as np
import matplotlib.pyplot as plt

plt.subplot(2,2,1)
plt.plot([1,2,3])

plt.subplot(2,2,2)
plt.plot([1,2,3])

plt.subplot(2,2,3)
plt.plot([1,2,3])

plt.subplot(2,2,4)
plt.plot([1,2,3])

plt.show()
```

得到的图形这样：

![image-20210107102029953](../images/playopenwrt_pic/image-20210107102029953.png)

基本符合我的要求了。

现在要加上标题。



# figure函数

```
import numpy as np
import matplotlib.pyplot as plt
 
fig1 = plt.figure(num="3*1 inches",figsize=(3,1))   
fig2 = plt.figure(num="6*2 inches",figsize=(6,2))
 
plt.show()
plt.close
```

这样得到的是2个窗口。一个figure就是一个窗口。

figsize:以英寸为单位的宽高，缺省值为 rc figure.figsize (1英寸等于2.54厘米)



![image-20210107103300358](../images/playopenwrt_pic/image-20210107103300358.png)



查看图片，可以用explorer.exe来打开图片。这样就是调用系统默认的图片查看工具来打开的。

现在显示图片没有问题，就是横轴需要拉长。



正弦波的，只要选取一个周期的。

直线型的，就把全部数据取出来。

# 生成exe

现在生成的exe运行不起来。

看执行的过程中，有打印一些错误。

```
23626 INFO: Import to be excluded not found: 'PySide'

ModuleNotFoundError: No module named 'tornado'
```

安装tornado试一下看看。

还是不行，看一下执行的错误信息。

```
Could not find the matplotlib data files
```

网上搜索了一下，说是需要把matplotlib版本降低到3.0.3或者3.1.3的。

我当前安装的是3.3.3的。

那就降级到3.0.3看看。

现在报错不一样了。

```
ModuleNotFoundError: No module named 'matplotlib.backends.backend_tkagg'
```

这个即使在pycharm里运行也是报这个错误。

```
ModuleNotFoundError: No module named 'tkinter'
```

安装一些tkinter，pycharm里运行再看看。

还是不行。

在我的python文件里，加上这个matplotlib.use("Agg")就可以了。

如下：

```
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```

现在再生成exe，执行也正常了。

# 发展历史

Matplotlib 是一个用于 Python 的绘图库，广泛用于数据可视化。它的发展历史可以追溯到以下几个关键阶段：

### 1. 起源 (2003)
- **创建者**：Matplotlib 由 John D. Hunter 开发，最初的目的是为了创建一个符合 MATLAB 风格的绘图库。
- **目标**：提供一个灵活且强大的工具，方便科学计算和数据分析中的图形展示。

### 2. 初期版本 (2003-2005)
- **基本功能**：早期版本支持基本的 2D 绘图功能，包括折线图、散点图和直方图等。
- **集成性**：可以与 NumPy 和其他科学计算库无缝集成，逐渐受到科学界的欢迎。

### 3. 发展与壮大 (2005-2010)
- **社区参与**：随着用户群体的扩大，越来越多的开发者开始参与项目，贡献代码和功能。
- **新特性**：引入了更多的绘图功能，如 3D 绘图、动画和交互式图形。

### 4. 进一步改进 (2010-2015)
- **版本更新**：推出了多个重要版本，改进了性能和可用性。
- **文档和示例**：增强了文档，增加了丰富的示例，帮助用户更好地理解如何使用库。

### 5. 现代化 (2015-至今)
- **大规模应用**：Matplotlib 被广泛应用于科研、工程、数据分析和机器学习等领域。
- **用户界面**：推出了 Jupyter Notebook 的支持，使得在交互式环境中绘图变得更加直观。
- **持续更新**：持续进行功能扩展和性能优化，支持新的绘图需求和标准。

### 6. 未来展望
- **用户反馈**：项目团队积极听取用户反馈，计划引入更多现代化的功能。
- **集成新技术**：与其他数据科学工具和库（如 Pandas、Seaborn 等）更好地集成，进一步提升用户体验。

Matplotlib 的持续发展和广泛应用使其成为数据可视化领域的重要工具之一。你是否对某个特定的版本或功能有更深入的兴趣？

# 它可以做哪些事情

Matplotlib 是一个功能强大的绘图库，能够满足多种数据可视化需求。以下是一些主要功能和应用场景：

### 1. 基本图表
- **折线图**：适合显示随时间变化的数据。
- **散点图**：用于展示两个变量之间的关系。
- **直方图**：用于显示数据分布。

### 2. 多种图形类型
- **条形图**：用于比较不同类别的数据。
- **饼图**：显示各部分占整体的比例。
- **箱形图**：用于描述数据的分布特征，如中位数和四分位数。

### 3. 高级绘图
- **3D 绘图**：支持创建三维图形，如 3D 曲面图和散点图。
- **极坐标图**：适合展示极坐标数据。
- **热图**：用于表示矩阵数据的强度，常用于展示相关性。

### 4. 自定义和样式
- **图表样式**：支持自定义颜色、线条样式、标记等外观。
- **注释和标签**：可以在图中添加注释、标题和坐标轴标签，以增强图表的可读性。

### 5. 动画和交互式图形
- **动画绘图**：可以创建动态更新的图形，适合演示和可视化变化过程。
- **交互式图形**：与 Jupyter Notebook 集成，支持缩放、平移等交互操作。

### 6. 数据处理与分析
- **与 NumPy 和 Pandas 集成**：可以直接从数据框架或数组中绘图，方便数据分析。

### 7. 多图表布局
- **子图**：在同一画布上绘制多个子图，便于比较和分析。
- **图例**：可以添加图例以区分不同数据系列。

### 8. 导出与共享
- **多种格式导出**：支持将图形导出为 PNG、PDF、SVG 等格式，方便共享和发表。

Matplotlib 的灵活性和强大功能使其成为数据科学家和工程师进行数据可视化的首选工具。如果你有特定的图表需求或想了解某个功能的实现，欢迎询问！

# 典型使用场景

Matplotlib 的灵活性使其在许多场景中都能发挥作用。以下是一些典型的使用场景：

### 1. 科学研究
- **数据分析**：研究人员使用 Matplotlib 可视化实验数据，帮助识别趋势和模式。
- **论文发表**：图表常用于学术论文中，以清晰展示研究结果。

### 2. 数据科学与机器学习
- **数据探索**：数据科学家在数据清洗和预处理阶段，通过图表分析数据分布和特征。
- **模型评估**：使用 ROC 曲线、混淆矩阵等图形评估模型性能。

### 3. 财务分析
- **时间序列分析**：通过折线图展示股票价格、经济指标等随时间变化的趋势。
- **投资组合可视化**：用饼图或条形图展示资产配置。

### 4. 工程与制造
- **过程监控**：实时监测生产数据，使用图表展示关键性能指标（KPI）。
- **质量控制**：利用箱形图和直方图分析产品质量数据。

### 5. 教育与培训
- **教学演示**：教师使用 Matplotlib 创建图形，帮助学生理解复杂的概念。
- **实验报告**：学生在实验报告中使用图表展示实验结果。

### 6. 数据可视化仪表板
- **动态仪表板**：与其他库（如 Dash 或 Streamlit）结合，创建互动式数据仪表板展示实时数据。

### 7. 地理数据可视化
- **地理信息系统 (GIS)**：通过热图或散点图可视化地理位置数据，分析区域特征。

### 8. 网络数据分析
- **网络流量监控**：使用折线图或条形图分析网络流量变化，识别异常活动。

### 9. 社会科学研究
- **人口统计分析**：通过多种图表展示人口特征、社会经济数据等。

这些场景展示了 Matplotlib 的广泛应用和强大功能。如果你对某个具体场景或应用有兴趣，欢迎进一步询问！

# 参考资料

1、

https://www.matplotlib.org.cn/API/

2、三、Matplotlib系列---pyplot的中文显示

https://blog.csdn.net/skyli114/article/details/77508247

3、例子

https://www.matplotlib.org.cn/gallery/#lines-bars-and-markers

4、

https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.subplot.html

5、matplotlib将图横向拉长，自定义x轴

https://blog.csdn.net/TH_NUM/article/details/108817356

6、

https://stackoverflow.com/questions/63103147/could-not-find-the-matplotlib-data-files

7、

https://blog.csdn.net/a214919447/article/details/73870705