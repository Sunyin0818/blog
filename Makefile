# 本地开发便捷封装：先自动维护 _index.md，再跑 Hugo。
# Cloudflare 侧无需改动——它的构建命令 `bash .ci/guard.sh && hugo ...`
# 已在 guard.sh 内部调用 .ci/gen-index.py。

.PHONY: gen serve build

gen:
	python3 .ci/gen-index.py

serve: gen
	hugo server -D

build: gen
	bash .ci/guard.sh
	hugo --gc --minify ${CF_PAGES_URL:+-b $(CF_PAGES_URL)}
