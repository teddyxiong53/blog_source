---
title: graphql（1）
date: 2024-05-14 20:19:11
tags:
	- web
---

--

# graphql简介

| 特点         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| **简介**     | GraphQL是一种由Facebook于2012年开发的数据查询语言和运行时环境。它旨在提供更高效、强大和灵活的API设计选择。 |
| **目的**     | GraphQL旨在解决传统REST API的一些限制和缺点，如过度获取数据、多个端点和版本控制。它提供了一种更精确、更可预测和更高效的数据查询方式。 |
| **核心概念** | GraphQL基于三个核心概念：类型系统、查询语言和执行引擎。它使用类型来定义数据模型，查询语言来描述客户端所需的数据，执行引擎负责解析和执行这些查询。 |
| **灵活性**   | GraphQL允许客户端精确地指定其数据需求，从而减少了过度获取的问题，并允许在单个请求中获取多个资源的数据，减少了网络请求次数。 |
| **生态系统** | 由于其灵活性和强大性，GraphQL在开发者社区中受到广泛欢迎，并有许多工具和库可供开发者使用，如Apollo GraphQL、GraphiQL等。 |
| **应用范围** | GraphQL可用于各种应用场景，包括Web应用、移动应用和IoT设备，适用于任何需要数据交换和数据查询的场景。 |



# 发展历史

| 时间   | 事件                                                         |
| ------ | ------------------------------------------------------------ |
| 2012年 | Facebook开始内部开发GraphQL，并在2012年底首次在内部发布使用。 |
| 2015年 | Facebook宣布将GraphQL开源，并正式发布了GraphQL规范。         |
| 2016年 | 2016年，GraphQL持续在社区中获得关注和采用，并在GitHub上建立了相应的仓库。 |
| 2017年 | 2017年，GraphQL开始获得更广泛的采用，并在开发者社区中受到追捧。 |
| 2018年 | 2018年，GraphQL生态系统持续发展，出现了更多的工具和库，如Apollo GraphQL等。 |
| 至今   | 目前，GraphQL已经成为构建现代API的首选技术之一，并在各种应用场景中广泛使用。 |

GraphQL的发展历程是一个持续不断的过程，在Facebook内部孵化成熟后，逐渐被开源并得到了广泛的认可和采用。

# 官网信息

https://graphql.org/

向你的API发送一个GraphQL查询，并得到你所需要的，不多不少。

GraphQL查询总是返回可预测的结果。

使用GraphQL的应用程序是快速和稳定的，因为它们控制它们获得的数据，而不是服务器。

GraphQL查询不仅访问一个资源的属性，

还可以平滑地跟踪它们之间的引用。

虽然典型的REST API需要从多个URL加载，

但GraphQL API可以在单个请求中获取应用所需的所有数据。

使用GraphQL的应用程序即使在缓慢的移动的网络连接上也可以快速运行。



GraphQL是一种用于API的查询语言，也是一个服务器端运行时，用于使用您为数据定义的类型系统执行查询。

GraphQL不绑定到任何特定的数据库或存储引擎，而是由您现有的代码和数据支持。



# Python 举例

以下是使用Python实现GraphQL的示例：

```python
from graphene import ObjectType, String, Schema

# 定义GraphQL对象类型
class Query(ObjectType):
    hello = String(name=String(default_value="World"))

    # 定义查询字段的解析方法
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

# 创建GraphQL模式
schema = Schema(query=Query)

# 执行GraphQL查询
result = schema.execute('{ hello }')
print(result.data['hello'])  # 输出: Hello World!

result = schema.execute('{ hello(name: "Alice") }')
print(result.data['hello'])  # 输出: Hello Alice!
```

在这个示例中，我们使用了Python中的`graphene`库来实现GraphQL。首先，我们定义了一个GraphQL对象类型`Query`，其中包含一个名为`hello`的字段，它接受一个参数`name`，默认值为"World"。然后，我们定义了`resolve_hello`方法来解析`hello`字段，返回一个包含问候语的字符串。

接着，我们创建了一个GraphQL模式，并执行了两个GraphQL查询：一个不带参数的，另一个带有名为"Alice"的参数。最后，我们输出了查询结果，分别为"Hello World!"和"Hello Alice!"。

这只是一个简单的示例，实际中可以根据需求定义更复杂的对象类型和查询。

# 参考资料

https://medium.com/@ryk.kiel/graphql-and-fastapi-the-ultimate-combination-for-building-apis-with-python-f4391bf5505c
