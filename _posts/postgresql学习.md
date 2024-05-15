---
title: postgresql学习
date: 2020-12-09 16:28:30
tags:
	- 数据库
---

--

# 简介

PostgreSQL（通常简称为Postgres）是备受推崇的选择之一。

它是一种功能强大的开源关系型数据库系统，

具有高度可扩展性、稳定性和安全性。

PostgreSQL 提供了许多先进的功能，

包括复杂的查询、事务处理、触发器、视图和存储过程等。

它还支持多种编程语言和数据类型，并具有强大的扩展性，用户可以根据需要添加自定义功能。

PostgreSQL 的社区庞大活跃，提供了丰富的文档、教程和支持，使其成为许多企业和开发者的首选数据库解决方案之一。

# 发展历史

以下是 PostgreSQL 的主要发展历史：

| 时间   | 事件                                           |
| ------ | ---------------------------------------------- |
| 1986年 | 开始作为 POSTGRES 项目在加州大学伯克利分校开发 |
| 1995年 | 发布了第一个稳定版本 PostgreSQL 6.0            |
| 1996年 | 首次开源发布                                   |
| 2000年 | 发布了版本 7.0，引入了 MVCC（多版本并发控制）  |
| 2005年 | 发布了版本 8.0，引入了表空间、保存点等功能     |
| 2008年 | 发布了版本 8.3，引入了在线表空间重新组织功能   |
| 2010年 | 发布了版本 9.0，引入了流复制和热备份等功能     |
| 2013年 | 发布了版本 9.3，引入了可扩展性和JSONB支持      |
| 2016年 | 发布了版本 9.6，引入了并行查询功能             |
| 2017年 | 发布了版本 10.0，引入了逻辑复制和全文搜索功能  |
| 2020年 | 发布了版本 13.0，引入了更多的性能优化和改进    |

PostgreSQL 的发展历程充满了创新，不断引入新的功能和改进，使其成为一款功能强大、稳定可靠的开源数据库系统。

# 在ubuntu下的安装实验

安装 PostgreSQL 在 Ubuntu 上是相对简单的。以下是一些基本步骤：

1. **更新软件包列表**：
   在终端中执行以下命令，确保系统的软件包列表是最新的：

   ```bash
   sudo apt update
   ```

2. **安装 PostgreSQL**：
   使用以下命令安装 PostgreSQL：

   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

   这将安装 PostgreSQL 服务器和一些附加组件。

3. **启动 PostgreSQL 服务**：
   安装完成后，PostgreSQL 服务会自动启动。如果没有自动启动，可以使用以下命令手动启动：

   ```bash
   sudo service postgresql start
   ```

4. **验证安装**：
   使用以下命令验证 PostgreSQL 是否成功安装：

   ```bash
   sudo -u postgres psql -c "SELECT version();"
   ```

   如果成功安装，将显示 PostgreSQL 的版本信息。

5. **创建新用户**（可选）：
   可以创建一个新的 PostgreSQL 用户来进行管理。执行以下命令以创建新用户：

   ```bash
   sudo -u postgres createuser --interactive
   ```

   接下来，按照提示输入新用户的名称，并选择是否允许该用户创建数据库。

6. **创建新数据库**（可选）：
   可以使用新创建的用户登录到 PostgreSQL 并创建新的数据库。执行以下命令以登录到 PostgreSQL：

   ```bash
   sudo -u [新用户的名称] psql
   ```

   登录后，可以执行 SQL 命令来创建新的数据库、表等。

通过这些步骤，您应该能够在 Ubuntu 上成功安装和配置 PostgreSQL。

# docker方式启动

使用 Docker 启动 PostgreSQL 是一种方便快捷的方法，可以轻松创建和管理 PostgreSQL 实例。以下是使用 Docker 启动 PostgreSQL 的基本步骤：

1. **安装 Docker**：
   如果您的系统上尚未安装 Docker，请按照 Docker 官方文档的说明进行安装：[Get Docker](https://docs.docker.com/get-docker/)。

2. **拉取 PostgreSQL 镜像**：
   在终端中执行以下命令拉取 PostgreSQL 官方镜像：

   ```bash
   docker pull postgres
   ```

3. **运行 PostgreSQL 容器**：
   使用以下命令在 Docker 中运行 PostgreSQL 容器：

   ```bash
   docker run --name my_postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
   ```

   这将在后台运行一个名为 `my_postgres` 的 PostgreSQL 容器，并设置了 `POSTGRES_PASSWORD` 环境变量为 `mysecretpassword`，您可以根据需要更改密码。

4. **验证容器是否运行**：
   使用以下命令验证容器是否正在运行：

   ```bash
   docker ps
   ```

   如果看到 `my_postgres` 容器正在运行，则表示 PostgreSQL 容器已成功启动。

5. **连接到 PostgreSQL**：
   您可以使用以下命令连接到正在运行的 PostgreSQL 容器：

   ```bash
   docker exec -it my_postgres psql -U postgres
   ```

   这将连接到 PostgreSQL 数据库，并要求输入密码。输入您在步骤 3 中设置的密码（默认为 `mysecretpassword`）即可登录到 PostgreSQL。

通过这些步骤，您应该能够使用 Docker 成功启动 PostgreSQL 容器，并且可以通过 `psql` 工具连接到 PostgreSQL 数据库。

# psql工具用法

`psql` 是 PostgreSQL 提供的交互式终端工具，用于连接和管理 PostgreSQL 数据库。以下是一些常见的 `psql` 工具用法：

1. **连接到 PostgreSQL 数据库**：
   使用以下命令连接到本地 PostgreSQL 数据库：

   ```bash
   psql -U username -d dbname
   ```

   - `-U`：指定要连接的用户名。
   - `-d`：指定要连接的数据库名称。

2. **连接到远程 PostgreSQL 数据库**：
   如果要连接到远程 PostgreSQL 数据库，可以使用以下命令：

   ```bash
   psql -h hostname -U username -d dbname
   ```

   - `-h`：指定 PostgreSQL 服务器的主机名或 IP 地址。

3. **执行 SQL 查询**：
   连接到数据库后，您可以直接在 `psql` 提示符下执行 SQL 查询，例如：

   ```sql
   SELECT * FROM tablename;
   ```

4. **退出 `psql`**：
   在 `psql` 提示符下，执行以下命令可以退出 `psql`：

   ```sql
   \q
   ```

5. **查看帮助信息**：
   在 `psql` 提示符下，执行以下命令可以查看 `psql` 的帮助信息：

   ```sql
   \?
   ```

6. **查看当前连接信息**：
   在 `psql` 提示符下，执行以下命令可以查看当前连接的数据库和用户信息：

   ```sql
   \conninfo
   ```

7. **列出数据库**：
   在 `psql` 提示符下，执行以下命令可以列出当前 PostgreSQL 服务器上的所有数据库：

   ```sql
   \l
   ```

这些是一些 `psql` 工具的基本用法，让您能够连接到 PostgreSQL 数据库并执行一些基本的数据库操作。

# postgresql和mysql有多大的差异

PostgreSQL 和 MySQL 是两种不同的关系型数据库管理系统 (RDBMS)，它们在很多方面都有一些显著的差异。以下是它们之间的一些主要区别：

| 特征                   | PostgreSQL                                          | MySQL                                                |
| ---------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| 开发语言               | 使用 C 语言编写                                     | 使用 C 和 C++ 语言编写                               |
| 许可证                 | PostgreSQL 使用 BSD 许可证，更自由                  | MySQL 使用 GPL 许可证，有一些商业版本                |
| 存储引擎               | 支持多种存储引擎，包括 B-Tree、Hash、GIN、GiST 等   | 主要使用 InnoDB 和 MyISAM 存储引擎                   |
| 外键支持               | 完全支持外键约束                                    | MyISAM 引擎不支持外键约束                            |
| JSON 支持              | 从版本 9.2 开始支持 JSON 类型和 JSONB 存储格式      | 从版本 5.7 开始支持 JSON 类型                        |
| 全文搜索               | 支持全文搜索功能，并提供了全文搜索索引              | 提供了全文搜索功能，但在某些方面不如 PostgreSQL 完善 |
| MVCC（多版本并发控制） | 使用 MVCC 实现事务隔离级别                          | 也使用 MVCC，但实现略有不同                          |
| 默认字符集             | 默认字符集为 UTF-8                                  | 默认字符集为 UTF-8 或 Latin1                         |
| ACID 支持              | 支持 ACID（原子性、一致性、隔离性、持久性）事务特性 | 同样支持 ACID 事务特性                               |
| 存储过程和触发器       | 支持存储过程和触发器                                | 同样支持存储过程和触发器                             |
| 社区和生态系统         | 社区庞大，提供了丰富的文档和支持                    | 社区同样庞大，有大量的文档和支持                     |

总的来说，PostgreSQL 和 MySQL 都是功能强大的关系型数据库系统，但在一些特定的功能和使用场景下可能有不同的优劣。选择使用哪个取决于您的具体需求、偏好以及项目的特点。

# postgresql使用在哪些场景

PostgreSQL 在许多场景下都是一种理想的选择，特别是在需要稳定性、可扩展性和高级功能的情况下。以下是一些适合使用 PostgreSQL 的常见场景：

1. **Web 应用程序**：
   PostgreSQL 可以作为后端数据库用于各种 Web 应用程序，包括电子商务网站、博客、社交网络等。其支持复杂的查询、事务处理和数据完整性，适合处理各种类型的数据。

2. **地理信息系统 (GIS)**：
   PostgreSQL 提供了丰富的地理空间数据类型和功能，适用于构建地理信息系统、地理定位服务和地理数据分析等应用。

3. **数据分析和报告**：
   由于 PostgreSQL 支持复杂的查询和分析功能，因此它适合用于存储和分析大规模数据集，并生成复杂的报告和分析结果。

4. **在线事务处理 (OLTP)**：
   由于 PostgreSQL 提供了强大的事务支持和高并发性能，因此它适合用于处理在线事务处理 (OLTP) 应用程序，如电子商务网站、银行系统等。

5. **数据仓库**：
   PostgreSQL 提供了丰富的数据类型和索引功能，适合用作数据仓库存储和分析大规模数据集。

6. **金融和保险**：
   由于 PostgreSQL 支持 ACID 事务特性和高级安全功能，因此它适合用于金融和保险行业的应用程序，如交易处理系统、保单管理系统等。

7. **科学研究**：
   由于 PostgreSQL 支持复杂的数据类型和函数，因此它适合用于科学研究和数据分析领域，如生物信息学、气象学等。

总的来说，PostgreSQL 是一种功能丰富、稳定可靠的关系型数据库管理系统，适用于许多不同的应用场景。

# python连接操作postgresql

要在 Python 中连接和操作 PostgreSQL 数据库，您可以使用 `psycopg2` 模块。以下是连接和操作 PostgreSQL 数据库的基本步骤：

1. **安装 psycopg2**：
   首先，确保您已经安装了 `psycopg2` 模块。如果尚未安装，可以使用 pip 进行安装：

   ```bash
   pip install psycopg2
   ```

2. **导入 psycopg2 模块**：
   在 Python 脚本中导入 `psycopg2` 模块：

   ```python
   import psycopg2
   ```

3. **连接到 PostgreSQL 数据库**：
   使用 `psycopg2.connect()` 函数连接到 PostgreSQL 数据库，并获取数据库连接对象和游标对象：

   ```python
   try:
       connection = psycopg2.connect(
           user="your_username",
           password="your_password",
           host="your_host",
           port="your_port",
           database="your_database"
       )
       cursor = connection.cursor()
       print("Connected to PostgreSQL")
   except (Exception, psycopg2.Error) as error:
       print("Error while connecting to PostgreSQL:", error)
   ```

   请替换 `your_username`、`your_password`、`your_host`、`your_port` 和 `your_database` 分别为您的 PostgreSQL 数据库的用户名、密码、主机名、端口号和数据库名称。

4. **执行 SQL 查询**：
   使用游标对象执行 SQL 查询，并处理查询结果：

   ```python
   try:
       cursor.execute("SELECT * FROM your_table")
       rows = cursor.fetchall()
       for row in rows:
           print(row)
   except (Exception, psycopg2.Error) as error:
       print("Error while executing SQL query:", error)
   ```

   这将执行一个简单的查询并打印结果。您可以根据需要执行任意 SQL 查询。

5. **关闭连接**：
   在完成所有数据库操作后，务必关闭游标和数据库连接：

   ```python
   if connection:
       cursor.close()
       connection.close()
       print("PostgreSQL connection is closed")
   ```

通过这些步骤，您可以在 Python 中连接到 PostgreSQL 数据库，并执行各种数据库操作。

