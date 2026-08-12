# RUN_RESULT

| 字段 | 值 |
| --- | --- |
| 是否已运行真实 API | 否 |
| 离线合同验证时间 | 2026-08-12 |
| 离线合同验证是否成功 | 是 |
| 模型名 | 未使用真实模型；测试占位符 `m` |
| 真实 API 耗时 | —；stub 耗时不代表 Groq 性能 |
| 未实跑原因 | 本轮未授权付费/真实 API 调用，也未读取或配置凭据 |

## 备注

- 本轮未读取 `.env`，未发起真实网络请求，也未安装依赖。
- 在仓库外 disposable archive 中使用内存 stub 验证：缺少凭据时 exit 2/no HTTP；base URL 归一化、Bearer/body 和结果写入；HTTP 429 失败；响应结构异常失败。
- Groq 的真实延迟仍未验证；不得从瞬时 stub 运行推断服务性能。

## 运行日志（你跑完后手动追加）

```text
mock-contract-tests: PASS (missing config, success, 429, malformed)
syntax: PASS
```
