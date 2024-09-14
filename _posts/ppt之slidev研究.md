---
title: ppt之slidev研究
date: 2024-09-14 18:34:28
tags:
	- ppt
---

--

现在是不是有写ppt的需求。

要在工作中更进一步，还是需要提高写ppt的能力。

这个也算是核心竞争力之一。

在ppt软件里编辑，总是比较耗时费力。

看看slidev能不能给我提供一套比较顺手的方案，让我可以快速编写ppt。

而且，要做到界面美观。

# 基本信息

从官网学习总结一下基本的信息。

https://cn.sli.dev/guide/why

slidev提供的价值是什么？

* 极强的灵活性和交互性。
* 帮助开发者使用熟悉的技术来提高演示的表现力。

使用markdown的方式编写ppt。

可以让你更急专注于内容。

ppt在浏览器里呈现。这意味着任何在web里能做到的效果，在slidev里都可以做到。

slidev也有渐进式设计。

就是你可以从最基本的markdown开始，逐渐添加效果。

编写的时候，通过vite的HMR实时渲染查看效果。效率高。

slidev还内置了录制和摄像头试图功能。

可以导出为pptx、pdf、图片格式。

也可以编译为静态html，方便你部署。

# 快速上手

```
npm init slidev@latest
```

这样会创建一个project，你就像做一个前端项目一样来写ppt。

也可以使用单文件的方式，但是不推荐：

```
npm install -g @slidev/cli
slidev slides.md
```

## 基本命令

```
slidev
	启动开发服务器。
slidev export
	导出为pdf等格式。
slidev build
	打包为html
slidev format
	格式化。
slidev --help
	查看帮助信息。
```

## 使用的技术栈

```
vite
vue3
unocss
	构建ppt的样式。
shiki, monaco
	为ppt嵌入code提供支持。
recordrtc
	录制工作和摄像头。
vueuse
iconify
	使用图标丰富你的ppt
drauu
	在ppt上绘图和批注。
katex
	使用latex渲染数学公式
mermaid
	基于文本的图标绘制。
```

# 语法

入口文件是slides.md文件。

使用`---`行来作为ppt的分页符。

## Frontmatter和Headmatter

在每一页ppt的开头，你可以添加一个Frontmatter来配置ppt。

其中，第一个frontmatter被称为headmatter，headmatter对整个ppt生效。

它们的文本是一个合法的yaml对象。

例如：

```
---
theme: default
title: hello world
---

# 第一页
第一页的Frontmatter也是整个文档的headmatter
---
layout: center
background: /1.png
class: text-white
---

---

# 第二页
1234

# 第三页
本页没有Frontmatter

---

---
src: ./pages/4.md # 本页只有Frontmatter
---

# 第五页

```

## 备注

在每一页ppt的最后的html注释内容会是ppt的备注信息。

注意是只有ppt最后的html注释才是，中间的不是。

```
<!-- 这个是备注 -->
```



