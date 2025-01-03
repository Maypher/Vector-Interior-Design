import showdown from "showdown";

const converter = new showdown.Converter({
    openLinksInNewWindow: true,
    simpleLineBreaks: true
});

export default function mdToHtml(md: string): string {
    return converter.makeHtml(md);
}
