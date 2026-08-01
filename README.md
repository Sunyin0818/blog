# Sunyin 的笔记博客（Hugo + PaperMod + Cloudflare Pages）

> **`content/` 与 `static/images/` 由 Enveloppe 生成，人只维护 `_index.md`、配置文件与 `layouts/`/`assets/`/`.ci/`。**
> 改文章的唯一入口是 Obsidian；不要在本仓库手改 `content/` 下的文章。

## 三个最脆弱的点（改任何东西前先读）

1. **Enveloppe 的 `conversion.links.wiki` 必须永远是 `false`。** 改回 `true` 会静默破坏 3 篇 Linux 笔记的 bash `[[ -z ... ]]` 代码块，CI 不一定发现。
2. **`autoclean.excluded` 正则 + `_index.md` 里的 `index: true` 是一对，缺一不可。** 删掉 `_index.md` 不报错，只会让分类页悄悄变空、所有文章丢 categories。
3. **自动 merge 意味着 GitHub 上的内容无法事前拦截。** 唯一硬门禁是 Cloudflare 构建期的 `.ci/guard.sh`：扫描失败 → 构建失败 → 站点停在上一个成功版本，泄漏内容永不公开。仓库设 private 兜最后底。

## 仓库结构

```
blog/
├── hugo.yaml                 # 站点配置（人维护）
├── go.mod / go.sum           # Hugo Module 锁 PaperMod@master（hugo mod get 生成）
├── .ci/
│   ├── guard.sh              ★ CF 构建期硬门禁
│   ├── secret-rules.txt      密钥正则清单（第一梯队硬失败）
│   ├── secret-allow.txt      误报白名单
│   └── check_frontmatter.py  发布前 frontmatter 校验
├── .github/workflows/
│   ├── alert.yml             push 后跑同一套 guard + gitleaks（非门禁，仅告警）
│   └── weekly-scan.yml       每周一全历史重扫
├── content/                  ◄── Enveloppe 写入区
│   ├── _index.md search.md archives.md about.md
│   └── {AIO,AI,Coding,Linux,Misc}/_index.md   # 人维护，带 cascade.categories + index:true
├── static/images/            ◄── Enveloppe 写入区
├── layouts/                  Hugo ≥0.146 覆盖层
│   ├── _partials/  comments.html  post_meta.html  extend_footer.html
│   └── _markup/    render-blockquote.html  render-codeblock-mermaid.html
├── assets/css/extended/custom.css
└── i18n/zh.yaml
```

## 部署（详见 SETUP.md）

1. `hugo mod get github.com/adityatelange/hugo-PaperMod@master`（写 go.mod/go.sum）
2. 建 `Sunyin0818/blog`（private）+ `Sunyin0818/blog-comments`（public + Discussions + giscus），填 `comments.html` 的 repo-id / category-id
3. 推 `main` → Cloudflare Pages 连仓库，build 命令 `bash .ci/guard.sh && hugo --gc --minify -b $CF_PAGES_URL`，output `public`，v3
4. 环境变量 `HUGO_VERSION=0.164.0` / `HUGO_ENV=production` / `HUGO_ENABLEGITINFO=false` / `TZ=Asia/Shanghai`（Production + Preview 各配一遍）
