---
title: Android之上下文
date: 2019-03-30 17:43:32
tags:
	- Android
---



Android的context具体指什么东西呢？

我们在加载资源、启动一个新的Activity、获取系统服务、获取内部文件路径、创建View的时候，都需要涉及到Context。



从代码上看，Context是一个抽象类。

Activity、Service、Application，都是它的子类。

从Android系统的角度看，Context是一个场景，代表与os交互的一种过程。



在Activity里，需要用到Context的时候，一般是传递this。

在匿名内部类里，因为不能使用this，需要写XXXActivity.this。

有的人会这样写：getApplicationContext。这个写法不太正确。

Activity的Context和Application的Context，肯定还是不同的。



使用Context时需要注意的一些事情。



#引用的保持

大家在写工具类的时候，一般写成单例的。

工具类很多都需要访问资源。

也就是要用到Context。

这个时候，就需要注意Context的引用问题。

```
import android.content.Context;

public class CustomManager {
    private static CustomManager sInstance;
    private Context mContext;

    private CustomManager(Context context) {
        this.mContext = context;
    }
    public static syncronized CustomManager getInstance(Context context) {
        if(sInstance == null) {
            sInstance = new CustomManager(context);
        }
        return sInstance;
    }
    
}
```

上面代码的问题在于，Context的来源不确定，如果我们在某个Activity里，为了方便，直接传递了this。

这样就导致了这样的问题：

我们的sInstance是static的，这样只要我们的app没有退出，对应的Activity就一直不会被释放。

这个导致了内存泄露。

怎么解决这个问题呢？

这样写：

```
public static syncronized CustomManager getInstance(Context context) {
        if(sInstance == null) {
            sInstance = new CustomManager(context.getApplicationContext());//就改了这里。
        }
        return sInstance;
    }
```





参考资料

1、Android Context 上下文 你必须知道的一切

https://blog.csdn.net/lmj623565791/article/details/40481055

2、Android Context完全解析，你所不知道的Context的各种细节

https://blog.csdn.net/guolin_blog/article/details/47028975