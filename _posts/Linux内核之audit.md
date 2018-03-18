---
title: Linux内核之audit
date: 2018-03-17 22:05:05
tags:
	- Linux

---



audit是审计的意思。这个功能在运维中还是很重要的。

Linux内核有用日志记录事件的能力。

我在树莓派上进行实验。

默认没有安装auditd。安装。

```
sudo apt-get install auditd
```

安装会失败。我看了一下树莓派的config文件，默认没有把audit的支持打开。

我有不想重新编译内核。所以我换个机器看看。

在我的Ubuntu上可以安装成功。

auditd会在后台运行，把记录信息写入到磁盘里。

相关的工具和配置文件有：

```
auditctl：控制审计的行为，例如增减规则。
aureport：查看和生成审计报告。
ausearch：查找。
auditspd：转发事件给其他应用，而不是写入到日志里。
autrace：跟踪某个进程的行为。

/etc/audit/audit.rules
/etc/audit/auditd.conf
```



看看默认的autdid.conf内容。

```
log_file = /var/log/audit/audit.log
log_format = RAW
log_group = root
priority_boost = 4
flush = INCREMENTAL
freq = 20
num_logs = 5
disp_qos = lossy
dispatcher = /sbin/audispd
name_format = NONE
##name = mydomain
max_log_file = 6
max_log_file_action = ROTATE
space_left = 75
space_left_action = SYSLOG
action_mail_acct = root
admin_space_left = 50
admin_space_left_action = SUSPEND
disk_full_action = SUSPEND
disk_error_action = SUSPEND
##tcp_listen_port = 
tcp_listen_queue = 5
tcp_max_per_addr = 1
##tcp_client_ports = 1024-65535
tcp_client_max_idle = 0
enable_krb5 = no
krb5_principal = auditd
##krb5_key_file = /etc/audit/audit.key
```

看看默认的规则有什么。

```
root@teddy-ubuntu:/etc/audit# auditctl -l
No rules
```

没有内容。

我们使用审计功能，一般是想检测某些目录和文件的改动情况，例如/etc/passwd这种敏感文件。



查看审计报告。

```
root@teddy-ubuntu:/etc/audit# sudo aureport

Summary Report
======================
Range of time in logs: 2018年03月18日 12:24:30.819 - 2018年03月18日 12:33:12.798
Selected time for report: 2018年03月18日 12:24:30 - 2018年03月18日 12:33:12.798
Number of changes in configuration: 0
Number of changes to accounts, groups, or roles: 0
Number of logins: 0
Number of failed logins: 0
Number of authentications: 1
Number of failed authentications: 0
Number of users: 2
Number of terminals: 2
Number of host names: 1
Number of executables: 2
Number of commands: 0
Number of files: 0
Number of AVC's: 0
Number of MAC events: 0
Number of failed syscalls: 0
Number of anomaly events: 0
Number of responses to anomaly events: 0
Number of crypto events: 0
Number of integrity events: 0
Number of virt events: 0
Number of keys: 0
Number of process IDs: 4
Number of events: 10
```

