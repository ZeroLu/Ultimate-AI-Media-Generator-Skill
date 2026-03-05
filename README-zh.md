# Ultimate-AI-Media-Generator-Skill

[![GitHub Repo stars](https://img.shields.io/github/stars/ZeroLu/Ultimate-AI-Media-Generator-Skill?style=for-the-badge)](https://github.com/ZeroLu/Ultimate-AI-Media-Generator-Skill/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ZeroLu/Ultimate-AI-Media-Generator-Skill?style=for-the-badge)](https://github.com/ZeroLu/Ultimate-AI-Media-Generator-Skill/network/members)
[![MIT License](https://img.shields.io/github/license/ZeroLu/Ultimate-AI-Media-Generator-Skill?style=for-the-badge)](./LICENSE)

![Ultimate AI Media Generator Skill Cover](./assets/readme-cover-2k-16x9.jpg)

一个开源的 **ai image generator skill** 与 **ai video generator skill**，为 AI Agent 提供一站式图像/视频生成能力。支持 Nano Banana 2、Sora 2、Seedance、Kling 等模型，适合内容生产、创意设计与自动化工作流。

[快速开始](#快速开始) | [核心特性](#核心特性) | [支持平台](#支持平台) | [平台调用示例](#platform-prompts) | [典型场景](#典型场景) | [English README](./README.md)

---

## 核心特性

- 🚀 **更高性价比生成**：在很多场景下，CyberBara 成本低于官方模型 API。
- 💳 **先看积分再提交**：先 `quote` 预估积分，再决定是否发起任务。
- 🧠 **精选提示词库**：由艺术家与提示词工程师整理，降低上手门槛。
- 🛠️ **内置工作流模板**：覆盖 **ai ppt skill**、**ai seo article skill**、AI 漫剧创作等场景。
- 🔓 **完全开源可定制**：支持 fork、改造、二次开发。
- 🌍 **多 Agent 平台兼容**：面向主流 skill 生态平台可直接使用。

---

## 支持平台

本 skill 支持所有支持 skill 的平台，包括但不限于：

- OpenClaw
- Claude Code
- Codex
- Claude Cowork
- Cursor
- Antigravity
- 其他兼容 skill 的 Agent 平台

---

## 快速开始

### Vibe Install

只需要把下面这句话发给 AI（OpenClaw、Claude Code、Codex 等），AI 会帮你安装：

```text
Help me install this skill, use command `npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all`
```

### Manual Install

### Step 1) 安装（npx skills）

```bash
# 查看可安装内容
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --list

# 安装全部技能
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all

# 可选：按指定 Agent 安装（如果你的 skills 运行时支持）
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all -a codex -a claude-code
```

### Step 2) 获取并配置 API Key

免费 API Key 获取地址：https://cyberbara.com/settings/apikeys

推荐一次性配置：

```bash
python3 scripts/cyberbara_api.py setup-api-key "<your_api_key>"
```

该命令会把 key 保存到 `~/.config/cyberbara/api_key`，后续无需每次重复配置。

<a id="platform-prompts"></a>

### Step 3) 在 Codex、Claude Code、OpenClaw、Claude Cowork、Cursor、Antigravity 中使用 skill

你可以直接把下面提示词粘贴到 Agent 对话框，或直接让 Agent 帮你生图/生视频。

#### A) 生图示例（nano banana skill）

```text
Use $ultimate-ai-media-generator-skill to generate one image:
- model: nano-banana-pro
- scene: text-to-image
- prompt: A cute kitten dancing, 3D cartoon style, dynamic full body, clean stage background
- options: aspect_ratio=16:9, resolution=1k
Return task id, final status, and output image URL.
```

#### B) 生视频示例（seedance 2.0 skill / sora 2 skill）

```text
Use $ultimate-ai-media-generator-skill to generate one video:
- model: seedance-2.0-pro
- scene: text-to-video
- prompt: Cinematic wide shot of a futuristic city at sunrise, smooth drone motion
- options: duration=10, resolution=standard
If seedance-2.0-pro is unavailable, fallback to sora-2.
Return task id and final video URL.
```

#### C) 生成前先查积分

```text
Use $ultimate-ai-media-generator-skill to quote credits before submission for this request:
- model: nano-banana-pro
- media_type: image
- scene: text-to-image
- prompt: Minimalist product poster for a smart watch
- options: aspect_ratio=1:1, resolution=1k
Return estimated_credits and can_afford.
```

#### D) 查询余额与最近使用记录

```text
Use $ultimate-ai-media-generator-skill to check current credit balance and the latest 20 usage records.
```

---

## 典型场景

- **ai image generator skill**：社媒配图、广告素材、产品主视觉
- **ai video generator skill**：短视频制作、分镜预演、创意样片
- **ai ppt skill**：生成演示文稿配图与风格统一素材集
- **ai seo article skill**：生成文章封面、插图与元数据图组
- **open claw image generator skill**：OpenClaw + CyberBara 联动出图工作流

工作流模板：

- [AI PPT Workflow](./workflows/ai-ppt-skill.md)
- [AI SEO Article Workflow](./workflows/ai-seo-article-skill.md)
- [AI Comic Drama Workflow](./workflows/ai-comic-drama-skill.md)

精选提示词：

- [Curated Prompt Library](./workflows/curated-prompts.md)

---

## 模型覆盖（Model Coverage）

CyberBara 当前支持的图像与视频模型：

| 媒体类型 | 模型 | 支持场景 |
| -------- | ---- | -------- |
| Image | `nano-banana-2` | `text-to-image`, `image-to-image` |
| Image | `nano-banana-pro` | `text-to-image`, `image-to-image` |
| Video | `sora-2` | `text-to-video`, `image-to-video` |
| Video | `sora-2-pro` | `text-to-video`, `image-to-video` |
| Video | `seedance-1-pro` | `text-to-video`, `image-to-video` |
| Video | `seedance-1-lite` | `text-to-video`, `image-to-video` |
| Video | `seedance-1-pro-fast` | `image-to-video` |
| Video | `kling-2.6` | `text-to-video`, `image-to-video` |
| Video | `veo-3.1-fast` | `text-to-video`, `image-to-video` |
| Video | `veo-3.1-quality` | `text-to-video`, `image-to-video` |
| Video | `kling-video-o1` | `video-to-video` |

具体和最新积分费用请访问：https://cyberbara.com/credit-costs

---

## 核心命令（CLI）

```bash
python3 scripts/cyberbara_api.py setup-api-key "<your_api_key>"
python3 scripts/cyberbara_api.py models --media-type image
python3 scripts/cyberbara_api.py models --media-type video
python3 scripts/cyberbara_api.py quote --json '{...}'
python3 scripts/cyberbara_api.py generate-image --json '{...}'
python3 scripts/cyberbara_api.py generate-video --json '{...}'
python3 scripts/cyberbara_api.py wait --task-id <TASK_ID> --interval 5 --timeout 900
python3 scripts/cyberbara_api.py balance
python3 scripts/cyberbara_api.py usage --limit 20
```

---

## 欢迎贡献

欢迎提交 Issue 和 Pull Request，一起完善提示词库、工作流模板、文档和平台适配能力。

如果这个项目对你有帮助，欢迎点个 Star 支持。

---

## 许可证

本项目采用 MIT 协议，详见 [LICENSE](./LICENSE)。

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ZeroLu/Ultimate-AI-Media-Generator-Skill&type=Date)](https://star-history.com/#ZeroLu/Ultimate-AI-Media-Generator-Skill&Date)
