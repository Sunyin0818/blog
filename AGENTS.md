# AGENTS.md — blog（Hugo 站点）

本仓库是 `blog.sunyin.fun` 的构建源（Hugo + PaperMod，Cloudflare Pages 构建上线）。
笔记内容由 **Obsidian Enveloppe 插件**从 OneDrive 真实库（`文档\Notes\`）自动发布：
Enveloppe 把 `publish: true` 的笔记 PR 进本仓库的 `content/`，再触发 Cloudflare Pages 构建。

---

## ⚠️ 铁律：新建「站点页」一律放 `site-pages/`，绝不要放 `content/`

**适用对象**：任何"不是 Obsidian 笔记"的功能性页面——
例如「全部笔记」(`notes.md`)、「关于」(`about.md`)、搜索降级页(`search.md`)，
以及未来可能新增的友链 / 书单 / 归档统计等页面。

**做法**：把这种 `.md` 文件直接放进仓库根的 `site-pages/` 目录，
**不要**放进 `content/`。

**为什么**（关键，不遵守会被删）：
- `site-pages/` 在 `hugo.yaml` 的 `module.mounts` 里被挂载到 `content/`，
  对 Hugo 而言与普通 content 完全等价（URL、title、sitemap、RSS 均正常）。
- Obsidian Enveloppe 的 **`autoclean` 会清掉 `content/` 下"OneDrive 源里没有对应文件"的内容**。
  站点页只存在于本仓库、Obsidian 里没有源，一旦放进 `content/` 就会在每次发布时被删。
- 放 `site-pages/` 则物理上不在 `content/` 下，autoclean 够不到 —— **无需维护 `autoclean.excluded` 白名单**，autoclean 可保持全开（Actions 偶发失败时仍能自愈）。

**坑**：
- **别在 `site-pages/` 下放 `README.md`** —— 会被挂载成一个真实页面 `/readme/`。
- 笔记（Obsidian 发布的文章）永远走 `content/`，与本规则无关，不受影响。

**本仓库现有的 `site-pages/` 成员**：`notes.md`(全部笔记) / `about.md`(关于) / `search.md`(搜索降级页，主入口仍是自建弹层)。

---

## 相关护栏（改动时勿破坏）

- `content/_index.md`（首页）受 Enveloppe 保护，勿删。
- 已发布笔记必须有合法的 ASCII（拼音）`slug`；CI 门禁 `.ci/check_frontmatter.py`
  会拒绝 `publish: true` 但缺 slug 的笔记。
- `notes` 仓库只是 OneDrive 真实库的镜像备份（同步方向 OneDrive → 镜像 → GitHub），**不是发布目标**。
- 搜索是自建弹层（`layouts/_partials/extend_footer.html`），索引来自 `hugo.yaml`
  的 `outputs.home: [HTML, RSS, JSON]` 生成的 `/index.json`。**勿删 JSON output。**
- 不想要进 `/index.json` 搜索索引的站点页，frontmatter 加 `build: { list: never, render: always }`
  （Hugo 0.145+ 用 `build` 而非 `_build`，list 取值是 `always/never/local` 枚举）。
