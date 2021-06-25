---
title: qt之wearable例子分析
date: 2021-06-24 14:43:33
tags:
	- qt

---

--

这个例子，非常符合我的需求，所以可以作为一个典型例子来进行深入分析。

在quickcontrols2目录下。

除了一个简单的入口函数。其余的内容都是qml写的。

页面的切换关系是如何指定的？

如果要加入真实操作，例如打开蓝牙关闭蓝牙，这些操作代码如何跟界面对接起来？

很简单，qml里可以调用c++的函数。qml里可以写函数。

例如这样：

```
 //鼠标点击区域
    MouseArea{
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        //测试时点击左键或右键
        onClicked: {
            if(mouse.button===Qt.LeftButton){
                console.log('----qml 点击左键：Cpp发射信号')
                cpp_obj.name="gongjianbo"  //修改属性会触发set函数，获取值会触发get函数
                cpp_obj.year=1992
                cpp_obj.sendSignal() //调用Q_INVOKABLE宏标记的函数
            }else{
                console.log('----qml 点击右键：QML发射信号')
                root.qmlSignalA()
                root.qmlSignalB('gongjianbo',1992)
            }
        }
    }
```



参考资料

1、

https://blog.csdn.net/gongjianbo1992/article/details/87965925