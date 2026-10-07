document.addEventListener("DOMContentLoaded", () => {

    fetch("content/home.md")
        .then(response => response.text())
        .then(markdown => {
            document.querySelector("#content").innerHTML = marked.parse(markdown);
        });

});