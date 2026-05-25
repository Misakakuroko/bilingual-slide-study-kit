# Contributing

Thanks for considering a contribution.

This project is meant to help students turn lecture slides into bilingual, exam-ready study material. Contributions are especially welcome when they make the workflow easier to install, easier to verify, or safer for private course material.

## Good First Contributions

- Improve Windows, Linux, or macOS setup instructions.
- Add examples using self-authored or openly licensed slides.
- Improve the HTML review-page template.
- Add tests for the slide asset harness.
- Improve source-labeling and privacy guidance in the skill.

## Development Setup

```bash
git clone https://github.com/Misakakuroko/bilingual-slide-study-kit.git
cd bilingual-slide-study-kit
python3 -m unittest discover -s tests -v
```

On Windows:

```powershell
git clone https://github.com/Misakakuroko/bilingual-slide-study-kit.git
cd bilingual-slide-study-kit
py -3 -m unittest discover -s tests -v
```

## Contribution Rules

- Do not commit private lecture PDFs, copyrighted slide screenshots, or generated pages based on private course material.
- Do not commit personal paths, API keys, tokens, or local configuration files.
- Use self-authored or openly licensed material for public demos.
- Keep examples small enough to review quickly.
- Keep changes focused: one bug fix, feature, or documentation improvement per pull request is preferred.

## Before Opening A Pull Request

Run:

```bash
python3 -m unittest discover -s tests -v
```

Also check that no private course files or generated private assets were added:

```bash
git status --short
```

