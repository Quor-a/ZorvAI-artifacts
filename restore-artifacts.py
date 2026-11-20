#!/usr/bin/env python3
"""把 artifacts/ 里的分卷还原成原始大文件，放回 source/ 对应路径。

换环境用法：
  1. git clone https://github.com/Quor-a/ZorvAI-artifacts.git
  2. cd ZorvAI-artifacts && python restore-artifacts.py
  3. 用 source/ 作为完整源码树构建（见 README.md）

还原是幂等的：文件已存在且 SHA256 匹配就跳过。
"""
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART = ROOT / 'artifacts'
SRC = ROOT / 'source'

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

manifests = sorted(ART.rglob('*.manifest.json'))
if not manifests:
    print('没有找到分卷清单')
    raise SystemExit(1)

for mf in manifests:
    meta = json.loads(mf.read_text(encoding='utf-8'))
    rel = meta['original_path']
    # APK 放到仓库根，其它放回 source 树
    dest = ROOT / Path(rel).name if rel.endswith('.apk') else SRC / rel
    if dest.exists() and sha256(dest) == meta['sha256']:
        print('SKIP (already ok)', dest)
        continue
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + '.restoring')
    with tmp.open('wb') as out:
        for n in range(meta['parts']):
            part = mf.parent / ('%s.part%03d' % (Path(rel).name, n))
            if not part.exists():
                print('MISSING PART', part)
                raise SystemExit(2)
            with part.open('rb') as f:
                shutil.copyfileobj(f, out)
    got = sha256(tmp)
    if got != meta['sha256']:
        tmp.unlink()
        print('SHA MISMATCH', dest, got, '!=', meta['sha256'])
        raise SystemExit(3)
    tmp.replace(dest)
    print('RESTORED', dest, dest.stat().st_size, 'bytes', got[:16])
print('DONE')
