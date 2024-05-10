---
title: openfaas快速创建管理python虚拟环境
date: 2023-05-28 17:42:11
tags:
	- python
---

--

其实我一直想要有这样一个平台。

但是一直没有找到。现在有了chatgpt，就问到了这个东西。

现在看看怎么做。

需要安装了docker。

然后执行这个命令：

```
url -sLS https://get.arkade.dev | sh
```

# python虚拟环境

Python 虚拟环境是一种用于管理项目依赖项和隔离项目环境的工具。

它允许您在单个系统上同时运行多个 Python 项目，

每个项目都可以具有其自己的依赖项，而不会影响其他项目。

虚拟环境通常使用 Python 内置的 `venv` 模块或第三方工具（如 `virtualenv`）创建。

以下是 Python 虚拟环境的一些重要特性和优点：

1. **依赖隔离**：每个虚拟环境都有自己独立的 Python 解释器和依赖项，使得不同项目的依赖项不会相互干扰。

2. **项目隔离**：每个项目可以有自己的虚拟环境，使得项目之间的开发和部署更加独立和灵活。

3. **版本控制**：虚拟环境可以轻松地保存项目所需的 Python 版本和依赖项版本，确保项目的稳定性和可重复性。

4. **环境配置**：可以在虚拟环境中安装和管理项目所需的任何软件包和工具，而不会影响系统全局环境。

5. **轻量化**：虚拟环境通常只包含项目所需的依赖项，因此相对于全局安装依赖项，它们占用的空间更少。

在使用虚拟环境时，通常的工作流程包括以下步骤：

1. 创建虚拟环境：使用 `venv` 或 `virtualenv` 创建一个新的虚拟环境。

2. 激活虚拟环境：在项目目录中执行激活脚本，将当前 shell 的环境切换到虚拟环境中。

3. 安装依赖项：在虚拟环境中使用 pip 安装项目所需的所有依赖项。

4. 运行项目：在虚拟环境中执行项目的代码或命令。

5. 停用虚拟环境：完成项目开发或运行后，可以退出虚拟环境并返回到全局环境。

Python 虚拟环境是 Python 开发中的一项重要工具，它使得项目管理和环境配置更加简单和可控。

## venv和virtualenv关系

`venv` 和 `virtualenv` 都是用于创建 Python 虚拟环境的工具，但它们之间有一些区别。

1. **`venv`**:
   - `venv` 是 Python 3.3 版本引入的标准库，位于 Python 的标准库中，不需要额外安装。
   - `venv` 创建的虚拟环境是纯粹的 Python 环境，只包含 Python 解释器和标准库，不包含任何第三方库。
   - `venv` 可以创建具有不同 Python 版本的虚拟环境，每个虚拟环境都与其相应的 Python 版本关联。

2. **`virtualenv`**:
   - `virtualenv` 是一个独立的第三方工具，可通过 pip 安装：`pip install virtualenv`。
   - `virtualenv` 创建的虚拟环境可以包含任何 Python 版本，并且可以使用系统中已安装的 Python 解释器。
   - `virtualenv` 可以创建更加灵活和定制化的虚拟环境，例如可以选择是否包含系统全局库、是否共享系统 site-packages 目录等。

虽然 `venv` 是 Python 提供的官方标准库，但 `virtualenv` 在某些方面更加灵活和功能丰富，因此在实际使用中，有些人更喜欢使用 `virtualenv`。但需要注意的是，Python 3.3+ 版本中已经内置了 `venv`，因此如果您使用的是较新版本的 Python，并且只需创建纯粹的 Python 虚拟环境，那么使用 `venv` 是一个不错的选择。



# pyenv

我是在查找在ubuntu下安装python3.12的时候，找到这个的。

如果您的系统中没有安装 Python 3.12，您可以通过源代码编译安装 Python 3.12 或者使用第三方工具来安装。以下是两种可选的方法：

1. **通过源代码编译安装**：
   - 首先，下载 Python 3.12 的源代码压缩包并解压缩。
   - 进入解压后的 Python 3.12 目录，并执行以下命令进行编译和安装：

```bash
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

   - 这将编译并安装 Python 3.12，安装路径可能为 `/usr/local/bin/python3.12`。

2. **使用第三方工具安装**：
   - 您可以使用第三方工具，如 `pyenv` 或 `asdf` 来管理多个 Python 版本并安装 Python 3.12。
   - 以下是使用 `pyenv` 安装 Python 3.12 的示例：

```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 在 .bashrc 或 .bash_profile 中添加 pyenv 初始化脚本
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

# 安装 Python 3.12
pyenv install 3.12.0
```

   - 安装完成后，您可以使用 `pyenv global 3.12.0` 来设置全局默认的 Python 版本，或者使用 `pyenv local 3.12.0` 来将特定目录下的 Python 版本设置为 Python 3.12。

无论您选择哪种方法，一旦安装了 Python 3.12，您就可以按照之前提供的步骤创建 Python 3.12 的虚拟环境，并在其中进行开发工作。

## pyenv简介

`pyenv` 是一个 Python 版本管理工具，可以让您在系统中轻松管理多个 Python 版本。

使用 `pyenv`，您可以方便地安装、管理和切换不同版本的 Python，

同时还可以为每个项目创建独立的 Python 环境，

从而避免全局安装和版本冲突的问题。

以下是 `pyenv` 的一些主要特点和功能：

1. **安装多个 Python 版本**：`pyenv` 允许您在系统中同时安装多个不同版本的 Python。您可以从源代码编译安装 Python，也可以使用 `pyenv` 提供的插件来安装特定版本的 Python。

2. **全局和局部版本切换**：您可以使用 `pyenv global` 命令设置全局默认的 Python 版本，也可以使用 `pyenv local` 命令在特定目录下设置局部 Python 版本。这样，您可以根据需要轻松切换不同的 Python 版本。

3. **创建虚拟环境**：`pyenv` 可以与 `pyenv-virtualenv` 插件一起使用，用于创建和管理虚拟环境。虚拟环境是与特定项目关联的 Python 环境，可以独立于系统全局环境和其他项目环境。

4. **自动激活**：`pyenv` 可以自动激活虚拟环境，==使得进入项目目录时自动切换到相应的虚拟环境，而在离开项目目录时自动切换回全局或其他虚拟环境。==

5. **插件系统**：`pyenv` 提供了丰富的插件系统，可以扩展其功能，例如支持安装非官方 Python 版本、管理 Python 环境的依赖项、自动更新等。

`pyenv` 是一个强大而灵活的 Python 版本管理工具，特别适用于需要同时管理多个 Python 版本和项目的开发者。通过 `pyenv`，您可以轻松地创建和管理 Python 环境，避免版本冲突和依赖问题，提高开发效率和项目可维护性。

## pyenv发展历史

`pyenv` 是由日本开发者 Yuki Nishijima 创建的一个 Python 版本管理工具，旨在帮助开发者轻松地管理多个 Python 版本。`pyenv` 的发展历史可以追溯到 2011 年左右，其初版受到了 Ruby 版本管理工具 `rbenv` 的启发。

以下是 `pyenv` 的主要发展历程：

1. **初始版本**：
   - 初始版本的 `pyenv` 由 Yuki Nishijima 在 GitHub 上创建，并于 2011 年左右首次发布。该版本提供了基本的功能，包括安装和管理多个 Python 版本，以及设置全局和局部 Python 版本。

2. **插件系统**：
   - 随着用户需求的增加，`pyenv` 引入了插件系统，允许开发者编写自定义插件来扩展 `pyenv` 的功能。这为 `pyenv` 的进一步发展和定制提供了更多的可能性。

3. **`pyenv-virtualenv` 插件**：
   - `pyenv-virtualenv` 是一个用于创建和管理虚拟环境的插件，使得开发者可以在项目级别管理 Python 环境。这个插件大大提高了 `pyenv` 的灵活性和实用性。

4. **社区贡献**：
   - 随着时间的推移，`pyenv` 的用户社区不断壮大，许多开发者贡献了各种各样的功能和改进。这些社区贡献者为 `pyenv` 的发展和改进做出了重要贡献。

5. **持续维护和更新**：
   - 至今，`pyenv` 仍然在不断地维护和更新。开发者持续改进 `pyenv` 的稳定性、性能和用户体验，确保它与最新的 Python 发行版和操作系统保持兼容。

`pyenv` 作为一个成熟的 Python 版本管理工具，已经成为许多 Python 开发者的首选工具之一。它简单易用，功能强大，为开发者提供了方便和灵活的 Python 环境管理方案。

## pyenv和venv、virtualenv关系

`pyenv`、`venv` 和 `virtualenv` 是 Python 开发中常用的三种不同的工具，它们各自用于不同的目的，但也可以相互结合使用。

1. **pyenv**:
   - `pyenv` 是一个 Python 版本管理工具，用于在系统中安装和管理多个不同版本的 Python。它可以让用户方便地切换全局和局部的 Python 版本，以及为项目创建独立的 Python 环境。`pyenv` 可以与 `pyenv-virtualenv` 插件一起使用，来管理虚拟环境。

2. **venv**:
   - `venv` 是 Python 3.3+ 版本中内置的标准库模块，用于创建 Python 虚拟环境。虚拟环境是一个与系统全局环境隔离的 Python 环境，可以在其中安装和管理项目的依赖项。通过 `venv` 创建的虚拟环境通常只包含标准库和特定版本的 Python 解释器。

3. **virtualenv**:
   - `virtualenv` 是一个第三方工具，用于创建 Python 虚拟环境。与 `venv` 类似，`virtualenv` 也可以创建独立的 Python 环境，但它可以在任何 Python 版本下使用，并且提供了更多的定制选项。通过 `virtualenv` 创建的虚拟环境可以包含第三方库和其他系统全局环境的内容。

关于它们之间的关系：

- `pyenv` 可以用来管理系统中安装的多个 Python 版本，包括全局默认版本和局部版本。
- `venv` 和 `virtualenv` 则是用于创建项目级别的 Python 虚拟环境，使得项目可以在独立的环境中运行，并且可以隔离不同项目的依赖关系。
- `pyenv` 可以与 `pyenv-virtualenv` 插件一起使用，来管理虚拟环境。在这种情况下，`pyenv` 用于管理全局和局部的 Python 版本，而 `pyenv-virtualenv` 用于创建和管理虚拟环境。

综上所述，这三种工具各有其用途，可以根据具体需求选择使用其中的一种或多种。例如，您可以使用 `pyenv` 来管理系统中的 Python 版本，并使用 `venv` 或 `virtualenv` 在项目中创建虚拟环境来管理项目的依赖项。

## pyenv基本用法

以下是 `pyenv` 的一些基本用法：

1. **安装 Python 版本**：
   - 使用 `pyenv install` 命令安装指定版本的 Python。例如，要安装 Python 3.12.0，可以运行以下命令：

```bash
pyenv install 3.12.0
```

2. **列出已安装的 Python 版本**：
   - 使用 `pyenv versions` 命令列出当前系统上已安装的所有 Python 版本。例如：

```bash
pyenv versions
```

3. **设置全局默认 Python 版本**：
   - 使用 `pyenv global` 命令设置系统的全局默认 Python 版本。例如，要将全局默认 Python 版本设置为 Python 3.12.0，可以运行以下命令：

```bash
pyenv global 3.12.0
```

4. **设置局部 Python 版本**：
   - 使用 `pyenv local` 命令在特定目录下设置局部 Python 版本。例如，要在当前目录下设置 Python 版本为 Python 3.12.0，可以运行以下命令：

```bash
pyenv local 3.12.0
```

5. **创建虚拟环境**：
   - 使用 `pyenv virtualenv` 命令创建一个虚拟环境。例如，要在 Python 3.12.0 版本上创建一个名为 `myenv` 的虚拟环境，可以运行以下命令：

```bash
pyenv virtualenv 3.12.0 myenv
```

6. **激活虚拟环境**：
   - 使用 `pyenv activate` 命令激活一个已存在的虚拟环境。例如，要激活名为 `myenv` 的虚拟环境，可以运行以下命令：

```bash
pyenv activate myenv
```

7. **退出虚拟环境**：
   - 使用 `pyenv deactivate` 命令退出当前激活的虚拟环境。例如：

```bash
pyenv deactivate
```

这些是 `pyenv` 的一些基本用法，您可以根据自己的需求使用这些命令来管理 Python 版本和环境。

# openfaas



```
arkade get faas-cli
```



看了一下这个方案。太复杂了。

需要安装k8s。



最简单可靠的方式，还是创建docker的方式来做。



# 用flask构建一个web界面调用virtualenvwrapper

```
 sudo pip install virtualenvwrapper
```

设置环境：

```
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3  # 根据你的 Python 安装路径进行调整
source /usr/local/bin/virtualenvwrapper.sh  # 根据 virtualenvwrapper.sh 的实际位置进行调整

```

下面是一个基于 Flask 的简单示例，演示如何使用 Flask 调用 Virtualenvwrapper 来管理 Python 虚拟环境的 Web 界面：

```python
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    # 获取当前所有的虚拟环境列表
    envs = subprocess.check_output(['lsvirtualenv', '-b']).decode().splitlines()
    return render_template('index.html', envs=envs)

@app.route('/create', methods=['POST'])
def create():
    # 创建新的虚拟环境
    env_name = request.form['env_name']
    subprocess.call(['mkvirtualenv', env_name])
    return 'Success'

@app.route('/delete', methods=['POST'])
def delete():
    # 删除指定的虚拟环境
    env_name = request.form['env_name']
    subprocess.call(['rmvirtualenv', env_name])
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
```

上述示例中，我们使用 Flask 创建了一个简单的 Web 应用。在主页 ("/") 中，我们使用 `lsvirtualenv` 命令获取当前所有的虚拟环境列表，并将其传递给模板进行渲染展示。在创建和删除虚拟环境的路由 ("/create" 和 "/delete") 中，我们通过调用 `mkvirtualenv` 和 `rmvirtualenv` 命令来创建和删除虚拟环境。

注意，为了运行这个示例，你需要先安装 Flask 和 Virtualenvwrapper，并确保你的系统上已正确配置 Virtualenvwrapper。

在模板文件 `index.html` 中，你可以自定义展示虚拟环境列表、创建和删除虚拟环境的表单等。你可以根据自己的需求扩展和美化界面。

这只是一个简单示例，你可以根据自己的需求和具体场景来扩展和定制。你还可以添加其他功能，如切换虚拟环境、安装/卸载 Python 包等。根据 Virtualenvwrapper 的文档和命令行工具，你可以在 Flask 应用中调用相应的命令来实现更多功能。

# 参考资料



https://zhuanlan.zhihu.com/p/601314424

