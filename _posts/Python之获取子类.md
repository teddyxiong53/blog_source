---
title: Python之获取子类
date: 2018-11-26 21:41:28
tags:
	- Python

---



下面是一个简单的实例。

```
class AbstractSTTEngine(object):
	pass
	
class PocketSphoinx(AbstractSTTEngine):
	SLUG = 'PocketSphoinx'
	
class BaiduSTT(AbstractSTTEngine):
	SLUG = 'BaiduSTT'
	

def get_engine_by_slug(slug=None):
	selected_engines = filter(lambda engine: hasattr(engine, "SLUG") and engine.SLUG == slug, get_engines())
	print get_engines()
	
def get_engines():
	def get_subclasses(cls):
		subclasses = set()
		for subclass in cls.__subclasses__():
			subclasses.add(subclass)
			subclasses.update(get_subclasses(subclass))
		return subclasses
		
	return [stt_engine for stt_engine in list(get_subclasses(AbstractSTTEngine)) if hasattr(stt_engine, 'SLUG') and stt_engine.SLUG ]
	
	
get_engine_by_slug(slug='BaiduSTT')

```

输出结果：

```
teddy@teddy-ubuntu:~/work/test/python$ python test.py 
[<class '__main__.PocketSphoinx'>, <class '__main__.BaiduSTT'>]
```

