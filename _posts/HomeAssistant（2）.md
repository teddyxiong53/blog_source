---
title: HomeAssistant（2）
date: 2018-06-15 23:16:42
tags:
	- HomeAssistant

---



在前面一篇文章，我们已经把HA跑起来了。简单的添加和删除组件也都学会了。

现在主要逛中文论坛，把里面一些好的教程自己实践一遍。

我看到这篇文章 不错。

https://bbs.hassbian.com/thread-3971-1-1.html





看看当前的环境。

列出当前的Python虚拟环境安装的包。

```
(hass) pi@raspberrypi:~/work/hass/hass$ pip list
aiohttp (3.2.1)
aiohttp-cors (0.7.0)
astral (1.6.1) 用来计算月相的。
async-timeout (3.0.0)
attrs (18.1.0)
baidu-aip (1.6.6.0) 百度语言合成。
boto3 (1.7.40)  亚马逊AWS的Python库。
botocore (1.10.40)
certifi (2018.4.16)
chardet (3.0.4)
colorlog (3.1.4)
distro (1.3.0)
docutils (0.14)
ecdsa (0.13)
envs (1.2.6)
future (0.16.0)
gTTS-token (1.1.1)
home-assistant-frontend (20180608.0b0)
homeassistant (0.71.0, /home/pi/work/hass/hass)
idna (2.6)
idna-ssl (1.0.1)
Jinja2 (2.10)
jmespath (0.9.3)
MarkupSafe (1.0)
multidict (4.3.1)
mutagen (1.40.0)
netdisco (1.4.1)
netifaces (0.10.7)
Pillow (5.1.0)
pip (9.0.3)
pluggy (0.6.0)
ply (3.11)
psutil (5.4.5)
py (1.5.3)
py-cpuinfo (4.0.0)
pyasn1 (0.4.3)
pycryptodome (3.3.1)
pycryptodomex (3.6.1)
pysmi (0.3.1)
pysnmp (4.4.4)
python-dateutil (2.7.3)
python-jose-cryptodome (1.3.2)
pytz (2018.4)
PyYAML (3.12)
requests (2.18.4)
s3transfer (0.1.13)
setuptools (39.0.1)
six (1.11.0)
SQLAlchemy (1.2.8)
tox (3.0.0)
typing (3.6.4)
ua-parser (0.8.0)
urllib3 (1.22)
user-agents (1.1.0)
virtualenv (16.0.0)
voluptuous (0.11.1)
voluptuous-serialize (1.0.0)
warrant (0.6.1)
xmltodict (0.11.0)
yahooweather (0.10)
yarl (1.2.6)
zeroconf (0.20.0)
```

这样找到的内容多一些。

```
(hass) pi@raspberrypi:~/work/hass/hass$ python
Python 3.6.5 (default, Jun 16 2018, 23:47:39) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> help('modules')

Please wait a moment while I gather a list of all available modules...

Crypto              atexit              importlib           setuptools
Cryptodome          attr                inspect             shelve
PIL                 audioop             io                  shlex
__future__          base64              ipaddress           shutil
_ast                bdb                 itertools           signal
_asyncio            binascii            jinja2              site
_bisect             binhex              jmespath            six
_blake2             bisect              jose                smtpd
_bootlocale         boto3               json                smtplib
_codecs             botocore            keyword             sndhdr
_codecs_cn          builtins            lib2to3             socket
_codecs_hk          bz2                 libfuturize         socketserver
_codecs_iso2022     cProfile            libpasteurize       spwd
_codecs_jp          calendar            linecache           sqlalchemy
_codecs_kr          cdu                 locale              sqlite3
_codecs_tw          certifi             logging             sre_compile
_collections        cgi                 lzma                sre_constants
_collections_abc    cgitb               macpath             sre_parse
_compat_pickle      chardet             macurl2path         ssl
_compression        chunk               mailbox             stat
_crypt              cmath               mailcap             statistics
_csv                cmd                 markupsafe          string
_ctypes             code                marshal             stringprep
_ctypes_test        codecs              math                struct
_curses             codeop              mimetypes           subprocess
_curses_panel       collections         mmap                sunau
_datetime           colorlog            modulefinder        symbol
_decimal            colorsys            multidict           symtable
_dummy_thread       compileall          multiprocessing     sys
_elementtree        concurrent          mutagen             sysconfig
_functools          configparser        netdisco            syslog
_hashlib            contextlib          netifaces           tabnanny
_heapq              copy                netrc               tarfile
_imp                copyreg             nis                 telnetlib
_io                 cpuinfo             nntplib             tempfile
_json               crypt               ntpath              termios
_locale             csv                 nturl2path          test
_lsprof             ctypes              numbers             tests
_lzma               curses              opcode              textwrap
_markupbase         datetime            operator            this
_md5                dateutil            optparse            threading
_multibytecodec     dbm                 os                  time
_multiprocessing    decimal             ossaudiodev         timeit
_opcode             difflib             parser              tkinter
_operator           dis                 past                token
_osx_support        distro              pathlib             tokenize
_pickle             distutils           pdb                 tox
_posixsubprocess    doctest             pickle              trace
_pydecimal          docutils            pickletools         traceback
_pyio               dummy_threading     pip                 tracemalloc
_random             easy_install        pipes               tty
_sha1               ecdsa               pkg_resources       turtle
_sha256             email               pkgutil             turtledemo
_sha3               encodings           platform            types
_sha512             ensurepip           plistlib            typing
_signal             enum                pluggy              ua_parser
_sitebuiltins       envs                ply                 unicodedata
_socket             errno               poplib              unittest
_sqlite3            faulthandler        posix               urllib
_sre                fcntl               posixpath           urllib3
_ssl                filecmp             pprint              user_agents
_stat               fileinput           profile             uu
_string             fnmatch             pstats              uuid
_strptime           formatter           psutil              venv
_struct             fractions           pty                 virtualenv
_symtable           ftplib              pwd                 virtualenv_support
_sysconfigdata_m_linux_arm-linux-gnueabihf functools           py                  voluptuous
_testbuffer         future              py_compile          voluptuous_serialize
_testcapi           gc                  pyasn1              warnings
_testimportmultiple genericpath         pyclbr              warrant
_testmultiphase     getopt              pydoc               wave
_thread             getpass             pydoc_data          weakref
_threading_local    gettext             pyexpat             webbrowser
_tracemalloc        glob                pysmi               wsgiref
_warnings           grp                 pysnmp              xdrlib
_weakref            gtts_token          pytz                xml
_weakrefset         gzip                queue               xmlrpc
abc                 hashlib             quopri              xmltodict
aifc                hass_frontend       random              xxlimited
aiohttp             hass_frontend_es5   re                  xxsubtype
aiohttp_cors        heapq               reprlib             yahooweather
aip                 hmac                requests            yaml
antigravity         homeassistant       resource            yarl
argparse            html                rlcompleter         zeroconf
array               http                runpy               zipapp
ast                 idlelib             s3transfer          zipfile
astral              idna                sched               zipimport
async_timeout       idna_ssl            secrets             zlib
asynchat            imaplib             select              
asyncio             imghdr              selectors           
asyncore            imp                 setup        
```

