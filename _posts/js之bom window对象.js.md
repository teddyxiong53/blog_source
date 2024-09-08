---
title: js之bom window对象
date: 2024-09-08 09:56:17
tags:
	- 前端

---

--

# 常用属性

`window` 对象是 JavaScript 中的全局对象，代表浏览器的窗口。它包含许多属性和方法，用于控制浏览器窗口和与文档进行交互。以下是一些常用的 `window` 属性的介绍：

### 1. **`window.document`**
- 代表当前文档对象，允许访问和操作 HTML 内容。
  ```javascript
  const title = window.document.title;
  ```

### 2. **`window.location`**
- 表示当前文档的 URL，允许获取和改变地址。
  ```javascript
  console.log(window.location.href); // 获取当前 URL
  window.location.href = 'https://www.example.com'; // 跳转到新 URL
  ```

### 3. **`window.history`**
- 提供对浏览器会话历史的访问，允许前进和后退。
  ```javascript
  window.history.back(); // 返回上一页
  ```

### 4. **`window.navigator`**
- 代表浏览器的状态和信息，包括用户代理、语言等。
  ```javascript
  console.log(window.navigator.userAgent); // 获取用户代理字符串
  ```

### 5. **`window.console`**
- 提供对浏览器控制台的访问，用于调试。
  ```javascript
  window.console.log('调试信息');
  ```

### 6. **`window.innerWidth` 和 `window.innerHeight`**
- 返回浏览器窗口的内部宽度和高度（不包括工具栏和滚动条）。
  ```javascript
  console.log(window.innerWidth, window.innerHeight);
  ```

### 7. **`window.outerWidth` 和 `window.outerHeight`**
- 返回浏览器窗口的外部宽度和高度（包括工具栏和滚动条）。
  ```javascript
  console.log(window.outerWidth, window.outerHeight);
  ```

### 8. **`window.screen`**
- 提供关于用户屏幕的信息，如屏幕的宽度和高度。
  ```javascript
  console.log(window.screen.width, window.screen.height);
  ```

### 9. **`window.setTimeout()`**
- 设置一个定时器，在指定时间后执行代码。
  ```javascript
  window.setTimeout(() => {
      alert('3秒后执行');
  }, 3000);
  ```

### 10. **`window.setInterval()`**
- 设置一个定时器，按照指定的时间间隔重复执行代码。
  ```javascript
  const intervalId = window.setInterval(() => {
      console.log('每秒执行一次');
  }, 1000);
  ```

### 11. **`window.clearTimeout()` 和 `window.clearInterval()`**
- 用于取消之前设置的定时器。
  ```javascript
  window.clearTimeout(timeoutId);
  window.clearInterval(intervalId);
  ```

### 12. **`window.alert()`, `window.confirm()`, `window.prompt()`**
- 弹出对话框：
  - **`alert()`**: 显示信息。
  - **`confirm()`**: 显示确认框，返回布尔值。
  - **`prompt()`**: 显示输入框，返回用户输入的值。
  ```javascript
  window.alert('这是一个警告');
  const isConfirmed = window.confirm('你确定吗？');
  const userInput = window.prompt('请输入你的名字:');
  ```

### 13. **`window.localStorage` 和 `window.sessionStorage`**
- 用于在用户的浏览器中存储数据：
  - **`localStorage`**: 永久存储，直到被删除。
  - **`sessionStorage`**: 仅在同一会话中存储，窗口关闭后数据消失。
  ```javascript
  window.localStorage.setItem('key', 'value');
  const value = window.localStorage.getItem('key');
  ```

### 总结
`window` 对象提供了丰富的属性和方法，帮助开发者与浏览器环境和文档进行交互。通过这些属性，可以实现页面的动态行为、获取用户信息、处理浏览器历史等功能。