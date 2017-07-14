---
title: Android Handler
date: 2017-07-14 21:12:00
tags:

	- Android

---

Handler在Android里的主要用途是接受子线程发来的数据，并用收到的数据配合main线程（UI线程）更新UI。

# 1. Handler为什么要存在？

当一个应用启动时，Android会首先开启一个main线程（UI线程），main线程的职责是管理各个ui控件，进行事件分发。例如，你点击一个button，Android会分发事件到button上来，来响应你的操作。如果你接下来的操作是很耗时的，你就不能放在main线程里来做，这样严重影响使用体验，当main线程阻塞超过5s时，Android就会弹窗提示你是否关闭。所以这些耗时的操作，就需要另外创建线程去做，但是，Android的main线程不是线程安全的，刷新节目的工作只能由main线程来完成。

这个时候，就引入了handler这个东西。Handler运行在主线程里，它和子线程通过Message来传递数据。



# 2. Handler的特点

Handler可以分发Message对象和Runnable对象到main线程，每个Handler实例，都会绑定到main线程。

Handler有2个作用：

1、安排Message或者Runnable在main线程的某个地方执行。

2、安排一个动作在不同的线程中执行。

常用的接口有：

1、post(Runnable)

2、postAtTime(Runnable, long)

3、postDelayed(Runnable, long)

4、sendEmptyMessage(int)

5、sendMessage(Message)

6、sendMessageAtTime(Message, long)

7、sendMessageDelayed(Message, long)



# 3. 使用示例

```
public MyHandlerActivity extends Activity {
	Button button;
	MyHandler myHandler;
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.handler);
		button = (Button )findViewById(R.id.button);
		myHandler = new MyHandler();
		MyThread thread = new MyThread();
		new Thread(thread).start();
	}
	
	class MyHandler extend Handler {
		public MyHandler() {
			
		}
		public MyHandler(Looper L) {
			super(L);
		}
		@override
		public void handleMessage(Message msg) {
			super.handleMessage(msg);
			Bundle b = msg.getData();
			String color = b.getString("color");
			MyHandlerActivity.this.button.append(color);
		}
	}
	class MyThread implements Runnable {
		public void run() {
			try {
				Thread.sleep(10000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			Message msg = new Message();
			Bundle b = new Bundle();
			b.putString("color", "123");
			msg.setData(b);
			MyHandlerActivity.this.myHandler.sendMessage(msg);
		}
	}
}
```



