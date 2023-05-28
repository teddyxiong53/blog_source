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

