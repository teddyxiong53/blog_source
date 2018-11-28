---
title: buildroot之micropython
date: 2018-11-28 13:40:28
tags:
	- buildroot
	- Python

---



我在buildroot里选配了python组件。现在看看具体表现。

默认就是micropython的，你必须输入micropython才能启动。

```
# micropython 
MicroPython v1.8.7 on 2018-10-26; linux version
Use Ctrl-D to exit, Ctrl-E for paste mode
>>> 
>>> import sys
>>> help(sys)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'help' is not defined
>>> dir(sys)
['__name__', 'path', 'argv', 'version', 'version_info', 'implementation', 'platform', 'byteorder', 'maxsize', 'exit', 'stdin', 'stdout', 'stderr', 'modules', 'exc_info', 'print_exception']
>>> print sys.version
Traceback (most recent call last):
  File "<stdin>", line 1
SyntaxError: invalid syntax
>>> print(sys.version)
3.4.0
>>> print(sys.implementation)
(name='micropython', version=(1, 8, 7))
```

从上面这些东西，可以看出：

1、实现的python标准是3.4.0的。

2、micropython版本是1.8.7的。

3、print必须要用括号。

4、help没有实现，dir实现了。

有tab自动补全功能。

看看自带的库有哪些。

```
# cd /usr/lib
# cd micropython/
# ls
__future__.py          getpass.py             select.py
_libc.py               gettext.py             selectors.py
_markupbase.py         glob.py                shelve.py
abc.py                 gzip.py                shlex.py
argparse.py            hashlib                shutil.py
asyncio_slow.py        heapq.py               signal.py
base64.py              hmac.py                smtplib.py
benchmark              html                   socket.py
binascii.py            http                   socketserver.py
binhex.py              imaplib.py             sqlite3.py
bisect.py              imp.py                 stat.py
calendar.py            inspect.py             statistics.py
cgi.py                 io.py                  string.py
cmd.py                 ipaddress.py           stringprep.py
collections            itertools.py           struct.py
concurrent             json                   subprocess.py
contextlib.py          keyword.py             tarfile.py
copy.py                linecache.py           telnetlib.py
csv.py                 locale.py              tempfile.py
curses                 logging.py             test
datetime.py            machine                tests
dbm.py                 mailbox.py             tests.py
decimal.py             mailcap.py             textwrap.py
difflib.py             mimetypes.py           threading.py
email                  multiprocessing.py     time.py
errno.py               nntplib.py             timeit.py
example-extract.py     numbers.py             trace.py
example_blink.py       operator.py            traceback.py
example_getenv.py      optparse.py            tty.py
example_logging.py     os                     types.py
example_open.py        pathlib.py             uasyncio
example_pub.py         pdb.py                 uasyncio.py
example_pub_button.py  pickle.py              ucontextlib.py
example_sigint.py      pickletools.py         ucurses
example_sigint_exc.py  pkg_resources.py       umqtt
example_sigint_ign.py  pkgutil.py             unicodedata.py
example_strftime.py    platform.py            unittest.py
example_sub.py         poplib.py              upip.py
example_sub_led.py     posixpath.py           upip_utarfile.py
example_sub_robust.py  pprint.py              upysh.py
example_time_tuple.py  profile.py             urequests.py
example_timer.py       pty.py                 urllib
example_warn.py        pyb.py                 urllib.py
example_yield_coro.py  pystone.py             utarfile.py
fcntl.py               pystone_lowmem.py      uu.py
ffilib.py              queue.py               uuid.py
fnmatch.py             quopri.py              warnings.py
formatter.py           random.py              weakref.py
fractions.py           re.py                  xmltok.py
ftplib.py              reprlib.py             zipfile.py
functools.py           runpy.py
getopt.py              sched.py
```



把这些自带的库的源代码阅读一遍。

#`__future__.py`

就定义了几个变量

```
nested_scopes = True
generators = True
division = True
absolute_import = True
with_statement = True
print_function = True
unicode_literals = True
```

##`_libc.py`

里面就2个函数，

get和set_names。

另外有个变量bitness，就是int的长度。

是通过把maxsize的值来计算得到的。

依赖了sys和ffi。

ffi是micropython特有的一个库。

sys库是写在C代码里的。

可以通过ffi，直接调用C语言函数。

可以在micropython源代码目录下的：

```
./examples/unix/ffi_example.py
```

这个文件里看到用法。

```
>>> libc = ffi.open("libc.so.0")
>>> print("libc:", libc)
libc: <ffimod 66040>
>>> time = libc.func("i", "time", "p")
>>> time
<ffifunc 76e69f14>
>>> time(None)
1543386220
```

## os目录

`__init__.py`

这个里面mkdir这些函数，就是借助ffi，封装了libc的对应函数。出错时都是返回OSError。

```
error = OSError
name = "posix"
sep = "/"
curdir = "."
pardir = ".."
libc = ffilib.libc()

if libc:
    chdir_ = libc.func("i", "chdir", "s")
    mkdir_ = libc.func("i", "mkdir", "si")
    
    
    
def mkdir(name, mode=0o777):
    e = mkdir_(name, mode)
    check_error(e)
```



# argparse.py

这个可以把代码看懂。

