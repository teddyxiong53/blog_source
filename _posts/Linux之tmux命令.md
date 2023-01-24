---
title: Linux之tmux命令
date: 2020-01-16 15:52:19
tags:
	- Linux
---

1

Tmux 是一个终端复用器（terminal multiplexer），非常有用，属于常用的开发工具。

命令行的典型使用方式是，

打开一个终端窗口（terminal window，以下简称"窗口"），

在里面输入命令。

**用户与计算机的这种临时的交互，称为一次"会话"（session）** 。



会话的一个重要特点是，

窗口与其中启动的进程是[连在一起](https://www.ruanyifeng.com/blog/2016/02/linux-daemon.html)的。

打开窗口，会话开始；关闭窗口，会话结束，

会话内部的进程也会随之终止，不管有没有运行完。



一个典型的例子就是，[SSH 登录](https://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html)远程计算机，打开一个远程窗口执行命令。

这时，网络突然断线，再次登录的时候，是找不回上一次执行的命令的。

因为上一次 SSH 会话已经终止了，里面的进程也随之消失了。



**为了解决这个问题，会话与窗口可以"解绑"：**

窗口关闭时，会话并不终止，而是继续运行，等到以后需要的时候，再让会话"绑定"其他窗口。



**Tmux 就是会话与窗口的"解绑"工具，将它们彻底分离。**

（1）它允许在单个窗口中，同时访问多个会话。这对于同时运行多个命令行程序很有用。

（2） 它可以让新窗口"接入"已经存在的会话。

（3）它允许每个会话有多个连接窗口，因此可以多人实时共享会话。

（4）它还支持窗口任意的垂直和水平拆分。



类似的终端复用器还有 GNU Screen。Tmux 与它功能相似，但是更易用，也更强大。

# 安装、进入和退出

安装

```
sudo apt-get install tmux
```

进入：

```
tmux
```

退出：

```
按ctrl+d
或者输入exit
```

# 前缀键

Tmux 窗口有大量的快捷键。所有快捷键都要通过前缀键唤起。默认的前缀键是`Ctrl+b`，即先按下`Ctrl+b`，快捷键才会生效。

举例来说，帮助命令的快捷键是`Ctrl+b ?`。它的用法是，在 Tmux 窗口中，先按下`Ctrl+b`，再按下`?`，就会显示帮助信息。

然后，按下 ESC 键或`q`键，就可以退出帮助。

# 实际操作

按照这个来做。

https://www.bilibili.com/video/BV1ab411J7xT/

## 先看window的。

```
在按了前缀键后，
输入：
c 表示create window
& 表示close window
l 切换到last window
n 下一个window
p 上一个window
w 查看window list
```

## 再看pane窗格

```
按了前缀键后
按
% 左右划分（记忆就是5是在键盘中间的位置）
" 上下划分

x 关闭当前窗格。
; 切换到last pane
o 逆时针切换所有的pane
C-o 顺时针切换所有的pane。

pane最大化和还原，
都是z键，z表示zoom。
```

有了window和pane的就够用。

然后conf和session的保存，看后面的。配置后一次就不用管了。

## 一个我的典型工作流演示

以flask-vue-crud为例

```
2个window。
先tmux启动。
这个时候还是最简单的初始情况。
然后在window1开始，
在server目录下，新建一个pane。
然后左右切换，把右边的再上下切分。
上面是client的npm run serve
下面是client的npm run lint。

window1的就配置完了。
然后是window2的。
这个window用来做vim编辑。

window都配置好了。然后要保存。
保存就是先ctrl+b，然后按ctrl+s就保存了。
可以看到状态栏有提示。

把直接把shell窗口关闭。
在tmux启动。
然后按ctrl+b，再按ctrl+r，就恢复了现场。
连vim的编辑状态都是保存好的。
所有vim的保存是可以不做的了。

```

保存的信息是在.tmux/resurrect/last里。是这样的一些文本内容。

```
pane    0       0       1       :*      0       :/mnt/fileroot/hanliang.xiong/work/test/flask-vue-crud  1     vi       :vi .
pane    0       1       0       :-      0       :/mnt/fileroot/hanliang.xiong/work/test/flask-vue-crud/server python   :python app.py
pane    0       1       0       :-      1       :/mnt/fileroot/hanliang.xiong/work/test/flask-vue-crud/client npm      :npm run serve
pane    0       1       0       :-      2       :/mnt/fileroot/hanliang.xiong/work/test/flask-vue-crud/client bash     :
window  0       0       :vi     1       :*      b33d,111x23,0,0,0       :
window  0       1       :npm    0       :-      8fed,111x23,0,0{55x23,0,0,1,55x23,56,0[55x11,56,0,5,55x11,56,12,6]}    :
state   0
```



# .tmux.conf配置

可以在这里面配置按键mapping的。

# 会话管理

第一个启动的 Tmux 窗口，编号是`0`，第二个窗口的编号是`1`，以此类推。这些窗口对应的会话，就是 0 号会话、1 号会话。

使用编号区分会话，不太直观，更好的方法是为会话起名。



# 最简单的操作流程

综上所述，以下是 Tmux 的最简操作流程。

> 1. 新建会话`tmux new -s my_session`。
> 2. 在 Tmux 窗口运行所需的程序。
> 3. 按下快捷键`Ctrl+b d`将会话分离。
> 4. 下次使用时，重新连接到会话`tmux attach-session -t my_session`。



# pane操作

Tmux 可以将窗口分成多个窗格（pane），每个窗格运行不同的命令。以下命令都是在 Tmux 窗口中执行。



# 保存回复环境

一般就一个session里创建多个window。

先启动tmux。默认就一个session。我们可以给session改名，相当于创建一个project。prefix+$，是进行改变的，我们改成test_tmux。

然后命令行tmux ls，可以查看到：

```
test_tmux: 1 windows 
```



然后prefix+c，表示创建一个window。（prefix表示前缀键，默认是ctrl+b）

现在就有了2个window。

查看当前的window：prefix + w。然后按数字选择对应的window。

这个效果就可以跟开多个tab的效果类似了。切换更方便一些。

快捷切换：prefix+p，上一个，prefix+n下一个。

怎么保存session呢？



在日常开发中，我们可能需要同时打开好几个项目，

这时我们就可以使用tmux建立对应的几个窗口，

每个窗口对应不同的项目。

同时，每个窗口可以划分了不同的窗格，

一个窗格用于在编译目录下进行编译，

一个窗格用于在生成执行文件的路劲下进行测试，

一个窗格用于编辑代码，

并且有些窗口有设置了不同的环境变量。

但是一旦关机，tmux的这个会话就没有了。

然后再想恢复的话就需要耗费一些时间。

可以采用下面的方法永久保存会话。

```
$ mkdir ~/.tmux
$ cd ~/.tmux
$ git clone https://github.com/tmux-plugins/tmux-resurrect.git
```

然后创建~/.tmux.conf文件，在里面写入下面这句：

```
run-shell ~/.tmux/tmux-resurrect/resurrect.tmux
```

然后执行：

```
$ tmux source-file ~/.tmux.conf
```

然后保存会话：prefix，然后ctrl+s。就是保存会话。

然后我们退出tmux。

tmux a查看一下，当前没有session。

我们直接输入tmux进入到tmux。

然后输入：prefix+ctrl+r，恢复session。

就可以看到恢复我们退出之前的状态了。



会话我基本没有改动默认配置，因为我一般不会遇到需要操作多个会话的情况。

一个windows里，一般给2个pane吧。

水平分割：prefix + "

垂直分割：prefix + %

# pane的最大化和恢复

prefix + z就可以。

# 参考资料

1、Tmux 使用教程

https://www.ruanyifeng.com/blog/2019/10/tmux.html

2、

https://kxcblog.com/post/terminal/2.tmux-tutorial/

3、

https://mapan1984.github.io/tool/2018/03/10/tmux-tips

4、tmux关机永久保存会话

https://blog.csdn.net/daxiang10m/article/details/106440226

5、

https://www.jianshu.com/p/ccac114c522e

6、

这篇不错。

https://reishin.me/tmux/