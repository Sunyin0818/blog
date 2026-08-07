#!/usr/bin/env python3
"""发布前 frontmatter / slug 校验（CF 构建期由 guard.sh 调用）。

不依赖 PyYAML：自带最小 frontmatter 解析，覆盖本仓库模板实际产生的
标量 / 行内列表 [a, b] / 块列表 "- a" 三种形态。
"""
import os
import re
import sys
from datetime import datetime, timezone

CONTENT = "content"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SPECIAL_PAGES = {"search.md", "about.md"}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}
    fm = m.group(1)
    data = {}
    lists = {}
    cur = None
    for line in fm.splitlines():
        if cur is not None:
            lm = re.match(r"^\s*-\s+(.*)$", line)
            if lm:
                lists[cur].append(lm.group(1).strip())
                continue
            cur = None
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            if val == "":
                lists[key] = []
                cur = key
                data[key] = None
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                data[key] = [] if inner == "" else [
                    x.strip().strip('"').strip("'") for x in inner.split(",")
                ]
            else:
                data[key] = val.strip('"').strip("'")
    data.update(lists)
    return data


def main():
    errors = []
    slugs = {}
    md_files = []
    for dp, _, fnames in os.walk(CONTENT):
        for f in fnames:
            if f.endswith(".md"):
                md_files.append(os.path.join(dp, f))

    for path in md_files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        fm = parse_frontmatter(text)
        rel = os.path.relpath(path, CONTENT)
        base = os.path.basename(path)
        is_index = fm.get("index") in (True, "true", "True") or base == "_index.md"
        is_hand = is_index or ("layout" in fm) or (base in SPECIAL_PAGES)
        if is_hand:
            if not (fm.get("title") or "").strip():
                errors.append(f"{rel}: 页面缺少 title")
            continue

        # --- 文章校验 ---
        if not (fm.get("title") or "").strip():
            errors.append(f"{rel}: 缺少必填字段 title")
        # slug 可选：笔记只放本体、不写 slug，Hugo 默认用文件路径当 URL。
        # 若显式写了 slug 才校验格式（长度/字符），未写则不报错。
        slug = fm.get("slug")
        if slug:
            if not isinstance(slug, str) or not (slug or "").strip():
                errors.append(f"{rel}: slug 存在但为空")
            elif len(slug) > 40:
                errors.append(f"{rel}: slug 长度 > 40 ({slug})")
            elif not SLUG_RE.match(slug):
                errors.append(f"{rel}: slug 格式非法 ({slug})")
            else:
                slugs.setdefault(slug, []).append(rel)
        if not (fm.get("date") or "").strip():
            errors.append(f"{rel}: 缺少必填字段 date")
        if "tags" not in fm:
            errors.append(f"{rel}: 缺少 tags")
        elif not isinstance(fm.get("tags"), list):
            errors.append(f"{rel}: tags 必须是列表")
        dval = fm.get("date")
        if dval and isinstance(dval, str):
            try:
                dt = datetime.fromisoformat(dval.replace(" ", "T").replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt > datetime.now(timezone.utc):
                    errors.append(f"{rel}: date 在未来 ({dval})")
            except ValueError:
                errors.append(f"{rel}: date 无法解析 ({dval})")
        pub = fm.get("publish")
        if pub in (False, "false", "False"):
            errors.append(f"{rel}: 存在 publish: false（应已发布或不应出现）")
        # 发布笔记必须有 slug：生成稳定 ASCII URL，避免依赖中文文件名，
        # 也防止后续改标题导致 URL 漂移。未发布笔记仍允许不写 slug。
        if pub in (True, "true", "True") and not (
            slug and isinstance(slug, str) and (slug or "").strip()
        ):
            errors.append(f"{rel}: publish:true 必须有 slug（用于生成稳定 ASCII URL）")
        if "categories" in fm:
            errors.append(f"{rel}: 手写 categories（应由 _index.md 的 cascade 注入）")

    for slug, files in slugs.items():
        if len(files) > 1:
            errors.append(f"slug 重复 {slug}: {', '.join(files)}")

    # 注：曾要求「每个含 .md 的目录都必须有 _index.md」，理由是 cascade 注入 categories。
    # 但 categories 分类法已整体废弃（hugo.yaml 的 taxonomies 只保留 tag，/categories/ 不再生成），
    # 该前提不复存在。缺 _index.md 时 Hugo 仍会自动生成分区列表页（标题取目录名），
    # 「全部笔记」页也已改为按 Section 自动收录，不依赖任何白名单。
    # 因此不再强制 —— 新增内容分区无需在 blog 仓库手工建文件。
    # _index.md 现在纯属可选增强：想给分区起中文名时才加（见 site-pages/ 说明）。

    if errors:
        print(f"::error:: check_frontmatter 发现 {len(errors)} 处问题:")
        for e in errors:
            print("  " + e)
        sys.exit(1)
    print("check_frontmatter: OK")


if __name__ == "__main__":
    main()
