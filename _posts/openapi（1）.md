---
title: openapi（1）
date: 2024-05-09 20:19:11
tags:
	- python
---

--

# 简介

OpenAPI（OpenAPI Specification）是一种用于==描述和定义 RESTful APIs 的标准规范。==

它以可读性强的 YAML 或 JSON 格式编写，

提供了一种清晰的方式来描述 API 的端点、参数、响应、认证等信息。

通过使用 OpenAPI，开发人员可以更容易地理解和使用 API，

同时也能够自动生成文档、代码和测试用例，

从而加速 API 的开发和集成过程。

OpenAPI 规范包括以下主要部分：

1. **路径（Paths）：** 描述了 API 的各个端点以及它们支持的操作（如 GET、POST、PUT、DELETE 等）。
   
2. **参数（Parameters）：** 定义了在请求中发送的参数，包括路径参数、查询参数、请求头和请求体等。
   
3. **响应（Responses）：** 定义了 API 操作可能返回的各种响应，包括状态码、响应体内容和响应头等。
   
4. **模式（Schema）：** 定义了 API 的数据模型，包括对象结构、属性类型和验证规则等。
   
5. **安全（Security）：** 描述了 API 的安全机制，包括认证方式和授权要求等。

OpenAPI 规范的主要优点包括：

- **可读性和可维护性：** 使用简洁清晰的结构描述 API，易于理解和修改。
  
- **自动生成工具：** 可以利用 OpenAPI 规范自动生成 API 文档、客户端代码和服务器框架等，提高开发效率。
  
- **标准化和互操作性：** OpenAPI 是一个开放标准，有助于不同团队、不同技术栈之间的协作和集成。

总的来说，OpenAPI 规范提供了一种规范化的方法来描述和管理 RESTful APIs，有助于提高 API 的设计质量、开发效率和可维护性。

# 发展历史

OpenAPI 规范的发展历史可以追溯到 Swagger。以下是一些关键的发展里程碑：

1. **Swagger 1.0：** Swagger 最初于2011年由 Tony Tam 创建。它是一个用于描述和可视化 RESTful APIs 的工具。Swagger 1.0 版本定义了基本的 API 描述格式，并提供了一个 UI 来浏览和测试 API。

2. **Swagger 2.0：** 在 Swagger 1.0 的基础上，Swagger 2.0 引入了一种基于 JSON 或 YAML 的 API 描述语言。这一版本加强了对参数、响应和安全机制的描述，为自动生成 API 文档和客户端代码提供了更多支持。

3. **OpenAPI Specification 3.0：** 在 Swagger 2.0 的基础上，OpenAPI Specification 3.0 于2017年发布。这一版本对规范进行了重大改进和扩展，包括更好的支持 JSON Schema、更严格的验证规则、新增了响应内容协商、链接等功能，进一步提高了规范的灵活性和表达能力。

4. **OpenAPI Initiative：** 在 Swagger 成功推广之后，2015 年 Linux 基金会成立了 OpenAPI Initiative，旨在推动和维护 OpenAPI 规范的发展。该倡议得到了包括 Microsoft、Google、IBM 和 PayPal 等在内的众多公司的支持。

5. **OpenAPI 3.1：** 在 2020 年，OpenAPI 规范迎来了 3.1 版本。这一版本引入了一些新的功能和改进，例如对 OAuth 2.0 和 OIDC（OpenID Connect）的更好支持，以及对链接、回调等方面的增强。

6. **持续发展：** OpenAPI 规范在持续演进中，社区不断提出建议和改进意见，以适应不断变化的 API 设计和开发需求。目前，OpenAPI 仍然是业界最流行的 API 规范之一，被广泛应用于 RESTful API 的设计、开发和管理中。

# openapi规范中文版

https://openapi.apifox.cn/

