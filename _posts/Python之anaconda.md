---
title: Python之anaconda
date: 2018-06-30 19:11:40
tags:
	- Python

---



anaconda是Python的一个发行版本。

包含了conda、python等180多个科学包及其依赖。

安装包比较大，有500M。

所以还有一个mini版本，叫做miniconda。

anaconda是专注于数据分析的Python发行版本。

conda是开源包和虚拟环境的管理系统。

anaconda可以很方便设置虚拟环境。

# 简介

Anaconda是一个开源的软件包、环境管理器，

用于科学计算、数据分析和机器学习的Python和R编程语言。

它提供了一个方便的方式来安装、管理和使用各种数据科学工具和库。

Anaconda包含了大量常用的Python和R库，

例如NumPy、Pandas、Matplotlib、Scikit-learn等，以及用于包管理和环境管理的工具conda。

除了Python和R语言的工具和库之外，Anaconda还包含了Jupyter Notebook等交互式开发环境，使得数据分析和可视化更加方便。

Anaconda还支持在不同的操作系统上运行，包括Windows、macOS和Linux。

总的来说，Anaconda提供了一个完整的数据科学平台，使得用户可以快速搭建和管理数据分析环境，进行科学计算、数据处理和机器学习等任务。

# anaconda、conda、mini-conda它们的关系

Anaconda、conda和Miniconda之间有一些关联，但它们又有各自的特点和用途。

1. **Anaconda**：Anaconda是一个数据科学平台，它是一个完整的Python和R语言的发行版本，包含了大量的数据科学工具和库。Anaconda不仅仅是一个软件包管理器，它还包括了许多预安装的工具、库和环境，如Jupyter Notebook等。Anaconda相对较大，因为它包含了许多预安装的工具和库，适合于需要一站式解决方案的用户。

2. **conda**：conda是Anaconda的包管理器和环境管理器，它可以用于安装、更新和删除软件包，以及创建和管理不同的工作环境。conda可以独立于Anaconda安装和使用，它可以用于管理任何Python软件包，不限于数据科学相关的工具和库。conda也是一个跨平台的工具，可以在不同的操作系统上运行。

3. **Miniconda**：Miniconda是一个精简版的Anaconda，它只包含了conda和一些基本的Python包。与Anaconda相比，Miniconda的安装包更小，因为它只包含了最基本的组件，用户可以根据需要在其基础上构建自己的环境。Miniconda适合于那些希望更加灵活地定制自己的Python环境的用户，他们可以根据自己的需求手动安装所需的软件包和库。

综上所述，Anaconda是一个完整的数据科学平台，包含了大量预安装的工具和库；conda是Anaconda的包管理器和环境管理器，用于安装、更新和管理软件包和环境；而Miniconda是一个精简版的Anaconda，只包含了conda和一些基本的Python包，适合于自定义环境的用户。

# anaconda的好处

八个字：省时省心，分析利器。

# 使用方法

安装就是一个exe，下一步就好了。

安装完成后，需要在cmd里运行一下：

```
conda upgrade --all
```

这是为了升级所有的工具包，以避免可能发生的错误。

需要把安装路径加入到PATH里。

安装一个包：

```
conda install xxx
```

删除：

```
conda remove xxx
```

升级：

```
conda update xxx
```

查看：

```
conda list
```







# 安装出错的解决方法

http://so.kszixue.com/?id=20

```
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
show_channel_urls: true
```

# ubuntu安装miniconda

因为virtualenv安装本地不存在的python环境有点问题。

想看看conda能不能实现。

其实nvm那样就很好，本地不存的版本，就从网上自动下载一个来使用。

从这里下载安装包：

https://docs.conda.io/en/latest/miniconda.html

安装：

```
bash Miniconda3-latest-Linux-x86_64.sh
```

这个默认是安装到你的home目录下的。

根据提示输入yes。很快就安装好。

安装之后，需要source ~/.bashrc，然后就可以看到conda命令已经可以用了。

这个时候，在你的命令行提示符的前面，就有一个(base)。

这个表示激活了系统默认的Python。

需要不要，就执行：

```
conda deactivate
```

配置默认不要激活

```
conda config --set auto_activate_base false 
```

我当前安装的是4.10.3版本的conda。

查看本地有的环境

```
$ conda env list
# conda environments:
#
base                  *  /home/amlogic/miniconda3
```

当前只有一个base。

创建一个虚拟环境，使用Python3.9的。

```
conda create --name resunet-env python==3.9
```

很顺利地从网上下载安装了。

激活环境

```
conda activate resunet-env
```



# 参考资料

1、致Python初学者：Anaconda入门使用指南

http://python.jobbole.com/87522/?repeat=w3tc

2、Anaconda完全入门指南

https://www.baidu.com/link?url=LMgL6ZhUPrZHWe5CutfZLCfdyICQ6AbRkTv5oe89OgjDi7olB3dPa6eR7kb9HCDj&wd=&eqid=db46c6610006cb3e000000035b669f27