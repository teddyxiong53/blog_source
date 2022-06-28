---
title: express之模板引擎
date: 2021-01-27 11:51:11
tags:
	- express

---

--

看了不少的express项目，发现大家是各种模板引擎都在用。所以还是把模板引擎梳理一下，方便阅读别人的项目代码。

支持的模板引擎有：

jade（默认），现在改名为pug了。这个受haml启发

haml.js。

ejs

dust.js

dot

mustache

handlerbars。

nunjunks

ejs-mate



发现有些用的模板，在官网都没有列出来。

例如：xtpl。



希望模板引擎提供这些特性：

1、支持模板继承extend。

2、支持模板扩展block。

3、支持模板组合。

4、支持预编译。

可以混合使用多种模板引擎。

只需要在render('index.jade')这样后面加上对应的后缀名就好了。



保证能看懂就好了。我主要还是用ejs的。



# pug

这个在所有的模板引擎里，算是最特别的。

因为它的结构，完全不像html的风格。

而是python风格的。

这个就不看了。不会用这个的。

# 模板引擎原理

javascript的模板引擎主要战场是浏览器和node端，两端其实差不多，常用的就是jade，ejs，art-template，



​	关于视图模板的初始设置大部分是放在app.settings对象中，相关属性有

- view    管理视图模板的类，一个实例对应一个试模板文件

- views   视图模板文件存放的路径

- view engine   默认的视图模板引擎名称

  

```
 var engine = require('ejs-mate'),
 // use ejs-locals for all ejs templates:
  app.engine('ejs', engine);
   
  app.set('views', __dirname + '/views');
  app.set('view engine', 'ejs'); // so you can render('index') 加上这句，就是可用省略后缀名的。
```

  

  还有一个关于视图模板的引擎类型的属性，单独放在app.engines对象中

在Express上唯一暴露的使用接口就是res.render,所以我们就从这个函数看起

```
res.render = function render(view, options, callback) { //codes... }
```

可以看到，他的参数有三个，

其中view参数是必选的,是要渲染的模板文件的名字，

剩下的两个是可选的，

内部会根据参数数量进行包装,

其中view还是view，

opts将传进的options和response对象的locals属性进行了合并，

done参数是传入的，可选的，接收模板最后输出的字符串的函数，如果不传入就会简单的包装成如下

```
 done = done || function (err, str) {
    if (err) return req.next(err);
    self.send(str);
 };
```

​	在app.render中会再次对opts选项进行合并，

将一些全局的属性合并进去，

最后生成一个renderOptions对象，

该对象表示一次模板渲染的所有选项。

同时在这里，还会生成模板文件管理实例，

也就是前面说过的View的一个实例，

这个实例管理这个名字的模板文件和对应解析引擎之间的映射关系，

**如果这个管理实例有被缓存，就会直接在缓存中取。**

最后将view实例，renderOptions对象，和包装的done函数传给，tryRender函数

```
tryRender(view, renderOptions, done);
```

# 自己写一个简单的模板引擎

取名为vin。

就实现一个变量替换渲染的功能。变量用$包裹起来。

```
// hello.vin
<html>
<head>
    <title>$title$</title>
</head>
input content is $content$;
</html>
```

```
const VinParser = require('./VinParser.js');
app.engine('vin', VinParser);
```

```
const fs = require('fs');
const regexp = /(?<=$).*?(?=$)/g;
module.exports = function VinParser(path, options, callback) {
    var res;
    try {
        str = fs.readFileSync(path).toString();
        const matchedKeys = str.match(regexp);
        for (let key of matchedKeys) {
            console.log(key, options[key]);
            str = str.replace(`$${key}$`, options[key]);
        }
        res = str;
    } catch (err) {
        callback(err);
    }
    callback(null, res);
}
```

调用进行渲染

```
/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('hello', {
    content: 'HelloWorld',
    title: 'vin template'
  });
});

```

# ejs-mate和ejs关系

应该是田永强同学的一个ejs分支，实现了layout模板等其他优化。

我印象中是 ejs 最新版不支持 partial，只支持 include。所以包了一层。

不过这东西是历史产物了。



参考资料

1、

https://cnodejs.org/topic/5416f576b7bf157329027972

# 参考资料

1、Express：模板引擎深入研究

https://www.cnblogs.com/chyingp/p/express-render-engine.html

2、

https://expressjs.com/en/resources/template-engines.html

3、

https://juejin.cn/post/6955450775338221599