---
title: github使用经验
date: 2018-03-06 21:21:43
tags:
	- github

---



#  用wget下载代码zip文件

wget https://codeload.github.com/xxx/yyy/zip/master

xxx：用户名

yyy：仓库名。

不过，我们直接看到的是https://github.com/teddyxiong53/MyAlgo 这种url。

我们手动转换太麻烦。写一个Python脚本，用正则表达式来自动帮我们转换。

这个过程是，

1、在github.com和https://中间插入codeload。

2、在最后加上/zip/master。

3、默认的名字是master。不直观。我们下载完成后，自动改一下名字。

```
#!/usr/bin/python

#encoding: utf-8

import sys,os,re

repo_name = "master"

def usage():
    print "usage: ./mywget url"

def check_url(url):
    pattern = re.compile(r"([a-z]{2,})://([\S])+")
    match = pattern.match(url)
    if match:
        return True
    else:
        return False
#https://github.com/teddyxiong53/MyAlgo
def get_repo_name(url):
    match = re.search(r"(.*)\.com\/(.*)\/(.*)", url)
    #print match
    if match:
        return match.group(3)
def process_url(url):
    #get repo name
    global repo_name
    repo_name = get_repo_name(url)
    #1. add codeload after https://
    url_tmp = "https://codeload."
    url_tmp += url[8:]
    url_tmp += "/zip/master"
    return url_tmp

def main(argv):
    try:
        url = sys.argv[1]
    except Exception, e:
        usage()
        sys.exit(1)
    valid = check_url(url)
    if not valid:
        print "url is not valid"
        sys.exit(1)
    url = process_url(url)
    global repo_name
    print repo_name
    os.system("wget -c " + url)
    os.rename("master", repo_name+".zip")
if __name__ == '__main__':
    main(sys.argv)
```

脚本名字叫mywget。

```
./mywget.py https://github.com/teddyxiong53/MyAlgo
```



# 下载加速

```
192.30.253.112 assets-cdn.github.com
151.101.88.249 github.global.ssl.fastly.net
```

host文件里加上这个。速度没有看到明显提升。

但是至少不会下载时看不到进度，而且不会下载到中途认为完成了。实际上并没有完成。



# 下载子目录

有时候不想下载整个目录。只希望下载某个仓库下的子目录。怎么办？

https://minhaskamal.github.io/DownGit/#/home?url=

把你要下载的链接，输入到这里的输入框里，点击下载就好了。



# tortoisegit提交要输入密码

右键，进入设置，git的credential，选择manager - all windows users。

保存。然后提交测试一下，不用再输入了。



# workflow

看一篇文章里，提到利用github的workflow来实现借助github的服务器资源来进行padavan的代码编译。

了解一下这个过程。

# Github Actions

当然可以！GitHub Actions 是一个强大的 CI/CD 工具，可以帮助你自动化软件开发流程。以下是一步步掌握 GitHub Actions 的方法：

### 第一步：了解基本概念

1. **工作流 (Workflow)**：工作流是一个自动化过程，定义了要执行的任务。
2. **事件 (Event)**：工作流可以在特定事件发生时触发，如代码推送、拉取请求等。
3. **作业 (Job)**：工作流包含一个或多个作业，每个作业可以在一个或多个虚拟环境中运行。
4. **步骤 (Step)**：每个作业由多个步骤组成，步骤是具体的任务，可以是运行命令或调用其他操作。

### 第二步：创建你的第一个工作流

1. **创建 `.github/workflows` 目录**：
   在你的 GitHub 仓库中，创建一个目录 `.github/workflows`。

2. **添加工作流文件**：
   在该目录下创建一个 YAML 文件，例如 `ci.yml`。以下是一个简单的示例：

   ```yaml
   name: CI
   
   on: [push, pull_request]
   
   jobs:
     build:
       runs-on: ubuntu-latest
   
       steps:
         - name: Checkout code
           uses: actions/checkout@v2
   
         - name: Set up Node.js
           uses: actions/setup-node@v2
           with:
             node-version: '14'
   
         - name: Install dependencies
           run: npm install
   
         - name: Run tests
           run: npm test
   ```

### 第三步：理解工作流的结构

- **name**：工作流的名称。
- **on**：定义触发工作流的事件。
- **jobs**：定义要执行的作业。
- **steps**：在作业中定义具体的步骤。

### 第四步：运行和监控工作流

1. **提交代码**：将你的更改提交到 GitHub。
2. **查看运行状态**：
   - 转到你的 GitHub 仓库，点击 "Actions" 标签。
   - 你可以看到工作流的运行记录和状态。

### 第五步：使用动作 (Actions)

- GitHub 提供了很多现成的动作，你可以在社区中找到许多有用的动作。
- 在步骤中使用动作的基本语法是：

  ```yaml
  - name: Action name
    uses: username/repo@version
  ```

### 第六步：调试和优化

- 如果工作流失败，点击失败的步骤查看日志，找出问题所在。
- 你可以使用条件来控制步骤的执行，例如：

  ```yaml
  if: github.event_name == 'push'
  ```

### 第七步：深入学习

- 阅读 [GitHub Actions 官方文档](https://docs.github.com/en/actions) 以获取更多高级功能。
- 尝试使用矩阵构建、缓存依赖项等高级特性。

### 总结

通过以上步骤，你可以逐步掌握 GitHub Actions 的基本用法。建议多实践，试着创建不同的工作流以加深理解。祝你好运！



https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions

这里可以找到actions

https://github.com/marketplace?type=actions

# 参考资料

1、解决GitHub下载速度太慢的问题

https://blog.csdn.net/qing666888/article/details/79123742

2、TortoiseGit保存用户名和密码的方法

https://www.cnblogs.com/sapho/p/6140331.html