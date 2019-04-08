---
title: java之IntDef注解
date: 2019-04-08 14:05:30
tags:
	- java

---



IntDef这个注解是为了解决什么问题？

假设我们要定义一个weekday变量，要限制它的值只能是星期一到星期天。

最简单的写法。

```
public class Test {
    public static final SUNDAY = 0;
    //...
    public int weekday = SUNDAY;
}
```

这种写法有什么问题？

我们可以给weekday赋值任意int值。

怎么解决这个问题？

用枚举。

枚举写法

```
public class Test {
    public enum Weekday {
        SUNDAY,
    }
    private Weekday weekday = SUNDAY;
}
```

这种写法在普通的java代码里，是没有问题的。

但是Android上有的不妥。

一个枚举是一个类，会多占用内存。

所以Android用注解来做代码检查，还是用int类型。

具体操作如下：

```
public class MainActivity extends Activity {
    public static final SUNDAY = 0;
    //..
    @IntDef({SUNDAY, MONDAY})
    @Retention(RetentionPolicy.SOURCE)
    public @interface Weekday {}
    
    @Weekday int weekday = SUNDAY;
}
```

为了使用这个注解，你需要引入对应的支持包。

```
com.android.support:support-annotations
```



参考资料

1、Java 枚举和 Android IntDef/StringDef 注解

https://www.kancloud.cn/zhangzihao/articles/325612