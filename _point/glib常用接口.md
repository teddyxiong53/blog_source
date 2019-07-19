g_main_loop_run
	会一直阻塞，直到退出。
	有事件就处理事件，没有事件就sleep。
	直到收到g_main_loop_quit调用后。
	
	
GMainLoop
	代表了一个主事件循环。
	g_main_loop_new用这个函数来创建一个GMainLoop对象。
	在添加完初始事件源之后，执行g_main_loop_run函数。
	主循环一直检查事件源产生的事件。然后分发它们。
	直到检查到触发g_main_loop_quit的事件为止（例如窗口关闭事件）。
	GMainLoop可以被递归创建。这个是对应模态对话框的情况。
	
	

	# gthread.h

thread相关

```
增
	g_thread_new
	g_thread_try_new
删
	g_thread_exit
	g_thread_join
改
	g_thread_yield
	g_thread_ref
	g_thread_unref
查
	g_thread_self
	
```

mutex相关

```
增
	g_mutex_init
删
	g_mutex_clear
改
	g_mutex_lock
	g_mutex_unlock
	g_mutex_trylock
查
```

cond相关

```
增
	g_cond_init
删
	g_cond_clear
改
	g_cond_signal
	g_cond_broadcast
查
	g_cond_wait
	g_cond_wait_until
```

once相关

```
g_once_impl
g_once_init_enter
g_once_init_leave
```

打印函数
```
g_printf
g_fprintf
g_snprintf
g_sprintf

```

