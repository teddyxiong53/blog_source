---
title: Android之Application类
date: 2019-04-01 11:31:32
tags:
	- Android
---



在Android系统里，一个app启动时，系统就会创建一个Application对象。用来存储系统的一些信息。

一般情况下，我们不需要指定Application，系统会自动帮我们创建的。

如果要自己创建，也很简单，先继承Application类，在manifest里用application标签来注册。就是给application标签添加name属性。

启动Application的时候，系统会创建一个pid。所有的Activity都在这个pid上。

Application对象对于一个app来说，是单例的，唯一的。所有的Activity、Service都共用了一个Application。

所以可以通过Application来传递一些东西。

我们可以用Application类来实现全局变量。这种方式，比起静态工具类来说，更加有保障。



```
public class CustomApplication extends Application {
    private static final String VALUE = "xx";
    private String value;
    @Override
    public void onCreate() {
        super.onCreate();
        setValue(VALUE);
    }
    public void setValue(String value) {
        this.value = value;
    }
    public String getValue() {
        return value;
    }
}
```

主要就是重写onCreate方法。

然后我们写Activity。

```
public class FirstActivity extends Activity {
    private CustomApplication app;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        app = (CustomApplication) getApplication();
        Log.i("FirstActivity", "init value" + app.getValue());
        app.setValue("yy");
        Intent intent = new Intent();
        intent.setClass(this, SecondActivity.class);
        startActivity(intent);
    }
}
```

在SecondActivity里，也同样方法调用。





参考资料

1、Android中Application类用法

https://www.cnblogs.com/renqingping/archive/2012/10/24/Application.html