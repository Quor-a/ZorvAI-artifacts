# ZorvAI + DeepSeek Harness 构建产物仓库

换环境不用重新构建:拉本仓库 → 还原大文件 → 直接得到完整源码树和最新 APK。

## 仓库内容

- `source/` —— 完整源码树(`QuroAI-main-rc5`,即出包用的构建仓)
- `artifacts/` —— 大二进制分卷(90MB/片) + SHA256 清单
  - `snapshot.tar.xz` —— DSH rc5 快照(含全部插件,已注入 ZorvAI 灵魂插件)
  - `dsh-runtime.pack`、`ubuntu-noble-aarch64-pd-v4.18.0.tar.xz`
  - `apk/` —— 最新测试 APK `ZorvAI-v1.2.8-DSH-rc5-B20261121-0200.apk`
  - `keystore-sha256-only.json` —— 签名密钥**只存 SHA**,不存本体(安全)
- `MANIFEST.json` —— 版本、构建戳、产物清单
- `restore-artifacts.py` —— 一键还原分卷

## 换环境步骤

```bash
git clone https://github.com/Quor-a/ZorvAI-artifacts.git
cd ZorvAI-artifacts
python restore-artifacts.py     # 幂等,校验 SHA256
```

还原后:
- `source/` 就是完整可构建源码树(直接用它跑 Gradle)
- 根目录的 APK 可直接装机测试

## 关键事实

- 版本 `1.2.8 / 1002008`
- 构建戳 `B20261121-0200`
- APK SHA256 `b5490adfb25e4aec71...`(完整值见 `MANIFEST.json`)
- 快照 SHA `48b76347c6b9630e...`(三件套一致,资产未变)
- 业务仓源码同步分支 `Quor-a/ZorvAI` 的 `rc5-v1.2.8`
- 镜像源:Gradle 用阿里云优先;SDK/NDK 路径见 `source/local.properties`(本仓库已排除,需本地重建)

## 本次更新(v1.2.8)

相对 v1.2.7(B20261121-0112) 的改动:版本号与三处构建戳升级;源码树已同步业务仓 `rc5-v1.2.8` 的全部 44 个文件(peer 门禁放宽、must-enable 自愈、SnapshotFs 软链接、设置页白屏、控制台入口、终端初始化、虚拟屏桥接、ZorvAI 灵魂插件资产)。引擎大资产(snapshot/dsh-runtime/ubuntu)字节未变,分卷沿用。

## 安全说明

本仓库是**公开**的,已排除:
- 所有 keystore / `*.*keystore` / `*.jks`(只留 SHA 校验值)
- `local.properties`(本地 SDK 路径)
- `.git/` 历史(不含任何 remote token)
- `build/` / `node_modules/` / 各类缓存

如发现任何真实凭证误入,请立即联系仓库所有者删除并吊销。
