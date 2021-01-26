收集一些简单实用的web系统。

主要关注js全栈的。

前后端不分离的，就用bootstrap来做页面。

前后端分离的，就基于elementui来做前端页面。



# cnode

这个是express写的简单实用的论坛程序。

基于bootstrap的前端界面。

也提供了api。可以自己用vue实现界面。

具备实用价值。

而且围绕这个有一系列的开源软件，适合作为学习练习的项目。

代码：

https://github.com/cnodejs/nodeclub

这个是相关的代码：

https://github.com/topics/cnodejs

# jd-base/panel

https://github.com/EvineDeng/jd-base/blob/v3/panel

基于express。

有网页上编辑文本的功能。实用codemirror这个css文件和js文件。

有二维码生成。

可以做简单的需要编辑配置一些文件的系统。



# 结合cnode和panel

cnode和panel这2套，在理念上存在较大的不同。

以表单的提交为例，

panel的不是以表单为单位，而是给按钮绑定一个函数。

用jquery的post函数，手动取得username等信息再发送。

这个方式其实不太好。

而返回，也是靠弹窗来提示信息。

而cnode里，则是靠表单的action来提交。

返回信息，是靠重新渲染当前页面，信息是靠一个依赖error信息的div来显示。



我当前把两种风格混合起来，导致了混乱。

所以，统一为cnode的风格。



文件虽然浏览器可以识别，但是强制它点击时被下载。

指定超链接的download属性就好了。

```
<a href="/1.txt" download="1.txt">点击下载</a>
```

https://stackoverflow.com/questions/3802510/force-to-open-save-as-popup-open-at-text-link-click-for-pdf-in-html







基于bootstrap和express搭建一个最小模板

尽量少手写代码。

```
1、express -e 
	这样就是使用ejs模板，在当前目录生成了一个工程。
2、npm i
	这样就安装好了依赖。
3、百度搜索下载bootstrap、jquery，把min版本的文件，放到/public下面的目录里。
4、写一点测试代码，验证bootstrap已经正常工作。只要显示一个h1的文字就好了。因为bootstrap的字体跟默认字体明显不同。同时F12打开console，看看有没有错误。
5、用layoutit来在线绘制界面。画好后，点击下载，把代码放到你的html文件的body标签里。
发现一个问题，就是layoutit绘制得到的东西。
在我的下载最新的bootstrap5里，有些东西没有了。所以显示不支持。
例如，btn-default这个class就不存在了。
所以，我还是要选择跟layoutit可以兼容的bootstrap版本。
layoutit用的是bootstrap3.0.1的。
从这里看，每一个大版本都是一个分支。
https://getbootstrap.com/docs/versions/
我下载就取用v3.x的。最新的是v3.4的。
替换后显示就正常了。
```

然后就需要把登陆功能完成。



```
<!DOCTYPE html>
<html>
  <head>
    <title><%= title %></title>
    <link rel="stylesheet" href="/stylesheets/bootstrap.min.css">
    <link rel='stylesheet' href='/stylesheets/style.css' />
    <script src="/public/javascripts/jquery-3.5.1.min.js"></script>
    <script src="/public/javascripts/bootstrap.min.js"></script>
  </head>
  <body>
    <h1><%= title %></h1>
    <p>Welcome to <%= title %></p>
  </body>
</html>
```

判断当前用户是否在登陆状态。

最简单的方法是怎样的？



js时间格式化

还是就用moment就好了。

```
moment().format('YYYY-MM-DD')
```

日志的保存，想了一下，用sqlite好一点。



有个问题，就是res.render渲染后，url并没有变。

redirect又不能传递一下模板参数。

切换到某个tab，执行操作。

给ul添加一个id，为myTabs。这样就可以在点击的时候，进行一些操作。

```
$('#myTabs a[href="#record"]').on('shown.bs.tab', function (e) {
                //
            });
```

那就要靠jquery来动态给表格添加内容。

# 模拟微云

https://github.com/FantasyNJ/wy

这个后端其实没有做什么。

主要是前端，这个可以看到jquery可以实现的功能。

