# ZorvAI + DeepSeek Harness 构建产物仓库

换环境不用重新构建:拉本仓库 → 还原大文件 → 直接得到完整源码树和最新 APK。

## 仓库内容

- `source/` —— 完整源码树(`QuroAI-main-rc5`,即出包用的构建仓)
- `artifacts/` —— 大二进制分卷(90MB/片) + SHA256 清单
  - `snapshot.tar.xz` —— DSH rc5 快照(含全部插件,已注入 ZorvAI 灵魂插件)
  - `dsh-runtime.pack`、`ubuntu-noble-aarch64-pd-v4.18.0.tar.xz`
  - `apk/` —— 最新测试 APK `ZorvAI-v1.2.7-DSH-rc5-B20261121-0112.apk`
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

- 版本 `1.2.7 / 1002007`(锁死,不要改)
- 构建戳 `B20261121-0112`
- 快照 SHA `48b76347c6b9630e...`(三件套一致)
- 镜像源:Gradle 用阿里云优先;SDK/NDK 路径见 `source/local.properties`(本仓库已排除,需本地重建)

## 安全说明

本仓库是**公开**的,已排除:
- 所有 keystore / `*.*keystore` / `*.jks`(只留 SHA 校验值)
- `local.properties`(本地 SDK 路径)
- `.git/` 历史(不含任何 remote token)
- `build/` / `node_modules/` / 各类缓存

如发现任何真实凭证误入,请立即联系仓库所有者删除并吊销。
