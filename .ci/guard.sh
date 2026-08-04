#!/usr/bin/env bash
# Cloudflare 构建期硬门禁：任一检查失败 -> 构建失败 -> 站点停在上一个成功版本。
set -uo pipefail
FAIL=0

# 0. 自动维护分区 _index.md：新发布的分区/嵌套目录若缺 _index.md，
#    cascaded categories 会失效，且后续 check_frontmatter.py 会判构建失败。
#    先补生成，再跑门禁，保证 Enveloppe 推送即上线、零手动维护。
python3 .ci/gen-index.py || true

TARGETS=$(find content static -type f \( -name '*.md' -o -name '*.html' \) 2>/dev/null)
[ -z "$TARGETS" ] && exit 0

# ① 密钥正则（第一梯队，命中即失败）
while IFS='|' read -r NAME PATTERN; do
  [ -z "${NAME:-}" ] && continue
  case "$NAME" in \#*) continue;; esac
  HITS=$(echo "$TARGETS" | xargs -r grep -nPI "$PATTERN" 2>/dev/null \
         | grep -vFf .ci/secret-allow.txt || true)
  if [ -n "$HITS" ]; then
    echo "::error:: [$NAME] 命中："
    echo "$HITS" | sed -E 's/^([^:]+:[0-9]+):.*/  \1/' | sort -u   # 不回显密钥本身
    FAIL=1
  fi
done < .ci/secret-rules.txt

# ② 私密路径进入 content/
BAD=$(find content -type f | grep -Ei '(^|/)(Keys?|Private|Secret|Credential|恢复码|访问码|密钥)(/|\.md$)' || true)
[ -n "$BAD" ] && { echo "::error:: 私密路径进入 content/:"; echo "$BAD"; FAIL=1; }

# ③ 疑似 OneDrive 冲突副本
CONFLICT=$(find content -type f | grep -Ei '(conflict|冲突|副本|\(1\)\.md$)' || true)
[ -n "$CONFLICT" ] && { echo "::error:: 疑似 OneDrive 冲突副本:"; echo "$CONFLICT"; FAIL=1; }

# ④ 残留 Obsidian 语法 / 未重写的图片路径
LEFT=$(grep -rn -e '!\[\[' -e '](Assets/' -e '```dataview' content/ || true)
[ -n "$LEFT" ] && { echo "::error:: 残留 Obsidian 语法:"; echo "$LEFT"; FAIL=1; }

# ⑤ frontmatter / slug 校验
python3 .ci/check_frontmatter.py || FAIL=1

exit $FAIL
