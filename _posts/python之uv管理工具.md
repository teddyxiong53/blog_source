---
title: python之uv管理工具
date: 2025-05-02 17:31:11
tags:
	- python
---

--

现在全面转到用uv来管理python项目。

有必要把常用的命令总结梳理一下。

# 完全开始一个新的项目

```
uv init myproj
```

这个会创建myproj的目录，下面会生成pyproject.toml的文件。

然后创建并激活venv

```
uv venv
source .venv/bin/activate
```

创建venv还可以指定版本：

```
uv venv --python 3.11
```



然后安装需要的包：

```
uv add requests
```

查看安装的包的依赖关系：

```
uv tree
```

删掉一个包：

```
uv remove requests
```

锁定版本：

```
uv lock
```

也可以不激活虚拟环境的方式来运行：

```
uv run python hello.py
```

跟这个是等价：

```
uv run hello.py
```

打包和发布：

```
uv build
uv publish
```

在toml文件里添加镜像地址：

```
[[tool.uv.index]]
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
default = true
```

导出为requirements.txt

```
uv export > requirements.txt
```

# 如果是老的项目

初始化：

先进入到目录，执行

```
uv init
```

使用requirements.txt来安装：

```
uv add $(cat requirements.txt)
```

# 下载别人的uv管理的项目

安装依赖：

```
uv sync
```

