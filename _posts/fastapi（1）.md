---
title: fastapi（1）
date: 2023-07-02 11:21:51
tags:
	- web

---

--

看nicegui用的是fastapi。研究一下。

# 发展历史

FastAPI 是一个快速（fast）的 Web 框架，它使用 Python 3.6+ 的新特性，如类型注解、异步编程和协程。FastAPI 的开发始于 2018 年，由 Sebastián Ramírez（也称作 tiangolo）创造并开源发布。以下是 FastAPI 的主要发展历史：

- 2018 年 11 月，FastAPI 的第一个版本发布。FastAPI 的目标是提供一个快速、易用且符合标准的 Web 框架，可以帮助开发人员快速构建高性能的 Web API。
- 2019 年 2 月，FastAPI 发布了 0.2 版本，引入了许多新功能，如依赖注入、请求体验证和响应模型。
- 2019 年 5 月，FastAPI 发布了 0.3 版本，支持了多种新的数据类型，如 UUID、Decimal 和 datetime。
- 2019 年 8 月，FastAPI 发布了 0.4 版本，引入了新的测试工具和文档生成工具，使得编写测试和文档变得更加容易。
- 2019 年 12 月，FastAPI 发布了 0.6 版本，支持了多种新的验证器和序列化器，如 email-validator、pydantic 和 orjson。
- 2020 年 3 月，FastAPI 发布了 0.7 版本，支持了多种新的功能，如请求头验证和 WebSocket 支持。
- 2020 年 6 月，FastAPI 发布了 0.8 版本，支持了多种新的功能，如安全头、跨域资源共享（CORS）和异步后台任务。
- 2020 年 9 月，FastAPI 发布了 0.9 版本，引入了新的 API Router 和 API WebSocket Router，使得路由的编写变得更加简单明了。
- 2021 年 2 月，FastAPI 发布了 0.10 版本，支持了多种新的功能，如 OpenAPI 和 JSON Schema 的扩展和自定义异常处理。
- 2021 年 6 月，FastAPI 发布了 0.11 版本，引入了新的命令行工具，使得应用程序的管理和部署更加方便。

总之，FastAPI 是一个快速发展的 Web 框架，自发布以来不断增加新的功能和改进，使得它成为一个优秀的选择，特别是在构建高性能 Web API 的场景下。



# fastapi和flask对比

FastAPI 和 Flask 是 Python Web 开发中两个非常流行的 Web 框架。它们都提供了一套简单而强大的 API，使得构建 Web 应用程序变得更加容易。下面是 FastAPI 和 Flask 的一些对比：

1. 性能：FastAPI 比 Flask 更快。这是因为 FastAPI 使用了 Python 3.6+ 的新特性，如类型注解和异步编程，以及 Pydantic 库的数据验证和序列化功能，从而提高了性能。Flask 仍然是一个非常快速的框架，但是 FastAPI 的性能更高。

2. 异步编程：FastAPI 支持异步编程，使得多个同时进行的请求之间可以并行处理，从而提高了吞吐量和响应速度。Flask 使用传统的同步模型，无法支持异步编程。

3. 类型注解：FastAPI 使用类型注解来定义输入和输出参数的类型，从而使代码更加易于阅读和维护。Flask 不支持类型注解。

4. 数据验证：FastAPI 使用 Pydantic 库来进行数据验证和序列化，使得代码更加简洁和易于维护。Flask 并没有这样的内置功能，需要使用第三方库来实现。

5. API 文档：FastAPI 自动根据代码生成 OpenAPI 和 JSON Schema 文档，使得文档生成变得非常容易。Flask 需要使用第三方库来生成文档。

6. 社区支持：FastAPI 社区的规模和活跃度都比 Flask 更高。FastAPI 的开发始于 2018 年，但是已经得到了广泛的认可和支持。Flask 的开发始于 2010 年，已经成为 Python Web 开发中的经典框架，但是它的社区规模已经相对稳定。

总之，FastAPI 和 Flask 都是优秀的 Python Web 框架，在不同的场景下都有其优势。如果您需要构建高性能的 Web API，并且需要支持异步编程和数据验证，那么 FastAPI 是一个更好的选择。如果您需要一个轻量级的 Web 框架，并且需要更多的自定义和灵活性，那么 Flask 可能更适合您。



https://github.com/tiangolo/fastapi

