---
title: java之transient关键字
date: 2017-12-28 12:06:03
tags:
	- java

---



transient关键字是一个跟序列化有关的关键字。



对于网络应用，序列化是常用的手段，但是一个类的属性，有些不适合被序列化的。

例如：用户的敏感信息如密码，银行卡号等，这些不希望被序列化后放在网络上传输，那么怎么可以把这些成员在序列化的过程中排除掉呢？很简单，就是在定义这些成员变量的时候，加上transient关键字。



```


import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Rectangle implements Serializable{

    /**
     *
     */
    private static final long serialVersionUID = 1710022455003682613L;
    private Integer width;
    private Integer height;
    private transient Integer area;



    public Rectangle (Integer width, Integer height){
        this.width = width;
        this.height = height;
        this.area = width * height;
    }

    public void setArea(){
        this.area = this.width * this.height;
    }

    @Override
    public String toString(){
        StringBuffer sb = new StringBuffer(40);
        sb.append("width : ");
        sb.append(this.width);
        sb.append("\nheight : ");
        sb.append(this.height);
        sb.append("\narea : ");
        sb.append(this.area);
        return sb.toString();
    }
}

public class TransientExample{
    public static void main(String args[]) throws Exception {
        Rectangle rectangle = new Rectangle(3,4);
        System.out.println("1.原始对象\n"+rectangle);
        ObjectOutputStream o = new ObjectOutputStream(new FileOutputStream("rectangle"));
        // 往流写入对象
        o.writeObject(rectangle);
        o.close();

        // 从流读取对象
        ObjectInputStream in = new ObjectInputStream(new FileInputStream("rectangle"));
        Rectangle rectangle1 = (Rectangle)in.readObject();
        System.out.println("2.反序列化后的对象\n"+rectangle1);
        rectangle1.setArea();
        System.out.println("3.恢复成原始对象\n"+rectangle1);
        in.close();
    }
}
```

编译执行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/java $ javac *.java         
hlxiong@hlxiong-VirtualBox ~/work/test/java $ java TransientExample
1.原始对象
width : 3
height : 4
area : 12
2.反序列化后的对象
width : 3
height : 4
area : null
3.恢复成原始对象
width : 3
height : 4
area : 12
```



参考资料

1、Java中的关键字 transient

https://www.cnblogs.com/chenpi/p/6185773.html