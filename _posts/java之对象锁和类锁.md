---
title: java之对象锁和类锁
date: 2019-04-03 10:30:04
tags:
	- java
---



什么是对象锁？

就是对普通方法加syncronized修饰。

什么是类锁？

就是对static方法加syncronized修饰。



```
import java.util.concurrent.atomic.AtomicInteger;
 
public class MyThread extends Thread{
	
	private int count = 5 ;
	
	public void run(){
	/*public synchronized void run(){*/
		count--;
		System.out.println(this.currentThread().getName() + " count = "+ count);
	}
	
	public static void main(String[] args) {
		
		MyThread myThread = new MyThread();
		Thread t1 = new Thread(myThread,"t1");
		Thread t2 = new Thread(myThread,"t2");
		Thread t3 = new Thread(myThread,"t3");
		Thread t4 = new Thread(myThread,"t4");
		Thread t5 = new Thread(myThread,"t5");
		t1.start();
		t2.start();
		t3.start();
		t4.start();
		t5.start();
	}
}
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/java $ java MyThread          
t1 count = 4
t5 count = 0
t4 count = 1
t3 count = 2
t2 count = 3
```

并不是预期的依次打印4到0 。

我们把run函数加上syncronized修饰。

再运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/java $ java MyThread
t1 count = 4
t2 count = 3
t3 count = 2
t4 count = 1
t5 count = 0
```

就符合预期了。

上面的情况是多个线程一把锁。

还有多个线程多个锁的情况。



```
public class MultiThread {
 
	private int num = 0;
	
	//不存在锁竞争，因为t1获取的是m1对象的锁，t2获取的是m2对象的锁，各自执行代码体内容互不影响
	public synchronized void printNum(String tag){
		try {
			
			if(tag.equals("a")){
				num = 100;
				System.out.println("tag a, set num over!");
				Thread.sleep(1000);
			} else {
				num = 200;
				System.out.println("tag b, set num over!");
			}
			
			System.out.println("tag " + tag + ", num = " + num);
			
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		
		//2个对象
		final MultiThread m1 = new MultiThread();
		final MultiThread m2 = new MultiThread();
		
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				m1.printNum("a");//使用m1对象
			}
		});
		
		Thread t2 = new Thread(new Runnable() {
			@Override 
			public void run() {
				m2.printNum("b");//使用m2对象
			}
		});		
		
		t1.start();
		t2.start();
	}
}
```



参考资料

1、类锁 、对象锁探究

https://www.jianshu.com/p/f68a5f803f1f

2、java 对象锁和类锁的区别

https://blog.csdn.net/feiduclear_up/article/details/78019526

3、多个线程一个锁+多个线程多个锁+对象锁的同步和异步

https://blog.csdn.net/qiushisoftware/article/details/79103702