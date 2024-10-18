---
title: html之localStorage
date: 2019-01-21 17:16:12
tags:
	- html
---



在html5里，加入了一个localStorage的特性。

这个特性主要是用来做本地存储的。

解决了cookie存储空间不足的问题。cookie的大小限制是4K。

localStorage的一般是5M。

查看浏览器是否支持localStorage。

```
document.write(window.localStorage);
```

设置值的三种方式：

```
var storage = window.localStorage;
storage["a"] = 1;
storage.b = 2;
storage.setItem("c", 3);
console.log(typeof storage["a"]);
console.log(typeof storage["b"]);
console.log(typeof storage["c"]);
```

可以看到都是string的了。本来是int的。

因为localStorage只支持string类型。

相应的，有3种读取方式。

```
storage.a
storage["a"]
storage.getItem("a")
```

官方推荐getItem和setItem。

删除。

```
storage.clear();//全部清空
storage.removeItem("a");
```



我们一般和json一起用。

# localStorage存储的有效时间

`localStorage` 的存储是持久性的，一旦数据被存储，它会一直存在，直到被显式删除或浏览器的存储被清除。与 `sessionStorage` 不同，后者在浏览器窗口关闭时数据会被清空。

### 关键点：

- **有效期**：`localStorage` 中的数据没有有效时间限制，除非你手动删除它们，或者用户清除了浏览器的数据。
- **存储方式**：数据以键值对的形式存储，支持字符串类型。
- **容量限制**：通常每个源（域名）可以存储约 5MB 的数据，但具体限制可能因浏览器而异。

### 使用示例：

```javascript
// 存储数据
localStorage.setItem('key', 'value');

// 获取数据
const value = localStorage.getItem('key');

// 删除数据
localStorage.removeItem('key');

// 清空所有数据
localStorage.clear();
```

如果你有其他问题或需要更深入的解释，请告诉我！

# localStorage有哪些妙用

`localStorage` 是一种非常有用的Web存储方式，以下是一些妙用：

### 1. **用户偏好设置**
   - 保存用户的主题选择、语言设置或其他个性化配置，以便用户下次访问时自动应用。

### 2. **表单数据保存**
   - 在用户填写表单时，临时保存输入的数据，防止意外刷新或关闭页面导致数据丢失。

### 3. **购物车功能**
   - 在电商网站中，保存用户的购物车数据，确保在用户下次访问时仍然可用。

### 4. **离线支持**
   - 将应用的某些数据（例如文章列表）缓存到 `localStorage`，以便在离线状态下也能访问。

### 5. **用户认证令牌**
   - 存储用户的认证令牌，以便在页面刷新或重启时保持用户登录状态。

### 6. **访问计数**
   - 记录用户访问网站的次数，以便进行统计分析或个性化推荐。

### 7. **游戏状态保存**
   - 在Web游戏中保存玩家的进度、分数或其他状态，以便用户下次继续游戏。

### 8. **自定义仪表板**
   - 允许用户自定义页面布局和内容，并保存这些设置以便下次访问时加载。

### 9. **分析和跟踪**
   - 存储用户行为数据，进行分析以优化用户体验。

### 10. **快速缓存**
   - 将API请求的响应数据缓存到 `localStorage`，减少重复请求，提高性能。

### 使用示例：

```javascript
// 保存用户主题偏好
localStorage.setItem('theme', 'dark');

// 获取用户主题偏好
const theme = localStorage.getItem('theme');

// 删除用户偏好
localStorage.removeItem('theme');
```

这些只是 `localStorage` 的一些应用示例，实际应用中可以根据需要进行创意和扩展。如果需要更详细的代码示例或实现思路，请告诉我！

# 参考资料

1、localStorage使用总结

https://www.cnblogs.com/st-leslie/p/5617130.html