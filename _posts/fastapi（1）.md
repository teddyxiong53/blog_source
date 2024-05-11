---
title: fastapi（1）
date: 2023-07-02 11:21:51
tags:
	- web

---

--

看nicegui用的是fastapi。研究一下。

# 简介

FastAPI 是一个现代、快速（高性能）的 Web 框架，

用于基于标准 Python 类型提示使用 Python 构建 API。

快速：非常高的性能，与 NodeJS 和 Go 相当。最快的 Python 框架之一。



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

# 代码

https://github.com/tiangolo/fastapi

# fastapi适合编写什么类型的应用

FastAPI 适合编写各种类型的应用，特别是对性能要求较高、需要异步处理的场景。以下是一些适合使用 FastAPI 的应用类型：

1. **API 服务**: FastAPI 最初设计就是为了构建 Web API，因此非常适合用于构建各种类型的 API 服务，如 RESTful API、GraphQL API 等。

2. **微服务**: 由于 FastAPI 具有高性能和异步处理能力，因此它非常适合用于构建微服务架构。您可以将不同的功能模块拆分为独立的 FastAPI 应用，并通过 HTTP 或消息队列进行通信。

3. **实时应用**: FastAPI 的异步特性使其非常适合构建实时应用，如聊天应用、实时数据处理和监控系统等，能够处理高并发的请求。

4. **数据处理和分析**: FastAPI 与异步数据库访问库（如 SQLAlchemy-Async、Tortoise-ORM）结合使用，可用于构建数据处理和分析应用，处理大量数据并提供相应的 API 接口。

5. **后端服务**: FastAPI 可以作为后端服务的框架，为前端应用提供数据接口。它与前端框架（如 React、Vue.js）结合使用时效果很好。

6. **机器学习和人工智能应用**: 由于 FastAPI 的性能优势和支持异步处理，因此它也适合用于构建机器学习和人工智能应用的后端服务，能够处理大规模的数据和请求。

总之，FastAPI 是一款灵活且高性能的框架，适用于各种类型的应用开发，尤其在需要处理高并发请求和异步处理的场景下表现出色。

## fastapi搭建api服务举例

当使用 FastAPI 搭建 API 服务时，通常需要进行以下步骤：

1. **安装 FastAPI**: 首先，确保您已经安装了 Python 和 pip，然后可以通过 pip 安装 FastAPI：

    ```
    pip install fastapi
    ```

2. **安装 ASGI 服务器**: FastAPI 基于 ASGI（Asynchronous Server Gateway Interface）标准，因此需要一个 ASGI 服务器来运行应用。常见的 ASGI 服务器包括 Uvicorn、Hypercorn 等。这里以 Uvicorn 为例：

    ```
    pip install uvicorn
    ```

3. **编写应用代码**: 创建一个 Python 文件，编写 FastAPI 应用的代码。以下是一个简单的示例：

    ```python
    from fastapi import FastAPI

    # 创建 FastAPI 应用实例
    app = FastAPI()

    # 定义一个路由，处理 GET 请求
    @app.get("/")
    def read_root():
        return {"message": "Hello, FastAPI!"}

    # 定义另一个路由，处理 GET 请求
    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: str = None):
        return {"item_id": item_id, "q": q}
    ```

4. **运行应用**: 使用 Uvicorn 或其他 ASGI 服务器运行 FastAPI 应用。假设应用代码保存在 `main.py` 文件中，您可以通过以下命令运行应用：

    ```
    uvicorn main:app --reload
    ```

    这会启动一个开发服务器，监听在本地的 8000 端口，并且在代码修改后会自动重载应用。

5. **访问 API**: 应用成功运行后，您可以使用任何 HTTP 客户端来访问定义的 API 路由。例如，您可以在浏览器中访问 `http://localhost:8000/` 来查看 API 的响应。

这是一个简单的 FastAPI 应用示例，您可以根据实际需求添加更多的路由和功能。FastAPI 还支持异步请求处理、请求和响应模型验证、依赖注入等高级功能，使得开发 API 服务变得更加方便和高效。

### 都是返回json字符串吗？可以返回其他的东西吗

FastAPI 确实是通过返回 JSON 字符串来响应请求的，这是因为 JSON 是 Web API 中最常用的数据交换格式之一，它具有跨平台、易于解析等优点。

但是，FastAPI 并不限制您只能返回 JSON 字符串。您可以返回其他类型的数据，例如：

1. **Python 对象**: 您可以直接返回 Python 对象，FastAPI 会自动将其转换为 JSON 字符串并返回给客户端。

2. **文件**: 如果您的 API 需要返回文件（如图片、视频、PDF 等），您可以使用 FastAPI 的 `FileResponse` 类来返回文件流。这样，客户端可以直接下载文件。

3. **HTML 页面**: 虽然 FastAPI 主要用于构建 API，但您也可以返回 HTML 页面。您可以使用 Python 的模板引擎（如 Jinja2）来渲染 HTML 页面，然后将其作为响应返回。

4. **流式响应**: FastAPI 支持返回流式响应，这意味着您可以逐步生成响应并将其发送给客户端。这在处理大型文件或长时间运行的操作时非常有用。

以下是一个返回 Python 对象和文件的示例：

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

# 返回 Python 对象
@app.get("/items/", response_model=List[str])
async def read_items():
    return ["item1", "item2", "item3"]

# 返回文件
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # 处理文件上传逻辑
    return JSONResponse(content={"filename": file.filename})
```

以上示例展示了如何返回 Python 对象和文件，但您也可以根据需求返回其他类型的数据。

## fastapi搭建微服务举例

当使用 FastAPI 搭建微服务时，通常需要按照以下步骤进行：

1. **确定微服务边界**：首先，确定要构建的微服务的功能和边界。将业务逻辑划分为不同的微服务，每个微服务负责处理特定的功能或领域。

2. **定义接口**：为每个微服务定义清晰的接口，包括输入参数、输出数据和可能的错误情况。这些接口可以使用 FastAPI 中的路由和模型来定义。

3. **实现微服务**：根据定义的接口，编写每个微服务的实现代码。每个微服务通常是一个独立的 FastAPI 应用，可以单独开发、测试和部署。

4. **部署微服务**：将每个微服务部署到独立的服务器或容器中，可以使用 Docker、Kubernetes 等技术进行部署和管理。

5. **服务发现与通信**：确保微服务之间可以相互发现和通信。可以使用服务发现工具（如 Consul、Etcd）和通信框架（如 gRPC、HTTP）来实现微服务之间的通信。

下面是一个简单的示例，演示了如何使用 FastAPI 搭建两个微服务，一个用于用户管理，另一个用于订单管理：

```python
# users_service.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def read_user(user_id: int):
    # 查询用户信息的逻辑
    return {"user_id": user_id, "username": "user1"}

# orders_service.py
from fastapi import FastAPI

app = FastAPI()

@app.post("/orders/")
def create_order(user_id: int, item: str):
    # 创建订单的逻辑
    return {"user_id": user_id, "item": item, "order_id": 123}
```

在这个示例中，我们创建了两个 FastAPI 应用，一个用于用户管理（`users_service.py`），另一个用于订单管理（`orders_service.py`）。每个微服务都定义了自己的接口，并实现了相应的功能逻辑。

您可以根据需要扩展这个示例，添加更多的微服务和功能。FastAPI 提供了强大的工具和功能，使得构建和管理微服务变得更加简单和高效。

## fastapi搭建聊天应用

要使用 FastAPI 构建聊天应用，您可以遵循以下步骤：

1. **设计数据模型**: 首先，设计聊天应用所需的数据模型，例如用户、消息等。您可以使用 Pydantic 定义数据模型，并存储在数据库中（如果需要）。

2. **创建 WebSocket 路由**: 使用 FastAPI 支持的 WebSocket 功能创建 WebSocket 路由，以处理实时的消息传递。您可以使用 `WebSocket` 类来定义 WebSocket 路由，并在其中编写处理逻辑。

3. **处理连接和消息**: 在 WebSocket 路由中编写逻辑来处理新连接和收到的消息。您可以使用 Python 的异步特性来处理多个并发连接，并将消息广播给其他连接的客户端。

4. **编写前端界面**: 创建一个前端界面，用于与 WebSocket 服务器建立连接并发送/接收消息。您可以使用任何适合的前端框架（如 Vue.js、React、Angular）来实现前端部分。

5. **部署应用**: 将应用部署到服务器上，确保 WebSocket 服务器可以被外部客户端访问。您可以使用 ASGI 服务器（如 Uvicorn、Hypercorn）来运行 FastAPI 应用，并使用反向代理（如 Nginx、Traefik）来管理流量。

下面是一个简单的示例，演示了如何使用 FastAPI 构建一个简单的聊天应用：

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left the chat")
```

在这个示例中，我们创建了一个 `ConnectionManager` 类来管理所有的 WebSocket 连接。当客户端连接时，会调用 `connect` 方法将连接添加到活动连接列表中。当收到消息时，将调用 `broadcast` 方法将消息广播给所有连接的客户端。当客户端断开连接时，会调用 `disconnect` 方法将连接从活动连接列表中移除。

您可以根据需要扩展这个示例，添加认证、消息持久化等功能。 FastAPI 提供了丰富的功能和工具，使得构建实时聊天应用变得更加简单和高效。

## fastapi搭建AI应用

FastAPI 作为一个高性能的 Web 框架，非常适合用于构建 AI 应用的后端服务。您可以使用 FastAPI 来接收来自前端或其他服务的请求，然后将请求发送到 AI 模型进行处理，最后将处理结果返回给请求方。以下是搭建 AI 应用的一般步骤：

1. **选择 AI 模型**: 首先，选择适合您需求的 AI 模型。这可能是一个机器学习模型（如深度学习模型、传统的机器学习模型等）或者是一个预训练的模型（如图像分类、文本生成、语音识别等）。

2. **部署 AI 模型**: 部署您选择的 AI 模型，确保它能够接收输入数据，并返回相应的预测结果。您可以使用 TensorFlow Serving、TorchServe、ONNX Runtime 等工具来部署模型。

3. **创建 FastAPI 应用**: 使用 FastAPI 创建一个 Web 服务，接收来自客户端的请求，并将其传递给 AI 模型进行处理。您可以定义多个路由来处理不同的请求类型。

4. **与 AI 模型集成**: 在 FastAPI 应用中编写逻辑，将接收到的请求数据发送到 AI 模型进行处理，并将处理结果返回给客户端。您可以使用 Python 的请求库来与部署的 AI 模型进行通信。

5. **部署 FastAPI 应用**: 将 FastAPI 应用部署到服务器上，确保它能够被外部客户端访问。您可以使用 ASGI 服务器（如 Uvicorn、Hypercorn）来运行 FastAPI 应用，并使用反向代理（如 Nginx、Traefik）来管理流量。

以下是一个简单的示例，演示了如何使用 FastAPI 搭建一个简单的图像分类 AI 应用的后端服务：

```python
from fastapi import FastAPI, File, UploadFile
import requests

app = FastAPI()

# 接收上传的图片，并传递给图像分类模型进行处理
@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    # 将上传的图片发送给图像分类模型进行处理
    url = "http://your-model-service/predict"  # 替换为您的模型服务的地址
    files = {"file": (file.filename, file.file)}
    response = requests.post(url, files=files)
    
    # 返回模型预测结果
    return response.json()
```

在这个示例中，我们创建了一个 FastAPI 应用，定义了一个接收上传图片并进行图像分类的路由。在路由处理函数中，我们将上传的图片发送给部署的图像分类模型进行处理，并返回模型的预测结果给客户端。

您可以根据需要扩展这个示例，添加认证、日志记录、异常处理等功能。 FastAPI 提供了丰富的功能和工具，使得构建 AI 应用的后端服务变得更加简单和高效。

# 样板程序

https://github.com/mjhea0/awesome-fastapi?tab=readme-ov-file#boilerplate

https://github.com/markqiu/fastapi-mongodb-realworld-example-app

# 用fastapi实现消息推送服务器

要使用 FastAPI 实现消息推送服务器，您可以利用 WebSocket 功能来实现实时的消息推送。下面是一个简单的示例，演示了如何使用 FastAPI 来创建一个消息推送服务器：

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# 用于保存所有连接的 WebSocket 客户端
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    # 添加新的 WebSocket 连接
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # 关闭 WebSocket 连接
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # 广播消息给所有连接的客户端
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# WebSocket 路由，用于接收和发送消息
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 用于提供简单的 HTML 页面，用于测试 WebSocket 连接
@app.get("/")
async def get():
    return HTMLResponse("""
        <html>
            <head>
                <title>WebSocket Test</title>
            </head>
            <body>
                <h1>WebSocket Test</h1>
                <form action="" onsubmit="sendMessage(event)">
                    <input type="text" id="messageText" autocomplete="off"/>
                    <button>Send</button>
                </form>
                <ul id='messages'>
                </ul>
                <script>
                    var ws = new WebSocket("ws://localhost:8000/ws");
                    ws.onmessage = function(event) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        var content = document.createTextNode(event.data)
                        message.appendChild(content)
                        messages.appendChild(message)
                    };
                    function sendMessage(event) {
                        var input = document.getElementById("messageText")
                        ws.send(input.value)
                        input.value = ''
                        event.preventDefault()
                    }
                </script>
            </body>
        </html>
    """)

```

在这个示例中，我们创建了一个名为 `ConnectionManager` 的类，用于管理所有的 WebSocket 连接。在 `/ws` 路由中，我们使用 WebSocket 接受来自客户端的消息，并将其广播给所有连接的客户端。同时，我们提供了一个简单的 HTML 页面，用于测试 WebSocket 连接。

您可以通过向 `/ws` 路由发送消息来进行消息推送。其他连接到服务器的客户端会接收到发送的消息。这个示例是一个简单的消息推送服务器，您可以根据需要扩展功能，例如添加认证、消息过滤等。

要运行上面的示例，您需要按照以下步骤：

1. **安装 FastAPI 和 Uvicorn**: 如果您尚未安装 FastAPI 和 Uvicorn，请使用 pip 安装它们：

    ```
    pip install fastapi uvicorn
    ```

2. **将示例代码保存为 Python 文件**: 将上面提供的示例代码保存为一个 Python 文件，例如 `message_push_server.py`。

3. **运行 FastAPI 应用**: 在命令行中运行以下命令来启动 FastAPI 应用：

    ```
    uvicorn message_push_server:app --reload
    ```

    这会启动一个开发服务器，并监听在本地的 8000 端口上。`message_push_server` 是您保存的 Python 文件的文件名，`app` 是 FastAPI 应用的实例。

4. **访问 WebSocket 页面**: 打开浏览器，访问 `http://localhost:8000/`，您将看到一个简单的 WebSocket 页面。您可以在页面上输入消息并点击发送按钮，这些消息将通过 WebSocket 连接发送到服务器，并被广播给所有连接的客户端。

5. **使用 WebSocket 客户端**: 如果您想通过其他 WebSocket 客户端发送消息，您可以使用 WebSocket 客户端工具（如浏览器的开发者工具或 WebSocket 调试工具）连接到 `ws://localhost:8000/ws` 地址，并发送消息。

通过这些步骤，您应该能够运行并测试消息推送服务器。您可以在本地测试，或者将服务器部署到生产环境中供其他客户端连接。



# starlette 和fastapi关系

**FastAPI 和Starlette 完全兼容(并基于)**。 所以，你有的其他的Starlette 代码也能正常工作。 FastAPI 实际上是 Starlette 的一个子类。 所以，如果你已经知道或者使用Starlette，大部分的功能会以相同的方式工作。



# fastapi-mongodb-realworld-example-app

以这个为切入口来学习。

这个本地安装依赖很难成功。

所以还是靠docker方式来做。

但是docker方式也失败了。

