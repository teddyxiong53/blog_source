---
title: python之poetry管理工具
date: 2024-05-09 19:29:11
tags:
	- python
---

--

https://python-poetry.org/

# 简介

Poetry 是 Python 中用于管理项目依赖关系和构建工具的一个工具。

它可以帮助开发者更轻松地管理项目的依赖、创建虚拟环境、发布软件包等。

以下是 Poetry 的一些主要功能和特点：

1. **依赖管理**：Poetry 可以帮助开发者定义项目的依赖关系，包括所需的 Python 包、版本号、以及依赖之间的约束关系。它使用 `pyproject.toml` 文件来管理项目的依赖关系。

2. **虚拟环境管理**：Poetry 可以创建和管理项目的虚拟环境，使得项目的依赖包和版本可以被隔离和管理。开发者可以在项目目录中使用命令 `poetry env` 来管理虚拟环境。

3. **包管理**：Poetry 提供了一组命令来管理项目的 Python 包，包括安装依赖、更新依赖、卸载依赖等。开发者可以使用命令 `poetry add`、`poetry remove` 等来管理项目的依赖关系。

4. **版本管理**：Poetry 可以帮助开发者管理项目的版本号，包括主版本号、次版本号和修订版本号。开发者可以在 `pyproject.toml` 文件中定义项目的版本号。

5. **发布软件包**：Poetry 可以帮助开发者发布 Python 软件包到 PyPI（Python Package Index）上。开发者可以使用命令 `poetry publish` 来发布软件包。

6. **项目配置**：Poetry 提供了一些配置选项，可以帮助开发者定制项目的构建、发布和管理方式。开发者可以在 `pyproject.toml` 文件中设置项目的配置选项。

总的来说，Poetry 是一个强大而灵活的工具，可以帮助 Python 开发者更轻松地管理项目的依赖关系、虚拟环境、包管理、版本管理和软件包发布等任务。它的简洁的配置文件语法和强大的命令行工具使得项目管理变得更加方便和高效。

# 发展历史

Poetry 的发展历史可以追溯到 Python 社区中对于包管理工具的持续讨论和探索。以下是 Poetry 的主要发展历程：

1. **2017 年初**：Python 社区开始出现对于现有包管理工具（如 pip 和 setuptools）的一些不满，特别是在管理依赖关系和版本约束方面存在一些问题。一些开发者开始探索新的包管理工具的可能性。

2. **2017 年底**：随着 Python 社区对于包管理工具的需求不断增加，诸如 Pipenv 等新的工具开始出现。Pipenv 是一个用于管理 Python 项目依赖和虚拟环境的工具，受到了广泛关注和欢迎。

3. **2018 年初**：Poetry 项目正式启动，旨在提供一种更现代、更简单、更强大的 Python 包管理工具。Poetry 的设计灵感来自于 Node.js 的 npm 和 Rust 的 Cargo，旨在解决 Python 包管理领域的一些问题。

4. **2018 年底**：Poetry 项目发布了首个稳定版本（1.0.0），并开始受到 Python 社区的广泛关注和认可。Poetry 提供了一套简洁而强大的工具，使得 Python 开发者可以更轻松地管理项目的依赖关系、虚拟环境和包发布等任务。

5. **2020 年**：Poetry 逐渐成为 Python 社区中的主流包管理工具之一，受到越来越多开发者的青睐。Poetry 的发展进程也在不断推进，持续增加新的功能和改进现有功能。

6. **2021 年**：Poetry 继续稳步发展，发布了多个版本，不断改进和优化用户体验。它在 Python 社区中的影响力和用户基础不断扩大，成为了许多 Python 开发者的首选工具之一。

总的来说，Poetry 在 Python 包管理领域的出现填补了一些现有工具的不足，并为 Python 开发者提供了一种更现代、更简单、更强大的包管理工具，促进了 Python 生态系统的健康发展。

# poetry使用方法

使用 Poetry 可以方便地管理 Python 项目的依赖关系、虚拟环境和包发布等任务。以下是使用 Poetry 的基本方法：

### 1. 安装 Poetry

首先，需要安装 Poetry。可以通过以下命令在命令行中安装 Poetry：

```
curl -sSL https://install.python-poetry.org | python -
```

或者，如果你使用的是 Windows 系统，可以通过 PowerShell 安装：

```
(Invoke-WebRequest -Uri https://install.python-poetry.org/install.ps1 -UseBasicParsing).Content | python -
```

安装完成后，重启终端，确保 Poetry 命令已经添加到系统的 PATH 中。

### 2. 创建新项目

进入到你的项目目录，并使用以下命令创建一个新的 Poetry 项目：

```
poetry new my_project
```

这将在当前目录下创建一个名为 `my_project` 的新项目，并生成一个 `pyproject.toml` 文件，其中包含项目的元数据和依赖信息。

### 3. 添加依赖

使用 Poetry 添加项目的依赖，可以通过 `poetry add` 命令添加指定的依赖包，例如：

```
poetry add requests
```

这将会安装 `requests` 包并将其添加到项目的依赖列表中。

### 4. 安装依赖

执行以下命令安装项目的所有依赖：

```
poetry install
```

这将会根据 `pyproject.toml` 文件中的依赖信息安装项目所需的所有依赖包，并创建项目的虚拟环境。

### 5. 运行项目

运行项目中的 Python 脚本或者启动项目中的 Python 应用程序。

```
poetry run python my_script.py
```

### 6. 更新依赖

如果需要更新项目的依赖，可以使用以下命令更新指定依赖包：

```
poetry update requests
```

### 7. 发布包

如果需要发布 Python 包到 PyPI 上，可以使用以下命令发布：

```
poetry publish
```

以上是使用 Poetry 的基本方法，Poetry 还提供了更多功能和选项，可以根据具体的需求来使用。通过使用 Poetry，可以更方便地管理 Python 项目的依赖关系、虚拟环境和包发布等任务。

# 实际操作

https://python-poetry.org/docs/basic-usage/

## 新建一个项目

```
poetry new poetry-demo
```

生成的目录结构是这样：

```
poetry-demo
├── pyproject.toml
├── README.md
├── poetry_demo
│   └── __init__.py
└── tests
    └── __init__.py
```

最重要的是pyproject.toml这个文件。

看起来是这样：

```
[tool.poetry]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = ["Sébastien Eustace <sebastien@eustace.io>"]
readme = "README.md"
packages = [{include = "poetry_demo"}]

[tool.poetry.dependencies]
python = "^3.7"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 对于之前已经存在的项目

```
poetry init
```

