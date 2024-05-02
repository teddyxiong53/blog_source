---
title: AI之langchain
date: 2024-05-02 12:30:49
tags:
	- AI

---

--

# 什么是langchain

[LangChain](https://link.zhihu.com/?target=https%3A//docs.langchain.com/docs/%3Fref%3Dnotes.replicatecodex.com)是一个强大的框架，

旨在帮助开发人员使用语言模型构建端到端的应用程序。

它提供了一套工具、组件和接口，

可简化创建由大型语言模型 (LLM) 和聊天模型提供支持的应用程序的过程。

LangChain 可以轻松管理与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如 API 和数据库。

官网：

https://python.langchain.com/docs/get_started/introduction



https://www.langchain.asia/

https://zhuanlan.zhihu.com/p/620529542

# 核心概念

| 概念                        | 说明                                                         |
| --------------------------- | ------------------------------------------------------------ |
| Components and Chains       | component就是最小的模块单元。<br />chain就是把component组合起来。<br />一个 Chain 可能包括一个 Prompt 模板、一个语言模型和一个输出解析器，<br />它们一起工作以处理用户输入、生成响应并处理输出。 |
| Prompt Templates and Values | rompt Template 负责创建 PromptValue，这是最终传递给语言模型的内容<br />就是把我们杂乱的输入规范化，让LLM更好理解 |
| Example Selectors           | 当您想要在 Prompts 中动态包含示例时，Example Selectors 很有用。 |
| Output Parsers              | Output Parsers 负责将语言模型响应构建为更有用的格式。        |
| Indexes and Retrievers      | Index 是一种组织文档的方式，使语言模型更容易与它们交互。<br />检索器是用于获取相关文档并将它们与语言模型组合的接口。 |
| Chat Message History        | LangChain 主要通过聊天界面与语言模型进行交互。<br />ChatMessageHistory 类负责记住所有以前的聊天交互数据，<br />然后可以将这些交互数据传递回模型、汇总或以其他方式组合。<br />这有助于维护上下文并提高模型对对话的理解。 |
| Agents and Toolkits         | Agent 是在 LangChain 中推动决策制定的实体。<br />他们可以访问一套工具，并可以根据用户输入决定调用哪个工具。<br />Tookits 是一组工具，当它们一起使用时，可以完成特定的任务。<br />代理执行器负责使用适当的工具运行代理。 |

# 如何使用 LangChain？

要使用 LangChain，开发人员首先要导入必要的组件和工具，

例如 LLMs, chat models, agents, chains, 内存功能。

这些组件组合起来创建一个可以理解、处理和响应用户输入的应用程序。

LangChain 为特定用例提供了多种组件，

例如个人助理、文档问答、聊天机器人、查询表格数据、与 API 交互、提取、评估和汇总。

## 使用示例

LangChain 支持大量用例，例如：

- **针对特定文档的问答**：根据给定的文档回答问题，使用这些文档中的信息来创建答案。
- **聊天机器人**：构建可以利用 LLM 的功能生成文本的聊天机器人。
- **Agents**：开发可以决定行动、采取这些行动、观察结果并继续执行直到完成的代理。

## 使用 LangChain 构建端到端语言模型应用程序

- 首先，安装 LangChain。只需运行以下命令：

```bash
pip install langchain
```

- **环境设置**
  现在，由于 LangChain 经常需要与模型提供者、数据存储、API 等集成，我们将设置我们的环境。在这个例子中，我们将使用 OpenAI 的 API，因此我们需要安装他们的 SDK：

```bash
pip install openai
```

接下来，让我们在终端中设置环境变量：

```text
export OPENAI_API_KEY = "..."
```

或者，如果您更喜欢在 Jupyter notebook 或 Python 脚本中工作，您可以像这样设置环境变量:

**构建语言模型应用程序：LLM**
安装好 LangChain 并设置好环境后，我们就可以开始构建我们的语言模型应用程序了。LangChain 提供了一堆模块，您可以使用它们来创建语言模型应用程序。您可以将这些模块组合起来用于更复杂的应用程序，或者将它们单独用于更简单的应用程序。

**构建语言模型应用程序：Chat Model**
除了 LLM，您还可以使用聊天模型。这些是语言模型的变体，它们在底层使用语言模型但具有不同的界面。聊天模型使用聊天消息作为输入和输出，而不是“文本输入、文本输出”API。聊天模型 API 的使用还比较新，所以大家都还在寻找最佳抽象使用方式。

要完成聊天，您需要将一条或多条消息传递给聊天模型。LangChain 目前支持 AIMessage、HumanMessage、SystemMessage 和 ChatMessage 类型。您将主要使用 HumanMessage、AIMessage 和 SystemMessage。
下面是使用聊天模型的示例：



# 参考资料

1、

https://zhuanlan.zhihu.com/p/620529542