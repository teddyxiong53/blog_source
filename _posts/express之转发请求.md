---
title: express之转发请求
date: 2020-12-24 18:08:30
tags:
- express
---

1

我主要是想要搞清楚，在express里，请求其他的服务器，然后把结果处理一下，再返回给用户。

这个在微信服务端开发里是常见的场景。

而且在用nodejs做中间层的时候，应该也是需要的。

有5种常用方法

http标准库

request库

axios

superagent

got

下面以请求nasa的每日太空照片API为例进行讲解。

得到的是json格式的回复。

DEMO_KEY这个字符串是可以作为api_key用的。不会报错的。

# http标准库

```
var https = require('https')

https.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY', (resp)=> {
    let data =''
    resp.on('data', chunk=> {
        data += chunk
    })
    resp.on('end', ()=> {
        console.log(JSON.parse(data).explanation)
    })
}).on('error', (err)=> {
    console.log('Error: ' + err.message)
})

console.log('end')
```

http标准库的缺点：

1、你需要以chunk为单位收取数据，需要监听data和end这2个事件。

2、数据如果是json格式的，你还需要自己来解析。

3、http和https属于2个不同 模块，你得明确写出来。这就通用性不够好。

一般不直接用http标准库。

# request库

request的作用跟python里requests库作用类似。

简化了标准http库的使用，增强了功能。

是首选方案。

安装：

```
npm i request
```

同样实现上面的功能，代码如下。

```
var request = require('request')
request('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY', {json:true}, (err, res, body)=> {
    if(err) {
        return console.log(err)
    }
    console.log(body.url)
    console.log(body.explanation)
})
```

改进：

1、http和https用同样的接口。

2、不需要自己手动解析json。

3、只需要一个完成的回调函数。

# axios

这个是基于promise的http客户端。

可以在浏览器和nodejs里使用。

安装

```
npm i axios
```

代码

```
var axios = require('axios')
axios.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')
.then(response => {
    console.log(response.data.url)
    console.log(response.data.explanation)
})
.catch(e=> {
    console.log(e)
})
```

可以看到，代码有这些特点：

1、默认自动解析了json。

2、使用了异步机制。then

可以使用axios.all函数来发起多个并发请求。

```
var axios = require('axios')
var url1 = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2017-08-03'
var url2 = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2017-08-04'

axios.all([
    axios.get(url1),
    axios.get(url2)
]).then(axios.spread((res1, res2) => {
    console.log(res1.data.url)
    console.log(res2.data.url)
})).catch(e=> {
    console.log(e)
})
```

# superagent

在浏览器里用得比较多。

# got

特点是轻量。不看了。



参考资料

1、【译】深入解析Node.js中5种发起HTTP请求的方法

https://segmentfault.com/a/1190000010698468