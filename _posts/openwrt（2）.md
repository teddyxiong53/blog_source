---
title: openwrt（2）
date: 2025-04-10 19:22:37
tags:
	- openwrt
---

--

# Package/libconfig/install 这里为什么是小写字母开头？Build/InstallDev 这个为什么是首字母大写？命名的规律是什么？

在分析 OpenWrt 的 `libconfig` 软件包 `Makefile` 时，你提出了一个非常好的问题：为什么 `Package/libconfig/install` 使用小写字母开头，而 `Build/InstallDev` 使用首字母大写？这涉及到 OpenWrt 构建系统中定义块（`define`）的命名规律和约定。以下是详细解答：

---

### 1. OpenWrt 中 `define` 的命名规则
OpenWrt 的软件包 `Makefile` 使用 GNU Make 的 `define` 关键字来定义多行变量或函数，这些定义块会被构建系统解析并执行。命名规则并不是随机的，而是基于功能和上下文的约定，具体分为以下两类：

#### (1) `Package/` 开头的定义
- **格式**：`Package/<包名>/<目标>`，如 `Package/libconfig/install`。
- **命名特点**：
  - **小写开头**：`Package` 和后续的目标（如 `install`、`description`）通常使用小写。
  - **层级结构**：以 `Package/<包名>` 为前缀，表示与特定软件包的元数据或安装规则相关。
- **常见目标**：
  - `Package/<包名>`：定义包的基本属性（如 `SECTION`、`CATEGORY`）。
  - `Package/<包名>/description`：包的描述。
  - `Package/<包名>/install`：运行时安装规则。
  - `Package/<包名>/conffiles`：配置文件列表。
- **作用**：这些定义直接与生成的 `.ipk` 软件包相关，描述包的元信息和安装行为。

#### (2) `Build/` 开头的定义
- **格式**：`Build/<目标>`，如 `Build/InstallDev`。
- **命名特点**：
  - **首字母大写**：`Build` 和后续目标（如 `Configure`、`Compile`、`InstallDev`）使用驼峰命名法（CamelCase）。
  - **全局性**：不以特定包名为前缀，表示构建过程中的通用步骤。
- **常见目标**：
  - `Build/Configure`：自定义配置阶段。
  - `Build/Compile`：自定义编译阶段。
  - `Build/Install`：自定义安装阶段（完整安装）。
  - `Build/InstallDev`：安装开发文件（如头文件、库）。
- **作用**：这些定义覆盖构建系统的默认行为，适用于源码编译和安装的各个阶段。

---

### 2. 为什么 `Package/libconfig/install` 是小写？
- **约定原因**：
  - `Package/` 前缀下的目标是软件包的“属性”或“行为”，遵循 OpenWrt 的历史命名习惯，使用全小写。
  - 这类目标与最终生成的 `.ipk` 包直接相关，类似于元数据字段（如 `description`、`depends`），因此保持简洁和一致。
- **功能定位**：
  - `Package/libconfig/install` 定义了运行时文件（如 `libconfig.so`）如何安装到目标根文件系统。
  - 它是一个具体的、面向包的安装规则，与构建过程的通用步骤区分开。
- **历史背景**：
  - OpenWrt 的包系统源于早期嵌入式系统的简单设计，小写命名可能是为了与 shell 脚本或配置文件风格一致。

**示例**：
```makefile
define Package/libconfig/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libconfig.so* $(1)/usr/lib/
endef
```
- 这里 `install` 是包的安装逻辑，属于 `Package/libconfig` 的子目标。

---

### 3. 为什么 `Build/InstallDev` 是首字母大写？
- **约定原因**：
  - `Build/` 前缀下的目标是构建系统的“钩子”（hook），用于覆盖或扩展默认的构建流程。
  - 使用驼峰命名法（首字母大写）是为了与全局构建规则（如 `Build/Compile`）保持一致，同时突出其作为函数或方法的特性。
- **功能定位**：
  - `Build/InstallDev` 定义了开发文件（如头文件、库文件）如何安装到暂存目录（`staging_dir`），供其他包的编译依赖。
  - 它是构建过程中的一个阶段性步骤，与具体软件包无关，具有通用性。
- **设计理念**：
  - 驼峰命名反映了更现代化的编程风格，可能受到 C/C++ 或其他构建系统（如 CMake）的启发。

**示例**：
```makefile
define Build/InstallDev
	$(CP) $(PKG_INSTALL_DIR)/* $(1)/
endef
```
- 这里 `InstallDev` 是构建系统的一个钩子，处理开发文件的安装。

---

### 4. 命名规律总结

| **类别**   | **前缀**         | **命名风格** | **作用**                 | **示例**                    |
| ---------- | ---------------- | ------------ | ------------------------ | --------------------------- |
| `Package/` | `Package/<包名>` | 全小写       | 定义包的元数据和安装规则 | `Package/libconfig/install` |
| `Build/`   | `Build/`         | 驼峰命名     | 覆盖构建过程中的通用步骤 | `Build/InstallDev`          |

- **层次差异**：
  - `Package/` 是包级别的，绑定到具体软件包（如 `libconfig`），因此使用 `<包名>` 区分。
  - `Build/` 是构建级别的，适用于所有包，因此不带包名。
- **功能差异**：
  - `Package/.../install` 关注运行时文件，生成 `.ipk` 包的内容。
  - `Build/InstallDev` 关注开发文件，服务于交叉编译环境。

---

### 5. 为什么有这种差异？
- **历史演变**：
  - OpenWrt 的包系统设计较早，`Package/` 的小写命名可能沿袭了早期的简单约定。
  - `Build/` 的驼峰命名出现在后期，可能是为了与更现代化的构建系统（如 autotools）对齐。
- **语义区分**：
  - 小写表示“描述性”字段（如元数据）。
  - 驼峰表示“动作性”钩子（如构建步骤）。
- **避免冲突**：
  - 两种命名风格区分了包定义和构建逻辑，减少混淆。

---

### 6. 实际影响
- **调用方式**：
  - `Package/libconfig/install` 由 `BuildPackage` 模板自动调用，生成 `.ipk` 文件。
  - `Build/InstallDev` 在 `make package/libconfig/install` 或 `make package/libconfig/compile` 时触发，安装开发文件。
- **扩展性**：
  - 如果需要多个包（如 `libconfig` 和 `libconfig-dev`），可以定义多个 `Package/` 块，但 `Build/` 块保持单一。

---

### 7. 结论
- **`Package/libconfig/install` 小写**：因为它是包的安装规则，属于 `Package/` 下的元数据约定，历史和语义上使用全小写。
- **`Build/InstallDev` 首字母大写**：因为它是构建系统的钩子，遵循驼峰命名，突出其全局性和动作性。
- **规律**：`Package/` 用于包的静态描述（小写），`Build/` 用于构建的动态行为（驼峰）。

如果你对其他命名约定（如 `Host/`、`KernelPackage/`）或具体实现有疑问，欢迎继续探讨！

# Package/和Build/分别有哪些行为？给出完整列表

在 OpenWrt 的构建系统中，`Package/` 和 `Build/` 是两种主要的 `define` 定义块类型，它们分别用于不同的目的。`Package/` 定义与软件包相关的元数据和安装行为，而 `Build/` 定义构建过程中的自定义步骤。以下是对两者的完整行为列表及其详细说明，基于 OpenWrt 的源码和文档（截至 2025 年 4 月）。

---

### 1. `Package/` 定义的行为
`Package/<包名>/` 前缀用于定义软件包的属性和安装规则，与生成的 `.ipk` 文件直接相关。以下是完整的 `Package/` 子目标列表：

| **定义块**                      | **作用**                                                   | **示例**                                                     |
| ------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| `Package/<包名>`                | 定义软件包的基本元信息（如分类、标题、依赖等）。           | `SECTION:=libs`<br>`CATEGORY:=Libraries`<br>`TITLE:=Configuration File Library` |
| `Package/<包名>/description`    | 提供软件包的详细描述，显示在 `opkg info` 或 LuCI 中。      | `Libconfig is a simple library for manipulating structured configuration files...` |
| `Package/<包名>/install`        | 指定运行时文件的安装规则，决定哪些文件打包到 `.ipk` 中。   | `$(INSTALL_DIR) $(1)/usr/lib`<br>`$(CP) $(PKG_INSTALL_DIR)/usr/lib/libconfig.so* $(1)/usr/lib/` |
| `Package/<包名>/conffiles`      | 列出配置文件路径，标记为受保护文件（升级时保留用户修改）。 | `/etc/config/libconfig`                                      |
| `Package/<包名>/preinst`        | 定义安装前脚本（在解压 `.ipk` 前执行）。                   | `#!/bin/sh`<br>`echo "Checking system before installation..."` |
| `Package/<包名>/postinst`       | 定义安装后脚本（在解压 `.ipk` 后执行）。                   | `#!/bin/sh`<br>`echo "Installation completed!"`              |
| `Package/<包名>/prerm`          | 定义卸载前脚本（在移除文件前执行）。                       | `#!/bin/sh`<br>`echo "Removing libconfig..."`                |
| `Package/<包名>/postrm`         | 定义卸载后脚本（在移除文件后执行）。                       | `#!/bin/sh`<br>`rm -f /tmp/libconfig_temp`                   |
| `Package/<包名>/depends`        | 指定依赖的其他包（通常由 `DEPENDS` 变量替代，不常用）。    | `+libc +libpthread`                                          |
| `Package/<包名>/extra_provides` | 定义额外的虚拟包提供（较少使用）。                         | `Provides: config-lib`                                       |

#### 关键点
- **上下文**：这些定义与特定的 `<包名>` 绑定，通常与 `PKG_NAME` 一致。
- **调用时机**：
  - `Package/<包名>` 和 `description` 用于生成包元数据。
  - `install` 在 `make package/<包名>/install` 时执行，生成根文件系统内容。
  - `preinst`、`postinst`、`prerm`、`postrm` 被打包到 `.ipk` 的控制文件中，运行时由 `opkg` 执行。
- **扩展性**：可以定义多个包（如 `Package/libconfig` 和 `Package/libconfig-dev`），分别指定不同的 `install` 规则。

#### 示例完整定义
```makefile
define Package/libconfig
  SECTION:=libs
  CATEGORY:=Libraries
  TITLE:=Configuration File Library
  DEPENDS:=+libc
endef

define Package/libconfig/description
  Libconfig is a simple library for manipulating structured configuration files.
endef

define Package/libconfig/install
  $(INSTALL_DIR) $(1)/usr/lib
  $(CP) $(PKG_INSTALL_DIR)/usr/lib/libconfig.so* $(1)/usr/lib/
endef

define Package/libconfig/conffiles
  /etc/libconfig.conf
endef

define Package/libconfig/postinst
#!/bin/sh
echo "Libconfig installed."
endef
```

---

### 2. `Build/` 定义的行为
`Build/` 前缀用于自定义构建过程中的步骤，覆盖或扩展默认的编译、配置和安装行为。以下是完整的 `Build/` 子目标列表：

| **定义块**         | **作用**                                                     | **示例**                                                     |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `Build/Prepare`    | 自定义源码解压后的准备工作（如打补丁、创建目录）。           | `$(CP) ./files/* $(PKG_BUILD_DIR)/`<br>`$(call PatchDir,$(PKG_BUILD_DIR),./patches)` |
| `Build/Configure`  | 自定义配置阶段（默认调用 `./configure`），可覆盖参数或脚本。 | `$(Configure/Default)`<br>`--with-custom-option`             |
| `Build/Compile`    | 自定义编译阶段（默认调用 `make`），可指定额外命令。          | `$(MAKE) -C $(PKG_BUILD_DIR) all`                            |
| `Build/Install`    | 自定义完整安装阶段（默认调用 `make install`），安装到 `PKG_INSTALL_DIR`。 | `$(MAKE) -C $(PKG_BUILD_DIR) install DESTDIR=$(PKG_INSTALL_DIR)` |
| `Build/InstallDev` | 安装开发文件（如头文件、库）到 `staging_dir`，供其他包依赖。 | `$(CP) $(PKG_INSTALL_DIR)/* $(1)/`                           |
| `Build/Dist`       | 自定义源码分发的打包规则（较少使用）。                       | `tar -czf $(PKG_NAME)-dist.tar.gz $(PKG_BUILD_DIR)`          |
| `Build/DistCheck`  | 检查分发包的完整性（开发时使用，较少见）。                   | `tar -xzf $(PKG_NAME)-dist.tar.gz -C /tmp && make -C /tmp/$(PKG_NAME)` |

#### 关键点
- **上下文**：`Build/` 定义是全局的，不绑定特定包名，适用于当前软件包的构建流程。
- **调用时机**：
  - `Build/Prepare` 在解压源码后执行。
  - `Build/Configure` 在配置阶段执行（若未定义，使用 `package.mk` 默认规则）。
  - `Build/Compile` 在编译阶段执行。
  - `Build/Install` 在安装阶段执行（若 `PKG_INSTALL=1`，默认触发）。
  - `Build/InstallDev` 在安装开发文件时执行。
- **默认行为**：
  - 如果不定义这些块，OpenWrt 使用 `package.mk` 提供的默认规则（如 `./configure`、`make`、`make install`）。
- **变量**：
  - `$(PKG_BUILD_DIR)`：源码解压目录（如 `build_dir/target-<arch>/libconfig-1.4.9`）。
  - `$(PKG_INSTALL_DIR)`：临时安装目录。
  - `$(1)`：目标目录（由构建系统传入，如 `staging_dir` 或根文件系统）。

#### 示例完整定义
```makefile
define Build/Prepare
  $(CP) ./files/config.h $(PKG_BUILD_DIR)/
endef

define Build/Configure
  $(call Build/Configure/Default,--enable-shared)
endef

define Build/Compile
  $(MAKE) -C $(PKG_BUILD_DIR) CFLAGS="$(TARGET_CFLAGS)"
endef

define Build/InstallDev
  $(INSTALL_DIR) $(1)/usr/include
  $(CP) $(PKG_INSTALL_DIR)/usr/include/libconfig.h $(1)/usr/include/
  $(CP) $(PKG_INSTALL_DIR)/usr/lib/libconfig.so* $(1)/usr/lib/
endef
```

---

### 3. `Package/` 与 `Build/` 的对比

| **特性**     | **Package/**                 | **Build/**                        |
| ------------ | ---------------------------- | --------------------------------- |
| **前缀**     | `Package/<包名>`             | `Build/`                          |
| **命名风格** | 全小写                       | 驼峰命名（CamelCase）             |
| **作用范围** | 特定软件包的元数据和安装规则 | 构建过程中的通用步骤              |
| **目标**     | 生成 `.ipk` 文件和运行时行为 | 控制源码的编译和安装              |
| **调用者**   | `BuildPackage` 模板和 `opkg` | 构建系统（`make package/...`）    |
| **典型变量** | `SECTION`、`DEPENDS`、`$(1)` | `PKG_BUILD_DIR`、`CONFIGURE_ARGS` |

#### 功能分工
- **`Package/`**：面向最终用户，定义包的“外在”属性和安装内容。
- **`Build/`**：面向开发者，控制包的“内在”构建流程。

#### 执行顺序
1. `Build/Prepare` → `Build/Configure` → `Build/Compile` → `Build/Install`（构建源码）。
2. `Build/InstallDev`（安装开发文件到 `staging_dir`）。
3. `Package/<包名>/install`（安装运行时文件到根文件系统）。
4. 生成 `.ipk`，嵌入 `preinst`、`postinst` 等脚本。

---

### 4. 实际应用中的注意事项
- **重叠功能**：
  - `Build/Install` 和 `Package/<包名>/install` 都涉及安装，但前者是源码安装到临时目录，后者是选择性安装到目标文件系统。
- **默认行为覆盖**：
  - 如果不定义 `Build/Compile`，系统会执行 `make`，但你可以用自定义命令替换。
- **多包支持**：
  - 一个 `Makefile` 可以定义多个 `Package/` 块（如 `libconfig` 和 `libconfig-dev`），但 `Build/` 块只定义一次，共享构建逻辑。

---

### 5. 结论
- **`Package/`** 有 8 个常见行为，专注于包的描述和运行时安装。
- **`Build/`** 有 7 个常见行为，专注于源码的构建和开发文件处理。
- 两者的命名和功能清晰区分，确保构建系统的模块化和可扩展性。

如果你需要某个行为的更详细示例或有其他疑问，欢迎继续提问！

# 每个package下面的常用目录列表说明，例如PKG_INSTALL_DIR

在 OpenWrt 的构建系统中，每个软件包（`package`）的 `Makefile` 定义了其构建和安装行为，而构建过程中会涉及多个目录。这些目录由构建系统自动生成和管理，用于存储源码、中间文件和最终输出。以下是每个 `package` 下常用的目录列表及其说明，包括你提到的 `PKG_INSTALL_DIR`，并结合 OpenWrt 的工作机制进行详细分析。

---

### 1. 常用目录列表及说明

| **目录变量**      | **路径示例**                                   | **作用**                                                     |
| ----------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| `PKG_BUILD_DIR`   | `build_dir/target-<arch>/<pkg_name>-<version>` | 软件包源码解压和编译的工作目录，包含解压后的源码和中间文件（如 `.o` 文件）。 |
| `PKG_INSTALL_DIR` | `<PKG_BUILD_DIR>/ipkg-install`                 | 源码执行 `make install` 后的临时安装目录，存放完整的安装文件（如二进制、库、头文件）。 |
| `PKG_SOURCE_DIR`  | `<PKG_BUILD_DIR>`                              | 源码解压后的根目录，通常与 `PKG_BUILD_DIR` 相同，用于原始源码文件。 |
| `STAGING_DIR`     | `staging_dir/target-<arch>`                    | 全局暂存目录，存放所有包的开发文件（如头文件、库），供交叉编译依赖使用。 |
| `TARGET_DIR`      | `staging_dir/target-<arch>/root-<arch>`        | 目标设备的根文件系统目录，存放运行时文件，最终打包到固件中。 |
| `DL_DIR`          | `dl/`                                          | 下载目录，存放从 `PKG_SOURCE_URL` 下载的源码文件（如 `.tar.gz`）。 |
| `BIN_DIR`         | `bin/targets/<target>/<subtarget>/packages`    | 最终输出目录，存放生成的 `.ipk` 文件和固件镜像。             |
| `TMP_DIR`         | `tmp/`                                         | 临时目录，存放构建过程中的临时文件（如日志、状态文件），随时可能被清理。 |

---

### 2. 每个目录的详细说明

#### (1) `PKG_BUILD_DIR`
- **定义**：每个软件包的独立构建目录，由 `package.mk` 根据 `PKG_NAME` 和 `PKG_VERSION` 动态生成。
- **路径示例**：`build_dir/target-arm_cortex-a9+neon_musl_eabi/libconfig-1.4.9`
- **作用**：
  - 源码解压后存放于此。
  - 编译过程中生成的对象文件（`.o`）、可执行文件等也在这里。
- **生命周期**：
  - `make package/<pkg_name>/compile` 时创建和使用。
  - `make clean` 会清理此目录。
- **使用场景**：
  - 在 `Build/Compile` 中指定编译命令：`$(MAKE) -C $(PKG_BUILD_DIR)`。

#### (2) `PKG_INSTALL_DIR`
- **定义**：软件包源码执行 `make install` 后的临时安装目录，通常是 `PKG_BUILD_DIR` 的子目录。
- **路径示例**：`build_dir/target-<arch>/libconfig-1.4.9/ipkg-install`
- **作用**：
  - 存放源码安装的完整文件结构（如 `/usr/lib/`、`/usr/include/`）。
  - 作为中间缓冲区，供后续选择性安装到 `STAGING_DIR` 或 `TARGET_DIR`。
- **生命周期**：
  - 当 `PKG_INSTALL=1` 时，由 `Build/Install` 默认创建（执行 `make install DESTDIR=$(PKG_INSTALL_DIR)`）。
  - `make clean` 会清理。
- **使用场景**：
  - 在 `Package/<pkg_name>/install` 中引用：`$(CP) $(PKG_INSTALL_DIR)/usr/lib/libconfig.so* $(1)/usr/lib/`。

#### (3) `PKG_SOURCE_DIR`
- **定义**：源码解压后的根目录，通常与 `PKG_BUILD_DIR` 相同。
- **路径示例**：同 `PKG_BUILD_DIR`
- **作用**：
  - 存放原始源码文件（如 `configure`、`Makefile`）。
  - 在某些复杂包中，可能与补丁后的构建目录分离（较少见）。
- **生命周期**：与 `PKG_BUILD_DIR` 一致。
- **使用场景**：
  - 在 `Build/Prepare` 中操作原始文件：`$(CP) ./files/* $(PKG_SOURCE_DIR)/`。

#### (4) `STAGING_DIR`
- **定义**：全局暂存目录，分为目标架构部分（`target-<arch>`）和工具链部分（`toolchain-<arch>`）。
- **路径示例**：`staging_dir/target-arm_cortex-a9+neon_musl_eabi`
- **作用**：
  - 存放所有软件包的开发文件（如头文件 `.h`、库 `.so`、`.a`），供交叉编译时引用。
  - 由 `Build/InstallDev` 填充。
- **生命周期**：
  - 跨多个包共享，`make dirclean` 清理。
- **使用场景**：
  - 在 `Build/InstallDev` 中安装开发文件：`$(CP) $(PKG_INSTALL_DIR)/usr/include/* $(1)/usr/include/`。

#### (5) `TARGET_DIR`
- **定义**：目标设备的根文件系统目录，最终集成到固件镜像中。
- **路径示例**：`staging_dir/target-arm_cortex-a9+neon_musl_eabi/root-ramips`
- **作用**：
  - 存放运行时文件（如二进制、库、配置文件），由 `Package/<pkg_name>/install` 填充。
  - 反映设备上的文件结构（如 `/usr/lib/`、`/etc/`）。
- **生命周期**：
  - `make dirclean` 清理。
- **使用场景**：
  - 在 `Package/<pkg_name>/install` 中安装运行时文件：`$(INSTALL_DIR) $(1)/usr/bin`。

#### (6) `DL_DIR`
- **定义**：全局下载目录，位于源码根目录。
- **路径示例**：`dl/libconfig-1.4.9.tar.gz`
- **作用**：
  - 存储从 `PKG_SOURCE_URL` 下载的源码文件。
  - 支持缓存，避免重复下载。
- **生命周期**：
  - `make distclean` 清理。
- **使用场景**：
  - 由 `PKG_SOURCE` 自动引用，用户通常不直接操作。

#### (7) `BIN_DIR`
- **定义**：最终输出目录，按目标平台和子目标组织。
- **路径示例**：`bin/targets/ramips/mt7621/packages/libconfig_1.4.9-1_mipsel_24kc.ipk`
- **作用**：
  - 存放生成的 `.ipk` 文件和固件镜像。
  - 用户直接使用这些文件刷机或安装。
- **生命周期**：
  - `make dirclean` 清理。
- **使用场景**：
  - 由 `BuildPackage` 自动生成，无需手动操作。

#### (8) `TMP_DIR`
- **定义**：全局临时目录，位于源码根目录。
- **路径示例**：`tmp/<random_id>.log`
- **作用**：
  - 存放构建过程中的临时文件，如日志、状态标记等。
- **生命周期**：
  - 随时可能被覆盖或删除，`make clean` 清理。
- **使用场景**：
  - 构建系统内部使用，用户很少直接操作。

---

### 3. 目录之间的关系和流程
以下是 OpenWrt 构建系统中目录的典型工作流程：
1. **下载**：源码从 `PKG_SOURCE_URL` 下载到 `DL_DIR`。
2. **解压**：源码解压到 `PKG_BUILD_DIR`（`PKG_SOURCE_DIR`）。
3. **编译**：在 `PKG_BUILD_DIR` 执行 `Build/Configure` 和 `Build/Compile`。
4. **安装**：
   - `Build/Install` 将文件安装到 `PKG_INSTALL_DIR`。
   - `Build/InstallDev` 从 `PKG_INSTALL_DIR` 复制开发文件到 `STAGING_DIR`。
   - `Package/<pkg_name>/install` 从 `PKG_INSTALL_DIR` 复制运行时文件到 `TARGET_DIR`。
5. **打包**：`TARGET_DIR` 的内容集成到固件，`.ipk` 文件输出到 `BIN_DIR`。

#### 图示
```
DL_DIR → PKG_BUILD_DIR → PKG_INSTALL_DIR → STAGING_DIR (开发文件)
                                 ↓           → TARGET_DIR (运行时文件)
                                 ↓
                               BIN_DIR (.ipk 和固件)
```

---

### 4. 示例：`libconfig` 的目录使用
以 `libconfig` 的 `Makefile` 为例：
```makefile
define Build/InstallDev
	$(CP) $(PKG_INSTALL_DIR)/* $(1)/
endef

define Package/libconfig/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libconfig.so* $(1)/usr/lib/
endef
```
- **`PKG_INSTALL_DIR`**：源码 `make install` 后的临时目录，包含所有文件（如 `/usr/lib/libconfig.so`、`/usr/include/libconfig.h`）。
- **`$(1)` 在 `Build/InstallDev`**：指向 `STAGING_DIR`，安装所有文件供开发使用。
- **`$(1)` 在 `Package/libconfig/install`**：指向 `TARGET_DIR`，只安装共享库到 `/usr/lib/`。

最终：
- `STAGING_DIR/usr/lib/libconfig.so`（开发用）。
- `TARGET_DIR/usr/lib/libconfig.so`（运行时用）。
- `BIN_DIR/libconfig_1.4.9-1_<arch>.ipk`（输出包）。

---

### 5. 注意事项
- **动态生成**：这些目录由构建系统根据 `.config`（目标架构）和 `PKG_NAME` 自动生成。
- **隔离性**：每个包的 `PKG_BUILD_DIR` 和 `PKG_INSTALL_DIR` 是独立的，避免冲突。
- **清理**：
  - `make clean`：清理 `PKG_BUILD_DIR` 和 `PKG_INSTALL_DIR`。
  - `make dirclean`：清理 `STAGING_DIR`、`TARGET_DIR`、`BIN_DIR`。
  - `make distclean`：清理 `DL_DIR` 和 `TMP_DIR`。

---

### 6. 结论
OpenWrt 的目录设计清晰分工：
- `DL_DIR` 和 `BIN_DIR` 处理输入和输出。
- `PKG_*` 目录管理单个包的构建。
- `STAGING_DIR` 和 `TARGET_DIR` 分别服务于开发和运行时。
这些目录通过 `Package/` 和 `Build/` 定义块灵活使用，确保构建过程的模块化和可控性。

如果你需要某个目录的更深入分析或具体用法示例，请告诉我！
