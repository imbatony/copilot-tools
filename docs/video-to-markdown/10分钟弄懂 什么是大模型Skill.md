# 10分钟弄懂 什么是大模型Skill

> 来源: [https://www.youtube.com/watch?v=lnneAfJqd9M](https://www.youtube.com/watch?v=lnneAfJqd9M)
> 时长: 09:40
> 提取时间: 2026-01-30
> 作者: 程序人老王

## 要点摘要

### 一、Skill 是什么？

**Skill 本质上是一个管理提示词的机制**，每个针对不同用途的提示词就是一个 Skill。

- Skill 是一个**文件夹**，其中包含 `Skill.md` 文件
- `Skill.md` 存储完整的提示词内容
- 文件开头有 **MetaData**（简短介绍），用于快速描述 Skill 的用途

### 二、为什么需要 Skill？

| 问题 | Skill 的解决方案 |
|------|-----------------|
| 提示词太多，难以管理 | 按用途分类，存放在不同 Skill 文件夹 |
| 全部发送浪费 Token | 只发送简短的 MetaData |
| 无关信息让 AI 迷茫 | AI 按需选择相关 Skill |

### 三、Skill 工作机制的三个阶段

#### 1️⃣ Discovery（发现）
- 客户端收集所有 Skill 的 **MetaData**
- 将 MetaData 放入系统提示词，与用户问题一起发给 AI
- MetaData 简短，占用 Token 少

#### 2️⃣ Activation（激活）
- AI 通过语义理解，判断用户问题与哪个 Skill 相关
- AI 生成特殊指令，要求客户端读取对应 `Skill.md` 的完整内容
- 用户看不到中间的 Skill 选择过程

#### 3️⃣ Execution（执行）
- AI 可以通过命令读取 Skill 中引用的其他文件（按需加载）
- Skill 文件夹可以包含脚本/程序，AI 可以执行它们
- AI 甚至可以根据 Skill 中声明的库/工具，**动态生成代码**执行

### 四、Skill 的强大之处

1. **文件引用**：Skill.md 可以引用其他文件，进一步减小体积
2. **嵌套引用**：引用关系可以层层嵌套，AI 按需读取
3. **执行脚本**：Skill 文件夹可存放脚本，AI 可直接执行
4. **动态编程**：告诉 AI 有哪些库可用，AI 可动态生成代码完成任务

### 五、实际应用示例

以 Claude 官方的 PDF Skill 为例：
1. AI 通过 MetaData 发现有处理 PDF 的 Skill
2. 读取 Skill.md，发现有处理 PDF 的脚本和库（如 PyPDF、PDF Plumber）
3. 直接执行脚本，或动态生成代码完成用户任务

### 六、核心总结

> **"执行能力给了 AI 行动力，Skill 为 AI 指明了方向。当 AI 学会在 Skill 的边界内谨慎使用执行的权力时，它才实现了属于它自己的知行合一。"**

| 概念 | 作用 |
|------|------|
| MetaData | 让 AI 了解有哪些提示词可用 |
| Skill.md | 存储完整提示词和使用指南 |
| 执行能力 | 让 AI 能够执行脚本或动态生成代码 |


