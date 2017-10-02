---
title: Flask之FlaskBB安装使用
date: 2017-10-01 17:59:42
tags:
	- Python
	- Flask

---



1、新建一个叫flaskbb的virtualenv。

```
pi@raspberrypi:~$ mkvirtualenv flaskbb
```

2、切换到我们下载的flaskbb的代码目录下。安装依赖。

```
pip install -r requirements.txt
```

3、有一个可选的配置，就是redis。如果你要用redis的话，你要确保redis-server在运行。redis被用作默认的celery（celery是一个task queue，在FlaskBB里被用来发送非阻塞的email）结果和缓存后端。

按照下面的操作步骤进行安装设置就好：

```
sudo apt-get install redis-server
# 看看redis是否在运行
systemctl status redis-server
# 如果没有运行，启动redis
sudo systemctl start redis-server
# 设置开机就把redis启动
sudo systemctl enable redis-server
```



4、FlaskBB已经设置一些默认的参数，你可以不改。

FlaskBB提供了一个很好的wizard来帮助大家进行配置。

启动wizard的方法是：`flaskbb makeconfig`。

这个flaskbb其实就是一个Python脚本。

```
(flaskbb) pi@raspberrypi:~/work/test/flaskbb/flaskbb-master$ type flaskbb
flaskbb is hashed (/home/pi/.virtualenvs/flaskbb/bin/flaskbb)
(flaskbb) pi@raspberrypi:~/work/test/flaskbb/flaskbb-master$ ls -lh /home/pi/.virtualenvs/flaskbb/bin/flaskbb
-rwxr-xr-x 1 pi pi 385 Oct  1 14:56 /home/pi/.virtualenvs/flaskbb/bin/flaskbb
(flaskbb) pi@raspberrypi:~/work/test/flaskbb/flaskbb-master$ cat /home/pi/.virtualenvs/flaskbb/bin/flaskbb
#!/home/pi/.virtualenvs/flaskbb/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'FlaskBB','console_scripts','flaskbb'
__requires__ = 'FlaskBB'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('FlaskBB', 'console_scripts', 'flaskbb')()
    )
(flaskbb) pi@raspberrypi:~/work/test/flaskbb/flaskbb-master$ 
```

配置过程如下，我全部一直按Enter键默认的。

```
(flaskbb) pi@raspberrypi:~/work/test/flaskbb/flaskbb-master$ flaskbb makeconfig
[~] Using default config.
The path to save this configuration file.
Save to [/home/pi/work/test/flaskbb/flaskbb-master/flaskbb.cfg]: 
The name and port number of the server.
This is needed to correctly generate URLs when no request context is available.
Server Name [localhost:5000]: 
The URL Scheme is also needed in order to generate correct URLs when no request context is available.
Choose either 'https' or 'http'.
URL Scheme [http]: 
For Postgres use:
    postgresql://flaskbb@localhost:5432/flaskbb
For more options see the SQLAlchemy docs:
    http://docs.sqlalchemy.org/en/latest/core/engines.html
Database URI [sqlite:////home/pi/work/test/flaskbb/flaskbb-master/flaskbb.sqlite]: 
Redis will be used for things such as the task queue, caching and rate limiting.
Would you like to use redis? [Y/n]: 
Redis URI [redis://localhost:6379]: 
To use 'localhost' make sure that you have sendmail or
something similar installed. Gmail is also supprted.
Mail Server [localhost]: 
The port on which the SMTP server is listening on.
Mail Server SMTP Port [25]: 
If you are using a local SMTP server like sendmail this is not needed. For external servers it is required.
Use TLS for sending mails? [y/N]: 
Same as above. TLS is the successor to SSL.
Use SSL for sending mails? [y/N]: 
Not needed if you are using a local smtp server.
For gmail you have to put in your email address here.
Mail Username []: 
Not needed if you are using a local smtp server.
For gmail you have to put in your gmail password here.
Mail Password []: 
The name of the sender. You probably want to change it to something like '<your_community> Mailer'.
Mail Sender Name [FlaskBB Mailer]: 
On localhost you want to use a noreply address here. Use your email address for gmail here.
Mail Sender Address [noreply@yourdomain]: 
Logs and important system messages are sent to this address.Use your email address for gmail here.
Mail Admin Email [admin@yourdomain]: 
The configuration file has been saved to:
/home/pi/work/test/flaskbb/flaskbb-master/flaskbb.cfg
Feel free to adjust it as needed.
Usage: 
flaskbb --config /home/pi/work/test/flaskbb/flaskbb-master/flaskbb.cfg run
(flaskbb) pi@raspberrypi:~/work/test/flaskbb/flaskbb-master$ 
```

5、运行。

```
flaskbb --config flaskbb.cfg run
```

