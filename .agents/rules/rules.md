---
trigger: always_on
---

# Antigravity Agent Directives: Jekyll + Obsidian Integration

## Core Philosophy: The Dual Environment
* **Single Source of Truth:** Every `.md` file must be perfectly readable in the local Obsidian application while remaining fully compatible with the Jekyll static site build process. 
* **Graceful Degradation:** Do not use Jekyll-specific Liquid templating (e.g., `{% include %}` or `{{ site.url }}`) in the main body text if it will severely break the reading experience in Obsidian.

## Frontmatter & Metadata
* **Strict YAML:** Every file must begin with valid YAML frontmatter enclosed in `---`. 
* **Required Fields:** Ensure title, date, and layout are present if required by the Jekyll configuration.
* **Tagging:** Use the frontmatter `tags: [array, of, tags]` for Jekyll compatibility. Do not use inline Obsidian tags (e.g., `#tag`) in the body text unless explicitly instructed, as Jekyll does not natively parse them into taxonomies without plugins.

## Links & Routing
* **Link Formatting:** Use standard Markdown links `[Link Text](relative/path/to/file.md)` instead of Obsidian Wikilinks `[[File Name]]`, unless the Jekyll site is explicitly configured with a plugin (like `jekyll-obsidian` or `jekyll-spaceship`) to parse Wikilinks. 
* **File Extensions:** When linking internally, ensure the `.md` extension is handled correctly based on the Jekyll permalink configuration (often requiring standard Markdown links to point directly to the `.md` file for Obsidian, relying on Jekyll to rewrite them to `.html` on build).

## Assets & Images
* **Pathing:** This is the most critical boundary. Place all images in a dedicated `assets/` or `images/` folder that both Obsidian and Jekyll can read.
* **Image Syntax:** Use standard Markdown image syntax `![Alt Text](/assets/image.png)`. Do not use Obsidian's `![[image.png]]` embed syntax unless a Jekyll plugin is configured to support it. 
* **Absolute vs. Relative:** Ensure image paths use the root-relative slash (e.g., `/assets/...`) so Jekyll can locate them from the site root, while Obsidian's "Use absolute path in vault" setting can resolve them locally.

## Content Formatting
* **Callouts & Admonitions:** Obsidian uses `> [!info]` syntax for callouts. Only use this syntax if the Jekyll site has a corresponding markdown processor or plugin to render them. Otherwise, use standard blockquotes `>`.
* **Footnotes:** Use standard Markdown footnote syntax (`[^1]` and `[^1]:`). Both Obsidian and Jekyll's default Kramdown processor support this natively.