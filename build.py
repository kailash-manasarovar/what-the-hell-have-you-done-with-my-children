import markdown
from pathlib import Path
import re

content = Path("content")
site = Path("site")

site.mkdir(exist_ok=True)

# Convert Markdown files to HTML
for md_file in sorted(content.glob("*.md")):

    html = markdown.markdown(
        md_file.read_text(encoding="utf-8"),
        extensions=["extra"]
    )

    output = site / md_file.with_suffix(".html").name
    output.write_text(html, encoding="utf-8")

    print(f"Built {output}")

# Build the TOC from the HTML files in site/
chapters = sorted(site.glob("*.html"))

toc = []

for chapter in chapters:

    # Remove the file extension
    title = chapter.stem

    # Remove leading number, e.g. 01-
    title = re.sub(r"^\d+-", "", title)

    # Turn hyphens into spaces
    title = title.replace("-", " ")

    # Capitalise words
    title = title.title()

    toc.append(
        f'        <li><a href="site/{chapter.name}">{title}</a></li>'
    )

toc_html = "\n".join(toc)

# Put the TOC into index.html
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