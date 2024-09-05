---
title: sqlite代码分析
date: 2023-05-25 13:43:11
tags:
	- sqlite
---

--

# 资源收集

https://huili.github.io/sqlite/sqliteintro.html

# 代码结构

SQLite3是一个开源的嵌入式关系型数据库引擎，其源代码非常庞大且复杂。在这里，我将提供一个大致的概述，介绍SQLite3代码的组织结构和主要模块。

1. 核心模块：
   - `sqlite3.c`：这是SQLite3的核心代码文件，包含了数据库引擎的主要实现。它实现了SQL解析、查询处理、事务管理、索引和数据存储等核心功能。
   - `sqlite3.h`：这是SQLite3的头文件，定义了API接口和数据结构，供外部程序使用。
   - `sqlite3ext.h`：这是SQLite3的扩展接口头文件，用于开发和加载SQLite3的扩展模块。

2. 查询优化：
   - `select.c`：这个模块负责查询优化，包括语义分析、查询计划生成和执行计划等。
   - `where.c`：这个模块实现了WHERE子句的解析和处理，用于查询条件的评估和优化。

3. 存储和索引：
   - `pager.c`：这个模块实现了SQLite3的页面管理和缓存机制，负责数据的读写和缓存控制。
   - `btree.c`：这个模块实现了B树索引的创建和维护，用于加速数据的检索和查询。
   - `vdbe.c`：这个模块实现了虚拟数据库引擎（Virtual Database Engine），负责执行SQL语句和管理虚拟机的执行。

4. 事务和并发控制：
   - `transaction.c`：这个模块实现了SQLite3的事务管理，包括事务的开始、提交和回滚等操作。
   - `lock.c`：这个模块实现了SQLite3的并发控制机制，用于处理并发访问和资源锁定。

除了上述主要模块之外，SQLite3还包含了许多其他的辅助模块，用于处理错误处理、内存管理、编码转换、日期时间处理等功能。

请注意，这只是对SQLite3代码的一个简要概述，并不能涵盖所有细节和模块。要深入了解SQLite3的源代码，建议您直接访问SQLite3的官方源代码仓库，并阅读相关文档和注释。

# sqlite的FTS1/2/3这些是什么

SQLite 的 FTS（Full-Text Search）扩展用于实现全文搜索功能。FTS1、FTS2 和 FTS3 是 SQLite 的不同版本的全文搜索扩展，随着版本的演进，它们引入了更多的功能和改进。

### FTS1

- **基础功能**：FTS1 是最早的版本，提供基本的全文搜索功能。
- **限制**：功能相对简单，支持的查询和索引功能有限。

### FTS2

- **改进**：引入了一些新特性，例如：
  - 支持短语匹配。
  - 可以进行全文索引的增量更新。
- **性能**：在性能和查询效率上有所提升。
- **灵活性**：支持更复杂的查询。

### FTS3

- **更强大的功能**：
  - 支持多种查询操作，如布尔查询（AND、OR、NOT）。
  - 支持排序和权重。
  - 支持 `prefix` 查询（前缀匹配）。
- **改进的索引机制**：更高效的索引构建。
- **版本兼容性**：允许在同一数据库中使用多个 FTS 表。

### 使用示例

创建 FTS3 表的示例：

```sql
CREATE VIRTUAL TABLE articles USING fts3(
    title TEXT,
    content TEXT
);
```

插入数据：

```sql
INSERT INTO articles (title, content) VALUES ('Hello World', 'This is a test.');
```

进行搜索：

```sql
SELECT * FROM articles WHERE content MATCH 'test';
```

### 总结

SQLite 的 FTS1、FTS2 和 FTS3 版本提供了逐步增强的全文搜索能力。FTS3 是最先进的版本，提供了更多的功能和更高的性能，适合需要复杂搜索功能的应用程序。