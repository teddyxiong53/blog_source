---
title: js之保留关键字
date: 2019-03-16 11:09:11
tags:
	- js

---





除了C语言的那些关键字。

还有这些：

```
catch
delete
finally
in
function
instanceof
this
throw
try
typeof
var
with
```



把之前没有怎么了解的分析一下。

#异常的4个关键字

```
throw try catch finally
```

举例：

```
    <script>
        function CommonException(message, code) {
            this.message = message;
            this.code = code;
        }
        try {
            var exception = new CommonException("invalid value error", 1);
            throw exception;
            alert("这个代码执行不到");
        } catch(e) {
            alert(e.message);
            alert(e.code);
        } finally {
            alert("finally code");
        }
    </script>
```



#in

这个主要是跟for一起做循环。



# with

用来引用一个对象，使得访问属性和方法更加方便。不能增减属性和方法。

举例：

```
    <script>
        function MyObject(id, name) {
            this.id = id;
            this.name = name;
            this.getName = function() {
                return this.name;
            }
        }
        var myObj = new MyObject(1, "xxx");
        with(myObj) {
            console.log(id);
            console.log(name);
            console.log(getName());
            id = 4;
            console.log(id);
        }
        console.log(myObj.id);
    </script>
```



参考资料

1、JS 基础 —— JavaScript 关键字（keyword）与保留字

https://blog.csdn.net/qq_19865749/article/details/78128894