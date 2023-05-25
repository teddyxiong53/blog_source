---
title: repo工具使用
date: 2018-10-11 10:34:51
tags:
	- 工具

---



repo是谷歌开发的，用来管理Android代码的工具，是用Python对git进行了包装的工具。

简化了对多个git版本库的管理。

repo的使用流程是这样的：

1、初始化。基于xml文件。./repo/manifest.xml。

```
repo init
```

2、repo sync。

同步项目里的某一个部分，

repo sync xxx。



git也带了submodule，也是可以管理多个工程的。

为什么不用呢？

因为git的submodule有很多的坑。难以管理复杂的工程。

需要repo管理的，都是多个开源项目集合起来的。



# 服务器搭建

新建repo目录，下面新建repo_client和repo_server这2个子目录。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo$ tree -L 1
.
├── repo_client
└── repo_server
```

## repo_server

目录结构如下：

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_server$ tree
.
├── manifest.git
│   └── default.xml
├── pro1
│   └── 1.txt
└── pro2
    └── 2.txt
```

过程：

```
mkdir manifest.git
git init
touch default.xml
```

default.xml内容：

```
<?xml version="1.0" ?>
<manifest>
	<remote name="repo_server" fetch="/home/hlxiong/work/test/repo/repo_server" />
	<default revision="master" remote="repo_server" />
	<project name="pro1" path="pro1" />
	<project name="pro2" path="pro2" />
</manifest>
```

然后

```
git add .
git commit -m "add default.xml"
```

pro1和pro2这2个目录也都是git目录。进行git init和git commit。

这样，server端就搭建好了。

## repo_client

先执行repo init，是为了下载repo工具。

```
repo init 
```

得到.repo目录。

```
修改里面的.repo/repo/repo
```

把url修改一下：

```
REPO_URL = "/home/hlxiong/work/test/repo/repo_server"
```

然后，新建一个软连接。

```
repo -> .repo/repo/repo
```

执行

```
./repo init -u /home/hlxiong/work/test/repo/repo_server/manifest.git
```

然后执行

```
./repo sync
```

就可以了。



# 实验

基于上面搭建的环境，进行常用命令的学习。

repo_client下的.repo目录内容：

```
manifests
manifests.git
manifest.xml -> manifests/default.xml
project.list
	这个里面就2行，写着pro1和pro2 。
project-objects
projects
	这个下面有pro1.git和pro2.git目录。
repo
```



## repo info

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_client$ ./repo info
Manifest branch: master
Manifest merge branch: refs/heads/master
Manifest groups: all,-notdefault
----------------------------
Project: pro1
Mount path: /home/hlxiong/work/test/repo/repo_client/pro1
Current revision: master
Local Branches: 0
----------------------------
Project: pro2
Mount path: /home/hlxiong/work/test/repo/repo_client/pro2
Current revision: master
Local Branches: 0
----------------------------
```



我到pro1目录下，修改1.txt。

然后这么把这个修改提交呢？

repo status可以看到变化。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_client$ ./repo status
project pro1/                                   (*** NO BRANCH ***)
 M-     1.txt
```

repo diff也可以看到，更加详细一点。

## repo list

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_client$ ./repo list
pro1 : pro1
pro2 : pro2
```





# 提交上传代码

如果本地代码有修改，需要提交上传。

1、先到对应的project目录下，git commit。

2、repo upload进行上传。如果远程git仓库，你有可写权限，也可以直接在git目录下push就行了。





# repo init

有这些常用选项：

```
-u
	u表示url。后面跟的是一个manifest-url。
	表示仓库的地址。其实就是一个default.xml的位置。
-b
	只取某个分支或者版本。
-m
	指定一个xml文件名字。使用指定的这个manifest xml文件，而不是默认的default.xml文件。
	
```

如果已经repo init过一次，然后再repo init -m xx.xml，相当于把.repo/manifest.xml里的include的文件，替换为xx.xml文件。

如果还没有同步过，repo init等价于：

```
git clone
```

如果已经同步过，那么repo sync等价于：

```
git remote update
git rebase origin/<branch>
```

# repo upload

后面可以跟project的名字。

不带的话，就是提交所有的project。



# repo源代码分析

repo就是一个900行的python脚本。



整个工作过程是：

1、先通过wget工具，下载得到一个repo脚本。我们把这个脚本放入到PATH路径下。

2、用repo工具来安装一个repo仓库。

```
repo init -u http://xx/manifest
```

这个命令实际上包含了2个操作：安装repo仓库和manifest仓库。

我们看看repo脚本是如何执行repo init命令的。

每个命令都是这种格式：cmd opt  args

```
def main(orig_args):
  cmd, opt, args = _ParseArguments(orig_args)
```

_FindRepo函数，从当前目录开始往上找，直到根目录停止。如果中间某个目录存在一个.repo/repo目录。且这个目录下有一个main.py文件。

那么就会认为当前目录是aosp目录。



当前我们执行repo init的时候：

1、如果我们只是从网上下载了一个repo脚本，那么在执行repo命令的时候，就会从远程仓库clone一个repo仓库到当前目录来。

2、如果我们从网上下载的是一个带有repo仓库的repo叫本能，那么执行repo命令的时候，就会从本地clone一个repo仓库到当前目录。



如果我们执行repo脚本的时候，没有指定`--repo-url`和`--repo-branch`这2个参数。

那么就使用REPO_URL和REPO_REV。这个默认是

REPO_URL=https://gerrit.googlesource.com/git-repo

REPO_REV=stable



首先用git init在当前目录下的.repo/repo目录下初始化一个仓库。然后调用_SetConfig函数来设置git仓库的url等信息。

bundle文件是git提供的一种机制，用来解决不能正常通过git协议、ssh协议，http协议这些协议来clone的问题。

把整个仓库打包成一个bundle文件，直接拷贝到其他的电脑上可以用。



当repo init命令完成了repo仓库的安装之，就会调用main.py文件，

repo命令的子命令，都在.repo/repo/subcmds目录下。一个文件对应一个命令。



xml_manifest.py 这个对应的就是manifest.xml文件的对象。



# manifest.xml文件语法

## manifest元素

这个是根节点。

## remote元素

可以指定多个remote元素。不过一般就一个。

每个remote元素代表了一个git url。这个url被多个project共享。

属性：

```
name：
	一个short name。在本文件里要唯一。
	在各个project里，用这个name作为remote 的名字。在.git/config里有。
	因此，在git fetch/remote/pull/push这些命令可以直接使用这个name。
	
alias
	这个可以没有，如果有的话，就会覆盖name属性，在.git/config里使用。
	alias可以多个project相同。而name必须唯一。
	
fetch
	这个是git url prefix。加在所有的project前面。
	每个project的name前面都会自动加上这个fetch的值，构成最后的url。
	在clone的时候用。
pushurl
	这个也是git url prefix，在git push的时候用。
	这个是可选的，默认是跟fetch的一样。
	
review
	repo upload的时候，上传到的gerrit server的名字。
	这个属性可选，如果没有，那么repo upload没有作用。
	
revision
	这个是一个git branch的名字。例如master或者refs/heads/master。
	
```

## default元素

最多只能有一个default元素。作用就是对所有的project设置一些全局参数。project不单独设置，则默认使用default里的属性。

default元素的remote属性和revision属性，对于那些没有指定这2个属性的project都有效。

属性：

```
remote
	就是上面的那个remote元素的名字。如果project不单独指定remote，那么默认就是用这个remote。
revision
	git branch的名字。
dest-branch
	默认跟revision的一致。一般也不设置。
upstream
	一个git ref的名字。
sync-j
	sync的任务数，一般是4 。
sync-c
	bool类型。如果设置为true，那么只同步指定的git 分支。而不是整个ref space。
sync-s
	如果设置为true，也同步sub-projects。
	
```

## manifest-server元素

这个一般不设置。

## project元素

project是主要的内容。repo就是管理多个project的。

每一个project代表了一个git 仓库，你可以指定git-submodules来创建嵌套的project。

属性

```
name
	一个unique的名字。
	实际是一个路径。
	使用的时候，会被补全到fetch url后面。
	
path
	一个可选的属性。
	表示project取下来放在的目录，从当前路径开始的相对路径。
	
```

一般就用上面2个属性就够了。

## copy-file元素

是project的子元素。

描述了一个拷贝文件的行为。

有2个属性，一个是dest，一个src。

## link-file元素

也是project的子元素。

描述了一个建立软链接的行为。

## remove-project

这个用得少。

## include元素

这个就是包含其他的xml文件。就一个name属性。描述xml文件的位置。



# 固定版本

要发布的时候，需要把当前的版本固定下来。

这样的形式。

```
<project name="amlogic/tools/system_control" path="vendor/amlogic/system_control" revision="e9091be789ca740f62c53009e694ab2c39d8bd04" upstream="master"/>
```

有没有现成的命令？

有，这样就可以。

```
repo manifest -r -o 20170120.xml
```

# 问题解决

## cherry-pick问题

报错

```
project buildroot/
fatal: You have not concluded your cherry-pick (CHERRY_PICK_HEAD exists).
Please, commit your changes before you merge.

error: Cannot checkout linux/buildroot
Updating files: 100% (5016/5016), done.
```

原因是我在buildroot下进行过cherry-pick的操作。

解决方法：

```
git cherry-pick --abort 
```

然后再repo sync就好了。

参考资料

https://blog.csdn.net/qq_40147863/article/details/98647068

## remotes/m/master->xx

这个的箭头具体的内涵是什么？

remotes/m/android-4.2.2_r1.2 -> refs/tags/android-4.2.2_r1.2

所有以remotes/aosp/开头的分支都很好理解。就是在真正的远程服务器aosp上的库里，存在着对应的分支。

有一个分支名称看起来很奇怪：remotes/m/android-4.2.2_r1.2

更奇怪的是这个分支的名称后面还有一个箭头，指向另外一个名称。

那么这个remotes/m/android-4.2.2_r1.2 -> refs/tags/android-4.2.2_r1.2到底是什么意思呢？



其实并不神秘，首先看remotes/m/android-4.2.2_r1.2，

这个就是一个repo的清单库的分支，也就是当你在执行repo init -U [URL] -b [branch_name]的时候，-b参数后面的分支。

如果你repo init的时候，没有指定过-b参数。

那么这里就会显示remotes/m/master。

那么这个箭头后面的refs/tags/android-4.2.2_r1.2是什么呢？

它就是在清单库里的default.xml里面指定的单个git库的revision值。

需要说明的一点是，这个是repo工具自己添加的一个ref，只是利用了git的机制显示了出来。



那么repo工具添加这个功能有什么用呢？其实就是为了让用户方便的知道自己目前工作在清单库的哪个分支上。当前的清单库的这个分支又引用了当前git库的哪个branch/tag上。



## fatal: couldn't find remote ref refs/heads/master

```
这样的，是不能指定master分支的。
remotes/m/master -> amlogic/m-amlogic
这样的，才能使用默认的master分支。
remotes/m/master -> amlogic/master
```

这个在文件里的体现就是

```
hanliang.xiong@walle01-sz:~/work/soundbar/code/vendor/amlogic/tdk/.git/refs/remotes$ tree
.
├── amlogic
│   ├── openlinux
│   │   ├── ott
│   │   │   ├── q-amlogic
│   │   │   ├── r-amlogic
│   │   │   ├── r-amlogic-v3
│   │   │   └── r-amlogic-v3-20210130
│   │   └── tv
│   │       └── p-amlogic-20190219
│   ├── p-amlogic-hailstorm-2.1
│   ├── projects
│   │   └── openlinux
│   │       └── bl-2.2.0
│   ├── tdk-v2.4.4
│   └── tdk-v3.8.0
└── m
    └── master

7 directories, 10 files
hanliang.xiong@walle01-sz:~/work/soundbar/code/vendor/amlogic/tdk/.git/refs/remotes$ cat m/master 
ref: refs/remotes/amlogic/tdk-v2.4.4
```



参考资料

https://blog.csdn.net/u013377887/article/details/107517060



# repo加速

现在很多企业的网络一般都比较快, 

但是有的企业却会限速,

 如果需要从github和google code上面git clone大的仓库的话, 

那么需要耗费的时间是很可观的,  

例如从github或者google code, 

或者其他托管服务站点获取Android中需要的多个Kernel仓库, 

一般一个kernel仓库都有几GB, 如果是100KB/S的话, 那么将需要很长的时间.



与此同时, 不同的Android 版本(AOSP)代码, 

他们一般都会依赖许多相同的组件, 

甚至获取相同的仓库代码, 仅仅只是branch或者tag不同而已, 

例如对于Nexus 7 flo平板而言, 

不管是AOSP 4.4 Kitkat还是 5.X Lolipop, 

都会去下载flo-kernel这个内核, 

他们都remote都是一样的, 

唯一不同的是tag使用的不同, 

因此如果我们已经获取过Kitkat的代码,那么就可以复用其中的bare repo, 

从而达到快速clone.



要了解如何做, 我们需要对AOSP的代码结构非常熟悉,

 一般而言, 如果是系统工程师,那么几乎对AOSP的每一个目录都会很熟悉, 

对自己需要编译的target的依赖的每一个repo都几乎会心中有数(例如external中的哪些, vendor, device都会用到哪些), 

这种情况下, 就可以删除某些仓库的下载, 从而节省时间.



总结起来, 要节省git clone的时间就是从两个方面入手:



- \1. 复用已经clone的bare repo
- \2. 不要clone不需要的repo



repo分析

在实现前面的两点之前, 除了对AOSP的编译, 以及Target的依赖很熟悉外,

 我们还需要对google 的 repo工具以及其流程有个基本的熟悉和了解.

repo的执行过程

解析传入的args
checkout下来最新的repo
找到manifest的目录
解析manifest.xml
根据manifest或者其他xml文件调用git clone --bare-repo获取xml中定义的clone repo
从.repo/projects中的bare repo根据manifest xml中的projects信息checkout到当前目录

具体查看repo这个python脚本的源码.

下面使用具体例子来讲解.

repo init



repo本身的checkout



在repo init执行的时候会到: https://gerrit.googlesource.com/git-repo

checkout最新的repo, checkout下来后放在了.repo/repo目录



指定了从fetch/name这个位置clone, 

因为repo本身会将所有的projects放到.repo/projects目录下面, 

这个存放的位置就是由后面的groups来指定的, 

例如上面的flounder-kernel的repo 本地bare repo位于:

.repo/projects/device/flounder-kernel.git

而这个repository的objects则位于:

.repo/project-objects/aosp_device_asus_flo-kernel.git/

最后xml还可以使用include来包含, 实现"重载"



了解了repo的工作过程后,我们就可以想办法来重用以前的bare repository了, 也知道如何不去clone和建立不需要的project的bare repository.



## 一种加速方法

```
repo init -u https://github.com/seL4/sel4test-manifest.git --no-clone-bundle --depth=1
repo sync --jobs=8 --fetch-submodules --current-branch --no-clone-bundle
```

`--depth=1` 表示只下载最近版本的代码，只保留最近的commit版本。

使用`--depth` 可以节省本地磁盘空间，加速下载，对于开发够用了。

```
repo sync -c -f --no-tags --no-clone-bundle -j`nproc`
```

-c 或者--current-branch表示只拉取当前分支代码，坑爹啊，我在init指定了分支，同步的时候，你却悄悄给我拉些没用的。

--no-tags 不拉取tags，tag虽然不大，但架不住多

--no-clone-bundle 不使用clone.bundle，clone.bundle是git bundle一样的打包文件，使用bundle文件可以做cdn下载的分流，cdn听上去不错，**但是如果cdn到google的服务器，或者clone.bundle本来就占空间，不是很划算，**所以不使用clone.bundle

**-f 如果sync失败，继续同步（想想当年LZ写了一个while循环解决同步失败终止问题的）**
**--force-sync 如果文件目录有差异，强制覆盖掉**

 repo回滚
repo sync -d 可以将所有git 仓库的HEAD重置为manifest文件的指定版本。同时，处于暂存或者修改的目录变化不会被重置。

当然，-d 重置版本的妙用就是回滚，结合以下命令，可以让被指飞的git仓库门，全部恢复成干净的代码。

repo sync -d
repo forall -c 'git reset --hard'    # Remove all working directory (and staged) changes.
repo forall -c 'git clean -f -d'     # Clean untracked files


repo详解与如何更改manifest快速获取和复用AOSP代码

https://blog.csdn.net/sy373466062/article/details/55190634

# 自己创建仓库并进行管理

https://github.com/ZengjfOS/manifest

https://git-repo.info/zh_cn/docs/multi-repos/manifest-format/

# 参考资料

1、Repo工具的使用

https://blog.csdn.net/davidsky11/article/details/23291483

2、

https://www.zhihu.com/question/27000882

3、如何使用repo/git提交代码

https://blog.csdn.net/zhanglianyu00/article/details/56845462

4、简易repo服务器搭建

https://blog.csdn.net/eastmoon502136/article/details/72598297

5、

https://www.jianshu.com/p/9c57696165f3

6、repo: manifest.xml: What does the fetch=“..” mean?

https://stackoverflow.com/questions/18251358/repo-manifest-xml-what-does-the-fetch-mean

7、Android源代码仓库及其管理工具Repo分析

https://blog.csdn.net/Luoshengyang/article/details/18195205

8、Android中Repo 常用命令参考

https://www.jianshu.com/p/9e6097093854

9、Repo Cheatsheet

https://docs.sel4.systems/projects/buildsystem/repo-cheatsheet.html

10、manifest的xml里元素详解。

https://gerrit.googlesource.com/git-repo/+/master/docs/manifest-format.md

11、

https://blog.csdn.net/counsellor/article/details/86591081

12、

https://www.cnblogs.com/jiangxinnju/p/14274982.html