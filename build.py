import markdown
from pathlib import Path
import re

content = Path("content")
site = Path("site")

site.mkdir(exist_ok=True)

# Remove old generated HTML files
for old_file in site.glob("*.html"):
    old_file.unlink()

toc = []

# Build every Markdown file
for md_file in sorted(content.glob("*.md")):

    text = md_file.read_text(encoding="utf-8")

    # Get the first H1
    match = re.search(r"^# (.+)$", text, re.MULTILINE)

    if match:
        title = match.group(1).strip()
    else:
        title = md_file.stem

    # Convert Markdown to HTML
    html = markdown.markdown(
        text,
        extensions=["extra"]
    )

    # Create the HTML page
    output = site / md_file.with_suffix(".html").name

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
<main>
{html}
</main>
</body>
</html>
"""

    output.write_text(page, encoding="utf-8")

    # Add it to the TOC
    toc.append(
        f'        <li><a href="site/{output.name}">{title}</a></li>'
    )

    print(f"Built {output}")

# Build the TOC
toc_html = "\n".join(toc)

index = Path("index.html")
html = index.read_text(encoding="utf-8")

html = re.sub(
    r'(<nav id="toc" class="toc">\s*<h2>Contents</h2>\s*<ul>).*?(</ul>)',
    rf'\1\n{toc_html}\n        \2',
    html,
    flags=re.DOTALL
)

index.write_text(html, encoding="utf-8")

print("TOC updated.")