---
title: Python之load_entry_point
date: 2018-06-17 14:34:34
tags:
	- Python

---



看HomeAssistant的代码，看到bin/hass的内容是这样的。

这种用法之前没有见过。

```
#!/home/pi/work/hass/hass/bin/python3
# EASY-INSTALL-ENTRY-SCRIPT: 'homeassistant','console_scripts','hass'
__requires__ = 'homeassistant'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('homeassistant', 'console_scripts', 'hass')()
    )

```



1、什么是pkg_resources？

```

```

2、load_entry_point的用法。

```

```



entry point是用来放进setup.py里，用来让你的package可以当成一个脚本在命令行进行访问。

但是实际上，entry point的作用不止于此。

entry point可以作为一个模块插件的架构来使用。

用来在运行时给你的package增加功能。

下面以一个故事的形式来讲解。

要画出一条蛇，写一个snek.py。

```
ascii_snek = """\
    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__.
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
"""

def main():
    print(ascii_snek)
    
if __name__ == '__main__':
    main()
```

但是这个运行，需要python snek.py这样来运行。

但是客户是小白，他根本不懂什么Python。

我们要做得对用户友好一些。

所以，我们加入一个setup.py。

```
from setuptools import setup

setup(
	name = 'snek',
	entry_points = {
		'console_scripts': [
			'snek = snek:main',
		]
	}
)
```

安装。

```
teddy@teddy-ubuntu:~/work/test/python$ sudo python setup.py develop 
running develop
running egg_info
writing snek.egg-info/PKG-INFO
writing top-level names to snek.egg-info/top_level.txt
writing dependency_links to snek.egg-info/dependency_links.txt
writing entry points to snek.egg-info/entry_points.txt
reading manifest file 'snek.egg-info/SOURCES.txt'
writing manifest file 'snek.egg-info/SOURCES.txt'
running build_ext
Creating /usr/local/lib/python2.7/dist-packages/snek.egg-link (link to .)
snek 0.0.0 is already the active version in easy-install.pth
Installing snek script to /usr/local/bin

Installed /home/teddy/work/test/python
Processing dependencies for snek==0.0.0
Finished processing dependencies for snek==0.0.0
```

测试：

```
teddy@teddy-ubuntu:~/work/test/python$ snek
    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__.
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
```

现在要增加新的snek的类型。

```
#!/usr/bin/python3
import sys
normal_snek = 'normal_snek'
fancy_snek = 'fancy_snek'

def get_sneks():
	return {
		'normal': normal_snek,
		'fancy': fancy_snek,
	}
	
def main():
	if len(sys.argv) > 2:
		snek_type = sys.argv[2]
	else:
		snek_type = 'normal'
	print(get_sneks()[snek_type])
	
if __name__ == '__main__':
	main()
	
```

但是随着应用的越来越广泛，我们也疲于应付这种定制修改。

客户希望把snek当成基础设施，他们可以自己进行定制。

现在代码目录如下：

```
teddy@teddy-ubuntu:~/work/test/python$ tree
.
├── custom_snek
│   ├── custom_snek.py
│   └── setup.py
├── setup.py
├── snek.py
```

snek.py改为下面这样：

```
#!/usr/bin/python3
import sys, pkg_resources

normal_snek = 'normal_snek'
fancy_snek = 'fancy_snek'

def get_sneks():
	sneks =  {
		'normal': normal_snek,
		'fancy': fancy_snek,
	}
	for entry_point in pkg_resources.iter_entry_points('snek_types'):
		sneks[entry_point.name] = entry_point.load()
	return sneks
	
def main():
	if len(sys.argv) > 2:
		snek_type = sys.argv[2]
	else:
		snek_type = 'normal'
	print(get_sneks()[snek_type])
	
if __name__ == '__main__':
	main()
```

custom_snek.py：

```
custom_snek = 'custom_snek'
```

custom_snek/setup.py：

```
from setuptools import setup

setup(
	name = 'snek',
	entry_points = {
		'console_scripts': [
			'snek = snek:main',
		]
	}
)
```

然后我们在两个目录下，都进行sudo python setu.py develop

然后运行snek --type custom

就可以得到预期的结果了。



# 参考资料

1、Python pkg_resources.load_entry_point() Examples

https://www.programcreek.com/python/example/32721/pkg_resources.load_entry_point

2、Python Entry Points Explained

这篇文章讲得很细致，很好。

https://amir.rachum.com/blog/2017/07/28/python-entry-points/