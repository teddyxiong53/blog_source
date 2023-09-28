---
title: json之了解
date: 2018-02-06 17:04:12
tags:
	- json

---



# 基本情况

json是JavaScript Object Notation，字面含义是JavaScript对象注释。

json语法是JavaScript语法的一个子集。



基本规则：

1、基于键值对。都用引号括起来。

2、数据用逗号分开。

3、大括号保存对象。表示某几个字段是属于同一个对象。

4、中括号保存数组。



# 相关话题

作为配置文件，哪种格式是比较好的。

常见的配置文件格式有：

1、ini。古老实用。但是不能装很复杂的数据。

2、yml。有个减号，有点不爽。

3、json。不能加注释，这个比较坑。而且多写的逗号会有问题。其实不适合。

4、xml。



好的配置文件应该满足：

1、规则简单。

2、人类友好。

3、支持简单的层级关系。

4、允许注释。

# RFC6901

RFC 6901 是一份由 IETF（Internet Engineering Task Force）发布的标准文档，它定义了 JSON Pointer（JSON 指针）规范。JSON Pointer 是一种用于在 JSON 文档中定位特定值的轻量级方法。JSON Pointer 的设计目的是为了让开发者能够以简洁的方式引用 JSON 数据结构中的特定元素，类似于 XPath 用于 XML 文档的定位。

以下是 RFC 6901 的主要内容和说明：

1. **JSON Pointer 格式**：JSON Pointer 是一个由零个或多个“引用令牌”（reference tokens）组成的字符串，每个引用令牌之间用斜杠字符 `/` 分隔。引用令牌可以是空字符串或包含字母、数字和其他特殊字符的字符串。

2. **JSON Pointer 语法示例**：以下是 JSON Pointer 的一些示例：
   - `""` 表示整个 JSON 文档。
   - `"/foo"` 表示 JSON 文档中的顶级属性 "foo"。
   - `"/foo/0"` 表示 JSON 文档中属性 "foo" 的第一个元素（数组或对象）。
   - `"/foo/bar"` 表示 JSON 文档中属性 "foo" 中的属性 "bar"。

3. **解析规则**：JSON Pointer 的解析规则包括以下内容：
   - 当 JSON Pointer 是空字符串时，表示引用整个 JSON 文档。
   - 引用令牌可以引用对象的属性名或数组的索引。
   - 使用斜杠 `/` 分隔引用令牌。
   - 引用令牌中的特殊字符需要进行转义，例如 `~1` 代表 `/`，`~0` 代表 `~`。

4. **指针的操作**：JSON Pointer 可以用于以下操作：
   - 定位特定元素或属性。
   - 添加新元素或属性。
   - 替换或删除现有元素或属性。

5. **安全性和效率**：JSON Pointer 被设计为安全和高效的方式来引用 JSON 数据。由于其简单性，它不会引入严重的安全风险，并且可以在不复制数据的情况下引用和操作 JSON 结构。

6. **应用场景**：JSON Pointer 在许多领域有用，包括 Web 开发、API 设计、配置文件、数据传输和处理等。它允许开发者轻松地在 JSON 数据中导航和操作，而无需解析整个 JSON 文档。

总之，RFC 6901 定义了 JSON Pointer 规范，提供了一种简单而强大的方式来定位和操作 JSON 数据结构中的元素。JSON Pointer 在处理 JSON 数据时非常有用，尤其是在分散的数据结构中查找和操作特定数据元素时。它被广泛用于 Web 开发、API 设计和数据交换等领域。

# rfc6902

RFC 6902 是一份由 IETF（Internet Engineering Task Force）发布的标准文档，它定义了 JSON Patch（JSON 补丁）规范。

JSON Patch 是一种用于描述**如何将一个 JSON 文档转换为另一个 JSON 文档的格式。**

JSON Patch 可以用于添加、删除、替换和移动 JSON 文档中的数据，==以实现 JSON 数据的部分更新。==

以下是 RFC 6902 的主要内容和说明：

1. **JSON Patch 格式**：JSON Patch 是一个由一系列操作组成的 JSON 文档。每个操作都表示一种修改 JSON 文档的方式。JSON Patch 支持以下操作类型：
   - `add`：向 JSON 文档中添加新的元素或属性。
   - `remove`：从 JSON 文档中删除元素或属性。
   - `replace`：替换 JSON 文档中的元素或属性。
   - `move`：移动 JSON 文档中的元素或属性到另一个位置。
   - `copy`：复制 JSON 文档中的元素或属性到另一个位置。
   - `test`：测试 JSON 文档中的元素或属性是否等于预期的值。

2. **JSON Patch 操作示例**：以下是 JSON Patch 操作的示例：
   - `{ "op": "add", "path": "/foo", "value": "bar" }`：在 JSON 文档中添加属性 "foo"，其值为 "bar"。
   - `{ "op": "remove", "path": "/foo" }`：从 JSON 文档中删除属性 "foo"。
   - `{ "op": "replace", "path": "/foo", "value": "baz" }`：将属性 "foo" 的值替换为 "baz"。
   - `{ "op": "move", "from": "/foo", "path": "/bar" }`：将属性 "foo" 移动到属性 "bar"。
   - `{ "op": "copy", "from": "/foo", "path": "/bar" }`：复制属性 "foo" 到属性 "bar"。
   - `{ "op": "test", "path": "/foo", "value": "bar" }`：测试属性 "foo" 是否等于 "bar"。

3. **操作的顺序性**：JSON Patch 中的操作是有序的，它们按照在 JSON 文档上的应用顺序依次执行。这确保了操作的顺序性和可重现性。

4. **操作的原子性**：JSON Patch 中的操作是原子的，它们要么全部成功应用，要么全部失败。如果在应用 JSON Patch 时发生错误，不会修改目标 JSON 文档。

5. **安全性和效率**：JSON Patch 被设计为安全和高效的方式来描述 JSON 数据的修改。它允许在不传输整个 JSON 文档的情况下进行部分更新，从而减少了数据传输的开销。

6. **应用场景**：JSON Patch 在许多应用程序中都有用，包括 Web API 的部分更新、配置管理、协作编辑、数据同步等。它为开发者提供了一种简单且可扩展的方式来管理和更新 JSON 数据。

总之，RFC 6902 定义了 JSON Patch 规范，提供了一种描述如何修改 JSON 文档的标准方式。JSON Patch 可以用于在不传输整个 JSON 文档的情况下进行部分更新，这对于减少数据传输的开销和确保数据一致性非常有用。JSON Patch 在各种应用领域中得到广泛使用。

# rfc7396

RFC 7396 是一份由 IETF（Internet Engineering Task Force）发布的标准文档，它定义了 JSON Merge Patch（JSON 合并补丁）规范。JSON Merge Patch 是一种用于描述如何将一个 JSON 文档与另一个 JSON 文档合并的格式。它通常用于局部更新或修改 JSON 数据，特别是在 RESTful API 的应用程序中，以便客户端可以提供一个部分数据更新而不必发送整个 JSON 文档。

以下是 RFC 7396 的主要内容和说明：

1. **JSON Merge Patch 格式**：JSON Merge Patch 是一个 JSON 对象，它包含一系列操作，用于将一个 JSON 文档的一部分合并到另一个 JSON 文档中。JSON Merge Patch 支持以下操作：
   - 将属性添加到目标 JSON 文档。
   - 将属性从目标 JSON 文档中删除。
   - 替换目标 JSON 文档中的属性值。

2. **JSON Merge Patch 示例**：以下是 JSON Merge Patch 操作的示例：
   - `{ "name": "John" }`：将属性 "name" 添加到目标 JSON 文档中，其值为 "John"。
   - `{ "age": null }`：将属性 "age" 从目标 JSON 文档中删除。
   - `{ "city": "New York" }`：将属性 "city" 的值替换为 "New York"。

3. **操作的原子性**：JSON Merge Patch 中的操作是原子的，它们要么全部成功应用，要么全部失败。如果在应用 JSON Merge Patch 时发生错误，不会修改目标 JSON 文档。

4. **操作的顺序性**：JSON Merge Patch 中的操作是按顺序应用的，因此后续的操作可以覆盖前面的操作。

5. **安全性和效率**：JSON Merge Patch 被设计为安全和高效的方式来描述 JSON 数据的合并。它允许在不传输整个 JSON 文档的情况下进行局部更新，从而减少了数据传输的开销。

6. **应用场景**：JSON Merge Patch 在许多应用程序中都有用，特别是在 RESTful API 设计中，允许客户端提供一个部分数据更新而不必发送整个 JSON 文档。这对于减少网络流量、提高效率和确保数据一致性非常有用。

总之，RFC 7396 定义了 JSON Merge Patch 规范，提供了一种描述如何将一个 JSON 文档与另一个 JSON 文档合并的标准方式。JSON Merge Patch 通常用于部分更新 JSON 数据，特别是在 RESTful API 中，以减少数据传输的开销和提高效率。它在各种应用领域中得到广泛使用。