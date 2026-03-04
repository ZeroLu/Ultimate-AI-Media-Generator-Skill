# Ultimate-AI-Media-Generator-Skill

一个面向 AI Agent 的开源技能仓库：支持图像与视频生成、积分预估、任务轮询和工作流模板。

默认英文说明请看 [README.md](./README.md)。

---

## 核心优势

- 基于 CyberBara 的低成本接口能力：很多场景下，比官方 API 更便宜。
- 生成前可先看积分消耗：先 `quote`，再决定是否提交任务。
- 内置精选提示词库：由艺术家和提示词工程师整理，新手也能快速出高质量内容。
- 内置工作流模板：覆盖 `ai ppt skill`、`ai seo article skill`、AI 漫剧创作。
- 完全开源：可自行修改、二次开发、持续迭代。
- 多平台兼容：OpenClaw、Claude Code、Codex、Claude Cowork。

---

## 快速开始

### 第一步：安装（npx skills）

```bash
# 查看可安装内容
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --list

# 安装全部技能
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all
```

可选（手动安装）：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ZeroLu/Ultimate-AI-Media-Generator-Skill \
  --path .
```

安装后重启你的 AI Agent。

### 第二步：获取并配置 API Key

获取地址：

- https://cyberbara.com/settings/apikeys

配置：

```bash
export CYBERBARA_API_KEY="<your_api_key>"
```

### 第三步：在不同平台中用 prompt 调用

触发词：

- `$ultimate-ai-media-generator-skill`

示例（生图）：

```text
Use $ultimate-ai-media-generator-skill to generate one image:
- model: nano-banana-pro
- scene: text-to-image
- prompt: A cute kitten dancing, 3D cartoon style, dynamic full body, clean stage background
- options: aspect_ratio=16:9, resolution=1k
Return task id, final status, and output image URL.
```

示例（生视频 + 回退）：

```text
Use $ultimate-ai-media-generator-skill to generate one video:
- model: seedance-2.0-pro
- scene: text-to-video
- prompt: Cinematic wide shot of a futuristic city at sunrise, smooth drone motion
- options: duration=10, resolution=standard
If seedance-2.0-pro is unavailable, fallback to sora-2.
Return task id and final video URL.
```

示例（先查积分）：

```text
Use $ultimate-ai-media-generator-skill to quote credits before submission for this request:
- model: nano-banana-pro
- media_type: image
- scene: text-to-image
- prompt: Minimalist product poster for a smart watch
- options: aspect_ratio=1:1, resolution=1k
Return estimated_credits and can_afford.
```

---

## 典型场景

- `ai image generator skill`：社媒配图、广告图、产品图
- `ai video generator skill`：短视频、分镜预演
- `ai ppt skill`：生成演示文稿视觉素材
- `ai seo article skill`：生成 SEO 文章封面图和配图
- `open claw image generator skill`：OpenClaw + CyberBara 联动出图

工作流模板：

- [AI PPT Workflow](./workflows/ai-ppt-skill.md)
- [AI SEO Article Workflow](./workflows/ai-seo-article-skill.md)
- [AI Comic Drama Workflow](./workflows/ai-comic-drama-skill.md)
- [Curated Prompt Library](./workflows/curated-prompts.md)
