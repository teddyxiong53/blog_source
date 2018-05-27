---
title: Android之Application
date: 2018-05-27 11:46:55
tags:
	- Android

---



一般写简单的安卓应用，都是从Activity开始写。不涉及Application的。用来默认的。

但是实际上我们可以自己来实现Application。



Application是单例的。

我们在java里这样写。

```
import android.content.Context;
public class MainApplication extends Application {
    /** 
   * 全局的上下文 
   */ 
  private static Context mContext; 
  
    @Override 
  public void onCreate() { 
    superonCreate(); 
     
    mContext = getApplicationContext(); 
     
  }   
    /**获取Context 
   * @return 
   */ 
  public static Context getContext(){ 
    return mContext; 
  } 
}
```

然后在AndroidManifest.xml里加上。

```
    <application 
    android:icon="@drawable/ic_launcher" 
    android:label="@string/app_name" 
    android:name="MainApplication" > //这里。
```



# 关于Context类

字面意思是上下文。

在framework包下面的android.content.Context类。

是一个抽象类，它是实现是安卓系统来实现的。

用来允许访问一些类。

类似win32程序里的handle句柄。

在android中context可以作很多操作，但是最主要的功能是加载和访问资源。



在android中有两种context，一种是 application context，一种是activity context，通常我们在各种类和方法间传递的是activity context。
application context
我们可以使用application context。application context伴随application的一生，与activity的生命周期无关。





# 参考资料

1、谈谈Android里的Context的使用实例

http://www.jb51.net/article/97730.htm

2、对于android里面的content不理解，查找说这个是上下文，但是我还是没有这个概念，什么是上下文求大神讲解

https://zhidao.baidu.com/question/1882878459830448108.html