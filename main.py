"""api-lab-groq-minimal

最小化体验一次 Groq（高速推理）API 调用，并打印耗时。
Groq 提供 OpenAI-compatible /chat/completions 接口。
本仓库的关注点：让你「肉眼感受」到推理速度。
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

PROMPT = "请用两句话解释为什么推理速度对用户体验重要。"
TIMEOUT_SECONDS = 30
MAX_TOKENS = 80


def main() -> int:
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
    model = os.getenv("GROQ_MODEL", "").strip()

    if not api_key:
        print("[错误] 未在 .env 中检测到 GROQ_API_KEY。")
        print("       请运行: cp .env.example .env，然后填入真实 key。")
        return 2
    if not model:
        print("[错误] 未在 .env 中检测到 GROQ_MODEL。")
        print("       请填入你账户可用的模型名（去 Groq 控制台查可用模型清单）。")
        return 2

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
    }

    print(f"[信息] endpoint = {url}")
    print(f"[信息] model    = {model}")
    print(f"[信息] prompt   = {PROMPT}")
    print("[信息] 注意观察下面的耗时 —— 这是 Groq 的卖点。")

    started = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        print(f"[失败] 请求超时（{TIMEOUT_SECONDS}s）。")
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"[失败] 网络请求异常: {exc}")
        return 1
    elapsed = time.time() - started

    if resp.status_code != 200:
        print(f"[失败] HTTP {resp.status_code}")
        print(f"        响应片段: {resp.text[:300]}")
        print("        常见原因: API Key 无效 / 模型名错 / 当前地区不可用。")
        return 1

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        print("[失败] 响应结构不符合 OpenAI-compatible 预期。")
        print(f"        原始响应片段: {resp.text[:300]}")
        return 1

    print()
    print("[成功] 模型返回内容：")
    print(content)
    print()
    print(f"[信息] 总耗时: {elapsed:.3f}s")
    print(f"[信息] 注：这个耗时含网络往返，不是纯推理时间。")

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    result = {
        "provider": "groq",
        "base_url": base_url,
        "model": model,
        "prompt": PROMPT,
        "elapsed_seconds": round(elapsed, 3),
        "content": content,
    }
    out_file = out_dir / "result.json"
    out_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[信息] 已写入 {out_file}（不会被 git 提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
