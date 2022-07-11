---
title: 设计模式之中介者模式Mediator
date: 2020-12-21 17:27:30
tags:
- 设计模式
---

1

看autojs的安卓代码，看到里面有Mediator这样名字的类。

搜索了一下，这个就是中介者模式。

这个模式也叫调停者模式，用得不太多。

我们以一个现实场景来描述中介者模式。

假如有这样的智能家居场景：

你在浴室里拉上窗帘，希望联动音乐播放器和洗浴设备。

假如我们希望这3个设备，操作其中一个，其余2个都会联动。

例如，你在浴室里打开音乐播放器，也会自动拉手窗帘和打开洗浴设备。

我们现在就有3个对象，他们互相持有对方的引用。

这样当然是可以实现我们的目的的。

但是这样简单的做法，实际上是有缺陷的。

这3个对象之间的耦合太高了。

1、如果窗帘坏掉了，我们要换成其他品牌的窗帘。

2、假如我们希望加入新的联动，例如把门也自动锁上。

可以看到上面的实现方式，非常不便于维护和扩展。

怎么解决这种问题？

就需要引入中介者模式了。

![img](../images/playopenwrt_pic/20180902163810343)

这里的中介者，就相当于智能家居系统的中控。

所有的信息都通过它来传达。

在这个模式里，涉及到4个角色。

```
1、抽象中介者。Mediator
2、具体中介者。ConcreteMediator。
3、抽象同事。Colleague。
4、具体同事。ConcreteColleague。
```

上面场景的类图。

![img](../images/playopenwrt_pic/20180902163810341)

抽象同事

都需要实现2个方法，设备上线，操作设备。就是一个读，一个写。

```
package mediator_12;
 
public abstract class SmartDevice {
	//相关设备打开之后 使其进入准备状态
	public abstract void readyState(String instruction);
    //操作该设备
	public abstract void operateDevice(String instruction, SmartMediator mediator);
}
```

具体的同事，有3个。

```
package mediator_12;
 
public class CurtainDevice extends SmartDevice{
 
	public void operateDevice(String instruction,SmartMediator mediator) {
		System.out.println("窗帘已"+instruction);//通过传入指令，打开或关闭窗帘
		mediator.curtain(instruction);//窗帘通过中介者唤醒音乐设备和洗浴设备
	}
 
	public void readyState(String instruction) {
        //如果其他设备开启则调用此方法，唤醒窗帘
		    System.out.println("窗帘设备准备"+instruction);
	}
 
}
```

音乐播放器

```
package mediator_12;
 
public class MusicDevice extends SmartDevice{
 
	public void operateDevice(String instruction,SmartMediator mediator) {
		System.out.println("音乐设备已"+instruction);
		mediator.music(instruction);
	}
 
	public void readyState(String instruction) {
		System.out.println("音乐设备准备"+instruction);
	}
 
}
```

洗浴设备

```
package mediator_12;
 
public class BathDevice extends SmartDevice{
 
	public void operateDevice(String instruction, SmartMediator mediator) {
		System.out.println("洗浴设备"+instruction);
		mediator.bath(instruction);
	}
 
	public void readyState(String instruction) {
		System.out.println("洗浴设备正在准备"+instruction);
	}
 
}
```



然后看抽象中介者。

```
package mediator_12;
 
public abstract class SmartMediator {
    //保留所有设备的引用是为了当接收指令时可以唤醒其他设备的操作
	SmartDevice bd;
	SmartDevice md;
	SmartDevice cd;
	public SmartMediator(SmartDevice bd, SmartDevice md, SmartDevice cd) {
		super();
		this.bd = bd;
		this.md = md;
		this.cd = cd;
	}
	public abstract void music(String instruction);
	public abstract void curtain(String instruction);
	public abstract void bath(String instruction);
}
```

具体中介者。

```
package mediator_12;
 
public class ConcreteMediator extends SmartMediator{
 
	public ConcreteMediator(SmartDevice bd, SmartDevice cd, SmartDevice md) {
		super(bd, cd, md);
	}
 
	public void music(String instruction) {//音乐被唤醒后，使其他设备进入准备状态
		cd.readyState(instruction);//调用窗帘的准备方法
		bd.readyState(instruction);//调用洗浴设备的准备方法
	}
 
	public void curtain(String instruction) {
		md.readyState(instruction);
		bd.readyState(instruction);
	}
 
	public void bath(String instruction) {
		cd.readyState(instruction);
		md.readyState(instruction);
	}
 
}
```

测试程序

```
package mediator_12;
 
public class Client {
	public static void main(String[] args) {
		SmartDevice bd=new BathDevice();
		SmartDevice cd=new CurtainDevice();
		SmartDevice md=new MusicDevice();
		SmartMediator sm=new ConcreteMediator(bd, cd, md);//把设备引用都保存在调停者中
		cd.operateDevice("open",sm); //开启窗帘
		md.operateDevice("close",sm);//关闭音乐
	}
}
```

运行效果，可以看到实现了联动效果。

![img](../images/playopenwrt_pic/20180902163810388)

参考资料

1、

https://blog.csdn.net/zhen921/article/details/82316707

