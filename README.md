
# Ultimate-AI-Media-Generator-Skill

[![GitHub Repo stars](https://img.shields.io/github/stars/ZeroLu/Ultimate-AI-Media-Generator-Skill?style=for-the-badge)](https://github.com/ZeroLu/Ultimate-AI-Media-Generator-Skill/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ZeroLu/Ultimate-AI-Media-Generator-Skill?style=for-the-badge)](https://github.com/ZeroLu/Ultimate-AI-Media-Generator-Skill/network/members)
[![MIT License](https://img.shields.io/github/license/ZeroLu/Ultimate-AI-Media-Generator-Skill?style=for-the-badge)](./LICENSE)

![Ultimate AI Media Generator Skill Cover](./assets/readme-cover-2k-16x9.jpg)

An open-source **ai image generator skill** and **ai video generator skill** for AI agents. Empower your agent to generate images and videos on their own! Top models like Nano Banana 2, Sora 2, Seedance, Kling and much more are all supported!

[Quick Start](#quick-start) | [Key Features](#key-features) | [Supported Platforms](#supported-platforms) | [Platform Prompts](#step-3-use-the-skill-on-codex-claude-code-openclaw-claude-cowork-cursor-and-antigravity) | [Use Cases](#typical-use-cases) | [Chinese README](./README-zh.md)

---

## Key Features

- 🚀 **Cost-efficient generation**: in many scenarios, CyberBara pricing is lower than official model APIs.
- 💳 **Credit visibility before submission**: quote credits first, then decide whether to continue.
- 🧠 **Curated prompt library**: production-ready prompts selected and refined by artists and prompt engineers.
- 🛠️ **Built-in workflow templates**: starter workflows for **ai ppt skill**, **ai seo article skill**, and AI comic drama production.
- 🔓 **Fully open source**: fork, customize, and iterate for your own team or product.
- 🌍 **Multi-agent compatibility**: supports mainstream skill-enabled AI coding platforms.

---

## Supported Platforms

This skill supports all platforms that support skills, including but not limited to:

- OpenClaw
- Claude Code
- Codex
- Claude Cowork
- Cursor
- Antigravity
- Other compatible skill-enabled agent platforms

---

## Quick Start

### Vibe Install

Just send the following command to your AI(OpenClaw, Claude Code, Codex etc)

```text
Help me install this skill, use command `npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all`
```

### Manual Install

### Step 1) Install (npx skills)

```bash
# List what can be installed from this repo
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --list

# Install all skills from this repo
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all

# Optional: install for specific agents (if your skills runtime supports agent targeting)
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all -a codex -a claude-code
```


### Step 2) Get and configure API key

Get your free API key here: https://cyberbara.com/settings/apikeys

Configure it once (recommended):

```bash
python3 scripts/cyberbara_api.py setup-api-key "<your_api_key>"
```

This stores your key at `~/.config/cyberbara/api_key`, so you do not need to export it every session.

### Step 3) Use the skill on Codex, Claude Code, OpenClaw, Claude Cowork, Cursor, and Antigravity

You can paste these prompts directly in your agent chat, or just tell your agent to generate images and videos.

#### A) Create an image (nano banana skill)

```text
Use $ultimate-ai-media-generator-skill to generate one image:
- model: nano-banana-pro
- scene: text-to-image
- prompt: A cute kitten dancing, 3D cartoon style, dynamic full body, clean stage background
- options: aspect_ratio=16:9, resolution=1k
Return task id, final status, and output image URL.
```

#### B) Create a video (seedance 2.0 skill / sora 2 skill)

```text
Use $ultimate-ai-media-generator-skill to generate one video:
- model: seedance-2.0-pro
- scene: text-to-video
- prompt: Cinematic wide shot of a futuristic city at sunrise, smooth drone motion
- options: duration=10, resolution=standard
If seedance-2.0-pro is unavailable, fallback to sora-2.
Return task id and final video URL.
```

#### C) Check credits before generation

```text
Use $ultimate-ai-media-generator-skill to quote credits before submission for this request:
- model: nano-banana-pro
- media_type: image
- scene: text-to-image
- prompt: Minimalist product poster for a smart watch
- options: aspect_ratio=1:1, resolution=1k
Return estimated_credits and can_afford.
```

#### D) Check balance and recent usage

```text
Use $ultimate-ai-media-generator-skill to check current credit balance and the latest 20 usage records.
```

---

## Typical Use Cases

- **ai image generator skill** for social posts, ad creatives, product hero images.
- **ai video generator skill** for short promo clips and storyboard previsualization.
- **ai ppt skill** workflow to generate slide visuals and style-consistent image sets.
- **ai seo article skill** workflow to generate article covers, inline visuals, and metadata image sets.
- **open claw image generator skill** setup for teams using OpenClaw + CyberBara in the same workflow.

Workflow templates:

- [AI PPT Workflow](./workflows/ai-ppt-skill.md)
- [AI SEO Article Workflow](./workflows/ai-seo-article-skill.md)
- [AI Comic Drama Workflow](./workflows/ai-comic-drama-skill.md)

Curated prompts:

- [Curated Prompt Library](./workflows/curated-prompts.md)

---

## Model Coverage

CyberBara supported image and video models:

| Media Type | Model | Supported Scenes |
| ---------- | ----- | ---------------- |
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

For detailed and latest credit pricing by model, visit https://cyberbara.com/credit-costs.

---

## Core Commands (CLI)

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

## Contributing

Contributions are welcome. Please open an issue for bugs/feature ideas, and submit pull requests to improve prompts, workflows, docs, or platform integrations.

If this project helps you, please star the repository and help make it better together.

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ZeroLu/Ultimate-AI-Media-Generator-Skill&type=Date)](https://star-history.com/#ZeroLu/Ultimate-AI-Media-Generator-Skill&Date)
