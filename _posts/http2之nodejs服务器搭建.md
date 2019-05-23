---
title: http2之nodejs服务器搭建
date: 2019-05-22 15:00:51
tags:
	- http

---



# 基本例子

生成2048位的rsa私钥，采用des算法进行加密，输出文件名为server.pass.key。

密码为123456

```
openssl genrsa -des3 -passout pass:"123456" -out server.pass.key 2048
```

```
openssl rsa -passin pass:"123456" -in server.pass.key -out server.key
```

```
openssl req -new -key server.key -out server.csr
```

这个命令会让你输出一些信息。随便填写就行了。

还有一个密码，不知道是干啥用的。我也输入123456。

```
openssl x509 -req -sha256 -days 365 -in server.csr -signkey server.key -out server.crt
```

```
rm server.pass.key
```

然后

```
npm init -y
npm install --save express sdpy
touch app.js
```

现在目录结构是这样：

```
hlxiong@hlxiong-VirtualBox:~/work/test/http2$ ls
app.js  h2-node  node_modules  package.json  package-lock.json
```

那些证书都在h2-node目录下。

app.js内容：

```
const spdy = require('spdy');
const express = require('express');
const path = require('path');
const fs = require('fs');

const port = 4000;
const app = express();

app.get('*', (req, res) => {
    res
      .status(200)
      .json({error: 0, msg: "http2 OK"});
})

const options = {
    key: fs.readFileSync(__dirname + '/h2-node/server.key'),
    cert:  fs.readFileSync(__dirname + '/h2-node/server.crt')
}

spdy
  .createServer(options, app)
  .listen(port, (error) => {
    if (error) {
      console.error(error)
      return process.exit(1)
    } else {
      console.log('Listening on port: ' + port + '.')
    }
  })
```

访问https://localhost:4000就可以看到结果了。



# 用http2模块

```
npm install --save http2
```

注意，外层目录不能叫http2了。我改成http2_test。不然安装不行。

server.js

```
const http2 = require('http2');
const fs = require('fs');

const server = http2.createSecureServer({
  key: fs.readFileSync('./h2-node/server.key'),
  cert: fs.readFileSync('./h2-node/server.crt')
});
server.on('error', (err) => console.error(err));

server.on('stream', (stream, headers) => {
  // stream 是一个双工流
  stream.respond({
    'content-type': 'text/html',
    ':status': 200
  });
  stream.end('<h1>Hello World</h1>');
});

server.listen(8443);
```

client.js

```
const http2 = require('http2');
const fs = require('fs');
const client = http2.connect('https://localhost:8443', {
  ca: fs.readFileSync('./h2-node/server.crt')
});
client.on('error', (err) => console.error(err));

const req = client.request({ ':path': '/' });

req.on('response', (headers, flags) => {
  for (const name in headers) {
    console.log(`${name}: ${headers[name]}`);
  }
});

req.setEncoding('utf8');
let data = '';
req.on('data', (chunk) => { data += chunk; });
req.on('end', () => {
  console.log(`\n${data}`);
  client.close();
});
req.end();
```

当前会有错误提示。

```
Error [ERR_HTTP2_STREAM_CANCEL]: The pending stream has been canceled (caused by: Hostname/IP does not match certificate's altnames: Host: localhost. is not cert's CN: teddy)
    at ClientHttp2Session.destroy (internal/http2/core.js:1220:20)
    at TLSSocket.socketOnError (internal/http2/core.js:2606:13)
    at TLSSocket.emit (events.js:182:13)
    at emitErrorNT (internal/streams/destroy.js:82:8)
    at emitErrorAndCloseNT (internal/streams/destroy.js:50:3)
    at process._tickCallback (internal/process/next_tick.js:63:19)
Emitted 'error' event at:
    at emitErrorNT (internal/streams/destroy.js:82:8)
    at emitErrorAndCloseNT (internal/streams/destroy.js:50:3)
    at process._tickCallback (internal/process/next_tick.js:63:19)
```

应该我签名的时候，主机名给了teddy。

我重新生成一下看看。主机名就用localhost。

这样来生成。

```
openssl req -x509 -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' \
  -keyout localhost-privkey.pem -out localhost-cert.pem
```





参考资料

1、简单配置 http2 和 node.js

https://juejin.im/entry/57f3a546da2f60004f6eebbc

2、Node.js 的 Http/2 模块

https://itbilu.com/nodejs/core/Sy-2trZhQ.html

3、Node.js之HTTP/2服务器推送

https://blog.fundebug.com/2018/03/27/nodejs-and-http/