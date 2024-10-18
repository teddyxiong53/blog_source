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

# vue2 和vue3的区别

以下是 Vue 2 和 Vue 3 之间的一些主要区别，以列表形式对比：

| 特性                | Vue 2                             | Vue 3                               |
| ------------------- | --------------------------------- | ----------------------------------- |
| **响应式系统**      | 使用 Object.defineProperty()      | 使用 Proxy 进行更高效的响应式管理   |
| **组合式 API**      | 主要使用选项 API                  | 引入组合式 API（Composition API）   |
| **性能**            | 性能良好，但在大型应用中较慢      | 显著提高性能，优化了虚拟 DOM 和渲染 |
| **TypeScript 支持** | 支持有限                          | 原生支持 TypeScript                 |
| **Fragment 支持**   | 不支持多个根节点                  | 支持在组件中返回多个根节点          |
| **Teleport**        | 无                                | 提供 Teleport 组件方便地传送元素    |
| **Suspense**        | 无                                | 支持异步组件和加载状态的处理        |
| **生命周期钩子**    | 使用 `beforeDestroy`, `destroyed` | 使用 `beforeUnmount`, `unmounted`   |
| **自定义指令**      | 通过 `Vue.directive` 注册         | 通过 `app.directive` 注册           |
| **v-model 语法**    | 使用 `v-model`，支持单向绑定      | 支持双向绑定，语法更灵活            |
| **全局 API**        | 全局 API 不够一致                 | 全局 API 更加一致性和简洁性         |
| **性能优化**        | 一些优化措施，但不够全面          | 更全面的性能优化和内存管理          |

# 组合式api和选项式api对比说明

以下是组合式 API 和选项式 API 的对比说明，主要针对 Vue 3 中的这两种编写组件的方式：

| 特性             | 选项式 API (Options API)                  | 组合式 API (Composition API)                      |
| ---------------- | ----------------------------------------- | ------------------------------------------------- |
| **定义方式**     | 使用 `data`、`methods`、`computed` 等选项 | 使用 `setup()` 函数进行逻辑组合                   |
| **组织结构**     | 逻辑按选项分组（数据、方法、计算属性）    | 逻辑按功能分组，更加灵活和模块化                  |
| **可读性**       | 简单易懂，适合小型组件                    | 对于大型组件，可能更复杂但提供更好的可维护性      |
| **类型推导**     | TypeScript 支持有限                       | 更强的 TypeScript 支持，类型推导更简洁            |
| **重用性**       | 通过混入 (mixins) 和插件重用              | 使用组合函数 (composables) 提高逻辑重用性         |
| **响应式**       | 使用 `this` 访问响应式数据                | 使用 `ref` 和 `reactive` 明确控制响应式状态       |
| **生命周期钩子** | 使用选项定义如 `created`、`mounted`       | 在 `setup()` 中使用 `onMounted`、`onUnmounted` 等 |
| **测试**         | 组件逻辑较集中，单元测试相对简单          | 逻辑分散，可能需要更细粒度的测试                  |
| **代码分离**     | 难以在大型组件中做到逻辑分离              | 更容易实现逻辑分离和重用                          |

### 示例

#### 选项式 API 示例

```vue
<template>
  <div>
    <p>{{ message }}</p>
    <button @click="updateMessage">更新消息</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: 'Hello, Vue 2!',
    };
  },
  methods: {
    updateMessage() {
      this.message = 'Hello, Vue 3!';
    },
  },
};
</script>
```

#### 组合式 API 示例

```vue
<template>
  <div>
    <p>{{ message }}</p>
    <button @click="updateMessage">更新消息</button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const message = ref('Hello, Vue 3!');

    const updateMessage = () => {
      message.value = 'Hello, Vue 3!';
    };

    return {
      message,
      updateMessage,
    };
  },
};
</script>
```

### 结论

选项式 API 更适合小型项目和快速开发，而组合式 API 提供了更强大的灵活性和可维护性，特别是在大型项目中。选择哪种 API 取决于项目需求和开发团队的熟悉程度。如果你有具体问题或需要更多细节，请告诉我！

# Teleport 组件

`Teleport` 是 Vue 3 中的新组件，允许你将一个组件的子节点渲染到 DOM 的不同位置，而不是它们在组件树中的默认位置。这对于需要在特定位置（如模态框、弹出菜单等）渲染内容的场景非常有用。

### 使用示例

以下是一个使用 `Teleport` 组件的基本示例：

```vue
<template>
  <div>
    <h1>这是主内容</h1>
    <button @click="showModal = true">打开模态框</button>

    <Teleport to="body">
      <div v-if="showModal" class="modal">
        <h2>模态框标题</h2>
        <p>这是模态框的内容。</p>
        <button @click="showModal = false">关闭</button>
      </div>
    </Teleport>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showModal: false,
    };
  },
};
</script>

<style>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
```

### 关键属性

- **`to`**：指定要渲染的目标位置，可以是 CSS 选择器（如 `body`、`#app` 等）或一个 DOM 元素。
- **子节点**：`Teleport` 的子节点会被渲染到指定的 `to` 位置。

### 适用场景

1. **模态框**：将模态框内容渲染到 `body`，避免样式冲突。
2. **工具提示**：在页面的特定位置渲染工具提示或上下文菜单。
3. **通知**：将通知消息渲染到页面的顶部或底部。

### 结论

`Teleport` 是一个强大的工具，能够帮助开发者灵活地处理组件的渲染位置，提高应用的可用性和用户体验。如果你有具体问题或需要更多示例，请告诉我！

# ref说明

`ref` 是 Vue 3 中的一个核心概念，用于创建响应式数据引用。它允许开发者定义基本数据类型（如字符串、数字、布尔值等）或对象的响应式状态，并在 Vue 组件中使用。以下是 `ref` 的详细说明及使用示例：

### 基本概念

- **创建响应式引用**：使用 `ref()` 函数创建一个响应式引用。
- **访问和修改**：通过 `.value` 属性访问和修改引用的值。

### 使用示例

#### 1. 创建和使用 `ref`

```vue
<template>
  <div>
    <p>计数：{{ count }}</p>
    <button @click="increment">增加计数</button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const count = ref(0); // 创建一个响应式引用

    const increment = () => {
      count.value++; // 修改引用的值
    };

    return {
      count,
      increment,
    };
  },
};
</script>
```

### 关键特性

- **响应性**：当 `ref` 的值发生变化时，相关的视图会自动更新。
- **适用于基本数据类型**：`ref` 特别适合用于简单的基本数据类型，因为它可以使这些类型变得响应式。
- **嵌套对象**：如果使用 `ref` 包装一个对象，访问和修改其属性时仍需使用 `.value`。

#### 2. 嵌套对象示例

```vue
<template>
  <div>
    <p>用户：{{ user.name }}</p>
    <button @click="updateName">更新名称</button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const user = ref({ name: 'Alice' }); // 创建一个响应式对象

    const updateName = () => {
      user.value.name = 'Bob'; // 修改嵌套对象的属性
    };

    return {
      user,
      updateName,
    };
  },
};
</script>
```

### 3. 与 `reactive` 的对比

- **`ref`**：用于基本数据类型和简单对象，使用 `.value` 访问。
- **`reactive`**：用于创建深层响应式对象，自动处理嵌套属性。

### 4. 适用场景

- **简单状态管理**：适合管理简单的状态，如计数器、表单输入等。
- **与模板结合**：在模板中直接使用 `ref` 创建的响应式数据。
- **组合式 API**：在 `setup()` 中使用，充分利用 Vue 3 的新特性。

### 结论

`ref` 是 Vue 3 中用于创建响应式数据的基础工具，能够简化状态管理和组件逻辑。如果你有更多具体问题或需要进一步的示例，请告诉我！

# script setup

`<script setup>` 是 Vue 3 中的一种新的编写组件的方式，旨在简化组合式 API 的使用。它提供了一种更简洁的语法，可以让开发者更高效地定义组件的逻辑和数据。

### 主要特性

1. **简化语法**：去掉了 `export default`，直接在 `<script setup>` 中定义数据和方法。
2. **自动引入**：在 `<script setup>` 中使用的 Vue 函数（如 `ref`、`computed` 等）无需显式导入。
3. **更好的类型推导**：与 TypeScript 结合使用时，提供更好的类型推导支持。

### 使用示例

以下是一个使用 `<script setup>` 的基本示例：

```vue
<template>
  <div>
    <h1>{{ message }}</h1>
    <button @click="updateMessage">更新消息</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const message = ref('Hello, Vue 3!'); // 创建响应式引用

const updateMessage = () => {
  message.value = 'Hello, <script setup>!';
};
</script>

<style>
/* 自定义样式 */
</style>
```

### 关键点

- **响应式数据**：使用 `ref` 创建响应式变量，直接在 `<script setup>` 中使用。
- **方法定义**：可以直接定义函数，无需将其放入 `methods` 对象中。
- **组合逻辑**：可以轻松地组合多个逻辑，使用函数和变量。

### 适用场景

1. **小型和中型组件**：适合快速开发和原型设计。
2. **组合式 API**：在使用组合式 API 时，可以更简洁地组织代码。
3. **TypeScript 支持**：在 TypeScript 项目中，提供更好的类型推导和编写体验。

### 结论

`<script setup>` 是一种高效且简洁的方式来编写 Vue 3 组件，适合现代开发的需求。如果你有更多问题或需要具体示例，请告诉我！