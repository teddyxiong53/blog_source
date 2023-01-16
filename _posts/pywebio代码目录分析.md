# 目录

```
.
├── __init__.py  对外导出所有的符号。自己定义的一个符号就是enable_debug
├── __version__.py 定义版本信息。
├── exceptions.py 定义了4个Exception。都是空的。
├── input.py  加上注释一起800行。定义了10中输入控件。
├── io_ctrl.py 这个是input和output的底层实现。定义了Output这个重要的基础类。加上注释，400行。
├── output.py 加上注释1800行。重点看这个。
├── pin.py 定义了11种pin组件。不到400行。
├── platform
│   ├── __init__.py  各种import。
│   ├── adaptor
│   │   ├── __init__.py 空的。
│   │   ├── http.py 不到400行，基于http的后端。
│   │   └── ws.py  200行。
│   ├── page.py  config、make_application、seo等函数，300行。
│   ├── path_deploy.py 不到400行。
│   ├── remote_access.py 这个是一个局域网对外提供服务的东西。一般没有使用。
│   ├── tornado.py   400行。
│   ├── tornado_http.py 160行。
│   ├── tpl
│   │   └── index.html  页面模板。例如powered by pywebio就是写在这个文件里的。
│   └── utils.py  不到400行。
├── session
│   ├── __init__.py
│   ├── base.py
│   ├── coroutinebased.py
│   └── threadbased.py
└── utils.py
```

# utils.py

16个函数（2个是异步的），5个类。

函数

```
pyinstaller_datas
	指定pyinstaller要打包进去的内容。
catch_exp_call
	就是捕获异常，记录到日志里。
iscoroutinefunction
isgeneratorfunction
get_function_name
get_function_doc
get_function_attr

wait_host_port
	异步函数。
get_free_port
random_str
	生成随机字符串。默认16个字符。
	
run_as_function
to_coroutine
	异步函数。
check_webio_js
	检查webio.js文件是否存在。
	
parse_file_size
	解析10M这样的字符串为字节数。
	
strip_space
	
check_dom_name_value

```

类

```
Setter
	可以在对象属性上保存数据。当访问不存在的属性时，返回None，而不是抛出异常。
	其实就定义了一个方法：__getattribute__
	
ObjectDictProxy
	是对默认的dict进行了一个简单的封装。
	
ReadOnlyObjectDict
	继承了ObjectDictProxy
	
LimitedSizeQueue
	queue.Queue的子类。
	
LRUDict
	OrderedDict的子类。
	只有一个函数__setitem__
	
```

# io_ctrl.py

10个函数，2个类。

函数

```
scope2dom
	把scope字符串转成dom字符串。
	pywebio-scope-xx 这样的。
	
safely_destruct_output_when_exp
	当出现异常的时候，进行安全的销毁操作。
	是一个装饰器。
send_msg
single_input_kwargs
single_input
	调用了input_control
input_control
	调用了input_event_handle
check_item
trigger_onchange
input_event_handle
	这个比较复杂。
output_register_callback
```

类

```
Output
	一个staticmethod：json_encoder。
	2个classmethod：dump_dict、safely_destruct。
	构造函数：
		
	enable_context_manager
	__enter__和__exit__
	embed_data
	send，函数有个show的别名。
	style，自定义css。
	onclick，指定回调函数。
	__del__
	
OutputList
	是UserList的子类。
	就一个函数：__del__
	
```

# platform/adaptor/ws.py

3个函数，3个类。

函数

```
set_expire_second
	设置session超时时间。
clean_expired_sessions
	清理超时的session。
session_clean_task
	异步函数。
	调用了clean_expired_sessions
	
```

类

```
_state
	就几个成员变量。没有方法。
WebSocketConnection
	ABC的子类。
	这个是一个虚类。它的子类必须实现的方法，也就是abc.abstractmethod，有5个。
	get_query_argument
	make_session_info
	write_message
	closed
	close
	
WebSocketHandler
	几个class变量。
	_init_session方法
	_send_msg_to_client
	_close_from_session
	send_client_data
	notify_connection_lost
	
```



# platform/tornado.py

10个函数，1个类。

函数

```
set_ioloop
	保存到内部全局变量。_ioloop。
ioloop
	这个是直接返回内部的全局变量。_ioloop
_check_origin
	检查是不是同一个网站的。
_is_same_site
_webio_handler
	定义了一个内部的Handler类。然后返回了这个类的实例。
webio_handler
	调用了_webio_handler
open_webbrowser_on_server_started
	异步函数。
	这样来打开浏览器：threading.Thread(target=webbrowser.open
	
_setup_server
	定义了处理路由。
	handlers = [(r"/", webio_handler)]
	
start_server
	调用了_setup_server
	
start_server_in_current_thread_session
	这个是在scriptmode时候使用。
	
```

类

```
WebSocketConnection
	ws_adaptor.WebSocketConnection的子类。
	实现了要求实现的5个方法。
	
```



# platform/utils.py

提供了4个函数，一个类。

函数

```
cdn_validation
	检查cdn配置是否合法。
deserialize_binary_event
	把二进制的event反序列化。
get_interface_ip
	通过socket拿到网卡的ip地址。
print_listen_address
	打印监听的地址。
```

类

```
OriginChecker
	提供了2个函数：
	一个classmethod：check_origin
	一个staticmethod：is_same_site
	
```

# `session/__init__.py`

函数

```
register_session_implement
register_session_implement_for_target
get_session_implement
_start_script_mode_server
get_current_session
get_current_task_id
check_session_impl
chose_impl
next_client_event
hold
download
run_js
eval_js
run_async
run_asyncio_coroutine
register_thread
defer_call
set_env
go_app
get_info

```



# session/base.py

一个函数，一个类。

函数：

```
get_session_info_from_headers
```

类。

```
Session
	get_scope_name
	pop_scope
	push_scope
	send_task_command
	next_client_event
	send_client_event
	get_task_commands
	close
	closed
	on_task_exception
	register_callback
	defer_call
	
```

# session/threadedbase.py

类

```
ThreadBasedSession
	Session的子类。
	get_current_session
	get_current_task_id
	_get_task_id
	__init__
	_start_main_task
	send_task_command
	next_client_event
	send_client_event
	get_task_commands
	_trigger_close_event
	_cleanup
	close
	_activate_callback_env
	_dispatch_callback_event
	register_callback
	register_thread
	need_keep_alive
	
ScriptModeSession
	ThreadBasedSession的子类。
	就下面3个方法：
	get_current_session
	get_current_task_id
	__init__
```

