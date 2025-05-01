---
title: AI之fastmcp
date: 2025-04-19 17:26:37
tags:
	- AI
---

--

目前MCP非常火。

但是我感觉有些不知道怎么切入进去。

因为目前的应用，对我来说，都是没有用途的。

今天看到一篇介绍fastmcp的文章。

觉得这个python库不错。可以作为切入研究mcp的一个切入点。

https://github.com/jlowin/fastmcp

最近的很多学习都是在AI的对话基础上学习。感觉被信息轰炸了，还是要自己进行总结。梳理出知识要点，才能比较好地进行掌握。

MCP 协议功能强大，但实现它需要大量的样板代码——服务器设置、协议处理程序、内容类型、错误管理。FastMCP 处理所有复杂的协议细节和服务器管理，让您可以专注于构建优秀的工具。它旨在提供高级和 Pythonic 的体验；在大多数情况下，只需装饰一个函数即可。

FastMCP 1.0 让构建 MCP 服务器变得如此简单，现在它已成为官方模型上下文协议 Python SDK 的一部分！对于基本用例，您可以通过导入 `mcp.server.fastmcp.FastMCP` （或安装 `fastmcp=1.0` ）来使用上游版本。

基于 MCP 生态系统的演变，FastMCP 2.0 在这个基础上引入了各种新功能（以及更多实验性想法）。它增加了高级功能，如代理和组合 MCP 服务器，以及从 OpenAPI 规范或 FastAPI 对象自动生成它们。FastMCP 2.0 还引入了新的客户端功能，如 LLM 抽样。

我们强烈建议使用 uv 安装 FastMCP，因为它是通过 CLI 部署服务器所必需的：

```
uv pip install fastmcp
```

对于开发，请使用以下命令安装：

```
# Clone the repo first
git clone https://github.com/jlowin/fastmcp.git
cd fastmcp
# Install with dev dependencies
uv sync
```

让我们创建一个简单的 MCP 服务器，该服务器公开一个计算工具和一些数据：

```
# server.py
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
```

https://mp.weixin.qq.com/s?__biz=MzAwODIyMzE2MA==&mid=2247488889&idx=1&sn=fd6af0f562aa960ed153ea15208194ad&chksm=9ac39871d7e253fda963f29521ae8f8a528706ab77534ab671db45a4ac785fee15028a01a1a2#rd

```
from fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("智能金融助手", dependencies=["yfinance"])

@mcp.resource("stock://{symbol}/profile")
def stock_profile(symbol: str):
    """上市公司基本信息"""
    return yf.Ticker(symbol).info

@mcp.tool()
def portfolio_analysis(symbols: list[str]) -> dict:
    """投资组合分析"""
    return {
        sym: yf.Ticker(sym).history(period="1mo")
        for sym in symbols
    }
```

下面这个是用自然读取查看目录和文件内容。



```
from fastmcp import FastMCP
import os
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("本地文件助手", dependencies=[])

@mcp.resource("file://{path}")
def read_file(path: str):
    """读取指定路径的文本文件内容"""
    logger.info(f"Reading file: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"path": path, "content": content}
    except Exception as e:
        logger.error(f"Error reading file {path}: {str(e)}")
        return {"path": path, "error": f"读取文件失败: {str(e)}"}

@mcp.tool()
def list_directory(path: str) -> dict:
    """列出指定目录下的文件及其元数据"""
    logger.info(f"Listing directory: {path}")
    try:
        files = []
        for entry in os.scandir(path):
            if entry.is_file():
                stat = entry.stat()
                files.append({
                    "name": entry.name,
                    "size_bytes": stat.st_size,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        return {"path": path, "files": files}
    except Exception as e:
        logger.error(f"Error listing directory {path}: {str(e)}")
        return {"path": path, "error": f"列出目录失败: {str(e)}"}

@mcp.prompt("读取文件{path}的内容")
def read_file_prompt(path: str):
    """通过提示词调用 read_file 资源"""
    logger.info(f"Prompt triggered: read_file with path={path}")
    # 直接调用 read_file 函数，绕过 get_resource
    file_result = read_file(path)
    if "error" in file_result:
        return file_result["error"]
    return f"文件 {path} 的内容:\n{file_result['content']}"

@mcp.prompt("列出目录{path}下的文件")
def list_directory_prompt(path: str):
    """通过提示词调用 list_directory 工具"""
    logger.info(f"Prompt triggered: list_directory with path={path}")
    result = list_directory(path)
    if "error" in result:
        return result["error"]
    files = result["files"]
    if not files:
        return f"目录 {path} 为空"
    file_list = "\n".join(
        f"- {f['name']} ({f['size_bytes']} 字节, 最后修改: {f['last_modified']})"
        for f in files
    )
    return f"目录 {path} 下的文件:\n{file_list}"

if __name__ == "__main__":
    # 打印注册的资源、工具和提示词
    logger.info(f"Registered resources: {mcp.list_resources()}")
    logger.info(f"Registered tools: {mcp.list_tools()}")
    logger.info(f"Registered prompts: {mcp.list_prompts()}")

    # 测试提示词
    print(mcp.run_prompt("读取文件/tmp/test.txt的内容"))
    print(mcp.run_prompt("列出目录/tmp/test_dir下的文件"))
```

