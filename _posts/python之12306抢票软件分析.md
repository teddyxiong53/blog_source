---
title: python之12306抢票软件分析
date: 2019-09-28 16:56:48
tags:
	- python

---

1

先从github下载代码。

https://github.com/testerSunshine/12306

安装依赖。

```
pip install -r ./requirements.txt
```

我的python版本是3.7的。

```
python run.py
```



在windows上运行。报这个错误。

```
OSError: [WinError 87] 参数错误。
```

看到对python的版本，是有比较样的要求的。

有docker版本，直接用docker的方式来跑吧。

我在Ubuntu16.04上进行测试。

需要安装docker和docker-compose。

我的docker版本是18.09.2 。

安装docker-compose。

```
curl -L https://get.daocloud.io/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

运行：

```
sudo ./docker.sh run
```

这个会下载docker镜像，并运行一些python库安装命令，如果失败了，重新执行命令就可以继续安装的。

不行，还是需要升级我的python版本，并且把默认的python设置为python3 。

```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
```

最后面的1表示优先级。

docker方式不行，我还是用python3.6的（我当前就是这个版本）。

现在运行起来，报错了。到github上的issue里搜索了一下“cookie”。

```
Traceback (most recent call last):
  File "run.py", line 20, in <module>
    run()
  File "run.py", line 8, in run
    select_ticket_info.select().main()
  File "/home/hlxiong/work/test/python/12306-master/init/select_ticket_info.py", line 155, in main
    getDrvicesID(self)
  File "/home/hlxiong/work/test/python/12306-master/config/getCookie.py", line 17, in getDrvicesID
    driver = webdriver.Chrome(executable_path=TickerConfig.CHROME_PATH)
  File "/home/hlxiong/.local/lib/python3.6/site-packages/selenium/webdriver/chrome/webdriver.py", line 68, in __init__
    self.service.start()
  File "/home/hlxiong/.local/lib/python3.6/site-packages/selenium/webdriver/common/service.py", line 88, in start
    os.path.basename(self.path), self.start_error_message)
selenium.common.exceptions.WebDriverException: Message: '' executable may have wrong permissions. Please see https://sites.google.com/a/chromium.org/chromedriver/home
```

发现是COOKIE_TYPE要设置为0，默认是1的。

现在总是这样：

```
需要验证码
下载验证码...
下载验证码成功
Corrupt JPEG data: 16 extraneous bytes before marker 0xd9
无需加载模型model.v2.0.h5
题目为['蜜蜂']
1 蜜蜂
2 安全帽
3 冰箱
4 蜜蜂
5 双面胶
6 红酒
7 安全帽
8 红酒
验证码识别坐标为40,77,256,77
40,77,256,77
验证码通过,开始登录..
url: /passport/web/login返回参数为空, 接口状态码: 302
url: /passport/web/login返回参数为空, 接口状态码: 302
url: /passport/web/login返回参数为空, 接口状态码: 302
url: /passport/web/login返回参数为空, 接口状态码: 302
url: /passport/web/login返回参数为空, 接口状态码: 302
```

过了一会儿就登陆成功了。

然后打印了这个。

```
正在第1次查询 随机停留时长：4.26 乘车日期: 2019-09-30 车次：所有车次 下单无票 无候补机会 耗时：144.658ms
使用缓存中查找的联系人信息
{}
通过人证一致性核验的用户及激活的“铁路畅行”会员可以提交候补需求，请您按照操作说明在铁路12306app.上完成人证核验
```

现在12306的官方app，在“我的”tab下面，点击人证一致验证。

再执行脚本看看。

还是有302，不能正常登陆。



看了一下代码，整体的逻辑还是不复杂的，代码风格不是很好。



参考资料

1、

