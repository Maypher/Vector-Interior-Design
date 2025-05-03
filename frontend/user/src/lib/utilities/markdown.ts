import showdown from "showdown";

// Replaces all <h#></h#> tags with <p class="markdown-header markdown-header-#"></p>
// To not confuse web crawlers when finding multiple header tags
const headerToParagraph: showdown.ShowdownExtension = {
    type: "output",
    regex: /^<h([1-6]) id="(.+)">(.+)<\/h[1-6]>/gm,
    replace: (_match: string, level: string, id: string, content: string) => {
        return `<p id="${id}" class="markdown-header markdown-header-${level}">${content}</p>`;
    }
}

const converter = new showdown.Converter({
    openLinksInNewWindow: true,
    simpleLineBreaks: true,
    extensions: [headerToParagraph]
});

export default function mdToHtml(md: string): string {
    console.log(md);
    return converter.makeHtml(md);
}
