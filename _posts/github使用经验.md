---
title: github使用经验
date: 2018-03-06 21:21:43
tags:
	- github

---



# 1. 用wget下载代码zip文件

wget https://codeload.github.com/xxx/yyy/zip/master

xxx：用户名

yyy：仓库名。

不过，我们直接看到的是https://github.com/teddyxiong53/MyAlgo 这种url。

我们手动转换太麻烦。写一个Python脚本，用正则表达式来自动帮我们转换。

这个过程是，

1、在github.com和https://中间插入codeload。

2、在最后加上/zip/master。

3、默认的名字是master。不直观。我们下载完成后，自动改一下名字。

```
#!/usr/bin/python

#encoding: utf-8

import sys,os,re

repo_name = "master"

def usage():
    print "usage: ./mywget url"

def check_url(url):
    pattern = re.compile(r"([a-z]{2,})://([\S])+")
    match = pattern.match(url)
    if match:
        return True
    else:
        return False
#https://github.com/teddyxiong53/MyAlgo
def get_repo_name(url):
    match = re.search(r"(.*)\.com\/(.*)\/(.*)", url)
    #print match
    if match:
        return match.group(3)
def process_url(url):
    #get repo name
    global repo_name
    repo_name = get_repo_name(url)
    #1. add codeload after https://
    url_tmp = "https://codeload."
    url_tmp += url[8:]
    url_tmp += "/zip/master"
    return url_tmp

def main(argv):
    try:
        url = sys.argv[1]
    except Exception, e:
        usage()
        sys.exit(1)
    valid = check_url(url)
    if not valid:
        print "url is not valid"
        sys.exit(1)
    url = process_url(url)
    global repo_name
    print repo_name
    os.system("wget -c " + url)
    os.rename("master", repo_name+".zip")
if __name__ == '__main__':
    main(sys.argv)
```

脚本名字叫mywget。

```
./mywget.py https://github.com/teddyxiong53/MyAlgo
```



# 2. 下载加速

```
192.30.253.112 assets-cdn.github.com
151.101.88.249 github.global.ssl.fastly.net
```

host文件里加上这个。速度没有看到明显提升。

但是至少不会下载时看不到进度，而且不会下载到中途认为完成了。实际上并没有完成。

