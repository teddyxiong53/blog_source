---
title: js运行时bun
date: 2024-09-10 10:15:17
tags:
	- js
---

--

# 简介

Bun 是一个新的 JavaScript 运行时，从头开始构建，以服务于现代 JavaScript 生态系统。

它有三个主要的设计目标：

- 速度。Bun 开始迅速并运行迅速。它扩展了 JavaScriptCore，这是为 Safari 构建的注重性能的 JS 引擎。快速的启动时间意味着快速的应用和快速的 API。
- 优雅的 API。Bun 提供了执行常见任务（如启动 HTTP 服务器和写入文件）的最小且高度优化的 API 集。
- 聚合 DX. Bun 是构建 JavaScript 应用的完整工具包，包括包管理器、测试运行器和打包器。



Bun 是为替换 Node.js 而设计的。它原生实现了数百个 Node.js 和 Web API，包括 `fs` ， `path` ， `Buffer` 和更多。

Bun 的目标是运行世界上大部分服务器端 JavaScript，并提供工具来提高性能、减少复杂性并增加开发人员的生产力。

# HelloWorld

安装，我现在尽量都基于x-cmd来安装各种环境。

```
x env use bun
```

这样就会自动安装bun。

创建项目：

```
bun init 
```

根据提示填入信息即可。默认生成了index.ts。里面有一行hello world打印。

生成的目录结构：

```
tree
.
├── bun.lockb
├── index.ts
├── node_modules
│   └── bun-types
│       ├── package.json
│       ├── README.md
│       └── types.d.ts
├── package.json
├── README.md
└── tsconfig.json
```



运行：

```
 bun run index.ts
Hello via Bun!
```

编译：

```
bun build
```

这个目前没有任何效果。

# 安装express

```
bun add express
```

修改index.ts

```
import express from 'express';

const app = express();
const PORT = 3000;

// 中间件
app.use(express.json());

// 路由
app.get('/', (req, res) => {
    res.send('Hello, Bun with Express and TypeScript!');
});

// 启动服务器
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
```

然后bun run index.ts即可。

# 官方教程

https://bun.sh/docs/quickstart

```
const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("Bun!");
  },
});

console.log(`Listening on http://localhost:${server.port} ...`);
```

可以直接：

```
bun index.ts
```

省去run那个命令。

