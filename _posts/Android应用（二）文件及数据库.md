---
title: Android（二）文件及数据库
date: 2018-01-25 09:56:31
tags:
	- Android

---



继续在xhl_simple_view的App里面进行开发。把btn12用起来，命名为“更多”。

点击进入到一个MoreDemoActivity的界面。这里放一个ListView。每一项都可以点击。

ListView里面Item超过一页时，自动就可以支持上下滚动的。现在要实现可以点击的操作。

加上这个代码就好了。

```
listView.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
```



# SharedPreference

SharedPreference用来保存少量的数据的。而且数据的格式化是很简单的那种。

例如应用的配置信息。

数据格式是键值对。

主要的接口有：

读取类：

1、contains，是否包含某个key。

2、getAll，获取全部键值对。

3、getXXX。XXX是Int、long等类型。

写入类：写入是靠SharedPreference的内部类Editor来实现的。

1、clear。清空所有数据。

2、putXXX

3、remove。

4、commit。

##测试代码编写

1、新建一个SPDemoActivity。对应布局文件，里面就放2个按钮，一个读，一个写。另外放一个TextView，用来显示内容。

2、保存程序使用的次数。打开时显示一下。

把文件SPDemoActivity.xml导出来看看。在/data/data/com.teddxyiong53.www.xhl_simple_view目录下。

```
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <int name="count" value="3" />
    <int name="random" value="71" />
</map>
```



# 文件存储

Context提供了2个接口来对文件进入写入和读取。

1、FileInputStream openFileInput(name)

2、FileOutputStream openFileOutput(name, mode)。模式可以是private、append、world_readable等。

另外还有这么几个方法：

1、getDir(name,mode)。在应用自己的目录下，如果获取不到，就新建一个目录。

2、File getFilesDir。获取应用的绝对路径。

3、String[] fileList。返回应用目录下的所有文件。

4、deleteFile。

## 测试代码

1、提供一个读、一个写按钮。

2、提供一个EditText进入输入。一个TextView进行显示。

用GridLayout。5x5宫格的。

```
输入：2x5
写入：1x2 （中间空一格）读取 1x2
显示：2x5 
```



# 数据库

1、创建数据库。

```
db = SQLiteDatabase.openOrCreateDatabase("/mnt/db/test.db3", null);
```

2、创建表。

```
sql = "create table news(_id integer primary key, title varchar(255), content varchar(1000));
db.execSQL(sql);
```

操作数据库，你可以都写sql命令。也可以用api接口如insert这些。

## 测试代码

1、新建一个DBDemoActivity。

## sqlite3工具使用

1、我的电脑安装了sqlite3工具，如果没有安装，Android SDK包里也是有的。

2、把模拟器里的test.db3文件导出到电脑上。

3、执行下面命令：

```
$ sqlite3 test.db3
sqlite> .database
sqlite> .tables
sqlite> select * from news
1|adf|fdafdfd
2|ADC|fdafdfdfdfdf
3|jkjkj|gfgsgfgs
4|fsfg|sfgss
```

