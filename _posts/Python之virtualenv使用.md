---
title: Python之virtualenv使用
date: 2017-10-01 18:12:43
tags:
	- Python
	- virtualenv

---



virtualenv用于创建独立的Python环境，多个Python相互独立。可以做到：

1、在没有权限的情况下安装新套件。

2、不同应用可以使用不同的套件版本。

3、套件升级不影响其他的应用。

安装方法：

```
sudo apt-get install python-virtualenv
```

使用方法：

# 1、创建一个叫my_python_env的虚拟环境

`virtualenv my_python_env`

```
pi@raspberrypi:~$ virtualenv my_python_env
New python executable in /home/pi/my_python_env/bin/python
Installing setuptools, pip, wheel...done.
```

到对应的目录下看看：

```
pi@raspberrypi:~/my_python_env$ tree -L 1
.
├── bin
├── include
├── lib
├── local
└── pip-selfcheck.json

4 directories, 1 file
pi@raspberrypi:~/my_python_env$ 
```

相当于是把系统的Python安装目录拷贝了一份。



默认情况下，虚拟环境会依赖系统里安装的site packages，如果不要用默认系统安装的第三方库，可以加上参数`no-site-packages`。

# 2、使用创建的环境

启动

```
pi@raspberrypi:~/my_python_env$ source ./bin/activate
(my_python_env) pi@raspberrypi:~/my_python_env$ 
(my_python_env) pi@raspberrypi:~/my_python_env$ 
```

查看python的位置。

```
(my_python_env) pi@raspberrypi:~$ which python
/home/pi/my_python_env/bin/python
(my_python_env) pi@raspberrypi:~$ 
```

退出：

```
(my_python_env) pi@raspberrypi:~$ deactivate 
pi@raspberrypi:~$ 
```

# 3、在虚拟环境下进行软件安装

从前面的安装过程打印可以看到，系统默认给你安装了pip，所以你可以直接用pip进行软件安装。



# 4、virtualenvwrapper

virtualenvwrapper是对virtualenv的扩展，帮助我们更方便地管理虚拟环境。可以做的事情有：

1、把所有的虚拟环境整合在一个目录下。

2、管理虚拟环境。增删改查。

3、切换虚拟环境。

## 4.1 安装

```
sudo pip install virtualenvwrapper
```

这样安装后，还不能用。需要做下面的几步。

1、在$HOME里建立一个.virtualenvs的目录，用来统一存放虚拟环境。

2、在`~/.bashrc`里增加下面的语句：

```
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

3、执行。

```
source ~/.bashrc
```

## 4.2 使用

1、新建一个虚拟环境。

可以看到创建后自动就激活了。

```
pi@raspberrypi:~$ mkvirtualenv ve1
New python executable in /home/pi/.virtualenvs/ve1/bin/python
Installing setuptools, pip, wheel...done.
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/ve1/bin/predeactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/ve1/bin/postdeactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/ve1/bin/preactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/ve1/bin/postactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/ve1/bin/get_env_details
(ve1) pi@raspberrypi:~$ 
```

2、查看当前有的虚拟环境。

```
pi@raspberrypi:~$ lsvirtualenv 
ve1
===


ve2
===
```

3、在不同虚拟环境上切换。

```
pi@raspberrypi:~$ workon ve2
(ve2) pi@raspberrypi:~$ workon ve1
(ve1) pi@raspberrypi:~$ 
(ve1) pi@raspberrypi:~$ 
```

4、退出也是用deactivate。



## 4.3 其他

mkproject等于在mkvirtualenv + 创建项目。

mkproject能够工作的前提是，在`~/.bashrc`里加上一句：

```
export PROJECT_HOME=$HOME/ve_workspace
```

这个目录是随意指定的。