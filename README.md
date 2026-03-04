# Ultimate-AI-Media-Generator-Skill

An open-source **ai image generator skill** and **ai video generator skill** for AI agents.

This skill is built around CyberBara Public API v1 and is designed for fast creation, predictable credit usage, and practical production workflows.

[Quick Start](#quick-start) | [Key Features](#key-features) | [Platform Prompts](#step-3-use-the-skill-on-codex-claude-code-openclaw-and-claude-cowork) | [Use Cases](#typical-use-cases) | [Chinese README](./README-zh.md)

---

## Key Features

- Lower-cost generation with CyberBara: in many scenarios, CyberBara pricing is cheaper than official model APIs.
- Credit visibility before submission: quote credits first, then decide whether to continue.
- Curated prompt library: includes production-ready prompts selected and refined by artists and prompt engineers, so beginners can create strong outputs without deep prompt engineering.
- Built-in workflow templates: includes starter workflows for **ai ppt skill**, **ai seo article skill**, and AI comic drama creation.
- Fully open source: fork, edit, and iterate the skill for your own team or product.
- Multi-agent compatibility: works with OpenClaw, Claude Code, Codex, and Claude Cowork.

---

## Quick Start

### Step 1) Install (npx skills)

Based on the same installation pattern used in `Generative-Media-Skills`:

```bash
# List what can be installed from this repo
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --list

# Install all skills from this repo
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all

# Optional: install for specific agents (if your skills runtime supports agent targeting)
npx skills add ZeroLu/Ultimate-AI-Media-Generator-Skill --all -a codex -a claude-code
```

Fallback (manual installer):

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ZeroLu/Ultimate-AI-Media-Generator-Skill \
  --path .
```

After installation, restart your AI coding agent.

### Step 2) Get and configure API key

Get your API key:

- https://cyberbara.com/settings/apikeys

Configure it:

```bash
export CYBERBARA_API_KEY="<your_api_key>"
```

API key resolution order:
1. `--api-key`
2. `CYBERBARA_API_KEY`
3. `~/.config/cyberbara/api_key`
4. interactive prompt

### Step 3) Use the skill on Codex, Claude Code, OpenClaw, and Claude Cowork

Use the skill trigger:

- `$ultimate-ai-media-generator-skill`

You can paste these prompts directly in your agent chat.

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

- Image: `nano-banana-2`, `nano-banana-pro` (nano banana skill workflows)
- Video: `seedance` family (seedance 2.0 skill workflows), `sora-2` (sora 2 skill workflows), and other CyberBara-supported models

---

## Core Commands (CLI)

```bash
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

## SEO Keyword Focus

This repository is optimized for:

- `ai image generator skill`
- `ai video generator skill`
- `ai ppt skill`
- `nano banana skill`
- `seedance 2.0 skill`
- `sora 2 skill`
- `ai seo article skill`
- `open claw image generator skill`

---

## License

Open-source repository. Add your preferred license file (`MIT`, `Apache-2.0`, etc.) if you want explicit reuse terms.
