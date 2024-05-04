---
title: windows之win10
date: 2024-04-24 14:29:17
tags:
	- windows

---

--

# win10的系统build号版本对应的细分版本

Windows 10系统的Build号版本对应的细分版本通常指的是Windows 10的主要更新版本。每次Windows 10发布主要更新时，都会引入一系列新功能、改进和修复。以下是一些常见的Windows 10 Build号版本及其对应的主要更新版本：

1. **Build 1507**: 初始发布版本，也称为Windows 10的第一版。
2. **Build 1511**: 2015年11月更新 (November Update)。
3. **Build 1607**: 2016年7月更新 (Anniversary Update)。
4. **Build 1703**: 2017年3月更新 (Creators Update)。
5. **Build 1709**: 2017年9月更新 (Fall Creators Update)。
6. **Build 1803**: 2018年4月更新 (April 2018 Update)。
7. **Build 1809**: 2018年10月更新 (October 2018 Update)。
8. **Build 1903**: 2019年5月更新 (May 2019 Update)。
9. **Build 1909**: 2019年11月更新 (November 2019 Update)。
10. **Build 2004**: 2020年5月更新 (May 2020 Update)。
11. **Build 20H2**: 2020年10月更新 (October 2020 Update)。
12. **Build 21H1**: 2021年5月更新 (May 2021 Update)。
13. **Build 21H2**: 2021年10月更新 (October 2021 Update)。

每个主要更新版本都会带来一些新功能、性能改进和安全更新，因此保持系统更新至最新版本是很重要的。您可以通过“设置”应用程序中的“更新和安全”部分来检查和安装最新的Windows 10更新。

# build号里的H字母是什么意思

在Windows 10的Build号中，H字母代表"Half-year"（半年），指示该版本是按半年更新的。

Microsoft通常在每年的4月和10月发布Windows 10的主要更新版本。

这些版本的命名惯例通常是以年份和半年（"H1"代表上半年，"H2"代表下半年）来命名。

因此，"20H2"代表2020年下半年发布的更新，"21H1"代表2021年上半年发布的更新，以此类推。

这样的命名方式有助于用户识别并了解他们所安装的Windows 10版本是哪一年的哪个半年发布的。

# AppData目录说明

AppData目录是Windows操作系统中存储应用程序数据的目录之一。它通常位于用户个人文件夹中，并包含三个子目录：Local、Roaming和LocalLow。

1. **Local**: 这个目录存储了==特定于计算机的应用程序数据==。这意味着这些数据是不可跨计算机移植的，通常包含一些比较大的文件，比如缓存文件等。这些数据只能在当前计算机上的当前用户下使用。

2. **Roaming**: 这个目录存储了用户特定的配置文件和数据，==这些数据会在用户在不同计算机上登录时自动同步。这使得用户可以在不同计算机上使用同样的配置和数据。==

3. **LocalLow**: 这个目录存储了与Local类似的数据，但通常是一些低权限或者安全性要求较低的应用程序使用的数据。==这些数据通常不被同步，也不会影响到其他用户。==

这些目录允许应用程序在不同的环境下存储数据，同时也确保了数据的安全性和隔离性。这对于多用户环境或者用户在不同计算机上使用相同应用程序时都是非常有用的。

# Windows上的WebView2

Windows上的WebView2是一个嵌入式Web浏览器控件，它使用Microsoft Edge浏览器内核来呈现网页内容。WebView2允许开发人员在其应用程序中嵌入现代的Web内容，提供了更强大的Web浏览和互动体验。

以下是关于WebView2的一些关键点：

1. **基于Chromium**: WebView2基于Chromium开源项目，这意味着它与Microsoft Edge浏览器内核相同。这使得WebView2能够支持现代的Web标准和技术，并提供高性能和兼容性。

2. **功能丰富**: WebView2支持HTML、CSS、JavaScript等Web技术，还提供了与浏览器类似的功能，如Cookies、Web存储、JavaScript交互等。

3. **可定制性**: 开发人员可以通过设置各种参数来定制WebView2的行为和外观，例如启用或禁用特定功能、设置浏览器代理等。

4. **集成性**: WebView2可以轻松地嵌入到Windows应用程序中，无论是使用.NET、Win32、或者其他框架进行开发，都可以方便地使用WebView2控件。

5. **跨平台**: 虽然WebView2目前主要针对Windows平台，但微软也在不断努力将其扩展到其他平台，例如.NET MAUI和Electron等。

WebView2为开发人员提供了一种强大的工具，使他们能够在其应用程序中集成现代的Web内容，从而提供更丰富、更交互的用户体验。

# 命令行安装软件

winget：我的电脑上工作不正常。

chocolatey：这个是基于NuGet的工具。

https://chocolatey.org/

https://blog.csdn.net/qq_39609993/article/details/120710357