---
title: electron之api例子分析
date: 2019-01-05 15:29:36
tags:
	- electron

---



地址在这里。

https://github.com/hokein/electron-sample-apps

运行方法：

先全局安装electron。

```
npm install -g electron
```

进入到目录，运行例子。

```
electron xx
```

# 

# main process模块

### app对象

在 Electron 应用的主进程中，`app` 对象是一个很重要的对象，它包含了许多方法，用于控制应用的生命周期、管理应用窗口、处理系统事件等。以下是 `app` 对象的一些主要方法：

1. **app.on(event, callback)**：
   - 用于监听各种应用生命周期事件，如应用启动、退出、激活等。
   - `event` 是一个字符串，表示要监听的事件类型，如 `'ready'`、`'window-all-closed'` 等。
   - `callback` 是一个回调函数，当事件触发时会被调用。

2. **app.quit()**：
   - 用于退出应用程序。
   - 调用该方法会触发 `'before-quit'` 和 `'will-quit'` 事件，并最终退出应用。

3. **app.exit(exitCode)**：
   - 用于立即退出应用程序，并可指定退出码。
   - `exitCode` 是一个整数，表示退出应用程序时的退出码。

4. **app.getPath(name)**：
   - 获取特定系统路径，如应用数据目录、用户桌面目录等。
   - `name` 是一个字符串，表示要获取的路径类型，如 `'userData'`、`'desktop'` 等。

5. **app.setAppUserModelId(id)**：
   - 设置应用的用户模型 ID，用于 Windows 平台的任务栏分组和通知显示。
   - `id` 是一个字符串，表示应用的用户模型 ID。

6. **app.isReady()**：
   - 检查应用是否已经准备好可以创建浏览器窗口。
   - 返回一个布尔值，表示应用是否已经准备就绪。

7. **app.whenReady()**：
   - 返回一个 Promise，在应用已准备好可以创建浏览器窗口时解析。
   - 可以使用 `await` 或 `.then()` 方法等来等待应用准备好后执行相应的操作。

8. **app.requestSingleInstanceLock()**：
   - 尝试获取单实例锁，用于确保应用只有一个实例在运行。
   - 返回一个布尔值，表示是否成功获取到单实例锁。

9. **app.releaseSingleInstanceLock()**：
   - 释放单实例锁，允许其他实例运行。

10. **app.allowRendererProcessReuse([reuse])**：
    - 控制是否允许渲染进程复用，默认为 `true`。
    - 设置为 `false` 可以在每次创建新的渲染进程时强制重新启动该进程。

以上是 `app` 对象的一些常用方法，通过这些方法可以控制 Electron 应用的各种行为和生命周期。



在 Electron 中，`app` 对象的类是 `App`，它是 Electron 提供的一个核心类，用于控制应用的生命周期、管理应用窗口、处理系统事件等。`App` 类提供了许多方法和事件，可以让开发者方便地管理应用的行为和状态。

在 Electron 应用的主进程中，通常通过以下方式来使用 `App` 类：

```javascript
const { app } = require('electron');

// 监听应用准备就绪事件
app.on('ready', () => {
  // 应用准备就绪后的操作
});

// 监听窗口关闭事件
app.on('window-all-closed', () => {
  // 所有窗口关闭时的操作
  // 在 macOS 中，通常不会退出应用，而是保持运行状态
});

// 监听应用激活事件
app.on('activate', () => {
  // 应用被激活时的操作
});
```

通过 `require('electron')` 引入 Electron 模块后，可以直接访问到 `app` 对象的实例，从而调用 `App` 类提供的方法和监听事件。

总之，`App` 类是 Electron 中负责管理应用生命周期的核心类，开发者可以利用它来控制应用的行为，并根据不同的生命周期事件执行相应的操作。

#### app对象的各种event

都是字符串，xx-yy这种横杠连接的格式。

## autoUpdater

`autoUpdater` 是一个 EventEmitter。

目前仅支持 macOS 和 Windows。 Linux 上没有对自动更新程序的内置支持，因此建议使用发行版的包管理器来更新您的应用程序。

在 Windows 上，您必须先将应用程序安装到用户的计算机中，然后才能使用 `autoUpdater` ，因此建议您使用 electro-winstaller、Electron Forge 或 grunt-electron-installer 包来生成Windows 安装程序。

## BaseWindow

注意 `BaseWindow` 提供了一种在单个窗口中组合多个 Web 视图的灵活方法。

例如有左边和右边的窗口的情况。

对于只有一个全尺寸 Web 视图的窗口， `BrowserWindow` 类可能是一个更简单的选项。

在发出 `app` 模块的 `ready` 事件之前，无法使用该模块。

还可以父子窗口

```
const { BaseWindow } = require('electron')

const parent = new BaseWindow()
const child = new BaseWindow({ parent })
```

模态窗口是禁用父窗口的子窗口。

要创建模式窗口，您必须设置 `parent` 和 `modal` 选项：

```
const { BaseWindow } = require('electron')

const parent = new BaseWindow()
const child = new BaseWindow({ parent, modal: true })
```

## BrowserWindow 

`BrowserWindow` 类公开了修改应用程序窗口的外观和行为的各种方法。

通过使用 `parent` 选项，您可以创建子窗口：

```js
const { BrowserWindow } = require('electron')

const top = new BrowserWindow()
const child = new BrowserWindow({ parent: top })
child.show()
top.show()
```

模态窗口是禁用父窗口的子窗口。要创建模式窗口，您必须设置 `parent` 和 `modal` 选项：

```js
const { BrowserWindow } = require('electron')

const top = new BrowserWindow()
const child = new BrowserWindow({ parent: top, modal: true, show: false })
child.loadURL('https://github.com')
child.once('ready-to-show', () => {
  child.show()
})
```

## clipboard 

## ipcMain

## Menu

# Render process module

## contextBridge

## ipcRenderer

