---
title: github使用经验
date: 2018-03-06 21:21:43
tags:
	- github

---



#  用wget下载代码zip文件

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



# 下载加速

```
192.30.253.112 assets-cdn.github.com
151.101.88.249 github.global.ssl.fastly.net
```

host文件里加上这个。速度没有看到明显提升。

但是至少不会下载时看不到进度，而且不会下载到中途认为完成了。实际上并没有完成。



# 下载子目录

有时候不想下载整个目录。只希望下载某个仓库下的子目录。怎么办？

https://minhaskamal.github.io/DownGit/#/home?url=

把你要下载的链接，输入到这里的输入框里，点击下载就好了。



# tortoisegit提交要输入密码

右键，进入设置，git的credential，选择manager - all windows users。

保存。然后提交测试一下，不用再输入了。



# workflow

看一篇文章里，提到利用github的workflow来实现借助github的服务器资源来进行padavan的代码编译。

了解一下这个过程。

# Github Actions

当然可以！GitHub Actions 是一个强大的 CI/CD 工具，可以帮助你自动化软件开发流程。以下是一步步掌握 GitHub Actions 的方法：

### 第一步：了解基本概念

1. **工作流 (Workflow)**：工作流是一个自动化过程，定义了要执行的任务。
2. **事件 (Event)**：工作流可以在特定事件发生时触发，如代码推送、拉取请求等。
3. **作业 (Job)**：工作流包含一个或多个作业，每个作业可以在一个或多个虚拟环境中运行。
4. **步骤 (Step)**：每个作业由多个步骤组成，步骤是具体的任务，可以是运行命令或调用其他操作。

### 第二步：创建你的第一个工作流

1. **创建 `.github/workflows` 目录**：
   在你的 GitHub 仓库中，创建一个目录 `.github/workflows`。

2. **添加工作流文件**：
   在该目录下创建一个 YAML 文件，例如 `ci.yml`。以下是一个简单的示例：

   ```yaml
   name: CI
   
   on: [push, pull_request]
   
   jobs:
     build:
       runs-on: ubuntu-latest
   
       steps:
         - name: Checkout code
           uses: actions/checkout@v2
   
         - name: Set up Node.js
           uses: actions/setup-node@v2
           with:
             node-version: '14'
   
         - name: Install dependencies
           run: npm install
   
         - name: Run tests
           run: npm test
   ```

### 第三步：理解工作流的结构

- **name**：工作流的名称。
- **on**：定义触发工作流的事件。
- **jobs**：定义要执行的作业。
- **steps**：在作业中定义具体的步骤。

### 第四步：运行和监控工作流

1. **提交代码**：将你的更改提交到 GitHub。
2. **查看运行状态**：
   - 转到你的 GitHub 仓库，点击 "Actions" 标签。
   - 你可以看到工作流的运行记录和状态。

### 第五步：使用动作 (Actions)

- GitHub 提供了很多现成的动作，你可以在社区中找到许多有用的动作。
- 在步骤中使用动作的基本语法是：

  ```yaml
  - name: Action name
    uses: username/repo@version
  ```

### 第六步：调试和优化

- 如果工作流失败，点击失败的步骤查看日志，找出问题所在。
- 你可以使用条件来控制步骤的执行，例如：

  ```yaml
  if: github.event_name == 'push'
  ```

### 第七步：深入学习

- 阅读 [GitHub Actions 官方文档](https://docs.github.com/en/actions) 以获取更多高级功能。
- 尝试使用矩阵构建、缓存依赖项等高级特性。

### 总结

通过以上步骤，你可以逐步掌握 GitHub Actions 的基本用法。建议多实践，试着创建不同的工作流以加深理解。祝你好运！



https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions

这里可以找到actions

https://github.com/marketplace?type=actions

# github里的开源项目的标准文件有哪些？README.md、LICENSE，还有哪些

在 GitHub 上的开源项目中，除了 `README.md` 和 `LICENSE` 文件，通常还会包含以下标准文件：

### 1. **CONTRIBUTING.md**
- **说明**：详细描述如何为项目贡献代码，包括提交规范、代码风格、测试要求等。

### 2. **CODE_OF_CONDUCT.md**
- **说明**：定义社区行为规范，确保项目参与者之间的尊重与包容。

### 3. **INSTALL.md 或 INSTALLATION.md**
- **说明**：提供项目的安装步骤和依赖项说明。

### 4. **CHANGELOG.md**
- **说明**：记录项目的版本历史及每个版本的变更内容。

### 5. **FAQ.md**
- **说明**：回答常见问题，帮助用户解决在使用项目时可能遇到的问题。

### 6. **.gitignore**
- **说明**：定义哪些文件和目录在 Git 中应被忽略，防止将不必要的文件提交到版本控制中。

### 7. **Makefile 或 build系统文件**
- **说明**：用于定义如何构建和编译项目的指令，通常用于 C/C++ 项目。

### 8. **docs/** 目录
- **说明**：包含项目的文档，可能包括 API 文档、用户指南等。

### 9. **LICENSE-*.md**
- **说明**：如果项目使用了多种许可证，可能会有不同的许可证文件。

### 10. **Dockerfile**
- **说明**：如果项目可以通过 Docker 部署，通常会包含 Dockerfile。

这些文件有助于用户更好地理解、使用和贡献项目，同时也能提升项目的可维护性和社区参与度。

# 2FA必须跟自己的手机绑定吗？如果自己离开公司，那账号怎么交接给其他人呢

GitHub 的 2FA 不一定必须绑定到个人手机，可以采用其他更适合团队管理的方式，这样即使某个员工离职，也能方便地将账号安全地交接给其他人。

------

### **1. 选择适合团队的 2FA 验证方式**

GitHub 支持以下几种 2FA 验证方式：

| 验证方式         | 适合情况                                                     |
| ---------------- | ------------------------------------------------------------ |
| **TOTP 应用**    | 使用 Google Authenticator、Authy 或 1Password 等工具生成动态验证码。适合个人使用。 |
| **硬件安全密钥** | 使用 YubiKey 或类似的物理设备，适合团队管理。支持多个密钥绑定到同一账号。 |
| **恢复代码**     | GitHub 提供一组恢复代码，保存好可以应对紧急情况，适合管理员和团队共享。 |

------

### **2. 推荐使用硬件安全密钥（YubiKey 等）**

硬件安全密钥更适合团队使用，可以绑定多个安全密钥到同一个 GitHub 账号：

1. 购买硬件安全密钥

   ：

   - 推荐 **YubiKey**（支持 USB-A/USB-C）或其他 FIDO2 兼容密钥。

2. 绑定多个密钥到账号

   ：

   - 进入 GitHub 的 **Settings > Account security > Two-factor authentication**。
   - 点击 **Register new security key**，依次添加多个密钥（为不同团队成员准备）。

3. 交接流程

   ：

   - 如果某人离职，只需回收他的安全密钥即可，无需修改账号或密码。

------

### **3. 共享管理的 2FA 方法**

如果必须使用 TOTP 验证码，可以采用以下方法：

#### **a) 使用团队共享的 TOTP 应用**

- 配置一个通用的 TOTP 应用（如 Authy、1Password 或 Bitwarden），将 GitHub 账号绑定到团队的共享账户。
- 所有团队成员可以通过共享账号登录 TOTP 应用，生成 GitHub 验证码。

#### **b) 保存 GitHub 的恢复代码**

- 启用 2FA 后，GitHub 会提供一组恢复代码（10 个一次性代码）。
- 将这些代码安全存储在团队管理的密码管理器中（如 1Password、LastPass 或 Bitwarden），作为备用验证方式。

------

### **4. 交接账号的最佳实践**

为了方便交接，建议将 GitHub 账号的管理工作分配到组织层级，而非单个个人账号：

#### **a) 使用 GitHub Organization 管理团队权限**

1. 创建 GitHub 组织，所有团队成员用自己的账号登录，无需共享公司主账号。
2. 主账号作为组织管理员，团队成员以具体角色（如只读或写入权限）加入。
3. 团队管理的核心代码存储在组织下的仓库中，方便交接。

#### **b) 文档化账号交接流程**

- 明确记录：
  - 登录账号所需的 URL 和密码。
  - 2FA 恢复代码存储位置。
  - 硬件安全密钥的分配情况。
- 使用密码管理工具（如 LastPass 或 1Password）集中存储这些信息。

------

### **总结操作建议**

| 操作                      | 方法                                                         |
| ------------------------- | ------------------------------------------------------------ |
| **绑定多个 2FA 安全密钥** | 使用 YubiKey 或其他硬件密钥，绑定多个设备，方便多人使用。    |
| **保存恢复代码**          | 将恢复代码存储在密码管理工具中，作为紧急备用方案。           |
| **共享 TOTP 验证**        | 使用团队共享的 Authy 或 1Password 等 TOTP 应用。             |
| **通过组织管理账号权限**  | 使用 GitHub 组织功能代替个人账号管理，提升权限控制的灵活性和交接便利性。 |
| **使用密码管理器**        | 使用 Bitwarden、LastPass 或 1Password 管理账号和 2FA 信息。  |

通过这些措施，可以确保账号的安全性和可交接性，减少因员工变动带来的管理风险。

# 恢复代码可以一直使用吗？还是一个恢复代码只能用一次？

GitHub 的恢复代码（Recovery Codes）**一次性使用**，即每个恢复代码只能用一次。使用后，GitHub 会自动将其标记为已用，无法再次使用。

------

### **恢复代码的特点**：

1. **单次有效**：
   - 每次登录时使用一个恢复代码，使用后该代码作废。
2. **批量生成**：
   - 启用 2FA 后，GitHub 会提供一组（默认 10 个）恢复代码。
   - 每组恢复代码中，每个代码是独立的，最多可以使用 10 次（用完一组后需生成新的恢复代码）。
3. **重新生成**：
   - 如果恢复代码用完或出于安全考虑，你可以重新生成一组代码。
   - 重新生成后，旧的恢复代码会全部失效。

------

### **如何管理恢复代码**：

1. **安全保存**：
   - 将恢复代码存储在安全的地方，例如密码管理器（如 1Password、LastPass、Bitwarden）或加密的文件中。
   - **避免截图或明文存储**，以防被泄露。
2. **重新生成代码**：
   - 登录 GitHub 账号。
   - 进入 **Settings > Account security > Two-factor authentication**。
   - 点击 **Recovery codes > Regenerate codes**。
   - 生成的新代码会覆盖旧代码。

------

### **最佳实践**：

- 确保你有至少一个备份恢复代码存储在安全的地方。
- 定期检查恢复代码的可用数量，如果用完或快用完，及时重新生成。
- 如果有多人管理账号，可以通过密码管理器共享恢复代码。

------

通过合理管理恢复代码，可以在紧急情况下确保访问 GitHub 账号的能力，同时保证安全性。

# TOTP原理

TOTP（Time-Based One-Time Password，基于时间的一次性密码）的原理基于以下几个关键概念和步骤：

------

### **1. 核心原理**

TOTP 是一种两步验证机制，它利用时间戳和共享的密钥生成一次性密码。这些密码通常每隔 30 秒更新一次，且每次都唯一。

TOTP 的核心基于以下算法：

- **HMAC（Hash-based Message Authentication Code）**：一种基于哈希函数（如 SHA-1、SHA-256）的消息认证码。
- **RFC 6238 标准**：定义了 TOTP 的计算方式。

------

### **2. 工作流程**

#### **a) 初始化阶段**

1. **共享密钥（Secret Key）**：
   - 服务器生成一个唯一的密钥，通常以 Base32 格式编码。
   - 用户将密钥导入 TOTP 应用（通过输入密钥或扫描二维码）。
2. **时间同步**：
   - TOTP 应用和服务器必须保持时间同步（一般通过 NTP 协议实现）。
   - 时间以 UNIX 时间戳（从 1970 年 1 月 1 日以来的秒数）为基准。

#### **b) 生成动态密码**

1. **时间片计算**：

   - 当前时间戳除以一个固定周期（如 30 秒），得到一个时间片（Time Step）。
   - 时间片是整数，代表当前时间范围内的编号。

   T=floor(current_timestamp/30)T = \text{floor}(\text{current\_timestamp} / 30)

2. **HMAC 计算**：

   - 用共享密钥和时间片作为输入，通过 HMAC 生成一个哈希值。
   - 哈希函数常用 SHA-1（或更高版本，如 SHA-256）。

3. **截取动态密码**：

   - 从 HMAC 的结果中取一部分（通常为 6 位或 8 位），生成一次性密码。

#### **c) 验证动态密码**

1. 用户在登录时输入 TOTP 应用生成的动态密码。
2. 服务器使用相同的密钥和时间片计算动态密码，并与用户输入的密码进行比较。
3. 如果匹配，验证通过；否则验证失败。

------

### **3. 公式总结**

#### TOTP 密码生成公式：

TOTP=truncate(HMAC(K,T))mod  10dTOTP = \text{truncate}(HMAC(K, T)) \mod 10^d

- **K**：共享密钥
- **T**：时间片
- **d**：密码位数（通常为 6 或 8）
- **truncate**：从 HMAC 结果中提取一段子串

------

### **4. 安全性保障**

1. **时间片短**：
   - 动态密码每隔 30 秒更新一次，暴力破解的时间窗口很短。
2. **共享密钥私密性**：
   - 共享密钥只存储在服务器和用户设备中，不通过网络传输。
3. **哈希算法抗碰撞**：
   - 使用 HMAC 确保生成的密码具有不可预测性。

------

### **5. 常见问题**

| 问题           | 原因                                   | 解决办法                                     |
| -------------- | -------------------------------------- | -------------------------------------------- |
| TOTP 验证失败  | 时间不同步（客户端和服务器时间不一致） | 确保设备启用自动时间同步（NTP）。            |
| 密码无法生成   | 共享密钥丢失或输入错误                 | 重新绑定密钥（需要管理员权限）。             |
| 动态密码被截获 | 恶意软件或钓鱼攻击                     | 开启硬件密钥验证（如 YubiKey）作为替代方案。 |

------

### **6. 应用场景**

- **账户登录**：GitHub、Google 等支持 TOTP 验证。
- **支付验证**：在线支付时生成动态密码。
- **服务器访问**：SSH 或管理面板登录的双因素认证。

TOTP 简单高效，广泛用于增强系统的安全性。

# 参考资料

1、解决GitHub下载速度太慢的问题

https://blog.csdn.net/qing666888/article/details/79123742

2、TortoiseGit保存用户名和密码的方法

https://www.cnblogs.com/sapho/p/6140331.html