---
title: 《chrome扩展及应用开发》读书笔记
date: 2019-01-19 20:41:51
tags:
	- chrome

---



书的地址在这：http://www.ituring.com.cn/book/miniarticle/60134

github在这里：

https://github.com/sneezry/chrome_extensions_and_apps_programming

# my_clock

**这个是演示最简单的应用。**

这个是第一个应用。

新建一个my_clock目录。

新建manifest.json文件。

这个只写了popup.html。没有写选项的文件。

我放在这里了。

https://github.com/teddyxiong53/chrome_plugin/tree/master/study/my_clock

# cannot_touch

**这个是演示操作当前界面元素。**

本来要实现的效果是你鼠标靠近谷歌的搜索按钮的时候，这个按钮的位置就会自动躲开。

可以没有图标，没有html文件，就一个manifest.json和一个js文件，也可以构成一个插件。

https://github.com/teddyxiong53/chrome_plugin/tree/master/study/cannot_touch

我在当前的谷歌网站上，是无法实验通过的。

因为现在的谷歌页面改了。

不管先。

这个的目的是测试操作用户正在浏览的界面。



#what_is_my_ip

**这个是演示跨域。**

简单说，就是访问其他的网站的内容。

跨域的概念：

跨域是指js通过XMLHTTPRequest请求数据时，调用js的页面所在的域和被请求页面的域不一致。

什么是域？协议+主机+端口号。这个就是一个域。

```
http://xx.com:8080
```

这就是一个域。

对于网站来说，浏览器处于安全的考虑，是不允许跨域的。

但是如果不允许插件跨域，那么插件的功能就受到很大的限制。

所以谷歌允许chrome扩展不受限于跨域。

需要在manifest.json里加上声明。

如果我们想要设计一款获取维基百科的数据并显示在其他网页中的扩展，就要在manifest里这样声明。

```
{
  "permissions": [
        "*://*.wikipedia.org/*"
    ]
}
```

我们可以利用如下的代码发起异步请求。

```
function httpRequest(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4) {
            callback(xhl.responseText);
        }
    }
    xhr.send();
}
```

这个我用httpbin的来替代。可以运行成功。

碰到一点问题，调试得到经验：

1、修改后，什么都不用做，直接点击插件就可以看到生效的。

2、在popup弹出的界面上右键，选择审查，可以看到对应的console，可以加log进行调试。

# website_status

**这个是演示常驻后台的用法。**

调试后台的方法。这个需要在chrome://extensions里，点击背景页，才可以看到对应的console。

我采用proxy switch的方法，并不能看出效果来。console里在打印错误。



# weather

**这个是演示带选项页面的用法。**

就是在manifest里加一个“options_page”的选项就好了。

把对应的html写了就行。

当前的写法不行了，因为这个网站现在需要认证了。



# 右键菜单



# 操作你的浏览器



# 参考资料

1、Chrome插件（Extensions）开发攻略

https://www.cnblogs.com/guogangj/p/3235703.html#t9

