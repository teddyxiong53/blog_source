---
title: html之input标签
date: 2019-01-22 11:05:55
tags:
	- html

---



```
type
	button
	checkbox
	file
	hidden
	image
	password
	radio
	reset
	submit
	text
```

# input是否必须放在form里

不是必须的，单独使用没必要写在form标签内，

但是假如你需要利用input标签收集用户信息并发送给后端，建议是写在form标签内

没有放在form中或**没有name属性**，那么form提交的时候会**忽略这个元素。**



input标签外是否添加form标签需要按情形区分：

应用场景的区别：

1.所有向后台提交数据（包括原生和ajax提交）的input都建议用form包裹，

2.如果**只是用来做前台交互效果则不推荐使用form包裹**。

但提交数据时，其实也可以不用form包裹input标签：

1.如果有form标签，在点击提交铵钮时，**浏览器自动收集参数，并打包一个http请求到服务器**，完成表单提交。

在这一过程中，浏览器会根据method的不同，将参数编码后，放在urI中(get)，或者放在请求的data中(post)。然后发送到服务器。



2.如果没有form，post方式的提交要使用ajax手工完成。get方式的提交需要自己拼接url。

# 除了空检查，还有属性可以进行更加高级的检查吗

是的，除了 `required` 属性，HTML 的输入元素还支持多种属性，以进行更高级的输入检查和验证。以下是一些常见的属性及其功能：

### 1. `pattern` 属性

- **用途**：定义输入字段的正则表达式模式，以限制用户输入格式。
- **示例**：
  ```html
  <input type="text" name="username" pattern="[A-Za-z]{3,}" title="用户名必须至少包含三个字母">
  ```

### 2. `min` 和 `max` 属性

- **用途**：用于数值输入（如 `number`、`date` 等），限制输入的最小值和最大值。
- **示例**：
  ```html
  <input type="number" name="age" min="18" max="99" required>
  ```

### 3. `maxlength` 和 `minlength` 属性

- **用途**：限制输入字段的字符数。
- **示例**：
  ```html
  <input type="text" name="password" minlength="6" maxlength="12" required>
  ```

### 4. `type` 属性

- **用途**：不同类型的输入字段会自动进行相应的验证。例如：
  - `email`：自动检查邮箱格式。
  - `url`：自动检查 URL 格式。
  - `tel`：可用于电话格式。
- **示例**：
  ```html
  <input type="email" name="email" required>
  ```

### 5. `step` 属性

- **用途**：对数值输入进行增量限制，适用于 `number` 或 `date` 类型。
- **示例**：
  ```html
  <input type="number" name="quantity" min="1" step="1" required>
  ```

### 6. 自定义数据验证

- **用途**：结合 JavaScript，可以实现更复杂的逻辑。
- **示例**：
  ```javascript
  document.getElementById('myForm').addEventListener('submit', function(event) {
      const emailInput = document.getElementById('email');
      if (!emailInput.value.includes('@')) {
          event.preventDefault(); // 阻止表单提交
          alert("请输入有效的邮箱地址。");
      }
  });
  ```

### 总结

使用这些属性可以进行更复杂的输入验证，确保用户输入符合预期格式，提高表单的有效性和用户体验。结合 JavaScript，可以实现更灵活的验证逻辑。

# 参考资料

1、

http://www.w3school.com.cn/tags/tag_input.asp

2、

https://www.imooc.com/qadetail/300404?t=477023

3、input标签之外是否一定添加form标签

https://www.cnblogs.com/jokes/p/9884958.html