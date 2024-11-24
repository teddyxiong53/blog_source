---
title: Vue之vuetify
date: 2024-10-14 16:20:30
tags:
	- vue
---

--

看到这个web应用不错，很简洁。

https://toprss.webfollow.cc/

这个是基于vuetify做的。

代码在这里：

https://github.com/weekend-project-space/top-rss-hub

# vuetify

Vuetify 是一个基于 Vue.js 的 Material Design 组件框架，旨在帮助开发者快速构建美观且响应式的用户界面。以下是 Vuetify 的一些关键特点：

### 1. **Material Design**
   - Vuetify 遵循 Google 的 Material Design 规范，提供了丰富的视觉效果和交互体验。

### 2. **组件丰富**
   - Vuetify 提供了超过 80 个预构建的组件，例如按钮、卡片、对话框、表单等，开发者可以轻松使用。

### 3. **响应式设计**
   - 所有组件都支持响应式布局，能够在不同设备上良好展现。

### 4. **主题定制**
   - 支持创建和定制主题，开发者可以轻松更改颜色、字体和其他样式设置。

### 5. **无缝集成**
   - 可以与 Vue Router、Vuex 等 Vue 生态系统的其他库无缝集成。

### 6. **强大的支持**
   - 拥有良好的文档和活跃的社区支持，开发者可以快速找到解决方案和示例。

### 7. **开发工具**
   - 提供了一些开发工具，例如调试和性能分析工具，帮助开发者优化应用。

### 使用示例

以下是一个简单的 Vuetify 组件示例：

```html
<template>
  <v-app>
    <v-container>
      <v-btn color="primary">Hello Vuetify</v-btn>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
@import '~vuetify/dist/vuetify.min.css';
</style>
```

### 结论
Vuetify 是一个强大且灵活的框架，非常适合需要快速构建现代 Web 应用的开发者。如果你有具体的问题或想了解更深入的内容，请告诉我！

# HelloWorld

https://play.vuetifyjs.com/

直接在这里做实验就好。很方便。

```
<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>我的应用</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <v-container>
        <h1>欢迎使用 Vuetify!</h1>
        <p>这是一个示例应用。</p>
      </v-container>
    </v-main>
    <v-footer app>
      <span>© 2024 我的应用</span>
    </v-footer>
  </v-app>
</template>

<script setup>
  import { ref } from 'vue'

  const msg = ref('Hello World!')
</script>

```

# 实际项目

这个简单而且典型。

https://github.com/weekend-project-space/top-rss-hub

# 官网学习总结

## 开始

最简单的方法，是这样安装：

```
pnpm create vuetify
```

这个命令执行的时候，会提示你进行一些配置。

完成后，就会生成一个基本的项目结构。

启动：

```
pnpm dev
```



vuetify是什么？

vuetify是一个基于vue的框架。

作用是用来创建美观且响应式的ui。

包含了各种可定制和可重用的组件。

## 一些基本的布局结构

* baseline。
* extended toolbar。
* systembar
* inbox。就是类似gmail那样的布局。
* constrained。类似v2ex页面那样的布局。
* side navigation。带侧边导航栏的。
* three column。
* discord。
* stream。

## feature

### a11y

Accessibility。就是无障碍模式。

这个不多看了。

### alias

可以给默认组件起别名。

举例：

```
export default createVuetify({
	aliases: {
		MyButton: VBtn,
		MyButtonAlt: VBtn,
	}
})
```

配置virtual component默认值。

```
export default createVuetify({
	aliases: {
		MyButton: VBtn,
	},
	defaults: {
		VBtn: {variant: 'flat'},
		MyButton: {variant: 'tonal'}
	}
})
```

这个默认值配置还可以嵌套。例如VCard里的VBtn才特别定制。

```
VCard: {
	MyButton: {color: 'secondary'}
}
```

### 应用布局

布局的组件有：

* v-app-bar
* v-system-bar
* v-navigation-drawer
* v-footer
* v-bottom-navigation
* v-main

### 蓝图

蓝牙是用来预设整个应用的风格的。

包含了组件、颜色、语言。

例如，下面就是使用Material Design 1的preset。

```js
import {md1} from 'vuetify/blueprints'
export default createVuetify ({
  blueprint: md1
})
```

可用的蓝图有3套：md1、md2、md3。分别是2014年、2017年、2022年推出的。

### Date处理

```vue
<script setup>
	import {useDate} from 'vuetify';
  const date = useDate();
  console.log(date.getMonth(new Date('20240101')));
</script>
```

useDate返回的date对象，有一个format方法，可用支持各种格式的format。

### Display处理

提供当前设备的显示相关信息。

在vue的组合式api里，这样来获取：

```vue
<script setup>
	import {onMounted} from 'vue';
  import {useDisplay} from 'vuetify';
  const {mobile} = useDisplay();
  onMounted(()=> {
    console.log(mobile.value);
  })
</script>
```

如果是使用vue的选项式api，则这样：

```vue
<script>
	export default {
    mounted() {
      console.log(this.$vuetify.display.mobile);
    }
  }
</script>
```

可用配置的属性是breakpoint和阈值。

```js
export default createVuetify({
  display: {
    mobileBreakpoint: 'sm',
    thresholds: {
      xs: 0,
      sm: 340,
      md: 540,
      lg: 800,
      xl: 1280,
    }
  }
})
```

### icon-font

这样引入：

```js
import {aliases, mdi} from 'vuetify/iconsets/mdi';
export default createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases, 
    sets: {
      mdi,
    }
  }
})
```

然后这样使用：

```vue
<template>
	<v-icon icon="mdi-home" />
</template>
```

Mdi 是Material Design Icon的缩写。

这样安装：

```
pnpm add @mdi/font -D
```

## Util css class

Css 工具类。这个是类似tailwindcss那样的一些工具类。

### border

```
border
border-thin
border-sm
border-md
border-0  这个表示width为0
border-t  表示top的width为thin
border-t-0

```

## components

可用分为这些大类：

* 密封组件。包括Button、Card、List、Chip、Divider、Expansion Panel、Menu、Dialog、Bottom Sheet、Overlay、Toolbar、Tooltip、Sheet。
* 导航组件。AppBar、FAB（就是安卓那个浮动在右下角的圆形按钮这种组件）、Navigation Drawer（导航抽屉）、分页组件、底部导航、面包屑、Footer、Speed Dial、SystemBar、标签页。
* 表单组件。Autocomplete、Combobox、TextField、Checkbox、Switch、Radio、FileInput、Form、Inputs、Number input、OTP Input（就是方框模式的验证码输入）、Select、Slider、TextArea。
* 布局组件。Grid
* Selection组件。轮播、按钮组、ChipGroup、Stepper。
* 数据和显示组件。弹窗、DataTable、
* 反馈组件。Alert、Badge、Banner、Skeleton、Rating、Timeline、Hover、Progress、
* 图片组件。Aspect、Avatar、
* Picker组件。ColorPicker、DatePicker。
* Provider组件。
* Misc组件。



# v-layout介绍

在 Vuetify 中，`v-layout` 是用于创建响应式布局的组件。虽然在最新版本的 Vuetify 中，`v-layout` 已被 `v-container`、`v-row` 和 `v-col` 组件取代，但理解其概念仍然很重要。

### 基本概念

- **`v-layout`**: 用于定义一个布局容器，可以包含多个列和行。它可以设置方向（水平或垂直）和对齐方式。
- **响应式**: 布局会根据屏幕大小自动调整，提供良好的用户体验。

### 主要属性

- **`row`**: 将布局设置为行。
- **`column`**: 将布局设置为列。
- **`align-center`**: 将内容垂直居中对齐。
- **`justify-center`**: 将内容水平居中对齐。

### 使用示例

在较新版本的 Vuetify 中，推荐使用 `v-container`、`v-row` 和 `v-col` 来替代 `v-layout`。以下是一个简单的示例：

```html
<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <div>列 1</div>
      </v-col>
      <v-col cols="12" md="6">
        <div>列 2</div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ExampleComponent'
}
</script>
```

### 总结

虽然 `v-layout` 在新版本中已被替代，但理解其基本概念有助于迁移到现代的布局组件。如果您有关于布局的具体问题或需要更多示例，请告诉我！

# v-slot

跟template会一起出现，我们会看到在template里面还有可能嵌套template。这个内部的template，一般就会带上v-slot属性。

使用插槽（如 `v-slot`）来定义组件的可插入内容，允许父组件向子组件传递内容。

```
<template>
  <v-card>
    <template v-slot:header>
      <h2>卡片标题</h2>
    </template>
    <p>卡片内容</p>
  </v-card>
</template>
```



# \#loading是什么的简略写法？

`#loading` 是 Vue 3 中具名插槽（named slot）的简写形式。它是 `v-slot:loading` 的简化写法。

### 详细解释

- **`#loading`** 是具名插槽的简写，表示插槽的名称为 `loading`。
- **`v-slot:loading`** 是完整的写法，功能相同。

### 示例

```vue
<!-- 使用 #loading -->
<template>
  <MyComponent>
    <template #loading>
      <div>Loading...</div>
    </template>
  </MyComponent>
</template>

<!-- 使用 v-slot:loading -->
<template>
  <MyComponent>
    <template v-slot:loading>
      <div>Loading...</div>
    </template>
  </MyComponent>
</template>
```

### 总结

`#loading` 是 `v-slot:loading` 的简写形式，两者功能相同，都是用于定义具名插槽。使用简写可以让代码更简洁。希望这个解释对你有帮助！如果还有其他问题，请随时询问。

# 属性和slot的区别是什么

在 Vue 中，属性（props）和插槽（slots）都是用来在组件之间传递数据和内容的机制，但它们的用法和目的有所不同。以下是它们之间的主要区别：

### 1. 属性（Props）

- **定义**: 属性是组件接收的数据，通常是父组件通过定义的属性传递给子组件的数据。
- **用法**: 在子组件中，可以通过 `props` 选项定义接收的属性，并在模板中使用它们。
- **作用**: 用于传递数据、配置组件的行为或状态。

#### 示例

```vue
<!-- ParentComponent.vue -->
<template>
  <ChildComponent message="Hello, World!" />
</template>

<!-- ChildComponent.vue -->
<template>
  <div>{{ message }}</div>
</template>

<script>
export default {
  props: {
    message: String,
  },
};
</script>
```

### 2. 插槽（Slots）

- **定义**: 插槽是一种内容分发机制，允许父组件在子组件的指定位置插入任意内容。
- **用法**: 在子组件中使用 `<slot>` 标签定义插槽，父组件则可以在子组件内提供内容。
- **作用**: **用于提供更大的灵活性，允许在组件中插入不同的内容，而不仅仅是数据。**

#### 示例

```vue
<!-- ParentComponent.vue -->
<template>
  <ChildComponent>
    <template #default>
      <h1>Hello, World!</h1>
    </template>
  </ChildComponent>
</template>

<!-- ChildComponent.vue -->
<template>
  <div>
    <slot></slot> <!-- 在这里插入父组件的内容 -->
  </div>
</template>
```

### 主要区别总结

1. **数据 vs 内容**:
   - **属性**: 用于传递数据（如字符串、数字、对象等）。
   - **插槽**: 用于插入内容（如 HTML、组件等）。

2. **灵活性**:
   - **属性**: 主要用于配置组件的状态或行为。
   - **插槽**: 允许动态插入不同内容，提供更高的灵活性。

3. **使用场景**:
   - **属性**: 当你需要传递具体数据时使用。
   - **插槽**: 当你需要在组件中插入自定义内容时使用。

希望这个解释能帮助你理解属性和插槽之间的区别！如果你还有其他问题，请随时询问。

# 给一个更加贴合实际的slot的例子

当然！以下是一个更贴合实际的插槽（slot）用法的示例，展示如何在一个自定义的卡片组件中使用插槽来插入标题、内容和操作按钮。

### 示例：自定义卡片组件

#### 1. 创建 `Card.vue` 组件

```vue
<template>
  <div class="card">
    <div class="card-header">
      <slot name="header">默认标题</slot>
    </div>
    <div class="card-body">
      <slot>默认内容</slot>
    </div>
    <div class="card-footer">
      <slot name="footer">默认操作</slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
};
</script>

<style>
.card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 16px;
  margin: 10px;
}
.card-header {
  font-weight: bold;
}
.card-footer {
  text-align: right;
}
</style>
```

### 2. 使用 `Card.vue` 组件的父组件

```vue
<template>
  <div>
    <Card>
      <template #header>
        <h3>卡片标题</h3>
      </template>
      <p>这是卡片的主要内容，可以是任何信息。</p>
      <template #footer>
        <el-button type="primary">确定</el-button>
        <el-button type="default">取消</el-button>
      </template>
    </Card>
    
    <Card>
      <template #header>
        <h3>另一张卡片</h3>
      </template>
      <p>这是另一张卡片的内容。</p>
    </Card>
  </div>
</template>

<script>
import Card from './Card.vue';

export default {
  components: {
    Card,
  },
};
</script>
```

### 解释

1. **Card 组件**:
   - 该组件定义了三个插槽：`header`、默认插槽和 `footer`。
   - 你可以在卡片中插入自定义的标题、内容和操作按钮。

2. **父组件**:
   - 使用 `Card` 组件时，你可以为 `header` 和 `footer` 插槽提供自定义内容。
   - 如果没有为插槽提供内容，`Card` 组件将显示默认内容。

### 总结

这个示例展示了如何使用插槽来创建灵活且可重用的组件。通过插槽，父组件可以根据需要动态插入不同的内容，而 `Card` 组件则保持了自己的结构和样式。这种方式极大地增强了组件的复用性和灵活性。希望这个例子能帮助你理解插槽的实际应用！如果有其他问题，请随时询问。



