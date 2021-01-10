---
title: vue之vuex
date: 2019-01-27 12:00:57
tags:
	- vue

---

--



什么是vuex？和vue是什么关系？

vuex集中管理和存储所有component的状态。

并且保证状态已一种可预测的方式发生变化。

```
new Vue({
  // state
  data () {
    return {
      count: 0
    }
  },
  // view
  template: `
    <div>{{ count }}</div>
  `,
  // actions
  methods: {
    increment () {
      this.count++
    }
  }
})
```

上面这个简单的计数器，包含了3个概念：

state：这个是驱动应用的数据源。

view：以声明的方式将state映射到视图。

actions：用户在view上的操作导致的状态变化。

![image-20210108144642101](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210108144642101.png)

上面显示的是单向数据流。

多个component之间进行状态共享的时候，单向数据流的简洁性很容易就被破坏。

例如：

1、多个视图依赖同一个状态。

2、来自不同视图的action需要修改同一个状态。

对于第一种情况，传参的方法，对于多层嵌套的component会非常繁琐，而且对于兄弟component无能为力。

对于第二种情况，我们经常会采用父子组件直接引用或者通过事件来变更 状态的多份拷贝。

上面的处理方式，都非常脆弱，导致代码难以维护。



因此，我们就很自然的想到，为什么不把component的共享的状态都提取出来。

用一个全局单例的模式进行管理呢？

在这个模式下，组件树就可以看做一个大的视图。

不管在树的哪个位置，任何component都可以set和get状态。



上面就是vuex背后的设计思想。

![vuex](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/vuex.png)



vuex使用了单一状态树。

也就一个对象，就包含了整个app的所有状态数据。

每个app仅包含一个store实例。

这种设计，让我们可以直接定位到任意一个特定的状态时刻。

这种设计跟模块化并不冲突。

```vue
import Vue from 'vue'
import App from './App'
import router from './router'


import Vuex from 'vuex'
Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment: state=>state.count++,
    decrement: state=>state.count--
  }
})
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  computed: {
    count() {//这里读取vuex里的状态。
      return store.state.count
    }
  },
  template: `
  <div id="app">
  <p>{{ count }}</p>
  <p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </p>
</div>
  `
  ,
  methods: {
    increment() {
      store.commit('increment')
    },
    decrement() {
      store.commit('decrement')
    }
  }
})

```



从vuex里读取状态的最简单的方法就是在computed里返回store里的内容。

在根component里注册store，store会被注入到所有的子component里，这样子component就可以直接用store了。是通过this.$store来进行使用。



上面我们是通过计算属性里来获取状态的。

如果状态有多种，这样写，就显得比较繁琐。

mapState这个vuex里的辅助函数，就是用来帮我们生成computed代码的。

我们上面是这样写的：

```
  computed: {
    count() {//这里读取vuex里的状态。
      return store.state.count
    }
  },
```

用mapState改造一下

```
computed: mapState({
    count: state => state.count
  }),
```

其实也没有什么太大的用处。

mapState函数返回的是一个对象。

如果我们要混用mapState跟基本的computed函数。就需要用对象展开符号来把对象进行展开。

```
computed: {
	count1() {
		//这个是基本的computed
	},
	...mapState({
	//把这个对象展开。
	})
}
```

上面这种写法是最实用的。



有的时候，我们需要从store的state里，抽取出一些状态，例如todolist应用里，我们希望获取到已经完成的事项的数目。

```
computed: {
	doneTodosCount() {
		return this.$store.state.todos.filter(todo=>todo.done).length
	}
}
```

如果有多个component都要用到这个属性，我们要么在多个文件里复制粘贴这个函数代码，要么放入到公共函数里，其他文件进行import。

这两种处理方式都不够好。

有没有更好的方式？

vuex针对这种情况，在store里面，我们可以定义getter，就相当于store里面的计算属性。

getter的返回值会根据它的依赖被缓存起来。

只有依赖发生变化的时候，getter才重新计算。

这样写：

```
const store = new Vuex.Store({
  state: {
    todos: [
      {id:1, text:'aa', done:true},
      {id:2, text:'bb', done:false},
    ]
  },
  getters: {
    doneTodos: state=> {
      return state.todos.filter(todo=>todo.done)
    }
  }
})
```

使用的时候，就用`this.$store.getters.doneTodos`







vuex是对复杂应用进行状态管理用的。

**对于简单应用，不需要vuex，vue的事件总线就够用了。**

每一个vuex应用的核心就是store。

store是一个容器，包含了你的应用里的大部分的state。

```
import Vuex from 'vuex';
```

这样得到的Vuex是一个实例。

在应用里，是全局单例的。

**Vuex 通过 `store` 选项，提供了一种机制将状态从根组件“注入”到每一个子组件中**

```
new Vue({
    router,
    store //在根组件里，把store传递进去，这样应用里所有的子组件都可以用。
}).$mount('#app');
```

子组件用的时候，是通过this.$store来用。

vuex管理的就是状态。

Actions、Mutations都是辅助实现对状态的管理的。

可以通过this.$store.state来直接获取状态。

也可以通过vuex提供的mapState辅助函数把state映射到computed里去。



当一个组件需要获取多个状态的时候，

将这些状态都声明为计算属性会有很多重复。

mapState函数可以帮助我们生成计算属性。

具体是这么写的

```
export default {
	computed: mapState({
		//箭头函数可以更加简洁
		count: state=>state.count,
		//传递字符串，等同于state=>state.count
		countAlias: 'count',
		//如果要使用this，那么就使用常规的函数写法
		countPlusLocalState(state) {
			return state.count + this.localCount
		}
	})
}
```

当映射的计算属性的名称跟state的子节点名称相同的时候，可以更简单。

```
computed: mapState({
	'count'//映射this.count为store.state.count
})
```



Getters的本质是对状态进行加工处理。

Getters跟state的关系，就跟vue里面的computed跟data的关系一样。

Getter的返回值会根据它的依赖被缓存起来。只有依赖发生变化的时候才重新计算。





vuex跟普通的全局变量的区别在于：

1、vuex的状态存储是响应式的。当store里的状态发生变化时，相应的组件会自动更新。

2、不能直接修改store里的状态。唯一的方式是commit mutation。这样可以让vuex很方便地追踪变化。

  state是什么?

  定义:state(vuex) ≈ data (vue)

 vuex的state和vue的data有很多相似之处,

都是用于存储一些数据,或者说状态值.

这些值都将被挂载 数据和dom的双向绑定事件,

也就是当你改变值的时候可以触发dom的更新.

虽然state和data有很多相似之处

但state在使用的时候一般被挂载到子组件的computed计算属性上,

这样有利于state的值发生改变的时候及时响应给子组件.

如果你用data去接收`$store.state`,

当然可以接收到值,

但由于这只是一个简单的赋值操作,

因此state中的状态改变的时候不能被vue中的data监听到,

当然你也可以通过watch $store去解决这个问题,那你可以针是一个杠精

综上所述,请用computed去接收state

```

  data () {
    return {
      dataCount: this.$store.state.count //用data接收
    }
  },
  computed:{
    count(){
      return this.$store.state.count //用computed接收
    }

```



用data接收的值不能及时响应更新,用computed就可以.

mapState是state的语法糖,

这么说可能你还想骂我,

因为你根本不了解什么叫做语法糖,

事实上我说的语法糖有自己的定义,

什么是语法糖?

我对语法糖的理解就是,

用之前觉得,我明明已经对一种操作很熟练了,并且这种操作也不存在什么问题,

为什么要用所谓的"更好的操作",用了一段时间后,真香!



不要在vue中为了偷懒使用箭头函数,

会导致很多很难察觉的错误,

**如果你在用到state的同时还需要借助当前vue实例的this,请务必使用常规写法.**



当然computed不会因为引入mapState辅助函数而失去原有的功能

---用于扩展当前vue的data,

只是写法会有一些奇怪,

如果你已经写了一大堆的computed计算属性,

做了一半发现你要引入vuex,

还想使用mapState辅助函数的方便,你可以需要做下列事情.

```
//之前的computed
computed:{
    fn1(){ return ...},
    fn2(){ return ...},
    fn3(){ return ...}
    ........
}
//引入mapState辅助函数之后
 
computed:mapState({
    //先复制粘贴
    fn1(){ return ...},
    fn2(){ return ...},
    fn3(){ return ...}
    ......
    //再维护vuex
    count:'count'
    .......
})
```



一个简单例子：

```
const store = new Vuex.Store({
	state: {
  	count: 0
  },
  mutations: {
  	increment: state=> state.count++,
    decrement: state=> state.count--
  
  }
})
new Vue({
	el: "#app",
  computed: {
  	count() {
    	return store.state.count;
    }
  },
  methods: {
  	increment() {
    	store.commit("increment");
    },
    decrement() {
    	store.commit("decrement");
    }
  }
})
```

就在jsfiddler这样的在线环境做就好了。

不用在搭建环境上浪费时间。

创建过程直截了当——仅需要提供一个初始 state 对象和一些 mutation：

现在，你可以通过 `store.state` 来获取状态对象，以及通过 `store.commit` 方法触发状态变更

再次强调，我们通过提交 mutation 的方式，而非直接改变 `store.state.count`，是因为我们想要更明确地追踪到状态的变化。

这个简单的约定能够让你的意图更加明显，这样你在阅读代码的时候能更容易地解读应用内部的状态改变。此外，这样也让我们有机会去实现一些能记录每次状态改变，保存状态快照的调试工具。有了它，我们甚至可以实现如时间穿梭般的调试体验。

由于 store 中的状态是响应式的，在组件中调用 store 中的状态简单到**仅需要在计算属性中返回即可**。触发变化也仅仅是在组件的 methods 中提交 mutation。



# 核心概念

## state

Vuex 使用**单一状态树**——是的，用一个对象就包含了全部的应用层级状态。

这也意味着，**每个应用将仅仅包含一个 store 实例。**单一状态树让我们能够直接地定位任一特定的状态片段，在调试的过程中也能轻易地取得整个当前应用状态的快照。

### mapState

当一个组件需要获取多个状态时候，**将这些状态都声明为计算属性会有些重复和冗余**。为了解决这个问题，我们可以使用 `mapState` **辅助函数帮助我们生成计算属性**，让你少按几次键：



使用 Vuex 并不意味着你需要将**所有的**状态放入 Vuex。虽然将所有的状态放到 Vuex 会使状态变化更显式和易调试，但也会使代码变得冗长和不直观。如果有些状态严格属于单个组件，最好还是作为组件的局部状态。你应该根据你的应用开发需要进行权衡和确定。

## Getter

## Mutation

改 Vuex 的 store 中的状态的唯一方法是提交 mutation。

Vuex 中的 mutation 非常类似于事件：

每个 mutation 都有一个字符串的 **事件类型 (type)** 和 一个 **回调函数 (handler)**。

这个回调函数就是我们实际进行状态更改的地方，并且它会接受 state 作为第一个参数：

## Action

Action 类似于 mutation，不同在于：

- Action 提交的是 mutation，而不是直接变更状态。
- **Action 可以包含任意异步操作。**

## Module

由于使用单一状态树，应用的所有状态会集中到一个比较大的对象。当应用变得非常复杂时，store 对象就有可能变得相当臃肿。

为了解决以上问题，Vuex 允许我们将 store 分割成**模块（module）**。每个模块拥有自己的 state、mutation、action、getter、甚至是嵌套子模块——从上至下进行同样方式的分割



Vuex 并不限制你的代码结构。但是，它规定了一些需要遵守的规则：

1. 应用层级的状态应该集中到单个 store 对象中。
2. 提交 **mutation** 是更改状态的唯一方法，并且这个过程是同步的。
3. 异步逻辑都应该封装到 **action** 里面。

使用了vuex的典型的目录结构。

```
├── index.html
├── main.js
├── api
│   └── ... # 抽取出API请求
├── components
│   ├── App.vue
│   └── ...
└── store
    ├── index.js          # 我们组装模块并导出 store 的地方
    ├── actions.js        # 根级别的 action
    ├── mutations.js      # 根级别的 mutation
    └── modules
        ├── cart.js       # 购物车模块
        └── products.js   # 产品模块
```

这里是购物车的例子。

https://github.com/vuejs/vuex/tree/dev/examples/shopping-cart

# 参考资料

1、理解Vuex，看这篇就够了

https://mobilesite.github.io/2016/12/18/vuex-introduction/

2、官网

https://vuex.vuejs.org/zh/guide/state.html

3、官网简单例子

https://jsfiddle.net/n9jmu5v7/1269/

4、Vuex入门（2）—— state,mapState,...mapState对象展开符详解

这篇文章很好。

https://blog.csdn.net/dkr380205984/article/details/82185740