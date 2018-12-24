---
title: javascript学习
date: 2017-02-11 19:18:04
tags:
	- javascript
---
希望把一些在浏览器上的操作自动化，觉得需要学习一下JavaScript。

# 1. helloworld
网页这一块接触不太多。所以也是摸着石头过河。
第一个问题，JavaScript的文件怎么运行？是嵌入在html文档里运行。
所以新建一个test.html文件。写入下面的内容：
```
<html>
<head>
	<script>
		alert("hello,js");
	</script>
</head>

<body>
hello, js.
</body>
</html>

```
把这个文件用浏览器打开，可以看到弹出提示框。所以最简单的JavaScript示例就写出来了。
从上面看基本约束，script标签可以写在head或者body里，写在head里的话，打开页面马上就会执行。
之前的老的写法还需要再script标签里指定为JavaScript，现在不需要了，现在默认就是JavaScript，这个说明JavaScript被广泛接纳了。


# 2. JavaScript一般用来做什么？
比较基础常用的就是在本地验证用户的输入，不用提交到服务器了才进行验证，有利于减轻服务端的负担。


# 3. 复杂一点的例子
JavaScript本质上是一种脚本语言，解释执行的。可以封装函数。
```
<html>
<head>
	<script>
		function ClickMe()
		{
			document.write("ClickMe !!!");
		}
	</script>
</head>

<body>
	<button onclick="ClickMe()" type="button">click me</button>
</body>
</html>

```
# 4. 把JavaScript代码独立成文件
JavaScript代码文件的后缀是.js。
我们就把第三节的例子改一下。新建clickme.js文件。内容如下：
```
function ClickMe()
{
	document.write("ClickMe !!!");
}
```
test.html文件改成这样：
```
<html>
<head>
	<script src="clickme.js">
	</script>
</head>

<body>
	<button onclick="ClickMe()" type="button">click me</button>
</body>
</html>

```

# 5. JavaScript的输出
JavaScript没有输出或者打印函数，那么数据怎么进行呈现呢？
有这么四种方法。
1. 使用window.alert来弹窗。
2. 用document.write来写到html文件了。在文档加载完之后，执行这个函数会导致整个文档被覆盖。
3. 用innerHTML写入到html元素里。
4. 用console.log写入到浏览器控制台。按一下F12就可以看到调试界面。


# 6. 基础语法
1. 字符串可以单引号或者双引号。
2. 用关键字var来定义变量。
3. 注释风格和c语言一样。
4. 使用unicode字符集。
5. 风格是使用驼峰标志。
6. 行尾的分号的可选的。
7. 用function关键字来定义函数。
8. 变量是动态类型，定义了一个变量后，后面可以随意改变它的类型。
9. 有true和false这2个bool值。
10. 数组的操作如下：
```
var books = new Arry();
books[0] = "aaa";
books[1] = "bbb";
```
11. JavaScript的对象的语法。用大括号括起来，逗号分割的键值对。
```
var person = {name:"xxx", age:15};
alert(person.name);
alert(person["name"];//这2种索引方法是等效的。
```
12. undefined和null。
13. 一切都是对象。
14. 返回值也可选的。
15. 变量的生命周期：从定义处开始，局部变量在函数内，全局变量在页面关闭后被删除。
16. `===`。连续3个等于号表示绝对相等，值和类型都一样。
17. 变量可以先使用后声明。实际上内部帮你提到前面去了。所以我们还是按正常的方式来写代码。
# 7. 关于对象
1. 定义及访问对象的函数。注意定义对象里的function的方法。方法名:function()
```
<html>
	<head>
	test
	</head>

	<body>
		<p id="demo"></p>
		<script>
			var person = 
			{
				name: "xxx",
				age: 15,
				nameAndAge:function()
				{
					return this.name + "--" + this.age;
				}
			};
			document.getElementById("demo").innerHTML = person.nameAndAge();

		</script>
	</body>
</html>
```

# 8. 事件
html事件可能是用户行为，也可以是浏览器行为。例如html页面加载完成、input字段发生变化、按钮被点击。
你可以在发生事件时触发js代码。
前面我们有修改button的onclick事件的函数为js函数。

# 9. 字符串
js的字符串可以是原始类型的，也可以用new来创建一个对象。
```
var name = "xxx";
var name2 = new String("yyy");
typeof name;//String
typeof name2;//Object
```
new String这种方式效率低，我们一般不用。

# 10. 类型转换
js里有5种不同的数据类型：string类型、number类型、bool类型、object类型、function类型。
3种对象类型：Object类型、Date类型、Array类型。
用typeof操作符来查看类型。

# 11. 错误处理
跟Java的类似，是try、catch、throw来做。
catch举例：
```
<html>
	<head>
	test
	</head>

	<body>
		<p id="demo"></p>
		<script>
			try {
				allert("xxx");//make a mistake here 
			} catch (err) {
				txt = "err happens \n";
				txt += "msg:" + err.message;
				alert(txt);
			}
		</script>
	</body>
</html>
```
# 12. 调试
浏览器都内置了调试工具。可以设置断点。
在需要停止执行的位置加`debugger;`就会让js代码运行停在这个位置。
另外就是在console上看打印了。


# 13. 应用实例

下面演示一个弹窗的例子。
新建一个pop.html文件，里面内容如下：
```
<html>

<head>
<style>
	.modal {
		display: none;
		position: fixed;
		z-index: 1;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		overflow: auto;
		background-color: rgb(0,0,0);
		background-color: rgba(0,0,0,0.4);
	}
	.modal-content {
		background-color: #fefefe;
		margin: 15% auto;
		padding: 20px;
		boarder: 1px solid #888;
		width: 80%;
	}
	.close {
		color: #aaa;
		float: right;
		font-size: 28px;
		font-weight: bold;
	}
	.close:hover,
	.close:focus {
		color: black;
		text-decoration: none;
		cursor: pointer;
	}
	
</style>
</head>

<body>


<button id="myBtn">open dlg</button>

<div id="myModal" class="modal">
	<div class="modal-content">
		<span class="close">X</span>
		<p>dlg content</p>
	</div>
</div>


<script type="text/javascript">
	var modal = document.getElementById("myModal");
	var btn = document.getElementById("myBtn");
	var span = document.getElementsByClassName("close")[0];
	//alert(btn);
	
	btn.onclick = function() {
		modal.style.display = "block";
	}
	span.onclick = function() {
		modal.style.display = "none";
	}
	
	window.onclick = function(event) {
		if(event.target == modal) {
			modal.style.display = "none";
		}
	}
</script>

</body>

</html>
```



# 参考资料

1、菜鸟教程

2、w3cschool

https://www.w3cschool.cn/javascript/