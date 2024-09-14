---
title: git之cgit使用
date: 2024-08-06 18:51:28
tags:
	- git
---

--





# cgit怎么安装

要在你的服务器上安装和配置 cgit，可以按照以下步骤操作。以 Ubuntu 系统为例：

### 1. 安装必要的依赖
首先，安装 cgit 及其依赖项：

```bash
sudo apt update
sudo apt install cgit fcgiwrap nginx git
```

### 2. 配置 Git 仓库目录
创建一个用于存放 Git 仓库的目录：

```bash
sudo mkdir -p /var/www/git
sudo chown -R www-data:www-data /var/www/git
```

### 3. 初始化示例 Git 仓库
在该目录下创建并初始化一些示例 Git 仓库：

```bash
cd /var/www/git
sudo mkdir -p xx/a/b.git xx/a/c.git xx/a/d.git
sudo git init --bare xx/a/b.git
sudo git init --bare xx/a/c.git
sudo git init --bare xx/a/d.git
```

### 4. 配置 cgit
编辑 cgit 配置文件 `/etc/cgitrc`：

```bash
sudo nano /etc/cgitrc
```

添加如下内容：

```plaintext
# CGit配置文件

# 全局设置
css=/cgit.css
logo=/cgit.png
favicon=/favicon.ico

# 缓存设置
cache-root=/var/cache/cgit

# 存储库根目录
root-title=My Repositories
root-desc=This is a simple cgit setup
scan-path=/var/www/git

# 示例仓库
section=xx/a
repo.url=xx/a/b.git
repo.path=/var/www/git/xx/a/b.git
repo.desc=Repository b under xx/a

repo.url=xx/a/c.git
repo.path=/var/www/git/xx/a/c.git
repo.desc=Repository c under xx/a

repo.url=xx/a/d.git
repo.path=/var/www/git/xx/a/d.git
repo.desc=Repository d under xx/a
```

### 5. 配置 Nginx
配置 Nginx 来提供 cgit 的服务。编辑 Nginx 配置文件：

```bash
sudo nano /etc/nginx/sites-available/default
```

将其内容替换为：

```plaintext
server {
    listen 80;
    server_name localhost;

    location /cgit {
        alias /usr/share/cgit;
    }

    location /cgit.css {
        alias /usr/share/cgit/cgit.css;
    }

    location /cgit.png {
        alias /usr/share/cgit/cgit.png;
    }

    location /favicon.ico {
        alias /usr/share/cgit/favicon.ico;
    }

    location / {
        fastcgi_pass  unix:/var/run/fcgiwrap.socket;
        include       fastcgi_params;
        fastcgi_param SCRIPT_FILENAME /usr/lib/cgit/cgit.cgi;
    }
}
```

### 6. 重启服务
重启 Nginx 和 fcgiwrap 服务：

```bash
sudo systemctl restart nginx
sudo systemctl restart fcgiwrap
```

### 7. 访问 cgit
现在你可以通过浏览器访问你的 cgit 安装，查看和管理你的 Git 仓库。访问 `http://your-server-ip/` 或 `http://localhost/`。

通过以上步骤，你可以成功安装和配置 cgit，并在网页上浏览你的 Git 仓库的层级结构。

# cgit的仓库可以有路径划分，github不能路径划分

是的，CGit 支持将仓库组织在不同的路径下，允许你根据项目或团队进行分层管理。相比之下，GitHub 的仓库通常是扁平结构，所有仓库都在同一层级下，无法直接进行路径划分。

### CGit 的路径划分

1. **多层目录结构**：
   - 在 CGit 中，你可以将仓库放在不同的子目录下，例如：
     ```
     /path/to/repositories/projectA/repo1.git
     /path/to/repositories/projectB/repo2.git
     ```

2. **配置方式**：
   - 在 CGit 的配置文件中，可以通过设置 `repo.path` 指定仓库的具体路径。

### GitHub 的结构

1. **扁平结构**：
   - GitHub 不支持在仓库中创建子目录结构，所有的仓库都处于同一级别。

2. **团队组织**：
   - 虽然 GitHub 提供了组织和团队功能来管理多个仓库，但每个仓库仍然是独立的，无法通过路径划分来组织。

### 总结

CGit 提供了灵活的路径管理，适合需要将仓库按项目或系统进行分类的场景。而 GitHub 更适合公共或共享的开源项目，强调社区和协作。根据你的需求选择合适的工具。
