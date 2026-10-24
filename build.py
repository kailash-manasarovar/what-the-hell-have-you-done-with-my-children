import markdown
from pathlib import Path
import re
from html import escape

content = Path("content")
site = Path("site")
chapter_list = Path("chapters.txt")

site.mkdir(exist_ok=True)

# Read chapter titles and filenames from chapters.txt
# Format: Chapter Title|filename.md
chapters = []
md_files = []

for line_number, line in enumerate(
    chapter_list.read_text(encoding="utf-8").splitlines(), start=1
):
    line = line.strip()

    # Ignore blank lines and comments
    if not line or line.startswith("#"):
        continue

    if "|" not in line:
        raise ValueError(
            f"Invalid line {line_number} in chapters.txt. "
            "Use the format: Chapter Title|filename.md"
        )

    title, filename = line.split("|", 1)
    title = title.strip()
    filename = filename.strip()

    if not title or not filename:
        raise ValueError(
            f"Missing title or filename on line {line_number} "
            "of chapters.txt."
        )

    if Path(filename).name != filename or not filename.endswith(".md"):
        raise ValueError(
            f"Invalid Markdown filename on line {line_number}: {filename}"
        )

    md_file = content / filename

    if not md_file.is_file():
        raise FileNotFoundError(
            f"Chapter listed in chapters.txt was not found: {md_file}"
        )

    md_files.append(md_file)

    chapters.append({
        "file": md_file.with_suffix(".html").name,
        "title": title,
    })

if not chapters:
    raise ValueError("No chapters found in chapters.txt.")

# Build the table of contents for chapter pages
chapter_toc = "\n".join(
    f'            <li><a href="{escape(chapter["file"], quote=True)}">'
    f'{escape(chapter["title"])}</a></li>'
    for chapter in chapters
)

# Remove old generated HTML files
for old_file in site.glob("*.html"):
    old_file.unlink()

# Build every Markdown chapter in the order specified in chapters.txt
for i, md_file in enumerate(md_files):
    text = md_file.read_text(encoding="utf-8")
    chapter = chapters[i]
    title = chapter["title"]

    # Convert Markdown to HTML
    body_html = markdown.markdown(
        text,
        extensions=["extra"]
    )

    # Previous / Next navigation
    previous_link = ""
    next_link = ""

    if i > 0:
        previous = chapters[i - 1]
        previous_link = (
            f'<a href="{escape(previous["file"], quote=True)}">'
            f'← {escape(previous["title"])}</a>'
        )

    if i < len(chapters) - 1:
        next_chapter = chapters[i + 1]
        next_link = (
            f'<a href="{escape(next_chapter["file"], quote=True)}">'
            f'{escape(next_chapter["title"])} →</a>'
        )

    # Create the chapter page
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-F1VGXS43G0"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());

        gtag('config', 'G-F1VGXS43G0');
    </script>

    <title>{escape(title)} — What the Hell Have You Done with My Children?</title>

    <link rel="stylesheet" href="../style.css">
</head>
<body>

<header class="book-header">
    <a class="book-name" href="../index.html">
        What the Hell Have You Done with My Children?
    </a>

    <details class="book-contents">
        <summary>☰ Contents</summary>
        <nav class="toc">
            <h2>Contents</h2>
            <ul>
{chapter_toc}
            </ul>
        </nav>
    </details>
</header>

<main>
{body_html}

<nav class="chapter-navigation" aria-label="Chapter navigation">
    <div>{previous_link}</div>
    <div>{next_link}</div>
</nav>
</main>

</body>
</html>
"""

    output = site / chapter["file"]
    output.write_text(page, encoding="utf-8")
    print(f"Built {output}")

# Update the TOC on index.html
index = Path("index.html")
index_html = index.read_text(encoding="utf-8")

index_toc = "\n".join(
    f'        <li><a href="site/{escape(chapter["file"], quote=True)}">'
    f'{escape(chapter["title"])}</a></li>'
    for chapter in chapters
)

pattern = (
    r'(<nav id="toc" class="toc">\s*<h2>Contents</h2>\s*<ul>)'
    r'.*?'
    r'(</ul>)'
)

index_html, count = re.subn(
    pattern,
    lambda m: f"{m.group(1)}\n{index_toc}\n        {m.group(2)}",
    index_html,
    flags=re.DOTALL
)

if count:
    index.write_text(index_html, encoding="utf-8")
    print("TOC updated on index.html")
else:
    print(
        "Warning: index.html TOC was not updated; "
        "its expected structure was not found."
    )

print("Book build complete.")
