---
title: Flask之常用接口
date: 2018-11-24 14:59:51
tags:
	- Flask
---



用dir函数查看对外的接口。

```
>>> import flask
>>> dir(flask)
['Blueprint', 'Config', 'Flask', 'Markup', 'Request', 'Response', 'Session', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', '__version__', '_app_ctx_stack', '_compat', '_request_ctx_stack', 'abort', 'after_this_request', 'app', 'appcontext_popped', 'appcontext_pushed', 'appcontext_tearing_down', 'before_render_template', 'blueprints', 'cli', 'config', 'copy_current_request_context', 'ctx', 'current_app', 'escape', 'flash', 'g', 'get_flashed_messages', 'get_template_attribute', 'globals', 'got_request_exception', 'has_app_context', 'has_request_context', 'helpers', 'json', 'json_available', 'jsonify', 'logging', 'make_response', 'message_flashed', 'redirect', 'render_template', 'render_template_string', 'request', 'request_finished', 'request_started', 'request_tearing_down', 'safe_join', 'send_file', 'send_from_directory', 'session', 'sessions', 'signals', 'signals_available', 'stream_with_context', 'template_rendered', 'templating', 'url_for', 'wrappers']
```

# Blueprint

蓝图，跟Application类似，但有不完全相同。

单独用文章来写了。

# Config

单独文章。



# Flask

单独文章。



# Markup

单独文章







参考资料

1、Modular Applications with Blueprints

http://flask.pocoo.org/docs/0.12/blueprints/

2、flask使用Blueprint进行多模块应用的编写

https://blog.csdn.net/u012734441/article/details/67631564