---
title: qt之小熊猫IDE分析
date: 2022-12-29 19:33:51
tags:
	- qt

---

--

参考这个说明：

https://github.com/royqh1979/RedPanda-CPP/blob/master/BUILD_cn.md

从这里下载压缩包，放到ubuntu下面：

https://github.com/royqh1979/RedPanda-CPP

安装这些依赖：

```
sudo apt install qtbase5-dev qttools5-dev-tools  libicu-dev libqt5svg5-dev  git qterminal
```

```
cd RedPanda-CPP/
qmake Red_Panda_CPP.pro 
make -j8
sudo make install
```

RedPandaIDE\main.cpp 这个是入口文件。