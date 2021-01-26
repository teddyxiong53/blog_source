---
title: js之codemirror
date: 2021-01-21 16:05:11
tags:
	- js

---

--

看https://github.com/EvineDeng/jd-base/blob/v3/panel 这个用到了codemirror做在线代码编辑功能。

看看codemirror。

codemirror是一个在浏览器里运行的代码编辑器，支持100多种语言。

还支持wiki、markdown、sql等文件格式。

如果需要在页面里嵌入一个代码编辑区，codemirror是最佳的选择。

https://github.com/codemirror/CodeMirror

使用方法：

文件分为js和css文件。

在jd-base的panel里，用到了这3个css文件。

codemirror.min.css 这个是核心css文件。

后面2个是主题css。一个白天，一个夜间。

```
<link rel="stylesheet" type="text/css" href="./css/codemirror.min.css">
    <link rel="stylesheet" type="text/css" href="./css/twilight.css">
    <link rel="stylesheet" type="text/css" href="./css/dracula.css">
```



# HelloWorld

这个官方没有给一个比较简单的例子。

我现在在panel/public下，新建一个test.html来做一下测试看看。

首先，需要引入需要的文件。

```
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script type="text/javascript" src="./js/jquery.min.js"></script>
    <script type="text/javascript" src="./js/codemirror.min.js"></script>
    <link rel="stylesheet" type="text/css" href="./css/codemirror.min.css">
    <link rel="stylesheet" type="text/css" href="./css/twilight.css">
</head>

<body>
    <div>
        <textarea name="testcode" id="testcode" ></textarea>
    </div>
    <script>
        $(document).ready(function () {
            var editor = CodeMirror.fromTextArea(document.getElementById('testcode'), {
                //构造选项
                theme: 'twilight',
                mode: 'shell',//用哪种编程语言的进行解析
            })
        })
    </script>

</body>
</html>
```

显示是这样：

![image-20210122104052380](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210122104052380.png)



对上面的进行改进，从文件读取内容填入编辑器里。

然后按钮进行保存到文件。

input file来读取文件内容，发现这个点我就有点难搞。



在浏览器中操作文件，多数情况下用到的是 File 对象，从<input type='file' />元素获取，

进而继续操作(例如将选择的图片展示在页面上，用ajax将文件上传至服务器等)。

这里介绍在浏览器中操作文件的相关API.

File 对象继承自 Blob 对象，先看看 Blob 对象。



一个 FileList 对象通常来自于一个 HTML <input> 元素的 files 属性，你可以通过这个对象访问到用户所选择的文件。

```
var file = document.getElementById('fileItem').files[0];
```

但是看这个，还是只能得到文件的名字。



这个其实是比较麻烦的。不这么做了。因为浏览器里直接读取本地文件，是被浏览器的安全策略禁止的。

# 填入内容

```
editor.setValue('<html><h1>123</h1></html>')
```

读取是这样

```
var data = editor.getValue();
```

# 扩展语言

jd-docker里，有一个shell.js。就是对codemirror扩展shell脚本语法支持的。

看看是如何进行扩展的。

codemirror的设计思路是，分为3个部分：

1、核心。

2、模式。

3、扩展。

核心库对外开放了很多接口。我们基于这些接口来实现新的模式和新的扩展。

如果我们需要的mode不在codemirror自带的mode库里的话，那么我们就需要自己来扩展。

例如ini就没有。

mode和language不是一一对应的关系。

例如，在html代码里，往往也有css和js代码。

对于这个，我们需要抽象一个htmlmixed模式，也就是多重模式。



大致原理

拿典型的js文件来说。

要完成js mode，只有定义一个词法分析程序就可以了。

首先，codemirror已经对整个js文件按行进行了拆分。

你在mode里需要做的，就是写一个词法分析程序分析每一行数据。

对于单行的字符串，词法分析程序需要从字符串开头分析到结束。

在这个过程中，会对需要识别的字符或者字符串进行特殊标记机，例如`[],{},(),this`等。

并且返回一个css样式给对于的字符或者字符串，用来做高亮显示。

这个就是基本的处理。

更高级的处理，就是进行缩进等。

首先主要注册一个mode。

使用CodeMirror.defineMode这个函数。

以shell.js为例。

```
CodeMirror.defineMode('shell', function() {
	//这里面有100多行代码，占了本文件的大部分内容。
}
```

defineMode函数有2个参数：

参数1：mode的名字。

参数2：一个函数。这个函数有2个可选参数。一个是CodeMirror的配置对象，一个是mode的配置对象。





参考资料

1、CodeMirror在线代码编辑器安装和使用

https://blog.csdn.net/qq_35038153/article/details/78991895

2、

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/Input/file

3、

https://www.runoob.com/try/try.php?filename=tryjsref_onchange

4、

https://www.runoob.com/jsref/prop-fileupload-value.html

5、

https://blog.csdn.net/snshl9db69ccu1aikl9r/article/details/108612839

6、Web 开发技术   Web API 接口参考  FileList

https://developer.mozilla.org/zh-CN/docs/Web/API/FileList

7、CodeMirror编辑器文本框Textarea代码高亮插件，CodeMirror的简单实用例子

https://www.cnblogs.com/zhenfei-jiang/p/7131024.html

8、

https://www.cnblogs.com/xmzzp/p/4318265.html