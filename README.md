# api-lab-groq-minimal

> 最小化体验：用 Groq 调一次聊天 API，并把耗时打出来。

## 它在做什么

Groq 用自研的 LPU 硬件做推理，主打「token/s 非常高」。它的接口本身是 **OpenAI-compatible**，
也就是说你已经在 `api-lab-openai-compatible-minimal` 学过的代码套用过来就能跑。

本仓库唯一的差别：

- 在调用前后做 `time.time()`，把**整轮请求耗时**打出来
- README 提示你重点看「速度感受」

## 运行步骤

```bash
cd api-lab-groq-minimal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 编辑 .env：
#   GROQ_API_KEY=gsk_...
#   GROQ_MODEL=（去 Groq 控制台查你账户可用的模型名）

python3 main.py
cat output/result.json
```

## 关于「耗时」

脚本打印的耗时 = **完整 HTTP 往返时间**，含：

1. 你机器到 Groq 网关的网络延迟
2. Groq 推理时间
3. Groq 把响应回传给你的网络延迟

所以：

- 如果你在中国大陆直连国外服务，看到的耗时大头会是网络
- 真正想感受 Groq 的极速，最好用一些有 token 流式输出的客户端（本仓库为了"最小"特意没做流式）

## 常见报错

| 终端打印 | 可能原因 | 怎么处理 |
| --- | --- | --- |
| `未在 .env 中检测到 GROQ_API_KEY` | 没填 key | 编辑 `.env` |
| `HTTP 401` | key 错或没传 | 重新去 Groq 控制台拿 key |
| `HTTP 404` / model not found | 模型名错或下线了 | 去 Groq 控制台查当前可用模型名 |
| `HTTP 429` | 限流 | 等几秒，不要循环重试 |
| 网络请求异常 | 当前地区/网络问题 | 不要反复重试，先确认网络 |

## .env.example

```
GROQ_API_KEY=填入你的Groq API Key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=填入你账户可用的模型名
```

## 不会做的事

- 不会自动重试
- 不会打印 API Key
- 不会自动选模型
