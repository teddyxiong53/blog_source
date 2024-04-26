---
title: vue（1）
date: 2018-12-27 17:14:25
tags:
	- 网页

---



把常见的前端框架都简单过一遍，了解一下基本的使用方法。

web库和web框架的区别

jQuery就是库。核心是dom操作。jQuery只是简化了这个操作。

vue就是框架。你按照框架要求填写代码。

vue是MVVM模式的应用。

在vue里，你关注的核心是数据，不要再去操作dom了。

vue，发音跟view一样。

用来构造用户界面的渐进式框架。

vue只关注视图层。

采用自底向上的增量开发设计。

下面的内容，参考https://cn.vuejs.org/v2/guide/#%E5%A3%B0%E6%98%8E%E5%BC%8F%E6%B8%B2%E6%9F%93来写的。

# 声明式渲染

```
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <script src="https://cdn.staticfile.org/vue/2.4.2/vue.min.js"></script>
</head>
<body>
    <div id="app">
        <p>{{ message }}</p>
    </div>
    <script>
    var app = new Vue({
        el: "#app",
        data: {
            message: 'hello vue'
        }
    })
    </script>
</body>
</html>
```

我们在chrome里，按F12打开控制台，输入：

```
app.message = "hello xhl"
```

然后就可以看到网页直接就变了。

除了文本插值，我们还可以像这样来绑定元素特征。

```
<div id="app">
        <span v-bind:title="message">
            鼠标悬停此处查看此处动态绑定的提示信息。
        </span>
    </div>
    <script>
        var app = new Vue({
            el: "#app",
            data: {
                message: "页面加载于 " + new Date().toDateString()
            }
        })
    </script>
```

这里我们遇到一点新的东西，v-bind，这种叫做指令。

指令是前面带有v-前缀的。用来表示它们是vue提供的特殊属性。



# 条件与循环

控制一个元素是否显示。

```
<div id="app">
        <p v-if="seen">你看到我了</p>
    </div>
    <script>
        var app = new Vue({
            el: "#app",
            data: {
                seen: true
            }
        })
    </script>
```

我们只需要在控制上输入

```
app.seen = false
```

“你看到我了”这行字就会消失。

vue提供了一个强大的过渡效果系统。可以在vue插入、更新、移除元素时，自动应用过渡效果。

v-for指令用来绑定数组的数据来渲染一个项目列表。

```
<div id="app">
        <ol>
            <li v-for="todo in todos">
                {{todo.text}}
            </li>
        </ol>
    </div>
    <script>
        var app = new Vue({
            el: "#app",
            data: {
                todos: [
                    {text: "xx"},
                    {text: "yy"},
                    {text: "zz"}
                ]
            }
        })
    </script>
```

然后我们在控制台：

```
app.todos.push({text:"aa"})
```

可以看到列表自动增加了。



# 处理用户输入

用v-on增加监听器。

```
<div id="app">
        <p>{{message}}</p>
        <button v-on:click="reverseMessage">逆转消息</button>
    </div>
    <script>
        var app = new Vue({
            el: "#app",
            data : {
                message: "hello vue"
            },
            methods: {
                reverseMessage: function() {
                    this.message = this.message.split('').reverse().join('')
                }
            },
        })
    </script>
```

这个过程中，我们都没有去操作dom的。

vue还提供了v-model指令，它可以实现表单输入和应用状态之间的双向绑定。

```
<div id="app">
        <p>{{message}}</p>
        <input v-model="message">
    </div>
    <script>
        var app = new Vue({
            el: "#app",
            data : {
                message: "hello vue"
            }
            
        })
    </script>
```

然后我们在输入框里进行输入，外面的显示也会变化。

# 组件化应用构建

组件系统是vue的一个重要概念。

是一种抽象，允许我们使用小型、独立和通常可以复用的组件构建大型应用。

在vue里，一个组件，本质上是一个拥有预定义选项的vue实例。

在vue里注册组件很简单。

```
<div id="app">
        <ol>
            <todo-item
                v-for="item in mylist"
                v-bind:todo="item"
                v-bind:key="item.id"
            >

            </todo-item>
        </ol>
    </div>
    <script>
        Vue.component("todo-item", {
            props: ['todo'],
            template: '<li>{{todo.text}}</li>'
        })
        var app = new Vue({
            el: "#app",
            data : {
                mylist: [
                    {id:0, text: 'xx'},
                    {id:1, text: 'yy'},
                    {id:2, text: 'zz'}
                ]
            }
            
        })
    </script>
```



# vue实例

## 创建一个vue实例

每个vue应用都是通过用Vue函数创建一个新的Vue实例开始的。

```
var vm = new Vue({
  //选项
})
```

虽然没有完全遵守mvvm模型，但是vue的设计也受到了它的启发。

因此在文档里经常用vm（ViewModel）这个变量名来表示Vue实例。

一个Vue应用由根Vue实例和组件树来构成。

例如，一个todo应用的组件树可以是这样：

```
根实例
	TodoList
		TodoItem
			DeleteTodoButton
			EditTodoButton
		TodoListFooter
			ClearTodoButton
			TodoListStatistics
```

## 数据与方法

当一个vue实例被创建时，它向vue的响应式系统里加入了data对象里的所有属性。

当这些属性值发生变化时，视图会发生响应。就是匹配为新的值。

## 实例生命周期钩子

每个vue实例在被创建的时候，都要经过一系列的初始化过程。

例如：

需要设置数据监听。

编译模板。

将实例挂接到dom

在数据变化时更新dom。

在这些节点上，可以挂接钩子函数，让用户实现自定义。

```
var app = new Vue({
            el: "#app",
            data : {
                a:1
            },
            created() {
                console.log("a is :" + this.a)
            },
        })
```

还有其他函数：

mounted

updated

destroyed。



# 模板语法

vue使用了基于html的模板语法。

允许开发者声明式地把dom绑定到底层vue实例的数据。

所有vue的模板都是合法的html。

如果你对虚拟dom很熟悉，而且喜欢使用JavaScript的原始力量，你可以直接写render函数。

## 插值

```
文本
html
```

文本的很简单，就是双层大括号。

html的需要使用v-html指令。

```

```

# 计算属性和监听器

模板里的表达式使用非常便利，但是设计的初衷是进行简单的运算的。

在模板里放入太多的逻辑，会让模板过重，而且难以维护。

所以对于任何复杂逻辑，都应该使用计算属性。

```
<div id="app">
        <p>{{message}}</p>
        <p>reverse: {{reversedMessage}}</p>
    </div>
    <script>
        Vue.component("todo-item", {
            props: ['todo'],
            template: '<li>{{todo.text}}</li>'
        })
        var app = new Vue({
            el: "#app",
            data : {
                message: "hello"
            },
            computed: {//这里就是计算属性。
                reversedMessage: function() {
                    return this.message.split('').reverse().join('')
                }
            },
        })
    </script>
```

计算属性，也可以用methods属性里的函数调用来做。

区别是：methods的方式，不会有缓存。

监听属性是watch。

```
<div id="app">
        <p>{{fullName}}</p>
    </div>
    <script>
        Vue.component("todo-item", {
            props: ['todo'],
            template: '<li>{{todo.text}}</li>'
        })
        var app = new Vue({
            el: "#app",
            data : {
                firstName: "foo",
                lastName: "bar",
                fullName: "foo bar"
            },
            watch: {
                firstName: function(val) {
                    this.fullName = val + " " + this.lastName;
                },
                lastName: function(val) {
                    return this.firstName + " " + val;
                }
            },
        })
    </script>
```

computed比watch要简洁很多。

## 计算属性的setter

计算属性默认只有getter。

我们可以自己实现setter。

```
var app = new Vue({
            el: "#app",
            data : {
                firstName: "foo",
                lastName: "bar",
                fullName: "foo bar"
            },
            computed: {
                fullName: {
                    get: function() {
                        return this.firstName + " " + this.lastName;
                    },
                    set: function(newValue) {
                        var names = newValue.split(' ')
                        this.firstName = names[0]
                        this.lastName = names[names.lengh - 1]
                    }
                }
            },
        })
```



虽然计算属性在大多数情况下更加合适，但是有时候还是需要自定义侦听器。

这就是为什么vue通watch选项提供了一个更加通用的方法。来响应数据的变化。

当需要在数据变化时，执行异步或者开销比较大的操作时，这种方式是最有用的。



```
v-text：改变dom对象的text内容。
v-html：改变dom对象的innerHTML。
v-bind
	简写就是冒号。
	<a v-bind:href="xxx"></a>
	<a :href="xxx"></a>
v-on
	v-on:click="say" or v-on:click="say('参数', $event)"
	简写：@click="say"
v-model
	实现form元素的双向数据绑定。
	说明：监听用户的输入事件以更新数据
v-for
	推荐：使用 v-for 的时候提供 key 属性，以获得性能提升。
	使用 key，VUE会基于 key 的变化重新排列元素顺序，并且会移除 key 不存在的元素。
	
提升性能：v-pre
提升性能：v-once
```



# 组件通信

有这种3种：

父组件到子组件：通过子子组件的props属性（一个数组）来传递。

子组件到父组件：父组件给子组件传递一个函数，子组件调用这个函数。

组件A到组件B，A和B没有父子关系：这个就创建一个空的vue实例，用来做通信。



# SPA

单页应用。

只有第一次会加载页面。后面的操作，都是js局部更新数据。

带来的好处：请求的数据少了。减轻了服务器的负担。

给用户本地应用类似的体验。

实现的技术：

1、ajax。

2、锚点的使用。

3、hashchange事件。



SPA往往是功能复杂的应用，为了有效管理所有视图内容，前端路由 应运而生

简单来说，路由就是一套映射规则（一对一的对应规则），由开发人员制定规则。
当URL中的哈希值（# hash）发生改变后，路由会根据制定好的规则，展示对应的视图内容



# props

组件接受的选项之一 props 是 Vue 中非常重要的一个选项。父子组件的关系可以总结为：

props down, events up

父组件通过 props 向下传递数据给子组件；子组件通过 events 给父组件发送消息。

## 什么是prop

prop就是出现在标签里的东西。

```
<mycomp prop1="xx"></mycomp>
```

"xx"，引号里面是js表达式。

一个实际一点的例子

```
<blog-post v-bind:is-published="post.isPublished">
</blog-post>
```

prop只能从父组件传递给子组件。

这样可以防止子组件意外改变父组件的内容。

父组件更新prop后，子组件里会自动刷新。



## props和data区别

Vue提供了两种不同的存储变量：`props`和`data`。

这些方法一开始可能会让人感到困惑，因为它们做的事情很相似，而且也不清楚什何时使用`props`，何时使用`data`。

那么`props`和`data`有什么区别呢？

`data`是每个组件的私有内存，可以在其中存储需要的任何变量。`props`是将数据从父组件传递到子组件的方式。

数据从根组件(位于最顶端的组件)沿着树向下流动。就像基因是如何代代相传的一样，父组件也会将自己的`props`传给了他们的孩子。

然而，当我们从组件内部访问`props`时，我们并不拥有它们，所以我们不能更改它们(就像你不能改变你父母给你的基因一样)。

但是有些情况我们需要改变变量，所以 `data` 就派上用场了。



# router-link

在vue1.0版本的超链接标签还是原来的`a`标签，链接地址由`v-link`属性控制

而vue2.0版本里超链接标签由`a`标签被替换成了`router-link`标签，但最终在页面还是会被渲染成a标签的

至于为什么要把a换成router-link原因还是有的，

比如我们之前一直惯用的nav导航里面结构是（ul>li>a），

router-link可以渲染为任何元素，

这里可以直接渲染成li标签，同样能实现跳转效果，节省了a标签的使用，

还有一个原因可能是因为a标签正常是链接的跳转的作用，

点击a时可能会重载页面，使用router-link，此标签会被vue所监听，跳转链接时就不会刷新页面了。

# provide和inject

provider/inject：简单的来说就是在父组件中通过provider来提供变量，然后在子组件中通过inject来注入变量

在vue的组件树里，任何一个组件，都可以通过`this.$root`来访问根节点。

也可以通过`this.$parent`来访问自己的父节点。

这是一种不太推荐的方式，用来在组件之间进行通信。（正常通信是用props来做）

因为可能在多层嵌套后，出现这样的代码：

```
this.$parent.$parent.$parent.xx
```

这样代码无法维护。

为了解决这种问题，vue提供了provide和inject这2个选项，用来实现依赖注入。

provide是一个函数，写在父组件里，用来给子组件提供数据或者方法。

```
provide: function() {
	return {
		getData: this.getData
	}
}
```

在任意的后代组件里，可以使用inject选项来指定接收。

```
inject: ['getData']
```

在uniapp的uni-list和uni-list-item里，就使用了这个。

父组件uni-list，把自己暴露给子组件。

![image-20210112173801752](../images/playopenwrt_pic/image-20210112173801752.png)

子组件，接收

![image-20210112173833624](../images/playopenwrt_pic/image-20210112173833624.png)

https://www.cnblogs.com/zhangmingyan/articles/12669987.html

官网介绍provide

https://cn.vuejs.org/v2/guide/components-edge-cases.html

# ref

ref是给你提供一个从js代码里操作一个dom控件的把手。



# slot

是在需要向组件传递内容的时候，在组件里放一个slot。这样传递进来的内容，就会插入到slot的位置上。

这篇文章写得非常好。值得学习。

https://blog.csdn.net/qq_41809113/article/details/121640035

# 大小写

组件名和prop名字，会有自动的大小写转换。

事件名不会有这种转换。推荐使用连字符的方式，因为事件名不会作为js变量名。



# .sync修饰符

虽然不推荐，但是有时候还是有对一个prop进行“双向绑定”。

真正的双向绑定会带来维护问题。

所以这里用触发事件的方式来替代真正的双向绑定。

例如，更新标题。

在子组件里，

```
this.$emit('update:title', 'new title')
```

在父组件里

```
<text-document
	v-bind:title="doc.title"
	v-on:update:title="doc.title = $event"
>
</text-document>
```

这样看起来比较啰嗦，提供一种简写方式，就是sync修饰符。

```
<text-document
	v-bind.title.sync="doc.title"
>
</text-document>
```

# data-v-xxx

在Vue开发中，会遇到html被浏览器解析后，在标签中出现’data-v-xxxxx’标记，如下：

```
<div data-v-fcba8876 class="xxx"> aaa</div>
```

​    这是在标记vue文件中css时使用scoped标记产生的，因为要保证各文件中的css不相互影响，给每个component都做了唯一的标记，所以每引入一个component就会出现一个新的'data-v-xxx'标记



由于样式中使用了scoped，所以编译后标签对中生成data-v-xxx属性。



https://blog.csdn.net/fengjingyu168/article/details/79769608



# vue2和vue3的主要区别

Vue 3 相对于 Vue 2 来说有一些重要的变化和改进。以下是一些主要区别：

1. **性能优化：** Vue 3 在性能方面有显著的改进。其中包括虚拟 DOM 的重写，提高了渲染速度，减少了内存使用。Vue 3 还引入了更好的 Tree-Shaking 支持，以及更快的初始化速度。

2. **Composition API：** Vue 3 引入了 Composition API，这是一个可选的新的组织组件逻辑的方式。相比于 Vue 2 中的 Options API，Composition API 更灵活，更易于组织和重用代码，尤其是在编写复杂组件或者逻辑复用时。

3. **Typescript 支持：** Vue 3 在设计时考虑了更好的 TypeScript 支持。Vue 3 的源码是用 TypeScript 编写的，因此对 TypeScript 的支持更加完善。

4. **更好的 TypeScript 集成：** Vue 3 改进了 TypeScript 的类型定义，使得开发者在使用 TypeScript 时拥有更好的开发体验。

5. **更小的体积：** Vue 3 在代码结构和模块化方面进行了改进，使得它的打包体积相对更小。

6. **Composition API：** Vue 3 中引入了 Composition API，可以更好地组织和重用组件逻辑，特别是在编写复杂组件时更为实用。

7. **Teleport 组件：** Vue 3 引入了 Teleport 组件，可以将子组件移动到 DOM 中的任何位置，而不会打破组件之间的关系。

8. **Fragments 支持：** Vue 3 支持 Fragments，允许组件返回多个根节点，而不再需要一个根元素包裹。

9. **Suspense 和异步组件改进：** Vue 3 中引入了 Suspense 组件，可以更方便地处理异步组件的加载状态，使得异步组件的使用更加简单和直观。

总的来说，Vue 3 在性能、开发体验和功能方面都有很大的改进，尤其是引入了 Composition API 这一新的组件编写方式，使得开发者可以更加灵活地编写和组织组件逻辑。

# vue原理

Vue.js 是一款用于构建用户界面的渐进式 JavaScript 框架，其核心原理主要包括数据驱动、组件化和虚拟 DOM。

1. **数据驱动：** ==Vue 的核心思想是数据驱动视图==。它通过建立一个响应式的数据模型来管理应用的状态，当数据发生变化时，视图会自动更新以反映这些变化，而不需要手动操作 DOM。这种数据绑定的实现是通过 Vue 的响应式系统来完成的，==它使用了 Object.defineProperty 或 ES6 的 Proxy 来监听数据的变化，并在数据变化时通知相关的视图更新。==

2. **组件化：** Vue 把用户界面拆分成一个个独立可复用的组件，每个组件都包含了自己的视图、样式和行为逻辑。组件化开发使得代码更易于维护和扩展，同时也提高了开发效率。Vue 的组件化开发还支持父子组件之间的通信，通过 props 和 events 实现了组件之间的数据传递和事件监听。

3. **虚拟 DOM：** ==虚拟 DOM 是 Vue 用来提高性能的重要技术之一==。Vue 在内部维护了一个虚拟 DOM 树，它是一个轻量级的 JavaScript 对象结构，用来描述真实 DOM 树的结构。当数据发生变化时，Vue 首先会生成一个新的虚拟 DOM 树，然后通过 diff 算法比较新旧虚拟 DOM 树的差异，并只更新发生变化的部分到真实 DOM，从而减少了 DOM 操作的次数，提高了性能。

4. **生命周期：** Vue 组件的生命周期钩子函数是一组在组件生命周期不同阶段被调用的函数，包括创建、挂载、更新和销毁等阶段。开发者可以通过这些钩子函数来执行自定义的逻辑，比如在创建前初始化数据、在挂载后发送网络请求、在更新前清理资源等。

总的来说，Vue.js 的原理基于数据驱动、组件化和虚拟 DOM，通过这些核心概念来实现高效的用户界面构建和开发体验。

# 一步步学习

我要学习vue3，请一步步教我怎么学习。首先我需要在本地搭建一个基础环境，vue的代码就引用cdn地址的就好了

## 搭建环境

学习 Vue.js 3 的第一步是搭建一个基础的开发环境，并且了解如何使用 Vue 的基本语法。以下是一些步骤：

### 步骤一：安装 Node.js 和 npm

1. 前往 Node.js 官网（https://nodejs.org/）下载并安装最新版本的 Node.js。
2. 安装完成后，打开命令行工具（如终端或命令提示符），运行以下命令来验证安装是否成功：
   ```
   node -v
   npm -v
   ```
   如果成功安装，会显示 Node.js 和 npm 的版本号。

### 步骤二：创建项目

1. 创建一个新的项目文件夹，例如 `vue3-demo`。
2. 在命令行中进入项目文件夹，并运行以下命令来初始化一个新的 npm 项目：
   ```
   npm init -y
   ```
   这会创建一个默认的 `package.json` 文件。

### 步骤三：安装 Vue CLI

1. Vue CLI 是 Vue.js 的官方脚手架工具，可以帮助你快速搭建 Vue 项目并进行开发。
2. 在命令行中运行以下命令来全局安装 Vue CLI：
   ```
   npm install -g @vue/cli
   ```
   
### 步骤四：创建 Vue 项目

1. 在命令行中运行以下命令来使用 Vue CLI 创建一个新的 Vue 项目：
   ```
   vue create my-vue3-app
   ```
   这里 `my-vue3-app` 是你的项目名称，你也可以使用其他名称。
2. Vue CLI 会提示你选择一些配置选项，如使用默认配置或手动选择特性，你可以根据需要进行选择。
3. 创建完成后，进入项目文件夹：
   ```
   cd my-vue3-app
   ```

### 步骤五：启动开发服务器

1. 在命令行中运行以下命令来启动开发服务器：
   ```
   npm run serve
   ```
2. Vue CLI 会启动一个开发服务器，并在浏览器中打开一个预览页面，你可以在其中进行开发。

### 步骤六：引入 Vue.js 3

1. 在项目中打开 `public/index.html` 文件。
2. 在 `<head>` 标签内添加以下代码来引入 Vue.js 3 的 CDN：
   ```html
   <script src="https://unpkg.com/vue@next"></script>
   ```

### 步骤七：编写 Vue 组件

1. 在 `src` 目录下创建一个新的 `.vue` 文件，例如 `HelloWorld.vue`。
2. 在文件中编写一个简单的 Vue 组件：
   ```vue
   <template>
     <div>
       <h1>{{ greeting }}</h1>
     </div>
   </template>
   
   <script>
   export default {
     data() {
       return {
         greeting: 'Hello, Vue 3!'
       };
     }
   }
   </script>
   ```
   
### 步骤八：在主文件中使用组件

1. 打开 `src/main.js` 文件。
2. 在文件中引入并注册你的组件：
   ```javascript
   import { createApp } from 'vue'
   import App from './App.vue'
   
   createApp(App).mount('#app')
   ```
   
### 步骤九：运行项目

1. 回到命令行，确保开发服务器正在运行。
2. 在浏览器中打开预览页面，你应该能够看到 `Hello, Vue 3!` 的文字。

现在，你已经成功搭建了一个基础的 Vue.js 3 项目，并且编写了一个简单的 Vue 组件。接下来，你可以继续深入学习 Vue.js 3 的其他特性和概念，例如组件化、路由、状态管理等。

## 下一步

下一步是深入学习 Vue.js 3 的核心概念和功能。以下是一些建议的学习路径：

### 1. Vue.js 官方文档

浏览 Vue.js 官方文档是学习 Vue.js 最有效的方式之一。官方文档详细介绍了 Vue.js 的各个方面，从基础概念到进阶特性都有涵盖。你可以按照自己的需求和兴趣，选择相应的章节进行学习。

- [Vue.js 官方文档](https://v3.vuejs.org/guide/introduction.html)

### 2. 组件化开发

学习如何使用 Vue.js 开发可复用、组件化的用户界面是非常重要的。你可以学习如何创建和组合 Vue 组件，以及如何进行组件间的通信、传递数据和事件等。

- 学习 Vue 组件的基本语法和使用方法。
- 了解组件之间的通信方式，如 props、events、$emit 等。
- 掌握 Vue 3 中的 Composition API，它提供了更灵活的组件代码组织方式。

### 3. 路由管理

如果你的应用需要多页面间的导航和路由管理，那么学习 Vue Router 就非常重要。Vue Router 是 Vue.js 的官方路由管理器，可以帮助你在单页面应用中实现路由导航。

- 学习 Vue Router 的基本用法，包括路由配置、路由导航、动态路由等。
- 掌握路由导航守卫的使用，用于控制路由跳转和页面访问权限。
- 了解 Vue Router 在 Vue.js 3 中的新特性和改进。

### 4. 状态管理

在大型应用中，状态管理是必不可少的。学习 Vue.js 的状态管理工具 Vuex 可以帮助你更好地管理应用的状态，使得代码结构更清晰、易于维护。

- 学习 Vuex 的基本概念，包括 state、mutations、actions 和 getters 等。
- 掌握如何在 Vue 组件中使用 Vuex 来管理状态。
- 了解 Vuex 4 在 Vue.js 3 中的新特性和改进。

### 5. 项目实践

最后，通过实际项目实践来巩固所学知识。你可以选择一个小型的项目，例如一个待办事项列表应用，然后尝试使用 Vue.js 3 来实现它。在项目实践中，你将会遇到各种实际的问题和挑战，这有助于你更深入地理解 Vue.js，并提升自己的开发能力。

继续学习和实践，不断积累经验，你将会成为一名熟练的 Vue.js 开发者。祝你学习顺利！

## 下一步

下一步是在 `my-vue3-app` 项目中学习如何使用 Vue Router 进行路由管理。

### 2. 路由管理

1. 首先，确保你已经安装了 Vue Router。如果没有安装，可以使用以下命令安装：

```
npm install vue-router@next
```

2. 创建一个新的文件夹 `views` 在 `src` 目录下，用于存放页面组件。

3. 在 `views` 目录下创建两个新的 Vue 组件，分别命名为 `Home.vue` 和 `About.vue`。这些组件将作为路由对应的页面。

4. 在 `src` 目录下创建一个新的文件夹 `router`，用于存放 Vue Router 相关的代码。

5. 在 `router` 目录下创建一个新的文件 `index.js`，用于配置和创建 Vue Router 实例。

6. 编写 `router/index.js` 文件的代码，配置路由：

```javascript
import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import About from '@/views/About.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
```

7. 在 `src/main.js` 文件中导入并使用 Vue Router：

```javascript
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

createApp(App).use(router).mount('#app');
```

8. 在 `App.vue` 组件中添加 `<router-view>` 标签，用于渲染匹配到的路由组件。

9. 运行项目，并尝试访问 `/` 和 `/about` 路径，查看效果。

现在，你已经学会了在 Vue.js 3 项目中使用 Vue Router 进行路由管理。接下来，你可以继续学习 Vuex 进行状态管理，或者进行更复杂的路由配置和功能开发。

# 参考资料

1、

http://www.runoob.com/vue2/vue-directory-structure.html

2、Vue学习看这篇就够

https://juejin.im/entry/5a54b747518825734216c3df

3、

https://cn.vuejs.org/v2/guide/#%E5%A3%B0%E6%98%8E%E5%BC%8F%E6%B8%B2%E6%9F%93

4、Vue props用法详解

https://www.jianshu.com/p/89bd18e44e73

5、

https://www.html.cn/web/vue-js/17249.html

6、Vue-详解设置路由导航的两种方法：` <router-link :to="..."> 和router.push(...)`

https://www.cnblogs.com/superlizhao/p/8527317.html

7、Vue的router-link标签

https://www.cnblogs.com/mr-wuxiansheng/p/11309507.html