---
title: "搜索"
layout: "search"
index: true
robots: noindex
# 站内搜索主入口是自建弹层（layouts/_partials/extend_footer.html，Ctrl/⌘+K 触发）。
# 本页仅作 no-JS / 弹层脚本未加载时的降级兜底，避免菜单「搜索」落到 404。
build:
  list: never          # 不进 /index.json 搜索索引（搜索页自己出现在搜索结果里没意义）
  render: always       # 页面本身照常生成
---
