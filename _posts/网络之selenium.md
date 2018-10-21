---
title: 网络之selenium
date: 2018-06-30 12:31:19
tags:
	- 网络

---



最近在学习爬虫，接触到selenium这个东西，需要专门研究一下。



有些网页，不能直接通过wget和curl来直接获取并把它真正的内容展示给用户。

因为里面含有js脚本。需要通过浏览器进行渲染才能得到想要的结果。

例如，我访问http://www.ip.cn/114.114.114.114

来查询这个服务器的地址在哪里。

有两种方式：

1、写web ui自动化脚本，让selenium启动真正的浏览器来打开该网页，然后调用webdriver来获取想要的页面元素。

2、找一种浏览器渲染引擎，可以让它解析并执行网页里的js代码，然后把js、css等执行后的html内容输出出来。

第二种方式，就是要依赖PhantomJS。

```
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("http://www.ip.cn/114.114.114.114")
print(driver.find_element_by_id("result").text)
```

运行：

```
您查询的 IP：114.114.114.114
所在地理位置：114 DNS
GeoIP: Nanjing, Jiangsu, China
NanJing XinFeng Information Technologies
```

现在我们要从这里面抽取出GeoIP后面的内容。不过这个就是字符串的处理的内容了。先不管。



# 设置代理

很多网站都设置了反爬虫的机制，对于某个ip的访问频率是有限制的。

所以需要设置代理ip。

```
import selenium
print (selenium.__version__)
```

得到的我selenium是3.12.0 。

到这里下载对应的版本。放入到c:python37\scripts目录下。

http://selenium-release.storage.googleapis.com/index.html?path=3.12/



已知一个元素定义如下：

```
<input type="text" name="passwd" id="passwd-id" />
```

可以通过这些方法来查找它。

```
element = driver.find_element_by_id("passwd-id")
element = driver.find_element_by_name("passwd")
element = driver.find_element_by_xpath("//input[@id='passwd-id']")
```



# 用法详解

用淘宝作为测试网站。

## 测试各种查找元素方法

```
from selenium import webdriver

browser = webdriver.PhantomJS()

browser.get("https://www.taobao.com")
input_first = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
input_third = browser.find_element_by_xpath('//*[@id="q"]')
print(input_first, input_second, input_third)

browser.close()
```



```
常用的查找方法 
find_element_by_name 
find_element_by_xpath 
find_element_by_link_text 
find_element_by_partial_link_text 
find_element_by_tag_name 
find_element_by_class_name 
find_element_by_css_selector
```







# 参考资料

1、使用Selenium和PhantomJS解析带JS的网页

https://blog.csdn.net/brandon2015/article/details/50490744

2、Not able to launch IE browser using Selenium2 (Webdriver) with Java

https://stackoverflow.com/questions/14952348/not-able-to-launch-ie-browser-using-selenium2-webdriver-with-java
3、phantomjs 使用代理

https://blog.csdn.net/zpf_07/article/details/78030249

4、官网教程

http://selenium-python-zh.readthedocs.io/en/latest/navigating.html

5、

https://blog.csdn.net/liuchunming033/article/details/46789085

6、查找页面元素的技巧。这个很有效，直接右键拷贝xpath。

https://blog.csdn.net/niedongri/article/details/70238142

7、Selenium2+python自动化45-18种定位方法（find_elements）

https://www.cnblogs.com/yoyoketang/p/6557421.html

8、selenium用法详解

https://www.cnblogs.com/themost/p/6900852.html