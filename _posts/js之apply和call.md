---
title: js之apply和call
date: 2019-08-22 16:45:03
tags:
	- js
---

--

# call和apply说明

`call` 和 `apply` 是 JavaScript 中的两个函数方法，用于改变函数内部的 `this` 指向。它们的主要区别在于参数的传递方式。

### `call`

- **语法**: `func.call(thisArg, arg1, arg2, ...)`
- **功能**: 调用一个函数，并指定 `this` 关键字的值，以及传递参数。
- **参数**:
  - `thisArg`: 在函数运行时使用的 `this` 值。
  - `arg1, arg2, ...`: 传递给函数的参数。

**示例**:
```javascript
function greet(greeting) {
    console.log(greeting + ', ' + this.name);
}

const person = { name: 'Alice' };
greet.call(person, 'Hello'); // 输出: Hello, Alice
```

### `apply`

- **语法**: `func.apply(thisArg, [argsArray])`
- **功能**: 类似于 `call`，但参数是通过数组传递的。
- **参数**:
  - `thisArg`: 在函数运行时使用的 `this` 值。
  - `argsArray`: 一个数组或类数组对象，包含传递给函数的参数。

**示例**:
```javascript
function greet(greeting) {
    console.log(greeting + ', ' + this.name);
}

const person = { name: 'Bob' };
greet.apply(person, ['Hi']); // 输出: Hi, Bob
```

### 总结

- 使用 `call` 时，参数逐个列出。
- 使用 `apply` 时，参数放在一个数组中。

这两个方法都非常有用，特别是在需要控制 `this` 上下文时。例如，在事件处理、回调函数或者是面向对象编程中。

# bind的用法和与call、apply的区别？

当然可以！`bind`、`call` 和 `apply` 都是 JavaScript 中用于设置函数上下文的工具，但它们的用法和目的有所不同。

### `bind`

- **语法**: `func.bind(thisArg[, arg1[, arg2[, ...]]])`
- **功能**: 创建一个新函数，该函数在调用时将 `this` 关键字设置为提供的 `thisArg`。与 `call` 和 `apply` 不同，`bind` 不会立即调用函数，而是返回一个新的函数。
- **参数**:
  - `thisArg`: 在新函数中使用的 `this` 值。
  - `arg1, arg2, ...`: 可选参数，可以在调用新函数时预先填充。

**示例**:
```javascript
function greet(greeting) {
    console.log(greeting + ', ' + this.name);
}

const person = { name: 'Charlie' };
const greetCharlie = greet.bind(person);
greetCharlie('Hello'); // 输出: Hello, Charlie
```

### `call` 和 `apply` 的区别

- **调用方式**:
  - `call`：立即调用函数，参数逐个列出。
  - `apply`：立即调用函数，参数作为数组传递。

- **返回值**:
  - `call` 和 `apply` 返回函数执行的结果。
  - `bind` 返回一个新函数，而不执行原函数。

### 总结

- **`call`** 和 **`apply`**: 用于立即调用函数并设置 `this`，参数传递方式不同。
- **`bind`**: 用于创建一个新函数，设置 `this`，并可以预先绑定参数，但不会立即执行。

这使得 `bind` 特别适合在事件处理和回调中使用，例如在某些情况下需要保持 `this` 的上下文。

# 参考资料

1、JavaScript 中 apply 、call 的详解

https://github.com/lin-xin/blog/issues/7