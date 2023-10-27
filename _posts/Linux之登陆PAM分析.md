---
title: Linux之登陆PAM分析
date: 2023-10-25 11:23:04
tags:
	- Linux

---

--

# linux登陆的pam说明

PAM（Pluggable Authentication Module）

是一个用于在Linux系统上进行身份验证和授权的模块化框架。

PAM允许系统管理员通过配置不同的模块来定义登录、密码更改和其他认证任务的行为。

**这些模块可以是系统提供的，也可以是第三方开发的，**

使系统管理员能够自定义认证策略，而无需修改系统的核心身份验证代码。

下面是PAM的主要组成部分和登录过程的说明：

1. **配置文件**：PAM的配置文件通常位于`/etc/pam.d/`目录下，每个应用程序或服务都有一个相关的PAM配置文件。例如，`/etc/pam.d/login` 文件用于配置登录认证。配置文件定义了哪些模块将在特定的认证过程中使用，以及它们的顺序。

2. **模块**：PAM模块是实际执行身份验证或授权的组件。每个模块负责不同的任务，如密码验证、账户检查、会话管理等。系统管理员可以根据需要在PAM配置文件中选择性地启用、禁用或重排序这些模块。以下是一些常见的PAM模块：
- `pam_unix`：用于基本的用户名和密码验证。
   - `pam_ldap`：用于与LDAP目录服务器进行身份验证。
   - `pam_google_authenticator`：用于实施双因素认证。
   - `pam_tally2`：用于跟踪登录尝试次数以实施帐户锁定。
   - `pam_selinux`：用于SELinux策略的集成。
   
3. **认证流程**：当用户尝试登录系统时，PAM会根据PAM配置文件中的定义执行相关的模块。通常，PAM会按照配置文件中的顺序依次执行模块，如果任何一个模块失败，认证流程就会中断，用户将无法登录。如果所有模块都成功通过，用户将被授权访问系统。

PAM配置文件的示例：

```bash
# /etc/pam.d/login

# auth
auth    requisite           pam_nologin.so
auth    required            pam_securetty.so
auth    required            pam_unix.so

# account
account required            pam_unix.so

# password
password requisite          pam_pwquality.so
password required           pam_unix.so

# session
session required            pam_unix.so
```

在上述示例中，配置文件定义了登录认证的PAM模块和其顺序。

`auth` 部分用于身份验证，

`account` 部分用于账户检查，

`password` 部分用于密码管理，

`session` 部分用于会话管理。

PAM的强大之处在于，系统管理员可以根据特定需求定制认证策略，例如实施双因素认证、限制登录次数、强密码策略等。通过编辑PAM配置文件，可以调整认证流程以满足系统的安全需求。