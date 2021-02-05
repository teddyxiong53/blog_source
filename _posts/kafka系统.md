---
title: kafka系统
date: 2021-02-01 14:38:11
tags:
	- 分布式

---

--

kafka是apache基金会的一个开源流处理平台。最开始是linkedin公司开发的。2010年捐献给了Apache。

使用scala和java编写。

kafka是一个分布式的消息订阅和发布系统。

可以处理消费者在网站里的所有动作流数据。

主要应用场景是：日志收集系统和消息系统。

kafka这个名字没有特别的含义，就是开发人员随意取的。

感觉类似于mqtt broker的作用。

在docker容器里创建一个kafka主题。

```
docker exec mockseckill_kafka_1 /opt/kafka/bin/kafka-topics.sh --create --topic CAR_NUMBER --replication-factor 1 --partitions 1 --zookeeper 172.16.2.153:2181
```



参考资料

1、Kafka

https://baike.baidu.com/item/Kafka/17930165?fr=aladdin

2、Kafka学习之路 （一）Kafka的简介

https://www.cnblogs.com/qingyunzong/p/9004509.html