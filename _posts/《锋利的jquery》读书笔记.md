---
title: 《锋利的jquery》读书笔记
date: 2019-01-23 21:05:05
tags:
	- jquery

---



#第1章

jquery的优势

```
1、小。只有18K（压缩后）。
2、强大的选择器。运行开发者使用从css1到css3的各种选择器。
3、出色的dom操作封装。
4、可靠的事件处理机制。
	在预留退路、循序渐进、非侵入式编码思想方面做得很好。
5、完善的ajax。
	把所有的ajax操作封装到一个工具函数$.ajax()里。
6、不污染顶级变量。
	jquery只建立一个名为jquery的对象，所有的函数方法都在这个对象下。
	它的别名$也可以随时交出控制权。
7、出色的浏览器兼容性。
8、链式操作方式。
	不需要重复获取对象。
9、丰富的插件支持。
10、完善的文档。
11、开源。
```



统一jquery代码风格

```
1、链式操作风格。
2、jquery获取到的对象，变量前面用$做前缀（非必须，方便识别）。
```



jquery转dom对象

```
使用场景：
1、对jquery对象提供的方法不熟悉，
2、jquery没有提供对应的封装方法时。

转换方法：
方法1
因为jquery对象是一个数组对象。可以通过数组索引来得到。
var $cr = $("#xx");//jquery对象。
var cr = $cr[0];//dom对象
方法2
用jquery的get(index)也可以拿到。
var $cr = $("#xx");
var cr = $cr.get(0);
```



dom转jquery对象

```
很简单，只需要把dom对象用$()包起来就好了。
```



解决jquery跟其他库的冲突

```
在其他库和jquery库都被加载完成时，可以选择调用jQuery.onConflict函数来把变量$的控制器转移给其他库。
```

例如我们在一个文件里同时使用prototype.js和jquery.js。

```
<head>
	<script src="./prototype.js"></script>
	<script src="./jquery.js"></script>
</head>
<body>
	<script>
		jQuery.noConflict();
		jQuery(function() {
          //..
		})
		$("xxx").style.display = "none";//$也是Prototype的别名。
	</script>
</body>
```

# 第2章 选择器

jQuery选择器完全继承了css的风格。

```
<script>
        function demo() {
            alert("hello");
        }
</script>
 <p onclick="demo();">click me</p>
```

这种风格不太好，把js和html元素混在一起了。

改成这样好点。加上class属性。

```
<script>
        $(".demo").click(function() {
            alert("hello");
        })
    </script>
    <p class="demo">click me</p>
```

我们先看看用原生js来进行的一些操作，再看看用jquery来实现的，这样对比，我们才能看出jquery的好处来。

```
给网页所有的p元素加上onclick事件。
```

```
    <p>xx</p>
    <p>yy</p>
    <script>
        var items = document.getElementsByTagName("p");
        var count = 0;
        for(var i=0; i<items.length; i++) {
            items[i].onclick = function() {
                console.log("clicked ", count++);
            }
        }
    </script>
```

```
给表格进行隔行变色
```

```
<table id="tb">
        <tbody>
                <tr><td>第一行</td><td>第一行</td></tr>
                <tr><td>第二行</td><td>第二行</td></tr>
                <tr><td>第三行</td><td>第三行</td></tr>
        </tbody> 
    </table>
    <script>
        var item = document.getElementById("tb");
        var tbody = item.getElementsByTagName("tbody")[0];
        var trs = tbody.getElementsByTagName("tr");
        for(var i=0;i <trs.length; i++) {
            if(i%2 == 0) {
                trs[i].style.backgroundColor = "red";
            }
        }
    </script>
```

```
对多选框进行操作，输出选中的多选框的个数
```

```
<input type="checkbox" name="check" id="cb1" value="1" checked>
    <input type="checkbox" name="check" id="cb2" value="2" checked>
    <input type="checkbox" name="check" id="cb3" value="3" checked>
    <input type="button" value="你选中的个数" id="btn">

    <script>
        var btn = document.getElementById("btn");
        btn.onclick = function() {
            var arrays = new Array();
            var items = document.getElementsByName("check");
            for(var i=0; i<items.length; i++) {
                if(items[i].checked) {
                    arrays.push(items[i].value);
                }
            }
            alert("选中的个数是:" + arrays.length);
        }
    </script>
```

上面这些例子都很简单，但是不断使用getElementById等冗长难记的名字，而且要写很多次。很麻烦。

jquery的选择器分类：

```\
1、基本选择器。
2、层次选择器。
3、过滤选择器。
	基本过滤
	内容过滤
	可见性过滤
	属性过滤
	子元素过滤
	表单对象属性过滤
4、表单选择器。

```

为了方便演示这些东西，我们先写一个基本界面。

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="./jquery-1.3.1.js"></script>
    <style>
        div, span, p {
            width: 140px;
            height: 140px;
            margin: 5px;
            background: #aaa;
            border: #000 1px solid;
            float: left;
            font-size: 17px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
        }
        div.mini {
            width: 55px;
            height: 55px;
            background-color: #aaa;
            font-size: 12px;
        }
        div.hiden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="one" id="one">
        id为one，class为one的div
        <div class="mini">class为mini</div>
    </div>
    <div class="one" id="two" title="test">
        id为two，class为one，title为test的div
        <div class="mini" title="other">class为mini，title为other</div>
        <div class="mini" title="test">class为mini，title为test</div>
    </div>
    <div class="one">
        <div class="mini">class为mini</div>
        <div class="mini">class为mini</div>
        <div class="mini">class为mini</div>
        <div class="mini"></div>
    </div>
    <div class="one">
        <div class="mini">class为mini</div>
        <div class="mini">class为mini</div>
        <div class="mini">class为mini</div>
        <div class="mini" title="tesst">class为mini，title为tesst</div>
    </div>
    <div style="display: none;" class="none">
        style的display为none的div
    </div>
    <div class="hiden">class为hide的div</div>
    <div>
        包含input的type为hiddendiv
        <input type="hidden" size="8">
    </div>
    <span id="mover">正在执行动画的span</span>
    <script>
        //1.基本选择器演示
        //$("#one").css("background", "yellow");
        //$(".mini").css("background","green");
        //$("div").css("background", "red");
        //$("*").css("background", "blue");
        //$("span, #two").css("background", "green");

        //2.层次选择器演示
        //把body里的div选中。
        //$("body div").css("bakground", "red");
        //把body第一个子层里的div选中
        //$("body > div").css("background", "red");
        //把class为one的下一个div选中
        //$(".one + div").css("background", "red");
        //选中id为two的所有元素后面的div
        //$("#two ~ div").css("background", "red");

        //3.过滤选择器
        //3.1 基本过滤器
        //选择第一个div元素
        //$("div:first").css("background", "red");
        //选择最后一个div元素
        //$("div:last").css("background", "red");
        //去除符合条件的
        //$("div:not(#one)").css("background","red");
        //选中索引是偶数的
        //$("div:even").css("background", "red");
        //选中索引是奇数的。
        //$("div:odd").css("background","red");
        //选择索引值等于某个值的，大于是gt，小于是lt
        //$("div:eq(1)").css("background","red");
        //选择所有的标题元素
        //$(":header").css("background", "red");
        //选择所有的只在执行动画的元素
        //$("div:animated").css("background", "red");

        //3.2 内容过滤器
        //选择含有指定文本的
        //$("div:contains('xx')").css("background","red");
        //选择不含有子元素的div
        //$("div:empty").css("background", "red");
        //选择含有p元素的div
        //$("div.has(p)").css("background","red");
        //选择有子元素的（就是非空的）div
        //$("div:parent").css("background","red");

        //3.3 可见性过滤
        //选择所有不可见的div元素
        //$("div:hidden").show(3000);
        //选择所有可见的div
        //$("div:visiable").css("background", "red");
        
        //3.4 属性过滤
        //选择有属性xx的元素
        //$("div[title]").css("background", "red");
        //选择有属性title且值为test的。
        //!=
        //^= 以xx开头。
        //$=
        //*= 包含
        //$("div[title=test]").css("background", "red");
        //多个属性过滤器串联
        //$("div[id][title=test]").css("background", "red");

        //4. 表单选择器
        //选择所有的input，包括了input、textarea、select、button。
        
    </script>
</body>
</html>
```

接下来，我们用jquery来改写上面的3个简单例子。

第一个，给所有的p元素加上onclick事件。

```
<p>xx</p>
    <p>xx</p>
    <p>xx</p>
    <script>
        $("p").click(function() {
            console.log("xx");
        })
    </script>
```

第二个，表格隔行显示颜色。

```
<table id="tb">
        <tbody>
            <tr><td>11</td></tr>
            <tr><td>22</td></tr>
            <tr><td>33</td></tr>
        </tbody>
    </table>
    <script>
        $("#tb tbody tr:even").css('background', "red");
    </script>
```

第三个，统计勾选的CheckBox的个数。

```
$("#btn").click(function() {
  var length = $("input[name="check"]:checked").length;
  alert("选择的个数是:" + length);
});
```

## 案例研究 

设计页面：

```
1、从第7条开始，隐藏后面的品牌。
2、当用户点击“显示全部品牌”按钮，执行这些操作：
	1）显示隐藏的品牌。
	2）“显示全部品牌”按钮的文本改成“精简显示品牌”。
	3）高亮显示推荐品牌。
3、当用户点击“精简显示品牌”时，执行：
	1）从第5条开始隐藏后面的品牌。
	2）“精简显示品牌”改成“显示全部品牌”。
	3）去掉高亮显示的推荐品牌。
```



# 第3章 jquery的dom操作

dom操作分为3种：

```
dom core
	document.getElementById("xx");
html dom
	document.forms
css dom
	xx.style.color = "red"
```

jquery的dom操作：

```
1、查找节点
	查找元素节点
	查找属性节点
2、创建节点
	创建元素节点
	创建文本节点
	创建属性节点
3、插入节点
4、删除节点
5、复制节点
6、替换节点
7、包裹节点
8、属性操作
9、样式操作
10、设置和获取html、文本和值
11、遍历节点

```



# 第4章 jquery里的事件和动画

```
$(document).ready(function() {
  
})
```

等价于

```
$(function() {
  
})
```

等价于

```
$().ready() {
  
}
```



# 第5章 jquery对表单、表格的操作



# 第6章 jquery和ajax应用



# 第7章 插件的使用和写法

插件也叫扩展，是一种遵循一定规范的api写出来的程序。

jquery的易扩展性，吸引了全球的开发者来给它写插件。

插件可以从这个地方下载：http://plugins.jquery.com

不过现在看官网上的写法，是推荐用nodejs的方式来进行下载安装了。

## validation

最经常使用js的地方就是表单的验证。

jquery为这种场景，有一个插件：Validation。

特点如下：

```
1、内置验证规则。
2、自定义验证规则。
3、简单强大的验证信息提示。
4、实时验证。
```



##Form插件



# 第8章 用jquery打造个性网站

是一个购物网站。

我提交在这里：https://github.com/teddyxiong53/front_end/tree/master/jane_shop

目录结构：

```
detail.html  images/  index.html  scripts/  styles/
```

index.html结构：

1、头部。放log。

2、导航栏。

3、内容。

对应3个div。

```
<body>
    <div id="header"></div>
    <div id="navigation"></div>
    <div id="content"></div>
</body>
```



然后是写css。

```
base.css 
header.css
nav.css
```

然后新建一个main.css。

```
@import url("base.css");
@import url("header.css");
@import url("nav.css");
```

在index.html里加上一行：

```
<link rel="stylesheet" href="./styles/main.css">
```

然后开始写base.css。

然后把网站的header部分写出来了。

然后就是写导航部分。

都是靠css来实现悬停展开列表的效果的。

下面看content部分的。

这部分分为左边和右边两部分。

新增index.css文件。

左边有2个模块，一个是最新动态，一个是产品分类。

完成了。

右侧有分为上下2个部分：滚动广告、新品上市。

现在index.html就写完了。

效果出来了。

现在需要设计detail.html的。

我们先跳过。

接下来是看脚本部分的。

在开始编写代码之前，我们需要先明确，需要实现哪些功能。

```
1、网页换肤。
2、导航效果。
3、左侧模块展开和关闭。
4、左边最新动态的滚动显示。
5、
```

## 换肤

新建文件changeSkin.js。

需要依赖jquery.cookie.js插件。是用来保存当前皮肤的。

这个比较简单，就是修改颜色。

替换css文件的做法。

## 导航





# css文件分析

我看css文件里，有不少的不理解的地方，一个个啃下来。

```
word-wrap: break-word; 一般是对于连字符的地方，才把一个单词断开写到下一行。这个设置后，就可以随意。
word-break: break-all; 这些的对亚洲文字和欧美文字的不同情况处理的。
```

```
background
background-color区别
background除了可以设置颜色，还可以设置图片。所以background包含了background-color。
no-repeat就是针对尺寸不过的实时，是否多张图片。
```

```
font: 12px/1.6em;
这种写法是什么意思？
1.6em表示行高是字体的1.6倍。
```

```
text-decoration
就是上中下这几种划线装饰。
```

```
border的属性
3个，
宽度、风格（实线虚线）、颜色。
```

```
font-weight: 700;
等价于bold。加粗。
```

