---
title: Python之pipenv
date: 2018-06-28 19:10:28
tags:
	- Python

---



看requests的代码里的Makefile，看到这么一句。

```
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock
```

pipenv是什么？从名字上看跟虚拟环境有关系的。

跟virtualenv是什么关系？

pipenv是对pip和virtualenv进行了封装。



pipenv是Kenneth Reitz写的一个命令行工具。

Kenneth Reitz是requests的作者，Pipfile的主要推动者。

pipenv包括：

1、Pipfile。用来替换简陋的requirements.txt。

2、pip。

3、click。

4、requests。

5、virtualenv。



Pipfile是TOML格式，而不是简单的txt文本。

TOML是一种新的配置文件，跟ini、json这些是一个类型的东西。



pipenv的项目宣言是：对人类友好的python开发工作流。



一个项目对应一个Pipfile。

支持开发环境和正式环境的区别。默认提供default和development区分。

提供版本锁支持。Pipfile.lock。

click是Flask作者写的库。

安装：

```
sudo pip install pipenv
```

在使用pipenv之前，应该忘记pip的存在。

新建一个pipenvtest目录。在这个目录下进行操作。

创建一个环境。

```
pipenv --python 2.7
```

安装一个包看看。

```
pipenv install requests
```

当前目录下就这些东西：

```
hlxiong@hlxiong-VirtualBox:~/work/test/pipenvtest$ tree
.
├── Pipfile
└── Pipfile.lock

0 directories, 2 files
```



```
hlxiong@hlxiong-VirtualBox:~/work/test/pipenvtest$ pipenv graph
requests==2.19.1
  - certifi [required: >=2017.4.17, installed: 2018.4.16]
  - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
  - idna [required: >=2.5,<2.8, installed: 2.7]
  - urllib3 [required: >=1.21.1,<1.24, installed: 1.23]
```

Pipfile内容：

```
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[dev-packages]

[packages]
requests = "*"

[requires]
python_version = "2.7"
```





# pipenv和pyenv、venv对比

`pipenv`、`pyenv`和`venv`是用于管理Python环境和依赖的工具，但它们的功能和用途有所不同。以下是它们之间的对比：

### 1. `venv`
- **用途**: 用于创建独立的Python虚拟环境。
- **功能**:
  - 创建一个隔离的环境，避免依赖冲突。
  - 轻量级，Python标准库自带。
- **命令**:
  ```bash
  python -m venv myenv
  source myenv/bin/activate  # 在Unix或MacOS上
  myenv\Scripts\activate     # 在Windows上
  ```
- **适用场景**: 当你只需要一个简单的虚拟环境时，`venv`是一个不错的选择。

### 2. `pyenv`
- **用途**: 用于管理多个Python版本。
- **功能**:
  - 安装和切换不同版本的Python。
  - 可以为每个项目指定不同的Python版本。
- **命令**:
  ```bash
  pyenv install 3.8.10
  pyenv global 3.8.10
  pyenv local 3.7.9  # 在当前目录下设置项目使用的Python版本
  ```
- **适用场景**: 当你需要在同一台机器上使用多个Python版本时，`pyenv`非常有用。

### 3. `pipenv`
- **用途**: 结合`pip`和`venv`的功能，用于依赖管理和虚拟环境管理。
- **功能**:
  - 自动创建和管理虚拟环境。
  - 使用`Pipfile`和`Pipfile.lock`管理依赖。
  - 提供更友好的依赖安装和管理体验。
- **命令**:
  ```bash
  pipenv install requests   # 安装依赖并创建虚拟环境
  pipenv shell              # 进入虚拟环境
  ```
- **适用场景**: 当你需要简单地管理项目依赖和环境时，`pipenv`提供了更高层次的抽象和便利。

### 总结
- **`venv`**: 最基础的虚拟环境管理工具，适合简单场景。
- **`pyenv`**: 专注于Python版本管理，适合需要多个版本的开发者。
- **`pipenv`**: 综合管理依赖和虚拟环境，适合现代Python项目管理。

根据你的需求选择合适的工具会更有效率！如果你有具体的使用场景或问题，欢迎继续提问。

# 参考资料

1、Python新利器之pipenv

https://www.jianshu.com/p/00af447f0005

2、TOML简介 (转) - 孤独信徒 - 博客园

https://www.cnblogs.com/unqiang/p/6399136.html

3、pipenv与pyenv、pyenv-virtualenv的关系和使用

https://www.xingjiehu.com/2019/06/20/cjxpsmsyd00158mom667oyav9/

4、

https://www.jianshu.com/p/cdee9e4d620a

5、拥抱pipenv

https://www.jianshu.com/p/d08a4aa0008e