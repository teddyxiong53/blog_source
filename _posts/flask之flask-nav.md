---
title: flask之flask-nav
date: 2022-11-06 11:59:32
tags:
	- flask

---

--

这个是一个给flask-bootstrap用python代码生成一个navbar的项目。

flask-bootstrap和flask-nav的作者就是同一个人。代码都不多。

很小，但是很有用。使用中我碰到几个问题。

所以需要深入学习一下这个。

在flask_nav.elements里的类，不应该有任何代码用来处理html。

html应该完全交给Renderer类。

实现了一个visitor模式。

当`flask_env.elements.NavigationItem.render()`方法被调用的时候，它只是查找对应的render，并且调用renderer的visit方法。

返回的结果是markupsafe的string。

# custom一个renderer

下面我们看一个例子。

创建一个renderer，它的作用是：

只使用div标签。

flask-nav使用dominate这个库来创建html output。

```
class JustDivRenderer(Renderer):
    def visit_Navbar(self, node):
        sub = []
        for item in node.items:
            sub.append(self.visit(item))
        return tags.div('Navigation:', *sub)

    def visit_View(self, node):
        pass
    def visit_Subgroup(self, node):
        pass
```

然后怎么使用呢？

在app.py里

```
from flask_nav import register_renderer

register_renderer(app, 'just_div', JustDivRenderer)

```

然后在html里：

```
{{nav.top.render(renderer='just_div')}}
```

# 定制element

所有的navigattion结构都是有一些item构成。

因为visitor模式，这些item可以是任意的class。

但是我们最好都 从NavigationItem进行继承。

Navbar类是最外层的容器。

但是不是必须的。

```python
class UserGreeting(Text):
    def __init__(self):
        pass
   	@property
    def text(self):
        return 'hello {}'.format('aa')
```

这个的实际用途，就是在navbar上显示用户的名字。

上面提到的这个，还只是改变navbar上某个元素的内容，并没有对元素的个数进行增加。

如果要对元素进行动态创建和销毁。

只需要把一个callbable的对象传递给register_element。

```python
def top_nav():
	return Navbar(...)
nav.register_element('top_nav', top_nav)
```

这种情况比较常见，所以提供了装饰器的方式进行使用。

```python
@nav.navgation
def top_nav():
    ...
```

每次需要渲染navbar的时候，都会调用top_nav函数。

这样就可以根据用户的登陆状态来呈现不同的菜单项了。



还可以预先实例化非动态的部分，把动态的部分结合起来。



flask-nav是对flask-navigation的改进。



在`__init__.py`里对外暴露的符号有这些：

```
register_renderer
get_renderer
NavbarRenderingError
ElementRegistry

Nav
```

另外还有2个py文件：

elements.py

有这些类，层次关系是这样：

```
NavigationItem
	Link
		View
	RawTag
	Separator
	Subgroup
		Navbar
	Text
```

```
NavigationItem
	继承了object。就一个renderer方法，调用了visit。
	Link
		有2个属性：一个text，表示显示的文字，一个是dest，表示目标连接地址。
		View
		是Link的子类。特点是什么？执行自己内部的链接（就是index这些函数名）
	RawTag
		就是一个普通的html标签。2个属性：一个content，表示文本。一个attribs。表示它的属性。
	Separator
		一条横线，分割线。class内部没有任何东西。就是pass。
	Subgroup
		2个属性，一个title，一个是items。表示内部的其他元素。
		Navbar
			只是pass。没有在Subgroup的基础上新增任何东西。
	Text
		就是一个文本。没有link属性。
```



renderers.py

```
就2个class。
Renderer
	继承了Visitor。通过mro的方式来查找有visit的对象。
SimpleRenderer
```

# 靠右的元素

这里有个讨论：

https://github.com/mbr/flask-bootstrap/issues/126

这个gist是一个实现。

https://gist.github.com/thedod/eafad9458190755ce943e7aa58355934#file-readme-md



flask-bootstrap本身也有nav

```
from flask_bootstrap.nav import BootstrapRenderer, sha1

```



# 参考资料

1、

https://pythonhosted.org/flask-nav