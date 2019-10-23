---
title: Python之暴力破解rar压缩文件
date: 2019-10-23 14:16:18
tags:
	- Python

---

1

有时候下载的压缩包是被加了密码的，用python来进行暴力破解看看。

生成密码的方式：

```
import itertools
words = "1234567890"
r = itertools.product(words, repeat=4)
import os
os.remove("10_digits.txt")
dic = open("10_digits.txt", "a")
for i in r:
    dic.write("".join(i))
    dic.write("".join("\n"))
dic.close()
```



完整代码：

```
import itertools as its
import threading
import rarfile
import os
words = '0123456789abcdefghijklmnopqrstuvwxyz' # 涉及到生成密码的参数
flag = True # 是否关闭线程的标志

def append_on_file(password,file_name):
  # 把解析出的密码写入到文件中
  with open('password.txt', 'a', encoding='utf8') as f:
    text = file_name+':'+password + '\n'
    f.write(text)
def get_password(min_digits, max_digits, words):
  """
  :param min_digits: 密码最小长度
  :param max_digits: 密码最大长度
  :param words: 密码可能涉及的字符
  :return: 密码生成器
  """
  while min_digits <= max_digits:
    pwds = its.product(words, repeat=min_digits)
    for pwd in pwds:
      yield ''.join(pwd)
    min_digits += 1
def extract(File,file_name):
  """
  若线程关闭标志为True，就执行循环，从密码生成器中取出密码，验证密码是否正确
  密码正确，则把密码写入文件中，并将线程关闭标志flag设定为False,通知其他线程关闭
  """
  global flag
  count = 0
  while flag:
    p = next(passwords)
    try:
      File.extractall(pwd=p) # 打开压缩文件,提供密码...
      flag = False
      print("password is " + p) ###破解到密码
      append_on_file(p,file_name)
      break
    except:
      #print(p)
      count +=1
      if count%500 == 0:
          print("count:",count)

def mainStep(file_path,file_name):
  """
  多线程并发验证密码
  :param file_path: rar压缩文件路径列表
  :return:
  """
  file = rarfile.RarFile(file_path)
  for pwd in range(10):
    t = threading.Thread(target=extract, args=(file,file_name))
    t.start()
# if __name__ == '__main__':
#   # 主程序
#   base_dir = r'E:\迅雷下载\rar'
#   for file_info in os.listdir(base_dir):
#     try:
#       # 拼接压缩文件路径
#       file_path = os.path.join(base_dir, file_info)
#       # 压缩文件名称
#       file_name = file_info.split('.')[0]
#       # 生成密码字典：密码长度最小为4，最大为11
#       passwords = get_password(4, 11, words)
#       # 将任务分发给线程执行
#       mainStep(file_path,file_name)
#     except:
#       pass

if __name__ == '__main__':
    file_path = r'D:\work\pycharm\text_render\1.rar'
    filename = "1"
    passwords = get_password(8,10, words)
    mainStep(file_path, filename)
```

运行起来后，cpu会飙升到100% 。用5个线程，cpu在66%左右。我破解自己的一个8位的密码看看需要多久。

靠这个函数来做。出错就换密码，如果没有出错，说明密码对了。

```
File.extractall(pwd=p)
```

8位的密码，每一位有36种可能，所有密码组合是2.8万亿个左右。



参考资料

1、python利用itertools生成密码字典并多线程撞库破解rar密码

https://www.jb51.net/article/167500.htm