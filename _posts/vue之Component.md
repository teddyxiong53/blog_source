---
title: vue之Component
date: 2020-09-03 17:38:57
tags:
	- vue

---

1

这里有两种组件的注册类型：**全局注册**和**局部注册**。

这样就是全局注册。

```
Vue.component('my-component-name', {
  // ... options ...
})
```

早些时候，我们提到了创建一个博文组件的事情。

问题是如果你不能向这个组件传递某一篇博文的标题或内容之类的我们想展示的数据的话，

它是没有办法使用的。

这也正是 prop 的由来。就是为了在组件之间传递数据而存在的。

例如，我们这样注册一个博客文章组件。

```
Vue.component("blog-post", {
	props: ['title'],
	template: <h1> {{title}}</h1>
})
```

一个组件默认可以拥有任意数量的 prop，任何值都可以传递给任何 prop。

在上述模板中，你会发现我们能够在组件实例中访问这个值，就像访问 `data` 中的值一样。

然后我们这样用这个props。

```
<blog-post title="My journey with Vue"></blog-post>
```

在一个博客程序里，可能是这样：

```
new Vue ({
	el: "#blog-post-demo",
	data: {
		posts: [
			{id:1, title: "first"},
			{id:2, title: "second"},
			{id:3, title: "third"},
		]
	}
})
```

然后为每一篇博客对应一个组件。

```
<blog-post
	v-for="post in posts"
	v-bind:key="post.id"
	v-bind:title="post.title"
	>
	
</blog-post>
```

如上面所示，你可以用v-bind来动态传递props。

当你实际写以博客程序的时候，你不会只有一个标题，至少还有正文部分。

```
<h1>{{title}}</h1>
<div v-html="content"></div>
```

不过这样写是会报错的。

因为每个组件必须只有一个根元素。

解决的办法也很简单，就是在外面再包一个div就好了。

```
<div class="blog-post">
	<h1>{{title}}</h1>
	<div v-html="content"></div>
</div>
```

随着我们程序的完善，我们就加入越来越多的东西。

例如加入时间、评论。

这个时候，我们的程序就变成了这样。

```
<blog-post
	v-for="post in posts"
	v-bind:key="post.id"
	v-bind:title="post.title"
	v-bind:content="post.content"
	v-bind:publishedAt="post.publishedAt"
	v-bind:comments="post.comments"
	>
	
</blog-post>
```

看起来比较繁杂。

需要改进一下。

让props，是放一个post对象。

```
<blog-post
  v-for="post in posts"
  v-bind:key="post.id"
  v-bind:post="post"
></blog-post>
```

```
Vue.component('blog-post', {
  props: ['post'],
```

当我们在开发blog-post组件的时候，它的一些功能可能需要跟父级组件进行通信。

例如，加入一个放大字体的按钮。我们在一篇文章里点击了放大字体的按钮，那么这个设置就对所有的文章都起作用。

怎么做呢？

首先是在父级组件里加一个postFontSize。

```
new Vue({
  el: '#blog-posts-events-demo',
  data: {
    posts: [/* ... */],
    postFontSize: 1
  }
})
```

在每一篇博文的正文前面都加一个按钮。

修改对应的template就好了。

```
Vue.component('blog-post', {
  props: ['post'],
  template: `
    <div class="blog-post">
      <h3>{{ post.title }}</h3>
      <button>
        Enlarge text
      </button>
      <div v-html="post.content"></div>
    </div>
  `
})
```

当点击这个按钮的时候，需要发送一个消息给父级组件。

Vue提供了一个自定义事件系统来支持这个功能。

父级组件v-on来监听对应的事件。

```
<blog-post
	v-on:enlarge-tex="postFontSize += 0.1"
>
</blog-post>
```

按钮里，通过`$emit`方法来发送事件。

```
<button 
	v-on:click="$emit('enlarge-text')"
	>
Enlarge text
</button>
```

发送事件，还可以带上参数呢。例如字体放大多少。







参考资料

1、官网

https://cn.vuejs.org/v2/guide/components.html