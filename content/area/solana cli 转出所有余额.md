---
title: solana cli 转出所有余额
categories:
  - area
tags:
  - bitcoin
publish: true
date: 2025-08-21 11:36:19
lastmod: 2025-10-13 15:34:09
---
# 1. 环境

> 系统环境：`Ubuntu 24.04.2 LTS`

## 1.1. 安装solana cli

```bash
curl --proto '=https' --tlsv1.2 -sSfL https://solana-install.solana.workers.dev | bash
```

## 1.2. 安装base58

> 钱包导出的私钥为base58，需要转换

```bash
sudo apt install python3-base58 -y
```

验证一下
```bash
root@ip-172-31-10-157:~# python3 -c "import base58;print(base58.b58decode('11111111111111111111111111111111'))"
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

# 2. 操作

## 绑定钱包

将私钥转换，将`WALLET_PRIVATE_KEY`换成实际的私钥
```python
root@ip-172-31-10-157:~# python3 - <<'PY' <WALLET_PRIVATE_KEY> > ~/.config/solana/phantom.json
import sys, json, base58
b58 = sys.argv[1].strip()
raw = base58.b58decode(b58)
print(json.dumps(list(raw)))
> PY
```

结果
```bash
root@ip-172-31-10-157:~# cat ~/.config/solana/phantom.json
[165, 186, 96, ...]
```

绑定密钥对
```bash
 solana config set --keypair ~/.config/solana/phantom.json
```

设置为主网
```bash
solana config set --url https://api.mainnet-beta.solana.com
```

检查一下当前的配置
```bash
solana config get
```

```ini
Config File: /root/.config/solana/cli/config.yml
RPC URL: https://api.mainnet-beta.solana.com
WebSocket URL: wss://api.mainnet-beta.solana.com/ (computed)
Keypair Path: /root/.config/solana/phantom.json
Commitment: confirmed
```

然后就可以查看钱包地址和余额
```bash
solana address # 地址
solana balance # 余额
```

## 转出

修改`RECIPIENT_ADDRESS`为目标钱包地址
```bash
solana transfer <RECIPIENT_ADDRESS> $(echo "$(solana balance | tr -d ' SOL') - 0.000005" | bc -l) --from ~/.config/solana/phantom.json
```

返回签名，即交易成功