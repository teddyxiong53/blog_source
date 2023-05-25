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
	但是实际没有使用。
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
	为什么要这个封装？默认的有什么问题？
	就是为了访问不存在的属性不要抛出异常。
	跟Setter的目的类似。
	在代码中的使用是：
	local = ObjectDictProxy(lambda: get_current_session().save)
	注意它的参数，是setter函数，是存到session的里面了。
	
ReadOnlyObjectDict
	继承了ObjectDictProxy
	readonly是靠把delitem、delattr、setitem、setattr这4个函数重写为
		raise NotImplemented。
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

# webiojs代码分析

浏览器是client，服务器是server。通过websocket连接进行双向通信。

client发给server的event。

server发给client的command。（这个命名跟avs的类似）

```
//session.ts里的定义：
export interface Command {
    command: string
    task_id: string
    spec: any
}

export interface ClientEvent {
    event: string,
    task_id: string,
    data: any
}

```

# pin的用法

## pin_update

有3个pin_xx函数

pin_update

pin_on_change

pin_wait_change



# demos分析

## markdown_previewer

这个没有使用async的方式。看看是怎么做到动态刷新的。

靠的是一个死循环里一个pin_wait_change。

这个模式我可以用来做edid解析器这样的应用。

实时修改并预览结果。

这个demo就是用来演示pin_wait_change的。

# remote_access实现分析

在start_server的函数，传递remote_access=True的话，那么会生成一个这样的可以在公网访问的地址：

```
http://w2flh9ps2hui.app.pywebio.online
```

这个是如何实现的？

```
start_remote_access_service
	依赖了ssh。
	server = os.environ.get('PYWEBIO_REMOTE_ACCESS', 'app.pywebio.online:1022')
	然后创建了一个thread。
	cmd = "ssh -oStrictHostKeyChecking=no -R 80:127.0.0.1:%s -p %s %s -- --output json" % (
        local_port, server_port, server)
```

# 支持websocket的backend

有3个：

aiohttp

fastapi

tornado

# `_activate_callback_env` 

`_activate_callback_env` 是 PyWebIO 内部使用的函数，用于激活回调环境。它用于在 PyWebIO 应用程序中处理异步回调时的上下文管理。

在 PyWebIO 中，异步回调是一种机制，允许在浏览器与服务器之间进行异步通信，以实现实时更新和交互功能。当用户在浏览器中执行某些操作（例如点击按钮、输入文本等），触发了回调事件时，PyWebIO 会在后台进行处理，并将结果返回给浏览器进行更新。

在处理回调事件时，PyWebIO 使用了一种上下文管理的方式来管理回调环境。这种上下文管理机制确保了每个回调事件的执行都在独立的上下文中进行，以避免并发和状态混乱的问题。

`_activate_callback_env` 函数的作用就是在处理回调事件之前，激活回调环境的上下文。它会创建一个新的回调环境，并将其设置为当前活动的回调环境，以确保回调事件的处理在正确的上下文中进行。

由于 `_activate_callback_env` 是 PyWebIO 内部使用的函数，通常不需要在应用程序中直接调用它。它在 PyWebIO 框架内部的其他组件中被使用，以确保回调事件的正确处理。在正常使用 PyWebIO 进行应用程序开发时，无需关注 `_activate_callback_env` 函数的细节和具体实现。