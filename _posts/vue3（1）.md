---
title: vue3（1）
date: 2024-05-15 17:10:11
tags:
	- web
---

--

# vue3的组合式api介绍

当然，以下是Vue 3 中的组合式 API 的简要介绍：

| 组合式 API               | 描述                                                         |
| ------------------------ | ------------------------------------------------------------ |
| `setup()`                | `setup()` 函数是组件中使用==组合式 API 的入口点。==在 `setup()` 函数中，可以设置组件的状态、计算属性、方法等。 |
| `reactive()`             | `reactive()` 函数用于==创建一个响应式对象==。当对象的属性发生变化时，相关的视图会自动更新。 |
| `ref()`                  | `ref()` 函数用于==创建一个响应式的引用类型==。与普通的变量不同，通过 `ref()` 创建的变量在模板中的使用需要使用 `.value` 进行访问。 |
| `computed()`             | `computed()` 函数用于==创建一个计算属性==。计算属性的值会根据其依赖的响应式数据自动更新。 |
| `watch()`                | `watch()` 函数用于观察响应式数据的变化，并在数据变化时执行相应的操作。 |
| `toRefs()`               | `toRefs()` 函数用于==将响应式对象转换为普通对象==，并将对象的每个属性转换为独立的引用。这样，在模板中使用时就不需要再加上 `.value`。 |
| `provide()` / `inject()` | `provide()` 和 `inject()` 用于在父组件中提供数据，然后在子组件中注入这些数据。 |
| `watchEffect()`          | `watchEffect()` 函数用于创建一个响应式副作用。它会自动追踪其依赖，并在依赖变化时重新运行。 |
| `onMounted()`            | `onMounted()` 函数用于在组件挂载后执行相应的操作。           |
| `onUpdated()`            | `onUpdated()` 函数用于在组件更新后执行相应的操作。           |
| `onUnmounted()`          | `onUnmounted()` 函数用于在组件销毁前执行相应的操作。         |

这些是 Vue 3 中常用的组合式 API，它们使得组件的逻辑更加清晰、灵活，并且更容易测试和重用。

# 为什么要推出组合式api

Vue.js 推出组合式 API 的主要目的

是为了解决在使用选项式 API 时可能出现的一些问题，

并提供更灵活、可维护的组件设计方案。

以下是推出组合式 API 的一些主要原因：

1. **逻辑复用**：在选项式 API 中，逻辑复用主要依赖于 mixins，但 mixins 存在一些问题，如命名冲突、难以追踪数据来源等。组合式 API 提供了更明确的逻辑复用方式，可以更轻松地将功能打包为可复用的逻辑单元。

2. **代码组织**：选项式 API 基于不同的选项（如 `data`、`methods`、`computed` 等）来组织代码，当组件逻辑变得复杂时，这种方式可能导致代码结构混乱、难以维护。组合式 API 允许将相关的代码逻辑放在一起，使代码更易于理解和维护。

3. **类型推导**：组合式 API 更有利于 TypeScript 等类型检查工具的类型推导，因为它能更清晰地表达组件的数据结构和方法。

4. **更好的 TypeScript 支持**：选项式 API 在 TypeScript 下可能会遇到一些类型推导的问题，而组合式 API 则更容易与 TypeScript 结合使用，提供更好的类型支持。

5. **更好的测试性**：组合式 API 提供了更明确的入口点（`setup()` 函数），使得组件的测试更加简单，可以更轻松地编写单元测试和集成测试。

总的来说，组合式 API 的推出旨在提供一种更灵活、可维护、易于测试的组件设计方案，以解决选项式 API 中存在的一些问题，并提升 Vue.js 在大型应用开发中的可用性和开发效率。

# 给出示例对比选项式api和组合式api

下面是一个简单的示例，演示了如何使用选项式 API 和组合式 API 实现相同的功能：

### 选项式 API 示例：

```vue
<template>
  <div>
    <button @click="increment">点击 {{ count }}</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      count: 0
    };
  },
  methods: {
    increment() {
      this.count++;
    }
  }
};
</script>
```

### 组合式 API 示例：

```vue
<template>
  <div>
    <button @click="increment">点击 {{ state.count }}</button>
  </div>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const state = reactive({
      count: 0
    });

    const increment = () => {
      state.count++;
    };

    return {
      state,
      increment
    };
  }
};
</script>
```

在这两个示例中，功能是相同的：点击按钮会增加计数器的值。但是实现方式略有不同：

- 选项式 API 示例使用了 `data` 和 `methods` 选项来定义数据和方法。
- 组合式 API 示例使用了 `setup()` 函数来设置组件的状态和方法，并且使用 `reactive()` 函数创建了一个响应式对象。

通过对比可以看出，

组合式 API 在代码结构上更加清晰，逻辑更加集中，

==而选项式 API 则更为传统，适合于一些简单的场景。==

组合式 API 的优势在于可以更方便地重用逻辑、组织代码，并且更易于测试和维护。

# defineComponent

`defineComponent` 是 Vue 3 中的一个函数，用于定义一个组件。它是通过 `createApp` 创建应用实例后的全局方法之一。

```javascript
import { defineComponent } from 'vue';

const MyComponent = defineComponent({
  // 组件的选项
  props: {
    // 定义组件的 props
  },
  setup(props, context) {
    // 设置组件的初始状态和逻辑
    // 使用 props 和 context 参数
    // 返回组件的响应式数据和方法
    return {
      // 返回组件的响应式数据和方法
    };
  },
  // 其他组件选项，如 methods、computed、watch 等
});

export default MyComponent;
```

`defineComponent` 接受一个包含组件选项的对象作为参数，并返回一个组件对象。

在这个对象中，你可以定义组件的属性（props）、组件的初始状态和逻辑（setup）、以及其他选项（methods、computed、watch 等）。

使用 `setup` 函数来设置组件的初始状态和逻辑，并返回组件的响应式数据和方法。

使用 `defineComponent` 可以更明确地定义组件，使得代码更易于理解和维护。