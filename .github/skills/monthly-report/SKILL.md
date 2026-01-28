---
name: monthly-report
description: >-
  月报工作汇总技能。将工作事项转换为专业的月报格式，每项工作一句话，
  按重要程度排序。格式：动词开头 + 具体内容 + 业务目标 + 量化指标。
  当用户需要写月报、总结工作、汇总成果时使用此技能。
license: MIT
metadata:
  author: copilot-tools
  version: "1.0.0"
---

# 月报工作汇总

将工作事项转换为专业的一句话汇总，按重要程度排序。**默认使用英文输出**。

## 格式要求

```
[Action Verb] + [Product/Feature] + [Technical Details], [enabling/achieving] + [Business Goal] + [Metrics].
```

## 快速参考

| 场景 | 推荐动词 |
|------|---------|
| 产品发布 | Shipped, Released, Launched |
| 指标达成 | Achieved, Attained, Reached |
| 技术实现 | Implemented, Developed, Built |
| 系统迁移 | Migrated, Upgraded, Transitioned |
| 流程优化 | Optimized, Enhanced, Streamlined |

## 示例

```
Shipped Hera Automation Desk v1.3.0 with Azure Monitor + OpenTelemetry integration, enabling end-to-end observability to drive data-informed workflow optimization.
```

## 详细指南

查看 [references/REFERENCE.md](references/REFERENCE.md) 获取完整案例和写作指南。
