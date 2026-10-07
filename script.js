function makeSlug(text) {
    return text
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, "")
        .replace(/\s+/g, "-");
}

const tocList = document.querySelector("#toc ul");
const headings = document.querySelectorAll("h1");

headings.forEach((heading) => {
    const id = makeSlug(heading.textContent);

    heading.id = id;

    const item = document.createElement("li");
    const link = document.createElement("a");

    link.href = "#" + id;
    link.textContent = heading.textContent;

    if (heading.tagName === "H3") {
        item.classList.add("toc-subsection");
    }

    item.appendChild(link);
    tocList.appendChild(item);
});
