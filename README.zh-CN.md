<p align="center"><a href="https://yunhao-feng.github.io/AgentGuard/"><img src="assets/brand/banner.svg" width="100%" alt="AgentGuard Team — 从风险到自适应防护" /></a></p>
<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>
<p align="center"><a href="https://yunhao-feng.github.io/AgentGuard/"><strong>研究主页 ↗</strong></a> &nbsp; · &nbsp; <a href="https://yunhao-feng.github.io/AgentGuard/metrics.html"><strong>探索研究指标 ↗</strong></a> &nbsp; · &nbsp; <a href="https://yunhao-feng.github.io/AgentGuard/#film"><strong>15 秒研究宣传片 ↗</strong></a></p>

智能体不仅回答问题，还会执行命令、调用工具、修改文件，并影响真实世界。**AgentGuard Team** 研究从发现风险、验证真实结果，到学习自适应防护的完整路径。

我们的研究连接了**五项互补贡献**：一个风险基准、一个可执行测试框架，以及三个防护模型训练方向。

## 一条研究主线，五项互补贡献

| 研究问题 | 工作 | 核心贡献 | 入口 |
| :-- | :-- | :-- | :-- |
| **危害在哪里产生？** | **AgentHazard** | 将有害目标分解为多步任务，量化计算机使用智能体的风险。 | [论文](https://arxiv.org/abs/2604.02947) · [代码](https://github.com/Yunhao-Feng/AgentHazard) |
| **实际发生了什么？** | **VERA** | 发现风险、构建可执行安全案例，并验证可观测的执行结果。 | [论文](https://arxiv.org/abs/2607.01793) · [代码](https://github.com/Yunhao-Feng/Vera) |
| **如何从演化威胁中学习？** | **BraveGuard** | 将开放世界的威胁发现与执行轨迹转化为防护模型的监督信号。 | [论文](https://arxiv.org/abs/2606.01166) · [代码](https://github.com/Yunhao-Feng/BraveGuard) |
| **如何优化安全判决？** | **HazardAuditor** | 用可执行威胁构建监督，通过 GuardPO 优化安全审计能力。 | [论文](https://arxiv.org/abs/2609.15134) · [代码](https://github.com/Yunhao-Feng/HazardAuditor) |
| **策略变化后如何判断？** | **AdaGuard** | 基于用户定义策略评估轨迹并识别违规规则，以 AdaptiveSafety 与 SafePO 支持学习。 | [研究资源](https://github.com/Yunhao-Feng/AdaGuard) · [代码](https://github.com/Yunhao-Feng/AdaGuard) |

**量化 → 验证 → 学习 → 适应。** 这是一条概念上的研究主线；五项工作各有独立贡献，并非一个已集成部署的系统。

## 15 秒了解我们的研究

[![观看 AgentGuard 研究宣传片](assets/teaser/poster.jpg)](https://yunhao-feng.github.io/AgentGuard/#film)

**[在线查看](https://yunhao-feng.github.io/AgentGuard/#film)** · [MP4](assets/teaser/agentguard-15s.mp4) · [英文字幕](assets/teaser/captions.en.srt) · [复现生成](docs/VIDEO.md)

1920 × 1080 · 30 fps · 英文文字 · 原创电子配乐。以动画呈现研究路线，无旁白。

## 开放数据、环境与模型

| 工作 | Hugging Face 资源 | 更多资源 |
| :-- | :-- | :-- |
| **AgentHazard** | [数据集 ↗](https://huggingface.co/datasets/Yunhao-Feng/AgentHazard) | [项目主页](https://yunhao-feng.github.io/AgentHazard/) |
| **VERA** | [AgentImages：运行环境镜像 ↗](https://huggingface.co/datasets/Yunhao-Feng/AgentImages) | [VERA-Bench 评估案例](https://github.com/Yunhao-Feng/Vera/tree/main/evaluation_bench) |
| **BraveGuard** | [模型仓库 ↗](https://huggingface.co/Yunhao-Feng/BraveGuard) | [训练与评估代码](https://github.com/Yunhao-Feng/BraveGuard) |
| **HazardAuditor** | [模型仓库 ↗](https://huggingface.co/Yunhao-Feng/HazardAuditor) | [项目主页](https://yunhao-feng.github.io/HazardAuditor/) |
| **AdaGuard** | [0.6B ↗](https://huggingface.co/Yunhao-Feng/AdaGuard-0.6B) · [4B ↗](https://huggingface.co/Yunhao-Feng/AdaGuard-4B) · [8B ↗](https://huggingface.co/Yunhao-Feng/AdaGuard-8B) | [训练与评估代码](https://github.com/Yunhao-Feng/AdaGuard) |

## 有出处、可探索的研究指标

| 研究产物 | 论文报告的规模 | 来源 |
| :-- | :-- | :-- |
| **AgentHazard** | 2,653 个实例 · 10 类风险 · 10 类攻击策略 | [研究来源](https://arxiv.org/abs/2604.02947) |
| **VERA-Bench** | 1,600 个可执行案例 · 124 类风险 | [研究来源](https://arxiv.org/abs/2607.01793) |
| **BraveGuard 任务池** | 7,308 个任务 · 28 类风险 · 32 类攻击方法 | [研究来源](https://arxiv.org/abs/2606.01166) |
| **CUA-EXEC 诊断集** | 4 个框架 · 各 100 条安全与 100 条不安全轨迹 | [研究来源](https://arxiv.org/abs/2609.15134) |
| **AdaptiveSafety** | 10,939 条训练样本 · 1,000 条测试样本 · 每个策略 1–100 条规则 | [研究资源](https://github.com/Yunhao-Feng/AdaGuard) |

**[指标探索页](https://yunhao-feng.github.io/AgentGuard/metrics.html)** 展示数据集统计、智能体攻击成功率、防护模型准确率／精确率／召回率／F1，以及规则识别能力。可切换评估条件、查看精确数值、导出当前表格；每组数据均标明研究来源与评估表格。

各项结果保留原始任务和基准条件。攻击成功、执行成功、二分类检测与规则识别回答不同问题，不合并成跨论文排行榜。完整来源见[机器可读数据](assets/data/metrics.json)。

## 与 Jev 对比

[查看对比页面](https://yunhao-feng.github.io/AgentGuard/jev.html)：同一评估中的结果、接口差异，以及双方各有优势的设置。

## 继续探索

[HazardArena](https://hazardarena-team.github.io/) · [AgentDojo](https://github.com/ethz-spylab/agentdojo) · [Agent-SafetyBench](https://github.com/thu-coai/Agent-SafetyBench) · [SWE-bench](https://www.swebench.com/) · [SWE-agent](https://github.com/SWE-agent/SWE-agent) · [OpenHands](https://github.com/All-Hands-AI/OpenHands) · [OWASP GenAI Security](https://owasp.org/projects/top-10-for-large-language-model-applications) · [MITRE ATLAS](https://atlas.mitre.org/)

## 使用与引用

[研究卡片](https://yunhao-feng.github.io/AgentGuard/#projects)上的 **引用** 按钮提供各篇论文的 BibTeX。请引用研究中实际使用的具体工作；本仓库是团队的研究入口。

网站支持 **English / 中文**、浅色／深色主题与手机访问。本地预览：

```bash
python3 scripts/serve.py
```

浏览器打开 `http://localhost:4173`。[部署与维护](docs/MAINTAINING.md) · [视频生成](docs/VIDEO.md) · [数据来源](docs/EVIDENCE.md)

<p align="center"><sub>AgentGuard Team · 为更安全的智能体开展开放研究。<br/>配色参考 <a href="https://www.swebench.com/">SWE-bench</a>。DM Sans 字体采用 <a href="assets/fonts/OFL.txt">SIL Open Font License</a>。</sub></p>
