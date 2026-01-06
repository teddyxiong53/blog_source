---
title: yocto（2）
date: 2025-09-10 16:21:37
tags:
	- yocto
---

--

# BUILD_ARCH、HOST_ARCH、TUNE_ARCH、TARGET_ARCH、PACKAGE_ARCH这些的区别和关系

很好，这几个变量在Yocto里经常让人混淆，我给你梳理一下它们的含义和关系：

| 变量             | 含义                                                   | 举例                                       | 说明                                                         |
| ---------------- | ------------------------------------------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| **BUILD_ARCH**   | 构建机架构 (build machine architecture)                | `x86_64`                                   | 你当前运行 `bitbake` 的主机架构。用于编译工具链本身。        |
| **HOST_ARCH**    | 运行工具链和编译器的架构 (host architecture for tools) | `x86_64`                                   | 指执行交叉编译工具的环境架构，一般和 BUILD_ARCH 相同（除非做 Canadian Cross）。 |
| **TUNE_ARCH**    | Yocto “tuning” 配置选出的目标 CPU 架构                 | `arm`、`aarch64`                           | 根据 `TUNE_FEATURES` 选出来的架构，比如 `armv7a`、`cortexa53`。影响 `TARGET_ARCH`。 |
| **TARGET_ARCH**  | 最终目标系统的架构 (target architecture)               | `arm`、`aarch64`                           | 表示要为哪个架构生成 rootfs 和 kernel。通常由 `TUNE_ARCH` 决定。 |
| **PACKAGE_ARCH** | 软件包架构 (package architecture)                      | `all`、`armv7a`、`cortexa53`、`qemux86_64` | 描述某个包能在哪些目标机型上复用。• `all`：架构无关，比如脚本、配置文件• `TUNE_PKGARCH`：和 CPU 优化相关• `MACHINE_ARCH`：与具体硬件绑定 |

**关系总结**

1. **BUILD_ARCH** → 你本机。
2. **HOST_ARCH** → 构建工具的运行环境，通常=BUILD_ARCH。
3. **TUNE_ARCH** → 通过 `TUNE_FEATURES` 推导出的 CPU 架构。
4. **TARGET_ARCH** → 最终 rootfs 的架构，由 TUNE_ARCH 派生。
5. **PACKAGE_ARCH** → 粒度更细，决定一个包是否能跨不同 machine/tune 复用。

典型场景：

- 你在 **x86_64 PC (BUILD/HOST_ARCH=x86_64)** 上，编译 **armv7a 的 rootfs (TUNE_ARCH=arm, TARGET_ARCH=arm)**。
- 生成的某些包是架构无关的（`PACKAGE_ARCH=all`），有些包跟 CPU 优化有关（`PACKAGE_ARCH=armv7a`），有些包跟具体板子绑定（`PACKAGE_ARCH=mesona4_ba400`）。



# PN

你贴的这一段其实是 Yocto **包名/版本/修订号的生成逻辑**，我来逐行拆解：

| 变量         | 含义                         | 逻辑                                                         | 举例                       |
| ------------ | ---------------------------- | ------------------------------------------------------------ | -------------------------- |
| **PN**       | Package Name，包名           | 从 `FILE`（配方文件路径）里解析出来的第一个元素；如果失败就用 `defaultpkgname` | `busybox`                  |
| **PV**       | Package Version，版本号      | 从 `FILE` 解析的第二个元素；默认 `1.0`                       | `1.36.1`                   |
| **PR**       | Package Revision，修订号     | 从 `FILE` 解析的第三个元素；默认 `r0`                        | `r0`、`r1`                 |
| **PE**       | Package Epoch，epoch         | 默认空字符串                                                 | 一般不用，除非需要强制升级 |
| **EXTENDPE** | epoch 的扩展前缀             | 如果 `PE > 0`，则是 `"${PE}_"`，否则空                       | `1_`                       |
| **PF**       | 包的全名 (full package name) | `${PN}-${EXTENDPE}${PV}-${PR}`                               | `busybox-1.36.1-r0`        |
| **P**        | 不含 revision 的包名         | `${PN}-${PV}`                                                | `busybox-1.36.1`           |

**核心关系**：

- `PN`、`PV`、`PR`、`PE` → 构成包的唯一标识。
- `PF` = 最终带 revision 的完整名字。
- `P` = 没带 revision 的版本号。

**例子**
 假设 `FILE = recipes-core/busybox/busybox_1.36.1.bb`：

- `PN = busybox`
- `PV = 1.36.1`
- `PR = r0` (默认)
- `PE = ""`
- `PF = busybox-1.36.1-r0`
- `P = busybox-1.36.1`

所以这套逻辑保证每个 `.bb` 文件可以自动提取出包名/版本号，形成唯一的 **recipe identity**。

# PRSERV_PV_AUTOINC 

这是Yocto Project中PRSERV（Package Revision Service）的一个配置选项。

PRSERV_PV_AUTOINC = "AUTOINC" 表示当包版本号需要自动递增时，PRSERV会自动处理版本号的递增，而不需要手动干预。

这个设置通常用于开发过程中，当配方(recipe)的版本需要频繁更新时，可以自动维护版本号的递增记录。

# TCMODE

这三行是 Yocto **配置层的变量定义**，我给你逐条解释：

| 变量       | 作用                          | 默认值          | 说明                                                         |
| ---------- | ----------------------------- | --------------- | ------------------------------------------------------------ |
| **TCMODE** | Toolchain Mode，工具链模式    | `"default"`     | 控制使用哪种交叉工具链模式。• `default` = Yocto 自己构建的工具链• `external` = 使用外部工具链 (如 Sourcery、Linaro) |
| **TCLIBC** | Toolchain C Library，C 标准库 | `"glibc"`       | 决定目标 rootfs 使用的 C 库。常见取值：• `glibc`（全功能）• `musl`（轻量，嵌入式常用）• `uclibc`（已过时，Yocto 新版移除了） |
| **TMPDIR** | 临时工作目录                  | `${TOPDIR}/tmp` | 所有编译的中间产物、sstate、工作目录都会放在这里。通常是 Yocto 构建树里的 `tmp/`。 |

**关系**

- `TCMODE` + `TCLIBC` 决定编译工具链和目标系统的基础 ABI 环境。
- `TMPDIR` 决定编译输出存放位置，几乎所有 bitbake 的工作都在这里展开。

**例子**

1. 如果配置：

```
TCMODE = "external"
TCLIBC = "musl"
```

那就表示：用外部工具链，并且目标 rootfs 使用 musl libc。

1. 默认：

```
TCMODE = "default"
TCLIBC = "glibc"
TMPDIR = "${TOPDIR}/tmp"
```

就意味着：用 Yocto 自己构建的交叉工具链，目标系统用 glibc，所有输出放在 `build/tmp`。

要不要我帮你画一个表格，展示不同 **TCMODE+TCLIBC** 的组合对最终 rootfs 的影响？

# ptest

`ptest` 是 Yocto 提供的 **包级测试机制**，主要用来在目标板上运行软件自带的测试用例。

| 项目         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| **全称**     | Package Test                                                 |
| **目标**     | 把上游软件的测试套件集成进 Yocto 包，方便在目标 rootfs 上验证功能是否正常 |
| **配置开关** | 在 `local.conf` 里加：`DISTRO_FEATURES_append = " ptest"`启用后构建时会生成 `*-ptest` 包 |
| **构建结果** | 对应的软件会多一个 `package-ptest` 包，比如 `busybox-ptest`、`glibc-ptest` |
| **安装目录** | 测试脚本和数据放在 `/usr/lib/<pkg>/ptest/`                   |
| **运行方式** | 在目标机上运行：`ptest-runner` 或者直接 `cd /usr/lib/<pkg>/ptest && ./run-ptest` |
| **使用场景** | - 验证交叉编译结果是否正常运行- 做功能回归测试- CI/CD 自动化测试 |

**例子**

1. 在配方里启用 ptest：

```bitbake
inherit ptest
```

1. 构建时会生成额外的包：

```
glibc
glibc-ptest
```

1. 在目标机上运行：

```sh
opkg install glibc-ptest
ptest-runner
```

**优缺点**

| 优点                               | 缺点                                       |
| ---------------------------------- | ------------------------------------------ |
| 自动化测试上游软件功能，提升可靠性 | 增加构建时间和 rootfs 体积                 |
| 支持在 CI/CD、硬件板子上做验证     | 测试结果可能依赖运行环境，不保证 100% 通过 |

要不要我帮你整理一张 **常见 Yocto 包 ptest 支持情况表**（比如 busybox、glibc、systemd 等哪些自带 ptest）？

# meta recipe

这个 `poky/meta/recipes-core/meta/build-sysroots.bb` 是一个 **特殊的 Yocto 配方**，它和普通软件包不一样，主要作用是 **驱动 sysroot 构建过程**。我来逐层拆解：

| 项目         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| **文件位置** | `meta/recipes-core/meta/build-sysroots.bb`                   |
| **类别**     | *meta-recipe*（元配方，不是真正的软件包）                    |
| **作用**     | 用来触发 `populate_sysroot` 任务，把编译好的库和头文件安装到 sysroot 目录（host sysroot 和 target sysroot），供其它包编译时使用 |
| **PN**       | 固定为 `build-sysroots`，不会生成最终的 rootfs 包            |
| **关键任务** | - `do_populate_sysroot`：收集依赖配方的 sysroot 内容- `do_build`：保证 sysroot 在整个构建过程中是可用的 |
| **依赖**     | 依赖所有需要提供 sysroot 内容的 recipe（例如编译器、glibc、headers 等） |
| **安装位置** | - `${TMPDIR}/sysroots-components/*`（分组件的 sysroot）- `${WORKDIR}/sysroot-destdir/`（打包时的临时目录）- `${SYSROOT_DESTDIR}`（最终合并 sysroot） |

**为什么需要它？**

- Yocto 是 **分层构建**，每个 recipe 自己只关心编译和安装；
- 但是要保证别的 recipe 在编译时能找到头文件和库，就必须有个机制来收集和安装 sysroot；
- 这个 `build-sysroots.bb` 就是专门用来 orchestrate（编排）整个 sysroot 构建过程。

**例子**
 当你在 Yocto 构建 `busybox` 时：

1. `busybox.bb` 需要交叉编译器和 libc 头文件
2. 这些来自 `gcc-runtime.bb`、`glibc.bb` 的 `do_populate_sysroot` 输出
3. `build-sysroots.bb` 会把这些依赖的内容汇总到 `${TMPDIR}/sysroots/${MACHINE}`
4. `busybox` 的 `do_compile` 阶段就能正确找到这些头文件和库

**总结**
 `build-sysroots.bb` 并不是一个给 rootfs 打包的 recipe，而是 Yocto 内部用来维护 **构建时 sysroot 环境一致性** 的“调度配方”。

要不要我帮你画一个 **sysroot 构建流程图**（从 recipe → do_populate_sysroot → build-sysroots → 最终 sysroot）？

# BBFILE_COLLECTIONS有什么用？

在 BitBake 中，`BBFILE_COLLECTIONS` 是一个关键变量，通常在层的配置文件（`conf/layer.conf`）中定义，用于标识和组织层的集合（collections）。它在 Yocto 项目等基于 BitBake 的构建系统中扮演重要角色，帮助管理多个层之间的配方和资源。以下是对 `BBFILE_COLLECTIONS` 的详细说明：

### 1. **BBFILE_COLLECTIONS 的作用**
`BBFILE_COLLECTIONS` 的主要作用是：
- **定义层的集合名称**：为一个层分配一个唯一的标识符（集合名称），用于区分不同的层。
- **支持多层管理**：在包含多个层的复杂项目中，`BBFILE_COLLECTIONS` 允许 BitBake 区分来自不同层的配方（recipes）、附加文件（append files）和其他资源。
- **避免冲突**：通过为每个层定义唯一的集合名称，BitBake 可以处理同名配方或文件的情况，结合 `BBFILE_PRIORITY` 来决定优先级。

### 2. **BBFILE_COLLECTIONS 的定义**
`BBFILE_COLLECTIONS` 通常在 `conf/layer.conf` 文件中设置，格式为一个或多个集合名称的列表。每个层通常定义一个唯一的集合名称。

示例 `layer.conf`：
```bash
BBFILE_COLLECTIONS += "custom-layer"
BBFILE_PRIORITY_custom-layer = "5"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"
BBFILE_PATTERN_custom-layer = "^${LAYERDIR}/"
```

在这个例子中：
- `BBFILE_COLLECTIONS += "custom-layer"` 将 `custom-layer` 添加到集合列表，表示这个层属于名为 `custom-layer` 的集合。
- 集合名称 `custom-layer` 会被用来关联该层的其他变量，如 `BBFILE_PRIORITY_custom-layer` 和 `BBFILE_PATTERN_custom-layer`。

### 3. **BBFILE_COLLECTIONS 的工作机制**
- **集合名称的唯一性**：每个层的 `BBFILE_COLLECTIONS` 名称应该是唯一的，BitBake 使用这个名称来区分不同层的配方和资源。
- **与 BBFILES 的关系**：`BBFILE_COLLECTIONS` 与 `BBFILES` 一起使用，`BBFILES` 定义了层中配方文件的路径，而 `BBFILE_COLLECTIONS` 提供这些文件的命名空间。
- **优先级管理**：当多个层提供同名配方时，BitBake 使用 `BBFILE_COLLECTIONS` 结合 `BBFILE_PRIORITY` 来决定使用哪个层的配方。例如，优先级较高的层的配方会覆盖优先级较低的层的同名配方。
- **动态解析**：BitBake 在解析 `BBLAYERS`（在 `bblayers.conf` 中定义的层列表）时，会读取每个层的 `layer.conf`，并将 `BBFILE_COLLECTIONS` 中的集合名称加入全局配置。

### 4. **典型用法**
`BBFILE_COLLECTIONS` 通常与以下变量一起使用：
- **`BBFILE_PATTERN_<collection>`**：定义层的路径匹配模式，通常设置为 `${LAYERDIR}/`，表示该层的根目录。
- **`BBFILE_PRIORITY_<collection>`**：设置层的优先级，决定同名配方或文件的解析顺序。
- **`BBFILES`**：指定层中配方文件（`.bb`）和附加文件（`.bbappend`）的路径。

示例：
假设有两个层，`meta-foo` 和 `meta-bar`，它们的 `layer.conf` 如下：

**meta-foo/conf/layer.conf**：

```bash
BBFILE_COLLECTIONS += "foo-layer"
BBFILE_PRIORITY_foo-layer = "6"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb"
BBFILE_PATTERN_foo-layer = "^${LAYERDIR}/"
```

**meta-bar/conf/layer.conf**：
```bash
BBFILE_COLLECTIONS += "bar-layer"
BBFILE_PRIORITY_bar-layer = "5"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb"
BBFILE_PATTERN_bar-layer = "^${LAYERDIR}/"
```

如果两个层都包含一个配方 `example_1.0.bb`，BitBake 会优先选择 `meta-foo` 中的配方，因为 `foo-layer` 的优先级（6）高于 `bar-layer` 的优先级（5）。

### 5. **实际应用场景**
- **多层项目**：在 Yocto 项目中，通常有多个层（如 `meta`, `meta-poky`, `meta-oe`, 自定义层等）。`BBFILE_COLLECTIONS` 确保每个层的配方和资源被正确分类和解析。
- **配方覆盖**：当你需要覆盖某个层的配方（例如，修改 `meta` 层的某个配方），可以在自定义层中使用相同的配方名称，并通过 `BBFILE_COLLECTIONS` 和 `BBFILE_PRIORITY` 控制优先级。
- **模块化开发**：`BBFILE_COLLECTIONS` 使得层可以独立开发和共享，而不会与其他层的配方冲突。

### 6. **注意事项**
- **集合名称唯一性**：确保每个层的 `BBFILE_COLLECTIONS` 名称是唯一的，避免命名冲突。如果两个层使用相同的集合名称，BitBake 可能报错或行为不可预测。
- **优先级配置**：`BBFILE_PRIORITY_<collection>` 必须与 `BBFILE_COLLECTIONS` 中的名称对应，否则优先级设置无效。
- **调试**：如果层未被正确解析，可以检查 `BBFILE_COLLECTIONS` 是否正确设置，使用以下命令查看：
  ```bash
  bitbake -e | grep ^BBFILE_COLLECTIONS=
  ```
  这会显示所有已注册的集合名称。

- **与 BBPATH 的关系**：`BBFILE_COLLECTIONS` 定义了逻辑上的层标识，而 `BBPATH` 提供实际的文件搜索路径。两者结合使用，确保 BitBake 能找到并正确解析层的文件。

### 7. **总结**
`BBFILE_COLLECTIONS` 是 BitBake 中用于标识层的集合名称的变量，帮助组织和区分多层环境中的配方和资源。它与 `BBFILE_PRIORITY` 和 `BBFILES` 等变量配合使用，支持层的模块化管理和配方优先级控制。在 Yocto 项目中，正确配置 `BBFILE_COLLECTIONS` 是构建可扩展和可维护项目的关键。

如果你有关于 `BBFILE_COLLECTIONS` 的具体问题或需要更详细的配置示例，请告诉我！

# BBFILE_PRIORITY优先级

在 BitBake 中，`BBFILE_PRIORITY` 的优先级设置直接影响多个层（layers）提供同名配方（recipe）或文件时的选择顺序。决定 `BBFILE_PRIORITY` 的值通常需要根据项目的需求、层的用途以及层之间的依赖关系来综合考虑。以下是一些关于如何决定 `BBFILE_PRIORITY` 优先级的指导原则和常见实践：

### 1. **理解层的角色和用途**
不同层的功能和定位会影响优先级的设置。以下是常见的层类型及其优先级设置的考虑：
- **基础层**（如 `meta`）：这些层通常提供核心配方（如内核、工具链等），优先级应设置为中等或较低（例如 5 或 6），以允许其他层覆盖。
- **扩展层**（如 `meta-oe`, `meta-poky`）：这些层提供附加功能或第三方软件包，通常优先级略高于基础层（例如 6 或 7），但低于自定义层。
- **自定义层**（如 `meta-custom`）：如果需要覆盖基础层或扩展层的配方，自定义层的优先级应设置较高（例如 8 或 9）。
- **硬件特定层**（如 `meta-bsp`）：板级支持包（BSP）层通常包含特定硬件的配置，优先级往往最高（例如 9 或 10），以确保硬件相关的配方优先于通用配方。

**原则**：功能越特定、越需要覆盖其他层的配方，优先级应越高。

### 2. **优先级的典型范围**
- `BBFILE_PRIORITY` 的值通常是整数，范围可以从 1 到 10（或更高），但大多数项目使用 1 到 10 的范围。
- **低优先级（1-4）**：用于通用或基础层，这些层的配方通常是默认实现，允许被覆盖。
- **中等优先级（5-7）**：用于扩展层或通用功能层，平衡覆盖和被覆盖的可能性。
- **高优先级（8-10）**：用于自定义层、BSP 层或其他需要优先于其他层的场景。

**示例**：
- `meta`（核心层）：`BBFILE_PRIORITY = "5"`
- `meta-poky`（发行版层）：`BBFILE_PRIORITY = "6"`
- `meta-oe`（开源扩展层）：`BBFILE_PRIORITY = "7"`
- `meta-custom`（自定义层）：`BBFILE_PRIORITY = "8"`
- `meta-bsp`（硬件支持层）：`BBFILE_PRIORITY = "9"`

### 3. **根据覆盖需求设置优先级**
- **覆盖默认配方**：如果你需要在自定义层中修改某个配方（如更改 `busybox` 的配置），将自定义层的 `BBFILE_PRIORITY` 设置为高于提供默认配方的层。例如，如果 `meta` 提供 `busybox_1.35.bb`（优先级 5），而你想用 `meta-custom` 的版本覆盖它，则将 `meta-custom` 的优先级设为 6 或更高。
- **附加文件（.bbappend）**：如果使用 `.bbappend` 文件来修改配方，BitBake 会自动应用所有匹配的 `.bbappend` 文件（无论优先级），但基础配方的选择仍由 `BBFILE_PRIORITY` 决定。

**原则**：确保需要覆盖的层的优先级高于被覆盖的层。

### 4. **考虑层的依赖关系**
- **层依赖**：某些层可能依赖其他层的配方或类文件（通过 `LAYERDEPENDS` 指定）。依赖层的优先级通常应低于主层，以避免意外覆盖。
  - 例如，如果 `meta-custom` 依赖 `meta-oe`，则 `meta-oe` 的优先级应低于 `meta-custom`（如 `meta-oe = 7`, `meta-custom = 8`）。
- **检查层依赖**：在 `layer.conf` 中，`LAYERDEPENDS_<collection>` 定义了依赖关系，确保优先级设置与依赖关系一致。

### 5. **避免冲突和歧义**
- **保持优先级差异**：为每个层设置不同的优先级值，避免多个层具有相同优先级导致的歧义。如果优先级相同，BitBake 会根据 `BBPATH` 的顺序决定，这可能导致不可预测的行为。
- **测试优先级设置**：在多层项目中，运行以下命令检查配方解析情况：
  ```bash
  bitbake -e <recipe> | grep ^BBFILE_PRIORITY
  ```
  或使用：
  ```bash
  bitbake-layers show-recipes <recipe>
  ```
  确认 BitBake 选择了预期的配方。

### 6. **常见实践和约定**
- **Yocto 项目中的默认优先级**：Yocto 官方层通常遵循一些约定：
  - `meta`：优先级 5（核心层，提供基础配方）。
  - `meta-poky`：优先级 6（发行版相关配置）。
  - `meta-oe`：优先级 7（开源软件扩展）。
  - BSP 层（如 `meta-intel`, `meta-raspberrypi`）：优先级 8 或 9。
- **自定义层优先级**：自定义层通常设置为 8 或更高，以覆盖默认层。
- **动态调整**：在开发阶段，可能需要频繁调整优先级以测试不同配方。建议在 `layer.conf` 中明确注释优先级设置的原因，方便维护。

### 7. **调试和验证**
- **检查优先级冲突**：如果配方未按预期选择，检查所有层的 `BBFILE_PRIORITY`：
  ```bash
  bitbake -e | grep ^BBFILE_PRIORITY
  ```
- **查看配方来源**：使用以下命令确认 BitBake 选择了哪个层的配方：
  ```bash
  bitbake-layers show-recipes <recipe>
  ```
- **日志分析**：启用详细日志（`bitbake -v`）或检查 `log.do_fetch` 等日志文件，查看配方解析的详细信息。

### 8. **总结**
决定 `BBFILE_PRIORITY` 的值需要综合考虑以下因素：
- **层的功能**：基础层优先级较低，特定层（如 BSP 或自定义层）优先级较高。
- **覆盖需求**：需要覆盖其他层配方的层应设置更高的优先级。
- **依赖关系**：确保依赖层的优先级低于主层。
- **避免歧义**：为每个层设置唯一的优先级值，避免与 `BBPATH` 顺序混淆。
- **约定与测试**：参考 Yocto 项目中的默认值，并通过调试工具验证优先级设置。

**建议**：
- 从低到高设置优先级（如 5 到 10），为未来扩展留出空间。
- 在 `layer.conf` 中添加注释，说明优先级设置的理由，例如：
  ```bash
  # 设置优先级为 8 以覆盖 meta-oe 的配方
  BBFILE_PRIORITY_custom-layer = "8"
  ```

如果你有具体的项目场景或需要帮助设置某个层的优先级，请提供更多细节，我可以为你提供更具体的建议！



# 自己定义的meta层典型目录说明

在 Yocto 项目或基于 BitBake 的构建系统中，自定义层（`meta` 层）是用于扩展或定制构建的常用方式。一个典型自定义 `meta` 层的目录结构遵循一定的约定，以确保 BitBake 能够正确识别和解析层中的配方（recipes）、配置文件和其他资源。以下是一个典型自定义 `meta` 层的目录结构说明，以及每个目录或文件的用途。

### 1. **典型自定义 meta 层目录结构**
假设自定义层名为 `meta-custom`，其典型目录结构如下：

```
/meta-custom
├── conf
│   ├── layer.conf
│   └── machine
│       ├── machine1.conf
│       └── machine2.conf
├── recipes-core
│   ├── example
│   │   ├── example_1.0.bb
│   │   └── files
│   │       ├── example.conf
│   │       └── example.patch
├── recipes-bsp
│   ├── bootloader
│   │   └── u-boot_2023.04.bb
│   └── kernel
│       └── linux-yocto_6.1.bbappend
├── recipes-extended
│   ├── custom-app
│   │   └── custom-app_1.0.bb
├── classes
│   └── custom.bbclass
├── scripts
│   └── setup-custom.sh
├── README.md
└── COPYING
```

### 2. **目录和文件说明**
以下是每个目录或文件的典型用途和说明：

#### 2.1 **conf/**
`conf` 目录是层的核心，包含层的配置文件，定义层的元数据和行为。

- **`layer.conf`**：
  - **作用**：定义层的元数据，包括层的集合名称（`BBFILE_COLLECTIONS`）、优先级（`BBFILE_PRIORITY`）、配方文件路径（`BBFILES`）等。
  - **内容示例**：
    ```bash
    # 设置层的集合名称
    BBFILE_COLLECTIONS += "custom-layer"
    # 设置层的优先级
    BBFILE_PRIORITY_custom-layer = "8"
    # 定义配方文件路径
    BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"
    # 定义层的路径模式
    BBFILE_PATTERN_custom-layer = "^${LAYERDIR}/"
    # 层依赖（可选）
    LAYERDEPENDS_custom-layer = "core openembedded-layer"
    ```
  - **说明**：`layer.conf` 是 BitBake 识别层的入口，必须存在。`LAYERDIR` 表示当前层的根目录，`BBFILES` 指定配方文件的位置。

- **`machine/`**（可选）：
  - **作用**：存放硬件特定的配置文件，定义支持的机器（`MACHINE`）。
  - **示例文件**：`machine1.conf`
    ```bash
    #@TYPE: Machine
    #@NAME: machine1
    #@DESCRIPTION: Machine configuration for Machine1
    PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
    MACHINE_FEATURES = "wifi bluetooth"
    ```
  - **说明**：用于定义特定硬件平台的配置，如内核、引导加载程序或硬件特性。通常在 BSP 层中更常见，但在自定义层中也可以包含。

#### 2.2 **recipes-<category>/**
配方目录通常以 `recipes-` 开头，按功能分类，存放配方文件（`.bb`）和附加文件（`.bbappend`）。常见的子目录包括：

- **`recipes-core/`**：
  - **作用**：存放核心组件的配方，如基础工具、库或系统服务。
  - **示例**：`example/example_1.0.bb`
    ```bash
    SUMMARY = "Example application"
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://${WORKDIR}/LICENSE;md5=..."
    SRC_URI = "file://example.conf file://example.patch"
    do_install() {
        install -d ${D}${sysconfdir}
        install -m 0644 ${WORKDIR}/example.conf ${D}${sysconfdir}/
    }
    ```
  - **子目录**：`example/files/` 存放配方所需的源文件、补丁或配置文件（如 `example.conf`, `example.patch`）。
  - **说明**：用于定义如何构建和安装核心软件包。

- **`recipes-bsp/`**：
  - **作用**：存放板级支持包（BSP）相关配方，如引导加载程序（U-Boot）、内核或设备树。
  - **示例**：`bootloader/u-boot_2023.04.bb` 或 `kernel/linux-yocto_6.1.bbappend`
  - **说明**：`.bbappend` 文件用于修改其他层（如 `meta`）提供的配方，例如调整内核配置。

- **`recipes-extended/`**：
  - **作用**：存放扩展功能的配方，如自定义应用程序或第三方软件。
  - **示例**：`custom-app/custom-app_1.0.bb`
  - **说明**：适合放置项目特定的应用程序或工具。

其他可能的配方目录：
- `recipes-connectivity/`：网络相关组件（如 Wi-Fi、蓝牙）。
- `recipes-multimedia/`：多媒体相关组件。
- `recipes-devtools/`：开发工具相关配方。

#### 2.3 **classes/**
- **作用**：存放自定义的类文件（`.bbclass`），定义可被配方或层继承的通用构建逻辑。
- **示例**：`custom.bbclass`
  ```bash
  do_custom_task() {
      bbnote "Running custom task"
  }
  addtask custom_task before do_build
  ```
- **说明**：类文件提供可重用的任务或配置，减少配方中的重复代码。自定义层可能包含特定于项目的构建逻辑。

#### 2.4 **scripts/**
- **作用**：存放辅助脚本，用于设置环境、调试或自动化任务。
- **示例**：`setup-custom.sh`
  ```bash
  #!/bin/bash
  echo "Setting up environment for meta-custom"
  export BBPATH=$BBPATH:/path/to/meta-custom
  ```
- **说明**：脚本通常用于开发者或 CI/CD 流程，简化层的使用。

#### 2.5 **README.md**
- **作用**：提供层的说明文档，描述层的作用、依赖、用法和维护信息。
- **内容示例**：
  ```
  # meta-custom
  This layer provides custom recipes and configurations for Project X.
  Dependencies: meta, meta-poky, meta-oe
  Usage: Add this layer to conf/bblayers.conf
  ```
- **说明**：帮助其他开发者理解层的用途和如何集成。

#### 2.6 **COPYING**
- **作用**：包含层的许可证信息（如 MIT、GPL）。
- **说明**：确保层符合开源许可证要求，通常直接复制标准许可证文本。

### 3. **设计自定义层的注意事项**
- **遵循命名约定**：配方目录以 `recipes-<category>` 开头，配方文件以 `<name>_<version>.bb` 命名，保持一致性。
- **模块化组织**：按功能划分配方目录（如 `recipes-core`, `recipes-bsp`），提高可维护性。
- **优先级设置**：在 `layer.conf` 中合理设置 `BBFILE_PRIORITY`，确保自定义层能够覆盖其他层的配方（参考前述讨论）。
- **依赖声明**：在 `layer.conf` 中使用 `LAYERDEPENDS` 声明依赖的层，例如：
  ```bash
  LAYERDEPENDS_custom-layer = "core openembedded-layer"
  ```
- **配方文件结构**：配方文件应包含必要的变量（如 `SUMMARY`, `LICENSE`, `SRC_URI`）和任务（如 `do_install`），确保构建逻辑清晰。
- **测试层**：使用 `bitbake-layers` 工具验证层：
  ```bash
  bitbake-layers show-layers
  bitbake-layers show-recipes
  ```

### 4. **典型工作流程**
1. **创建层**：
   ```bash
   yocto-layer create meta-custom
   ```
   这会生成基本的层结构，包括 `conf/layer.conf` 和 `README`。

2. **添加层到项目**：
   编辑 `conf/bblayers.conf`，添加：
   ```bash
   BBLAYERS += "/path/to/meta-custom"
   ```

3. **添加配方**：
   在 `recipes-*` 目录中创建配方文件，并将相关源文件放入 `files/` 子目录。

4. **测试构建**：
   ```bash
   bitbake <recipe>
   ```

### 5. **总结**
一个典型自定义 `meta` 层包含以下核心组件：
- `conf/layer.conf`：定义层元数据和优先级。
- `recipes-<category>/`：存放配方和相关文件，按功能分类。
- `classes/`：定义可重用的构建逻辑。
- `scripts/`：提供辅助工具。
- `README.md` 和 `COPYING`：提供文档和许可证信息。

通过遵循 Yocto 项目的命名和组织约定，自定义层可以无缝集成到构建系统中，并支持配方覆盖、硬件支持或项目特定功能。合理设置 `BBFILE_PRIORITY` 和 `LAYERDEPENDS` 是确保层正确工作的关键。

如果你有具体的自定义层设计问题或需要某个目录的详细配置示例，请告诉我！

# REQUIRED_DISTRO_FEATURES 

REQUIRED_DISTRO_FEATURES 只有在配方中包含 inherit features_check 时才会生效。

如果缺少 inherit features_check，BitBake 会忽略 REQUIRED_DISTRO_FEATURES，可能导致潜在的构建问题。

# 多个同名recipe文件怎么选择

BitBake 会优先选择来自层优先级较高的配方，而非版本号最高者。

配方文件通常命名为 <package-name>_<version>.bb，例如 bash_5.1.bb 和 bash_5.2.bb。

如果文件名不符合标准（如 package.bb 和 package-new.bb），BitBake 可能无法正确解析版本，导致不可预测的选择（通常按文件名字母顺序）。

# BBFILES_DYNAMIC

BBFILES_DYNAMIC 的引入主要是为了解决以下问题：

1. 条件性配方加载
   - 在 Yocto 构建系统中，不同的硬件平台、特性或配置可能需要不同的配方或附加文件。BBFILES_DYNAMIC 允许根据层的启用状态或其他条件动态加载特定的配方，而无需修改层的核心配置文件（layer.conf）。
   - 例如，一个层可能包含针对特定硬件架构的配方，只有当该架构的层被启用时才需要加载这些配方。
2. 减少不必要的配方解析
   - 如果所有配方都无条件地添加到 BBFILES 中，BitBake 需要解析所有这些文件，即使其中一些配方在当前配置中并不需要。这会增加解析时间和复杂度。
   - BBFILES_DYNAMIC 允许只加载与当前构建配置相关的配方，从而提高构建效率。
3. 支持模块化层设计
   - Yocto 的层机制鼓励模块化设计，BBFILES_DYNAMIC 使得层可以更灵活地声明哪些配方或附加文件在特定场景下生效。例如，一个层可能支持多种硬件平台，但只有在特定平台层被包含时才加载对应的配方。
4. 解决层依赖问题
   - 某些配方或附加文件可能依赖于其他层的存在（通过 LAYERDEPENDS 指定）。BBFILES_DYNAMIC 允许在依赖层存在时才加载相关配方，避免因缺少依赖而导致的解析错误。

假设有一个层 meta-example，它支持多种硬件平台（例如 arm 和 x86），并且包含特定于平台的配方。你可以在 meta-example/conf/layer.conf 中这样配置：

bitbake

```
# 基本 BBFILES 配置 BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend" # 动态 BBFILES 配置 BBFILES_DYNAMIC += "\    arm:${LAYERDIR}/recipes-arm/*/*.bb \    x86:${LAYERDIR}/recipes-x86/*/*.bb \ "
```

- 如果 meta-arm 层被启用（通常通过 BBFILE_COLLECTIONS 中包含 arm），BitBake 会将 ${LAYERDIR}/recipes-arm/*/*.bb 添加到 BBFILES 中。
- 如果 meta-x86 层被启用，则加载 ${LAYERDIR}/recipes-x86/*/*.bb。

这样，只有在相关层被启用时，特定平台的配方才会被解析和使用。



# STAGING_KERNEL_DIR 

STAGING_KERNEL_DIR 指向 tmp/work-shared//kernel-source

个目录包含完整的内核源码树，来自 do_unpack 和 do_patch 任务的输出。

STAGING_KERNEL_DIR 主要用于以下场景：

- 构建内核模块

  - 外部内核模块（out-of-tree modules）需要访问内核源码或头文件来编译模块（.ko 文件）。

  - 模块 recipe 会使用 

    STAGING_KERNEL_DIR

     查找 

    Makefile

     和内核头文件，例如：

    bash

    ```
    make -C ${STAGING_KERNEL_DIR} M=${S} modules
    ```

  - 示例：meta/recipes-kernel/hello-mod/hello-mod_0.1.bb 使用此变量编译简单的内核模块。

- 用户空间应用程序

  - 某些用户空间程序（如需要访问内核头文件的工具）会引用 STAGING_KERNEL_DIR 中的头文件（例如 include/linux/）。
  - 例如，perf 工具在构建时需要内核头文件。

- 内核配置检查

  - 一些 recipe 或任务可能需要检查内核配置（.config 文件），可以通过 STAGING_KERNEL_DIR/.config 访问。

- 交叉编译环境

  - STAGING_KERNEL_DIR 提供了一个标准化的路径，供其他 recipe 在交叉编译环境中引用内核源码，而无需直接访问原始源码。



# do_sizecheck[dirs] = "${B}" 这个说明什么

在执行 do_sizecheck 任务时，BitBake 会将当前工作目录设置为 ${B}（构建目录）。

# KCONFIG_MODE 

KCONFIG_MODE 是 Yocto 中用于控制 Linux 内核配置行为的重要变量，主要决定如何处理 defconfig 或配置片段：

- --allnoconfig：严格模式，仅启用明确指定的配置，适合最小化内核。
- --alldefconfig：宽松模式，保留内核默认值，适合通用或开发场景。
