---
title: nodejs之express
date: 2018-12-18 20:28:55
tags:
	- nodejs

---



express 是一个web应用框架。用来快速搭建一个网站的。

核心功能：

1、可以设置中间件来响应http请求。

2、定义路由表来执行不同的http请求动作。

3、可以通过向模板传递参数来动态渲染html页面。



# 安装及使用

```
npm install -g express
```

我当前安装的是4.16.4的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/express$ npm install express -g
+ express@4.16.4
added 48 packages from 36 contributors in 6.686s
```

写一个helloworld。

新建express_demo.js。

```
const express = require("express");
var app = express();
app.get("/", function(req, res) {
    res.send("hello express");
});

var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

node express_demojs。就可以访问了。

重点是request对象和Response对象。

我可以通过node的repl来探索他们的属性。

用tab提示看看有哪些属性。

但是nodejs的repl没有像python那样的help函数可以查看这些接口的详细信息。

所以我还是在vscode里来查看。

加打印看看。

```
app.get("/", function(req, res) {
    console.log("req.app type:", typeof req.app);
    console.log("req.baseUrl:", req.baseUrl);
    console.log("req.body:", req.body);
    console.log("req.hostname:", req.hostname);
    console.log("req.ip:", req.ip);
    console.log("req.orignalUrl:", req.originalUrl);
    console.log("req.params:", req.params);
    console.log("req.path:", req.path);
    console.log("req.protocol:", req.protocol);
    console.log("req.query:", req.query);
    console.log("req.route:", req.route);
    console.log("req.subdomains", req.subdomains);
    console.log("req.accepts:", req.accepts);
    console.log("req.acceptsCharsets:", req.acceptsCharsets);
    console.log("req.get:", req.get("Content-Type"));
    res.send("hello express");
});
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/express$ node express_demo.js 
server listen on 8080
req.app type: function
req.baseUrl: 
req.body: undefined
req.hostname: 192.168.56.101
req.ip: 192.168.56.1
req.orignalUrl: /
req.params: {}
req.path: /
req.protocol: http
req.query: {}
req.route: Route {
  path: '/',
  stack:
   [ Layer {
       handle: [Function],
       name: '<anonymous>',
       params: undefined,
       path: undefined,
       keys: [],
       regexp: /^\/?$/i,
       method: 'get' } ],
  methods: { get: true } }
req.subdomains []
req.accepts: function(){
  var accept = accepts(this);
  return accept.types.apply(accept, arguments);
}
req.acceptsCharsets: function(){
  var accept = accepts(this);
  return accept.charsets.apply(accept, arguments);
}
req.get: undefined
```



# 路由

前面我们已经了解了基本的请求。

路由就是分配谁去响应某个请求。

```
const express = require("express");
var app = express();
app.get("/", function(req, res) {
    console.log("主页get请求");
    res.send("hello get");
});

app.post("/", function(req, res) {
    console.log("主页post请求");
    res.send("hello post");
});

app.get("/del_user", function(req, res) {
    console.log("/del_user响应delete请求");
    res.send("hello del_user");
});

app.get("/list_user", function(req, res) {
    console.log("/list_user 响应");
    res.send("hello list_user");
});

app.get("/ab*cd", function(req, res) {
    console.log("/ab*cd响应");
    res.send("正则匹配");
});

var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```



# 静态文件

当前目录新建一个public目录，下面新建一个images目录，下面放一个logo.png文件。

express_demo.js如下：

```
加上这句：
app.use(express.static("public"));
相当于是把public设置为静态目录的顶层目录，在url里使用的时候，从public的子目录写起就可以了。
```

访问：http://192.168.56.101:8080/images/logo.png



现在目录如下：

```
.
├── index.html
├── public
│   └── images
│       └── logo.png
└── server.js
```

index.html：

```
<html>
    <body>
        <form action="/process_get" method="GET">
            first name: <input type="text" name="first_name"><br>
            last name: <input type="text" name="last_name"><br>
            <input type="submit" value="提交">
        </form>
    </body>
</html>
```

server.js：

```
const express = require("express");
var app = express();
app.use(express.static("public"));

app.get("/index.html", function(req, res) {
    res.sendFile(__dirname + "/"  + "index.html");
});
app.get("/process_get", function(req, res) {
    var response = {
        "first_name": req.query.first_name,
        "last_name": req.query.last_name
    };
    res.end(JSON.stringify(response));
})
var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

访问http://192.168.56.101:8080/index.html

填好，提交。得到返回的连接是这个。

http://192.168.56.101:8080/process_get?first_name=a&last_name=b

网页内容是：

```
{first_name":"a","last_name":"b"}
```

测试post方法。

server.js

```
const express = require("express");
var app = express();
var bodyParser = require("body-parser");

var urlencodedParser = bodyParser.urlencoded({extended: false});

app.use(express.static("public"));

app.get("/index.html", function(req, res) {
    res.sendFile(__dirname + "/"  + "index.html");
});
//方法改成了post。
app.post("/process_post", urlencodedParser,  function(req, res) {
    var response = {
        "first_name": req.body.first_name,//这里改成了body，get的是query。
        "last_name": req.body.last_name
    };
    res.end(JSON.stringify(response));
})
var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

index.html

```
<html>
    <body>
        <form action="/process_post" method="POST">
            first name: <input type="text" name="first_name"><br>
            last name: <input type="text" name="last_name"><br>
            <input type="submit" value="提交">
        </form>
    </body>
</html>
```

# 上传文件

先修改index.html如下：

```
<html>
    <body>
        <h3>选择一个文件上传</h3>
        <form action="/file_upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="image" size="50"><br>
            <input type="submit" value="上传文件">
        </form>
    </body>
</html>
```

server.js：

```
const express = require("express");
var app = express();
var fs = require("fs");

var bodyParser = require("body-parser");
var multer = require("multer");

app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended: false}));
app.use(multer({dest: "/tmp"}).array("image"));

app.get("/index.html", function(req, res) {
    res.sendFile(__dirname + "/"  + "index.html");
});

app.post("/file_upload", function(req, res) {
    console.log(req.files[0]);
    var dest_file = __dirname + "/" + req.files[0].originalname;
    fs.readFile(req.files[0].path, function(err, data) {
        fs.writeFile(dest_file, data, function(err) {
            if(err) {
                console.log(err);
            } else {
                response = {
                    message: "File upload ok",
                    filename: req.files[0].originalname
                };
            }
            console.log(response);
            res.end(JSON.stringify(response));
        });
    });
});

var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/express$ node server.js 
server listen on 8080
{ fieldname: 'image',
  originalname: '1.png',
  encoding: '7bit',
  mimetype: 'image/png',
  destination: '/tmp',
  filename: '7537a82c0aa2700ed20d23ddacc7ae1f',
  path: '/tmp/7537a82c0aa2700ed20d23ddacc7ae1f',
  size: 2292 }
{ message: 'File upload ok', filename: '1.png' }
```



# app.get和app.use区别

`app.get`和`app.use`是Express框架中用于定义路由和中间件的两种方法。它们的主要区别在于用途和匹配方式。

1. `app.get`方法用于定义一个特定HTTP方法（GET）的路由。它指定了当收到来自客户端的GET请求时，应该执行的处理程序。通常用于处理特定路由的请求，如处理特定URL路径的GET请求。

```javascript
app.get('/users', (req, res) => {
  // 处理/users路由的GET请求
});
```

2. `app.use`方法用于定义中间件。中间件是在请求到达路由处理程序之前执行的功能。它可以用于处理各种任务，如身份验证、日志记录、错误处理等。`app.use`方法可以用于所有HTTP方法，并且它会匹配所有的路径。

```javascript
app.use((req, res, next) => {
  // 中间件逻辑
  next();
});
```

需要注意的是，`app.use`方法定义的中间件会被应用于每个请求，而`app.get`方法定义的路由仅匹配特定路径和HTTP方法的请求。

另外，`app.use`方法还可以用于处理静态文件、路由组、子应用程序等更复杂的用例。它可以接受路径参数来指定中间件适用的路径范围。

总结来说，`app.get`用于定义特定HTTP方法的路由，而`app.use`用于定义中间件。它们在用途和匹配方式上有所区别，但都是Express框架中常用的方法，用于处理请求和构建应用程序的功能。



# 官网资料学习

安装生成器。

```
npm install express-generator -g
```

这样会得到express命令。

执行效果是这样，得到这样的目录结构。可以直接运行。

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ tree
.
├── app.js
├── bin
│   └── www
├── package.json
├── public
│   ├── images
│   ├── javascripts
│   └── stylesheets
│       └── style.css
├── routes
│   ├── index.js
│   └── users.js
└── views
    ├── error.jade
    ├── index.jade
    └── layout.jade
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ npm start     

> node@0.0.0 start /home/hlxiong/work/test/node
> node ./bin/www

GET / 200 648.894 ms - 170
GET /stylesheets/style.css 200 16.330 ms - 111
GET /favicon.ico 404 32.348 ms - 1102
GET /favicon.ico 404 21.055 ms - 1102
```

访问127.0.0.1:3000就可以了。



# 设置engine

设置html引擎

```
app.engine('html', ejs.__express);
```

设置视图引擎

```
app.set('view engine', 'html');
```

**修改的这些设置做了什么操作？**

**为什么修改了视图引擎还要增加设置html引擎？**

我们先看一下.engine()这个方法。

## **app.engine(ext, callback);**

Express默认使用jade模板。如果你尝试加载 "foo.jade" 文件，Express内部会调用如下操作。

```
app.engine('jade', require('jade').__express);
```

如果要使用其他模板引擎，如：将EJS模板映射至".html"文件：

```
app.engine('html', require('ejs').__express);
```

这行代码中，实际调用了EJS的.renderFile()方法，ejs.__express是该方法在EJS内部的另一个名字。

## **app.set(name, value);**

在.set()方法的参数中，有一项是'view engine'，表示没有指定文件模板格式时，默认使用的引擎插件。如果这里设置为html文件，设置路由指定文件时，只需写文件名，就会找对应的html文件

# get请求可以经过json和urlencode吗

在标准的HTTP规范中，GET请求通常不包含请求体。GET请求将数据作为查询字符串参数附加到URL上，而不是放在请求体中。

**对于GET请求，Express中间件`express.json()`和`express.urlencoded()`不会处理请求体数据**，因为它们主要用于解析请求体中的数据。它们更适合用于处理POST请求或其他请求类型中的请求体数据。

如果您想要在GET请求中传递数据，可以通过查询字符串参数进行传递。在Express中，您可以使用`req.query`对象访问查询字符串参数。以下是一个示例：

```javascript
const express = require('express');
const app = express();

app.get('/users', (req, res) => {
  // 获取查询字符串参数
  const name = req.query.name;
  const age = req.query.age;

  // 处理数据
  // ...

  res.send('User details');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

在上面的示例中，当发送GET请求到`/users`路由时，查询字符串参数`name`和`age`可以通过`req.query`对象获取。您可以根据需要在路由处理程序中使用这些参数进行相应的处理。

请注意，GET请求中的查询字符串参数是通过URL进行传递的，而不是放在请求体中。因此，在GET请求中使用`express.json()`和`express.urlencoded()`中间件是没有意义的。

# express.json() 的代码实现原理

`express.json()`中间件的实现原理涉及到请求体的解析和数据处理。下面是一个简化的示例代码，展示了`express.json()`的基本实现原理：

```javascript
function expressJson(req, res, next) {
  let data = '';

  // 监听请求体数据的事件
  req.on('data', (chunk) => {
    data += chunk;
  });

  // 请求体数据接收完毕后的处理
  req.on('end', () => {
    try {
      // 解析JSON数据
      req.body = JSON.parse(data);
      next();
    } catch (error) {
      // 解析失败时的错误处理
      res.status(400).send('Invalid JSON');
    }
  });
}

// 在应用程序中使用expressJson中间件
app.use(expressJson);
```

上述代码中，`expressJson`函数是一个自定义的中间件函数，用于解析JSON数据。它通过监听请求的`data`事件来获取请求体数据，将其存储在`data`变量中。然后，在请求的`end`事件中，将`data`解析为JSON对象，并将其存储在`req.body`中，以便后续的处理中可以访问。

需要注意的是，这只是一个简化的示例，实际的`express.json()`中间件更加复杂，考虑了更多的情况和错误处理。例如，它可以处理更大的请求体数据、支持不同的编码格式、处理错误情况等。

Express框架本身在其内部使用了更底层的库来处理请求体数据的解析，如`body-parser`。`body-parser`提供了更强大和全面的功能，支持不仅仅是JSON数据的解析，还包括URL-encoded数据和多部分数据的解析。因此，实际使用Express时，推荐使用`body-parser`模块来处理请求体数据的解析，而不是手动编写类似的中间件函数。

# express.urlencoded原理

`express.urlencoded()`中间件的实现原理与`express.json()`中间件类似，它涉及到请求体的解析和数据处理。下面是一个简化的示例代码，展示了`express.urlencoded()`的基本实现原理：

```javascript
function expressUrlencoded(req, res, next) {
  let data = '';

  // 监听请求体数据的事件
  req.on('data', (chunk) => {
    data += chunk;
  });

  // 请求体数据接收完毕后的处理
  req.on('end', () => {
    try {
      // 解析URL-encoded数据
      const decodedData = decodeURIComponent(data);
      const params = new URLSearchParams(decodedData);
      const body = {};

      for (const [key, value] of params.entries()) {
        body[key] = value;
      }

      req.body = body;
      next();
    } catch (error) {
      // 解析失败时的错误处理
      res.status(400).send('Invalid URL-encoded data');
    }
  });
}

// 在应用程序中使用expressUrlencoded中间件
app.use(expressUrlencoded);
```

在上述代码中，`expressUrlencoded`函数是一个自定义的中间件函数，用于解析URL-encoded数据。它通过监听请求的`data`事件来获取请求体数据，将其存储在`data`变量中。然后，在请求的`end`事件中，将`data`解码为URL-encoded字符串，并使用`URLSearchParams`对象解析参数。然后，将参数键值对存储在`req.body`中，以便后续的处理中可以访问。

需要注意的是，这只是一个简化的示例，实际的`express.urlencoded()`中间件更加复杂，考虑了更多的情况和错误处理。例如，它可以处理更大的请求体数据、支持不同的编码格式、处理错误情况等。

与`express.json()`类似，实际使用Express时，推荐使用`body-parser`模块来处理URL-encoded数据的解析，而不是手动编写类似的中间件函数。`body-parser`提供了更强大和全面的功能，可方便地处理URL-encoded数据的解析和处理。

# urlencoded具体表示什么含义

`urlencoded`是一种数据编码格式，用于在HTTP请求中传输数据。它表示将数据转换为URL可接受的格式，以便可以在URL中传递数据参数。

在URL中，特殊字符（例如空格、逗号、斜杠等）是不允许直接出现的，因为它们具有特殊含义。为了在URL中传递包含特殊字符的数据，需要对数据进行编码。`urlencoded`就是一种编码方式，它使用特定的规则将数据进行编码，使其符合URL的规范。

具体而言，`urlencoded`编码将特殊字符替换为 `%` 符号后面跟着两个十六进制数字的形式。例如，空格字符被编码为 `%20`，逗号字符被编码为 `%2C`，斜杠字符被编码为 `%2F`，等等。这样，就可以在URL中传递包含特殊字符的数据，而不会破坏URL的结构和含义。

当使用表单提交数据或进行POST请求时，常见的数据编码方式就是`urlencoded`。数据会被编码为键值对的形式，使用等号(`=`)将键和值分隔，使用`&`符号将不同的键值对分隔。例如，`key1=value1&key2=value2` 就是一个使用`urlencoded`编码的数据字符串。

在Express框架中，`express.urlencoded()`中间件用于解析URL-encoded数据，将其解码为JavaScript对象，并将其存储在`req.body`中，方便在路由处理程序中进行访问和处理。

总结来说，`urlencoded`表示一种数据编码格式，用于在URL中传递数据参数，它将特殊字符替换为 `%` 符号后面跟着两个十六进制数字的形式，以确保数据的可传递性和完整性。

# cookie-parser 实现原理

`cookie-parser`是Express框架中常用的中间件，用于解析和处理HTTP请求中的Cookie。它的实现原理相对简单，下面是一个简化的示例来说明其工作原理：

```javascript
function cookieParser(req, res, next) {
  // 从请求头中获取Cookie字符串
  const cookies = req.headers.cookie;

  if (cookies) {
    // 解析Cookie字符串为键值对形式
    const cookiePairs = cookies.split(';');

    // 将解析后的Cookie键值对存储在req.cookies对象中
    req.cookies = {};

    for (const pair of cookiePairs) {
      const [name, value] = pair.split('=');
      req.cookies[name.trim()] = decodeURIComponent(value.trim());
    }
  }

  next();
}

// 在应用程序中使用cookieParser中间件
app.use(cookieParser);
```

在上述代码中，`cookieParser`函数是一个自定义的中间件函数，用于解析Cookie。它从请求头中获取`Cookie`字段的值，该字段包含了客户端发送的所有Cookie信息。然后，将Cookie字符串拆分成键值对形式，并存储在`req.cookies`对象中。

在拆分Cookie字符串时，使用分号(`;`)作为分隔符将每个键值对分开，然后再使用等号(`=`)将键和值分隔。解析后的键值对被存储在`req.cookies`对象中，以键名作为属性名，对应的值作为属性值。

需要注意的是，`cookie-parser`还会对Cookie值进行解码操作，将URL编码的值解码为原始的字符串形式，以确保正确的数据展示。

实际上，上述代码只是一个简化的示例，`cookie-parser`在实现中还涉及更多的功能，例如处理Cookie的选项、处理多个Cookie、设置Cookie等。但是，上述示例可以帮助理解`cookie-parser`的基本原理和工作流程。

总结来说，`cookie-parser`中间件通过解析请求头中的`Cookie`字段，将Cookie字符串解析为键值对的形式，并存储在`req.cookies`对象中，以便在Express应用程序中进行访问和处理。

# helmet 实现

`helmet`是一个常用的Express中间件，用于增强应用程序的安全性。它实现了一系列的安全性功能，以保护应用程序免受各种常见的Web攻击。下面是一个简化的示例来说明`helmet`的实现原理：

```javascript
function helmet(req, res, next) {
  // 设置适当的HTTP标头来增强安全性
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");

  next();
}

// 在应用程序中使用helmet中间件
app.use(helmet);
```

在上述代码中，`helmet`函数是一个自定义的中间件函数，用于增强应用程序的安全性。它通过设置适当的HTTP标头来增加安全性措施。

具体来说，代码中通过设置`res.setHeader`方法来设置以下HTTP响应头：

- `X-Content-Type-Options`：禁止浏览器进行MIME类型的嗅探，防止MIME类型的错误推测。
- `X-Frame-Options`：防止点击劫持攻击，限制页面的嵌入方式。
- `X-XSS-Protection`：启用浏览器内置的跨站脚本攻击(XSS)过滤器。
- `Strict-Transport-Security`：启用严格的传输安全机制 (HSTS)，强制使用HTTPS连接。
- `Content-Security-Policy`：定义内容安全策略，限制页面资源的加载来源。

通过设置这些HTTP标头，`helmet`中间件增加了应用程序的安全性，防止一些常见的攻击，如MIME类型错误、点击劫持、跨站脚本攻击等。

需要注意的是，上述代码只是一个简化的示例，实际的`helmet`中间件实现包括更多的安全性功能和配置选项，以适应不同的安全需求。使用`helmet`中间件可以方便地为Express应用程序提供基本的安全性保护，减少潜在的Web攻击风险。

# express-validator 实现原理

`express-validator`是一个常用的Express中间件，用于验证和处理请求数据。它提供了一组验证器函数和中间件，用于验证和处理请求中的数据，并生成有关验证结果的错误信息。下面是一个简化的示例来说明`express-validator`的实现原理：

```javascript
function expressValidator(req, res, next) {
  // 检查请求中的数据并进行验证
  const errors = [];

  // 验证器函数
  function check(field, value, validationFn) {
    if (!validationFn(value)) {
      errors.push(`${field} is invalid`);
    }
  }

  // 在req对象上附加验证器函数
  req.check = check;

  // 继续处理下一个中间件或路由处理程序
  next();
}

// 在应用程序中使用expressValidator中间件
app.use(expressValidator);
```

在上述代码中，`expressValidator`函数是一个自定义的中间件函数，用于验证请求数据。它定义了一个`check`函数，该函数用于对请求数据进行验证，并将验证错误信息存储在`errors`数组中。

在中间件函数中，将`check`函数附加到`req`对象上，以便在后续的中间件或路由处理程序中可以使用它来进行验证。通过调用`req.check`方法，并传递字段名、字段值和验证函数，可以进行数据验证。如果验证失败，将错误信息添加到`errors`数组中。

实际上，上述代码只是一个简化的示例，`express-validator`库提供了更丰富和灵活的功能，例如自定义验证规则、异步验证、错误处理等。它还提供了一些内置的验证器函数，例如检查是否为空、检查是否是数字、检查是否符合正则表达式等。

在实际使用`express-validator`时，通常会与Express的路由处理程序结合使用，根据请求中的数据进行验证，并根据验证结果返回适当的响应。

总结来说，`express-validator`中间件的实现原理是通过附加验证器函数到`req`对象上，在后续的中间件或路由处理程序中使用这些验证器函数对请求数据进行验证，并生成验证错误信息。这样可以方便地进行请求数据的验证和处理。



# express-session 原理

`express-session`是Express框架中的一个常用中间件，用于处理会话（Session）管理。它基于客户端与服务器之间的Cookie实现会话跟踪，并提供了一种简单的方式来存储和访问会话数据。下面是一个简化的示例来说明`express-session`的实现原理：

1. 当客户端发送请求时，`express-session`中间件会在请求处理流程中被调用。

2. 在请求对象(`req`)中，会检查是否存在与会话相关的Cookie。如果存在会话Cookie，那么它会包含一个会话标识符（Session ID）。

3. 如果请求中不存在会话Cookie，或者会话Cookie无效，则会创建一个新的会话。

4. 会话标识符会存储在响应对象(`res`)的Cookie中，通过`Set-Cookie`标头发送给客户端。这样，客户端在随后的请求中会携带会话标识符。

5. 服务器会将会话数据存储在某个持久化存储介质中，例如内存、数据库或文件系统。存储会话数据的方式可以通过配置进行调整。

6. 在后续的请求中，`express-session`中间件会根据会话标识符读取相应的会话数据，并将其添加到请求对象的`req.session`属性中，以供后续中间件或路由处理程序使用。

7. 中间件或路由处理程序可以通过访问`req.session`来读取和修改会话数据。对`req.session`对象的修改会被自动保存到持久化存储介质中。

总结来说，`express-session`中间件的实现原理是通过会话标识符和Cookie进行会话跟踪，并将会话数据存储在持久化存储介质中。它提供了一种简单的方式来创建、访问和管理会话数据，以实现用户会话的状态管理。



当您使用`express-session`中间件在Express应用程序中进行会话管理时，可以按照以下方式简单实现：

```javascript
const express = require('express');
const session = require('express-session');

const app = express();

// 配置会话中间件
app.use(session({
  secret: 'mysecretkey', // 用于签署会话ID Cookie的密钥
  resave: false, // 是否在每个请求上保存会话，即使未修改
  saveUninitialized: true, // 是否保存未初始化的会话（新建但未修改）
}));

// 示例路由以演示会话的使用
app.get('/counter', (req, res) => {
  // 访问会话数据并递增计数器
  if (req.session.counter) {
    req.session.counter++;
  } else {
    req.session.counter = 1;
  }

  res.send(`计数器：${req.session.counter}`);
});

app.listen(3000, () => {
  console.log('服务器正在端口3000上运行');
});
```

在这个代码示例中，我们首先引入了`express`和`express-session`模块。然后，使用`express()`创建了一个Express应用程序实例。

接下来，我们通过使用`app.use(session(options))`来配置`express-session`中间件。在这里，我们提供了一些选项：

- `secret`：用于签署会话ID Cookie的密钥，应该是您选择的字符串。
- `resave`：设置为`false`，以避免在每个请求上保存会话，即使未修改。
- `saveUninitialized`：设置为`true`，以保存未初始化的会话，即新建但未修改的会话。

配置完中间件后，我们定义了一个用于`/counter`路由的处理程序。在该处理程序中，我们使用`req.session`对象来读取和修改会话数据。在这个示例中，我们递增了会话中存储的一个`counter`值。

最后，我们启动Express服务器并监听3000端口。

当您在浏览器中访问`/counter`路由时，您将看到计数器值随每个请求递增。这演示了`express-session`如何在多个请求之间管理会话数据。

请注意，这只是一个简化的示例，在实际的应用程序中，您通常会使用更安全和持久的存储选项来存储会话数据，例如数据库或Redis。



# connect-flash 实现原理

`connect-flash`是一个常用的Express中间件，用于在重定向时在会话中存储一次性的消息，并在下一个请求中将其取出。它的实现原理相对简单，下面是一个简化的示例来说明其工作原理：

1. 当使用`connect-flash`中间件时，它会在请求处理流程中被调用。

2. 在请求对象(`req`)中，`connect-flash`中间件会添加一个名为`flash`的特殊属性，用于设置和获取一次性的消息。

3. 当您需要在重定向后的页面中显示一次性的消息时，您可以使用`req.flash(type, message)`方法将消息存储到`flash`属性中。`type`表示消息的类型，例如"success"、"error"等，而`message`则是要显示的具体消息内容。

4. `connect-flash`中间件会将消息存储在会话(`req.session`)中，以便在下一个请求中取出。

5. 当下一个请求到达时，您可以通过`req.flash(type)`方法获取相应类型的消息。这个方法会返回该类型的所有消息，并在会话中将这些消息删除，以确保它们只被取出一次。

6. 在您的路由处理程序或模板中，您可以使用这些消息来渲染相应的提示或反馈给用户。

总结来说，`connect-flash`中间件的实现原理是通过在会话中存储一次性的消息，并在下一个请求中将其取出。它简化了在重定向过程中传递消息的方式，使您可以方便地在不同请求之间传递和显示消息。

请注意，`connect-flash`中间件依赖于`express-session`中间件，因此在使用`connect-flash`之前，您需要先配置和使用`express-session`中间件。

# multer 实现原理

`multer`是一个Node.js的中间件，用于处理表单数据中的文件上传。它的实现原理相对复杂，但可以概括为以下几个步骤：

1. 在Express应用程序中使用`multer`中间件，通过`multer()`函数创建一个中间件实例。

2. 当请求到达服务器时，`multer`中间件会拦截包含文件上传的表单数据。

3. `multer`会解析请求中的表单数据，并将文件保存到指定的目录或内存中，同时生成一个或多个临时文件。

4. 在解析和保存文件的过程中，`multer`会为每个文件创建一个包含文件信息的对象，例如文件名、文件大小、文件类型等。

5. `multer`将这些文件对象附加到请求对象(`req`)的`files`属性上，以便在后续的请求处理中可以访问它们。

6. 用户可以在请求处理程序中访问`req.files`来获取上传的文件信息，并进行相应的处理，例如将文件移动到其他位置、修改文件名等。

需要注意的是，`multer`可以根据配置选项支持各种功能，例如限制文件大小、限制文件类型、多文件上传等。您可以通过配置选项来定制`multer`的行为，以满足特定的需求。

总结来说，`multer`中间件的实现原理是通过拦截表单数据中的文件上传，解析并保存文件，然后将文件对象附加到请求对象上，以便后续处理程序可以访问和处理上传的文件。这样，开发人员可以方便地处理文件上传的功能。



当使用`multer`中间件进行文件上传时，以下是一个简单的示例代码：

```javascript
const express = require('express');
const multer = require('multer');

const app = express();

// 配置multer中间件
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // 指定文件保存的目录
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    // 自定义文件名
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage });

// 处理文件上传的路由
app.post('/upload', upload.single('file'), (req, res) => {
  // 获取上传的文件信息
  const file = req.file;

  if (!file) {
    return res.status(400).send('未选择文件');
  }

  // 文件上传成功
  res.send('文件上传成功');
});

app.listen(3000, () => {
  console.log('服务器正在端口3000上运行');
});
```

在上述示例中，我们首先引入了`express`和`multer`模块。然后，创建了一个Express应用程序实例。

接下来，我们使用`multer.diskStorage`配置`multer`中间件的存储选项。在这里，我们指定了文件保存的目录(`destination`)和自定义的文件名(`filename`)。

然后，我们通过`multer({ storage })`创建一个`upload`中间件实例，将存储选项传递给它。

在路由处理程序中，我们使用`upload.single('file')`来处理文件上传。这里的`'file'`是表单中文件上传字段的名称，您可以根据实际情况进行修改。

在处理程序中，我们可以通过`req.file`获取上传的文件信息。如果没有选择文件，我们返回一个错误响应。否则，我们返回一个成功的响应。

最后，我们启动Express服务器并监听3000端口。

通过这个示例，您可以进行简单的文件上传，并获取上传文件的信息进行后续处理。请确保在运行示例之前，创建一个名为`uploads`的目录，用于保存上传的文件。

# node-fetch 实现原理

`node-fetch`是一个用于在Node.js环境中进行HTTP请求的库，它的实现原理可以简单概括如下：

1. 当您在Node.js中使用`node-fetch`库时，首先需要安装该库并导入它。

2. 在代码中，通过调用`fetch(url, options)`方法来发起HTTP请求。其中，`url`表示请求的目标URL，而`options`是一个可选参数对象，用于配置请求的各种选项，如请求方法、请求头、请求体等。

3. 在`fetch`方法内部，它会创建一个`Request`对象，封装了请求的相关信息，包括URL、方法、请求头、请求体等。

4. `fetch`方法会使用`node-fetch`库提供的底层机制，将`Request`对象发送到目标URL，并等待服务器的响应。

5. 一旦收到服务器的响应，`fetch`方法会返回一个`Promise`对象，该对象表示异步操作的结果。您可以使用`.then()`方法来处理响应的数据，或使用`async/await`语法进行异步处理。

6. 当您使用`.then()`方法或`async/await`来处理响应时，可以通过响应对象的方法（如`response.text()`、`response.json()`等）来获取响应的数据。

总结来说，`node-fetch`库的实现原理是通过创建`Request`对象并使用底层机制发送HTTP请求，然后返回一个`Promise`对象以表示异步操作的结果。开发人员可以使用`.then()`方法或`async/await`语法来处理响应并获取响应数据。

需要注意的是，`node-fetch`库基于标准的Fetch API规范，并在Node.js环境中实现了该规范的功能。它提供了与浏览器中的`fetch`函数类似的使用方式，使得在Node.js中进行HTTP请求变得更加简单和便捷。

# 在express里使用node-fetch举例

在Express中使用`node-fetch`库可以实现在服务器端发起HTTP请求。以下是一个示例，展示如何在Express路由处理程序中使用`node-fetch`：

```javascript
const express = require('express');
const fetch = require('node-fetch');

const app = express();

app.get('/api/data', async (req, res) => {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: '请求数据失败' });
  }
});

app.listen(3000, () => {
  console.log('服务器正在端口3000上运行');
});
```

在上述示例中，我们首先导入了`express`和`node-fetch`模块。然后，创建了一个Express应用程序实例。

在路由处理程序中，我们使用`app.get`定义了一个GET请求的路由，路径为`/api/data`。

在路由处理程序的实现中，我们使用`node-fetch`库发起一个HTTP GET请求，目标URL为`https://api.example.com/data`。

我们使用`await`关键字将异步操作包装在`try/catch`块中。通过`await fetch(url)`发起请求后，我们使用`await response.json()`将响应的JSON数据解析为JavaScript对象。

最后，我们使用`res.json()`将获取到的数据作为响应发送给客户端。

如果发生错误，我们使用`res.status(500)`发送一个HTTP 500错误响应。

通过这个示例，您可以在Express应用程序中使用`node-fetch`库来发起HTTP请求，并在路由处理程序中处理返回的数据。这样，您可以方便地在服务器端获取其他API的数据，并将其返回给客户端。

# 为什么需要在服务端发起http请求？

在服务器端发起HTTP请求有多种原因和用途：

1. 数据聚合和整合：服务器端可能需要从多个外部API或服务中获取数据，并将它们聚合或整合成一个响应返回给客户端。通过在服务器端发起HTTP请求，可以方便地获取其他服务的数据，进行处理和转换后再返回给客户端。

2. 访问受限资源：某些资源可能受到访问限制，只允许来自特定IP地址或服务器的请求。在服务器端发起请求可以绕过客户端访问限制，并获取受限资源的内容。

3. 数据预处理：在将数据返回给客户端之前，服务器端可能需要对数据进行一些预处理、清理或过滤。通过在服务器端发起HTTP请求，可以获取原始数据并进行必要的处理，以确保返回给客户端的数据符合要求。

4. 访问外部服务：服务器端可能需要与其他服务进行交互，例如发送电子邮件、发送短信、调用第三方支付接口等。通过在服务器端发起HTTP请求，可以与这些外部服务进行通信，执行相应的操作。

5. 提高性能和安全性：在服务器端发起HTTP请求可以减少客户端与外部服务之间的直接通信，从而提高系统性能。此外，服务器端可以对外部请求进行安全性验证和过滤，确保只允许合法的请求通过。

总结来说，服务器端发起HTTP请求可以方便地获取外部资源、处理数据、与其他服务进行交互，并提供更高的性能和安全性。这使得服务器端具有更多的灵活性和控制力，可以实现更复杂的业务逻辑和功能。

# express 的错误处理

在Express中，您可以通过中间件来处理和捕获错误，以提供更好的错误处理机制。以下是一些常见的错误处理方法：

1. 使用错误处理中间件：
   ```javascript
   app.use((err, req, res, next) => {
     // 处理错误
     res.status(500).json({ error: '服务器错误' });
   });
   ```
   在应用程序的顶层或特定路由之后，可以定义一个错误处理中间件。错误处理中间件需要四个参数，其中第一个参数是错误对象。在这里，您可以根据需要对错误进行自定义处理，并返回适当的响应。

2. 使用try-catch语句：
   ```javascript
   app.get('/api/data', (req, res) => {
     try {
       // 可能引发错误的代码
       const data = someFunction();
       res.json(data);
     } catch (err) {
       // 处理错误
       res.status(500).json({ error: '服务器错误' });
     }
   });
   ```
   在路由处理程序中，您可以使用try-catch语句来捕获可能引发错误的代码块。如果发生错误，可以在catch块中进行错误处理，并返回适当的响应。

3. 使用自定义中间件：
   ```javascript
   const errorHandler = (err, req, res, next) => {
     // 处理错误
     res.status(500).json({ error: '服务器错误' });
   };

   app.use(errorHandler);
   ```
   您可以创建自定义的错误处理中间件，将其放置在应用程序的顶层或特定路由之后。这样，当发生错误时，请求将被传递到错误处理中间件进行处理。

无论您选择哪种方法，都可以根据具体情况自定义错误处理逻辑。您可以根据错误类型、状态码、日志记录等进行适当的处理，并向客户端返回合适的错误响应。

# express multipart举例

当在Express中处理包含文件上传的表单时，您可以使用`multer`中间件来处理multipart/form-data类型的请求。以下是一个使用`multer`处理文件上传的示例：

首先，您需要安装`multer`包：
```
npm install multer
```

然后，您可以创建一个包含文件上传的路由，并使用`multer`中间件来处理请求：
```javascript
const express = require('express');
const multer = require('multer');

const app = express();

// 创建multer实例，并指定上传文件的保存目录和文件名
const upload = multer({ dest: 'uploads/' });

// 使用multer中间件来处理文件上传
app.post('/upload', upload.single('file'), (req, res) => {
  // req.file包含上传的文件信息
  if (!req.file) {
    res.status(400).json({ error: '请选择一个文件' });
    return;
  }

  // 文件上传成功
  res.json({ message: '文件上传成功' });
});

app.listen(3000, () => {
  console.log('服务器正在端口3000上运行');
});
```

在上述示例中，我们首先导入`multer`中间件，并创建一个`multer`实例。通过指定`dest`选项，我们设置文件的保存目录为`uploads/`。

然后，我们定义一个POST路由`/upload`，并将`upload.single('file')`作为中间件来处理文件上传。这里的`file`是表单字段的名称，用于指定上传的文件。

在路由处理程序中，我们可以通过`req.file`访问上传的文件信息。如果`req.file`不存在，表示没有选择文件进行上传，我们返回一个错误响应。

如果文件上传成功，我们返回一个成功的响应。

需要注意的是，这里的示例只处理单个文件的上传。如果需要处理多个文件上传，可以使用`upload.array('files')`来处理以`files`为字段名称的多个文件上传。

通过以上示例，您可以使用`multer`中间件在Express中方便地处理文件上传的请求。

# express实现vhost

在Express中，您可以使用`vhost`中间件来实现虚拟主机（Virtual Host）的功能，允许您根据请求的主机名（hostname）来路由请求到不同的子应用程序。

以下是使用`vhost`中间件实现虚拟主机的示例：

1. 安装`vhost`包：
```
npm install vhost
```

2. 创建主应用程序和子应用程序：
```javascript
const express = require('express');
const vhost = require('vhost');

// 创建主应用程序
const app = express();

// 创建子应用程序1
const app1 = express();
app1.get('/', (req, res) => {
  res.send('子应用程序1');
});

// 创建子应用程序2
const app2 = express();
app2.get('/', (req, res) => {
  res.send('子应用程序2');
});

// 定义虚拟主机
app.use(vhost('app1.com', app1)); // 将请求主机名为app1.com的请求路由到子应用程序1
app.use(vhost('app2.com', app2)); // 将请求主机名为app2.com的请求路由到子应用程序2

// 启动服务器
app.listen(3000, () => {
  console.log('服务器正在端口3000上运行');
});
```

在上述示例中，我们创建了一个主应用程序和两个子应用程序。子应用程序1和子应用程序2分别定义了根路由处理程序。

通过使用`vhost`中间件，我们可以将不同的主机名映射到不同的子应用程序。在示例中，我们使用`vhost('app1.com', app1)`将主机名为`app1.com`的请求路由到子应用程序1，使用`vhost('app2.com', app2)`将主机名为`app2.com`的请求路由到子应用程序2。

当访问`app1.com`时，将会得到子应用程序1的响应，而当访问`app2.com`时，将会得到子应用程序2的响应。

这样，您可以根据不同的主机名配置不同的子应用程序，从而实现虚拟主机的功能。

需要注意的是，为了使虚拟主机生效，您需要配置相应的DNS解析和主机配置。您可以在本地的`hosts`文件或者DNS服务器上进行配置，将相应的主机名映射到本地开发环境的IP地址上。

通过上述示例，您可以了解如何使用`vhost`中间件在Express中实现虚拟主机功能，以便根据不同的主机名路由请求到不同的子应用程序。



# 什么是vhost？原理是什么？

在网络领域，vhost（Virtual Host，虚拟主机）是指在同一台服务器上运行多个网站或应用程序，每个网站或应用程序都有自己的域名和独立的配置。

虚拟主机的原理是通过在服务器上配置不同的域名和对应的目录，将来自不同域名的请求路由到不同的目录和处理程序。这样，多个网站或应用程序可以共享同一台服务器资源，但彼此之间相互隔离。

以下是虚拟主机的原理简要说明：

1. 域名解析：将域名解析到服务器的IP地址。当用户通过浏览器访问某个域名时，DNS解析会将域名解析为服务器的IP地址。

2. 请求路由：服务器根据请求中的域名来确定访问哪个虚拟主机。服务器会检查请求的`Host`头部字段，该字段包含了请求的域名。根据该字段的值，服务器判断请求属于哪个虚拟主机。

3. 虚拟主机配置：每个虚拟主机都有自己独立的配置，包括根目录、日志文件、SSL证书等。服务器根据请求的域名匹配相应的虚拟主机配置。

4. 请求处理：一旦确定了请求属于哪个虚拟主机，服务器将请求交给相应的虚拟主机进行处理。虚拟主机可以有自己的路由、中间件和业务逻辑，与其他虚拟主机相互独立。

通过虚拟主机，可以实现在同一台服务器上托管多个网站或应用程序，提高资源利用率，降低成本。虚拟主机可以灵活地配置多个域名，为不同的网站或应用程序提供定制化的设置。

在Node.js的Express框架中，可以使用`vhost`中间件来实现虚拟主机的功能。`vhost`中间件允许根据请求的域名将请求路由到不同的Express应用程序或路由处理程序。

虚拟主机是Web服务器中常见的功能，它使得在同一台服务器上托管多个网站变得简单而高效。通过虚拟主机，可以轻松管理多个域名，提供个性化的网站配置和服务。

# flask可以实现虚拟主机吗

在Flask中，可以使用Blueprint（蓝图）来实现虚拟主机的功能。虚拟主机可以用于在同一应用程序中处理多个域名的请求，并根据不同的域名进行路由和处理。

以下是使用Flask Blueprint实现虚拟主机的示例：

1. 创建Flask应用程序：
```python
from flask import Flask
app = Flask(__name__)
```

2. 创建虚拟主机的蓝图（Blueprint）：
```python
from flask import Blueprint

# 创建蓝图
vhost1 = Blueprint('vhost1', __name__)
vhost2 = Blueprint('vhost2', __name__)

# 定义路由和处理程序
@vhost1.route('/')
def vhost1_home():
    return '虚拟主机1'

@vhost2.route('/')
def vhost2_home():
    return '虚拟主机2'

# 注册蓝图
app.register_blueprint(vhost1, subdomain='vhost1', url_prefix='/')
app.register_blueprint(vhost2, subdomain='vhost2', url_prefix='/')
```

在上述示例中，我们创建了两个虚拟主机的蓝图，即`vhost1`和`vhost2`。每个蓝图都定义了一个根路由和相应的处理程序。

通过`register_blueprint`方法，我们将这些虚拟主机的蓝图注册到Flask应用程序中。`subdomain`参数指定了虚拟主机的子域名，`url_prefix`参数指定了虚拟主机的URL前缀。

3. 启动服务器：
```python
if __name__ == '__main__':
    app.run()
```

通过运行Flask应用程序，服务器将监听请求并根据请求的域名将请求路由到相应的虚拟主机蓝图处理程序。

请注意，要使虚拟主机在本地开发环境中生效，您需要在`hosts`文件或DNS服务器中配置相应的域名解析，将虚拟主机的域名映射到本地开发环境的IP地址上。

使用Flask的Blueprint机制，您可以在同一应用程序中实现虚拟主机的功能，根据不同的域名进行路由和处理，从而提供定制化的网站或应用程序服务。

# 自己用python socket编程实现vhost

实现虚拟主机功能可以使用Python的socket编程，通过监听不同的域名和端口，并根据请求的域名来路由请求到不同的处理程序。

下面是一个简单的示例，使用Python的socket编程实现基本的虚拟主机功能：

```python
import socket
import threading

# 处理客户端请求的函数
def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    
    # 解析请求报文中的域名
    hostname = None
    for line in request_data.split('\r\n'):
        if line.startswith('Host:'):
            hostname = line.split(' ')[1]
            break
    
    # 根据域名进行路由
    if hostname == 'vhost1.com':
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello from Virtual Host 1!'
    elif hostname == 'vhost2.com':
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello from Virtual Host 2!'
    else:
        response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n404 Not Found'
    
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

# 启动服务器
def start_server():
    host = '127.0.0.1'
    port = 80
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f'Server listening on {host}:{port}')
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'New connection from {client_address[0]}:{client_address[1]}')
        
        # 创建一个新线程来处理客户端请求
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# 启动服务器
start_server()
```

在上述示例中，我们创建了一个基本的HTTP服务器，通过解析请求报文中的域名来实现虚拟主机功能。根据不同的域名，我们发送不同的响应给客户端。

请注意，这只是一个简化的示例，用于说明虚拟主机的基本原理。在实际生产环境中，需要更完善的错误处理、安全性考虑和性能优化等。

使用Python的socket编程实现虚拟主机功能可以帮助您理解底层的网络通信原理，但对于实际生产环境的应用，通常建议使用成熟的Web框架（如Flask、Django等）来处理复杂的网络请求和应用逻辑。

# flask和express对比

Flask和Express是两个流行的Web应用框架，分别基于Python和Node.js开发。它们都提供了一组工具和功能，用于构建Web应用程序，但在一些方面存在一些区别。

下面是一些Flask和Express的比较：

1. 语言和生态系统：Flask使用Python作为开发语言，而Express使用Node.js。Python拥有广泛的生态系统和强大的数据科学库，适合于数据分析和科学计算。Node.js则以非阻塞I/O和事件驱动的特性而闻名，适合构建高并发的网络应用。

2. 代码风格和结构：Flask采用较为简洁和自由的代码风格，让开发者可以按照自己的喜好组织项目结构。Express则采用了更加约定和结构化的代码风格，有助于在团队开发中保持一致性。

3. 异步编程：由于Node.js的特性，Express更加注重异步编程和非阻塞I/O，适合处理高并发请求。Flask则是基于Python的同步编程模型，适用于较小规模的应用。

4. 中间件：Express的中间件系统非常灵活，可以通过中间件来处理请求和响应。Flask也有中间件概念，但不如Express的中间件系统灵活。

5. 数据库支持：Flask与Python的ORM（对象关系映射）工具集成较好，如SQLAlchemy。Express则可以与多种数据库进行集成，但没有内置的ORM工具。

6. 社区和生态系统：Flask和Express都有活跃的开发者社区和丰富的第三方库支持。Flask的社区较大且成熟，有大量的插件和扩展可供选择。Express的社区也非常活跃，有许多NPM包可用。

选择使用Flask还是Express取决于多个因素，包括开发者的偏好、项目需求、团队技术栈和生态系统。如果您熟悉Python和想要利用其丰富的生态系统，同时构建较小规模的应用，Flask可能是一个不错的选择。如果您熟悉JavaScript和Node.js，并且需要处理高并发请求或构建实时应用，那么Express可能更适合您的需求。

# 参考资料

1、Node.js Express 框架

http://www.runoob.com/nodejs/nodejs-express-framework.html

2、

https://blog.csdn.net/wthfeng/article/details/53366169

3、Express使用html模板

https://www.cnblogs.com/-nothing-/p/4943354.html