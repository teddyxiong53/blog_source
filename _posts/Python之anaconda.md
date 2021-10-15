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