# SETUP — 从本地骨架到上线

本目录是博客仓库的**本地骨架**（尚未连 GitHub）。按顺序执行：

## 1. 装 Hugo（仅首次）

需要 Hugo **0.164.0**（PaperMod master 要求）。PaperMod 0 个 `.scss`，**不需要 extended 版**。

- 下载：https://github.com/gohugoio/hugo/releases/tag/v0.164.0
- 验证：`hugo version` 应显示 `v0.164.0`

## 2. 锁 PaperMod（写 go.mod / go.sum）

```bash
cd BlogStaging
hugo mod get github.com/adityatelange/hugo-PaperMod@master
```

该命令会把 PaperMod 的 `require` 伪版本写入 `go.mod` 并生成 `go.sum`。
之后升级只在你主动 `hugo mod get -u` 时发生。

## 3. 建 GitHub 仓库

- `Sunyin0818/blog` —— **private**（万一漏了密钥，爆炸半径限制在 GitHub 内）
- `Sunyin0818/blog-comments` —— **public**，只开 **Discussions**，去 https://giscus.app 生成 repo-id / category-id

把 repo-id / category-id 填进 `layouts/_partials/comments.html` 的
`data-repo-id` / `data-category-id`（当前是 `YOUR_GISCUS_REPO_ID` 占位）。

## 4. 本地验证

```bash
make serve        # 先自动生成缺失的 _index.md，再 hugo server -D
# 或等价地：
python3 .ci/gen-index.py && hugo server -D
# 打开 http://localhost:1313 ，确认首页/分类/搜索/归档/评论/2 篇 mermaid 渲染正常
```

> 直接 `hugo server -D` 也能跑，但新建的分区在未生成 _index.md 前
> 不会出现在 /categories/ 归档页——所以用 `make serve` 最稳。

> 此时 `content/` 下只有骨架页，没有文章是正常的。文章由 Enveloppe 推送。

## 5. 推送 + 连 Cloudflare Pages

```bash
git init
git add -A
git commit -m "chore: blog skeleton"
git branch -M main
git remote add origin git@github.com:Sunyin0818/blog.git
git push -u origin main
```

Cloudflare Pages：
- 连 `Sunyin0818/blog`
- Build command：`bash .ci/guard.sh && hugo --gc --minify -b $CF_PAGES_URL`
- Output dir：`public`
- Build system：**v3**
- 环境变量（Production **和** Preview 各配一遍）：

| 变量 | 值 |
|---|---|
| `HUGO_VERSION` | `0.164.0` |
| `HUGO_ENV` | `production` |
| `HUGO_ENABLEGITINFO` | `false` |
| `TZ` | `Asia/Shanghai` |

首次部署成功后，把 `*.pages.dev` 地址回填到 `hugo.yaml` 的 `baseURL`，再 push 一次。

## 6. 全量上线（文章）

Enveloppe 配置走插件 UI（见实施方案 Phase 8）。分批（15~20 篇/批）设
`publish: true` → Upload → 看 CF 部署。
