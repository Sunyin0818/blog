---
title: 自定义Solana钱包地址
categories:
  - area
tags:
  - bitcoin
publish: true
date: 2025-09-03 15:31:48
lastmod: 2025-10-15 09:28:56
---
# 基本知识

Solana 地址其实是个由 ED25519 公钥经过 Base58 编码后的字符串

和其他区块链（ BTC 、ERC20 ）一样，你也可以自己不断计算（类似于暴力穷举）出一个指定前后缀的 Vanity Address

这样你就可以获得 V2EX 开头的个性钱包地址啦，类似于：

`V2EX...`

# 具体操作

虽然 Github 上有很多开源工具，这里推荐使用 Solana 官方的 Solana CLI 工具

**不建议你使用 GOOGLE 到的 XX 网页版生成工具，或者未经审查的软件，因为你有可能会泄露私钥，导致资产被盗！！**

## 第一步，安装 Solana CLI

[https://solana.com/docs/intro/installation#install-the-solana-cli](https://solana.com/docs/intro/installation#install-the-solana-cli)

## 第二步，使用 solana-keygen 生成地址即可

```shell
solana-keygen grind --starts-with V2EX:1
```

`--starts-with V2EX:1`：代表以 V2EX 开头，生成 1 个地址后就停止

与此对应的还有`--ends-with` 、 `--starts-and-ends-with` 参数

需要注意的是：指定的前后缀长度越长，难度是指数级递增，在我机器上生成一个 4 字符开头的地址大概需要 70 秒左右

耐心等待一会，见到输出下面的内容就是以及算出来一个可用的地址了：

```bash
Wrote keypair to V2EXxxxxxxxxxxx.json
```

## 第三步，将钱包地址导入其他钱包工具（ Phantom ）

`solana-keygen` 生成的地址会保存在当前目录的 json 文件中，其中文件名就是公钥（你的钱包地址）

你也可以通过 `solana-keygen pubkey xxx.json`来获取钱包地址

文件的内容是私钥，不过是[12,34,56...]这种格式的，一个包含 64 个字节的数组来表示私钥

如果你需要将这个钱包地址导入类似于 Phantom 钱包中，需要做一下转换，将其转换为 base58 格式即可

这里提供一个简单的 Python 转换脚本示例

```python
# 先安装依赖 pip install base58

import json
import sys
import base58

if len(sys.argv) != 2:
    print('用法: python convert.py [path]')
    sys.exit(1)

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    keypair_data = json.load(f)

secret_key = bytes(keypair_data)
encoded_secret_key = base58.b58encode(secret_key).decode()
print(f'Base58 编码的私钥：{encoded_secret_key}')
```

这样你就同时获得了公钥和对应的私钥，也就拥有了一个靓号地址了~ 转入 SOL 或 V2EX 代币试试吧