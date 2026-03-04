# AI PPT Skill Workflow

Goal: generate a complete visual package for a slide deck without design expertise.

## Inputs

- topic
- audience
- slide count
- visual style

## Prompt Template

```text
Create a visual plan for a {slide_count}-slide presentation about {topic}.
Audience: {audience}.
Style: {visual_style}.
Output:
1) one hero cover image prompt,
2) one visual prompt per slide,
3) icon style guide,
4) color palette,
5) short image alt text for accessibility.
```

## Media Generation Tips

- Use `nano-banana-pro` for fast image ideation.
- Keep consistent `aspect_ratio` and palette across slides.
