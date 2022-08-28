---
title: bootstrap之layoutit
date: 2020-08-26 22:40:08
tags:
	- bootstrap

---

--

这个系统的代码在这里，内容并不多。功能很符合我的需要。

https://github.com/justjavac/layoutit

这里有个在线的版本。

https://www.bootcss.com/p/layoutit/?#

看代码的最后部分有这个

```
  <script>
    var _hmt = _hmt || [];
    (function () {
      var hm = document.createElement("script");
      hm.src = "//hm.baidu.com/hm.js?5578a27c6c70bf44e7509eda26137f4c";
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(hm, s);
    })();
  </script>
```

hm.js是百度的统计用的。

百度统计服务端，通过接收到这个请求，并从这个图片的网址附带的参数获取相关信息，记录访客访问记录；当页面被用户关闭的时候，同样会触发一次请求hm.gif的过程，但这个过程不是所有浏览器和所有关闭动作都支持。

百度统计是基于cookie的，当请求js脚本的时候，会在你电脑里保存一个永久cookie，该cookie作为你的用户标识。

同时发现，但退出时候参数ep从最开始的0变为了“7289%2C115”，转义后是“7289，115”这是两个毫秒单位，即7.2秒和0.1秒的意思。

同时前两次请求hm.gif的时候lt参数(时间，javascript：(new Date).getTime())是不变的。rnd随机数每次都变。

下面我们就来模拟一次请求，本次使用的python语言。



菜鸟教程了有一个layoutit。而且是版本比较新的。

以后前端相关的东西，首先到菜鸟教程找。



# 其他类似方案

代码：

https://github.com/JakHuang/form-generator

对应的demo：

https://mrhj.gitee.io/form-generator/#/



组件分为3大类：

1、输入型。单行文本、多行文本、密码、编辑器。

2、选择型。下拉、级联、时间日期、评分、上传。

3、布局型。行容器。



阿里的xrender

https://github.com/alibaba/x-render

# 参考资料

1、

https://blog.csdn.net/weixin_39753616/article/details/118320220

2、

https://blog.csdn.net/seo_007/article/details/111582705