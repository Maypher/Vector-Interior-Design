import DOMPurify from 'isomorphic-dompurify';
import { marked } from 'marked';

/**
 * Get's the position of the start and end of selection inside the given textarea.
 * 
 * @param textArea The textarea to get the selection from
 * @returns [start, end] indices of the selected content. 
 */
function getSelectionPos(textArea: HTMLTextAreaElement): Array<number> {
    return [textArea.selectionStart, textArea.selectionEnd];
}

/**
 * Gets the selected content from a given textarea.
 * 
 * @param textArea The textarea to get the selected content from.
 * @returns The selected content.
 */
function getSelectionText(textArea: HTMLTextAreaElement): string {
    let [selStart, selEnd] = getSelectionPos(textArea);
    selEnd += 1;

    return textArea.value.substring(selStart, selEnd).trim();
}

/**
 * Gets the content that comes before the selected text up to the entire line.
 * 
 * @param textArea The textarea to get the line from.
 * @param offset The offset to get lines relative to the selected line. 
 * Negative values mean lines before selection and positive after.
 * @returns The text before the selection stopping at the beginning of the line. 
 */
function getSelectedTextLine(textArea: HTMLTextAreaElement, offset: number = 0): string | undefined {
    const [selStart, _] = getSelectionPos(textArea);

    const textBeforeSelection = textArea.value.substring(0, selStart);
    const lines = textBeforeSelection.split('\n');
    const lineBeforeSelection = lines.at(lines.length - 1 + offset);

    return lineBeforeSelection?.trim();
}

/**
 * Updates the given text area by replacing the selection with the given value.
 * 
 * @param textArea The textarea to update.
 * @param value The value to insert in the selected region.
 * @param allowEmpty If empty selection strings should be allowed during insertion.
 */
function updateTextArea(textArea: HTMLTextAreaElement, value: string, allowEmpty: boolean = false) {
    const selectedText = getSelectionText(textArea).trim();

    // Skip the replacement if no selection exists.
    if (['', '\n'].includes(selectedText.trim()) && !allowEmpty) return;

    const [selStart, selEnd] = getSelectionPos(textArea);

    // Replaces the selected text with the given value
    textArea.value =
        textArea.value.substring(0, selStart) + value + textArea.value.substring(selEnd);

    // Updates the selection position to keep writing at the end of the insertion.
    const pos = selStart + value.length;
    textArea.setSelectionRange(pos, pos);
    textArea.focus();
}

/**
 * Bolds the selected text from a given textarea. If bold already it will un-bold it.
 * @param textArea The textarea to bold text from.
 */
export function boldText(textArea: HTMLTextAreaElement) {
    const selectedText = getSelectionText(textArea).trim();
    let bold: string = '';

    // Remove the bold asterisks if they already exist.
    if (selectedText.startsWith('**') && selectedText.endsWith('**')) {
        bold = selectedText.substring(2, selectedText.length - 2);
    } else {
        bold = `**${selectedText}**`;
    }

    updateTextArea(textArea, bold);
}

/**
 * Italics the selected text from the given textarea.
 * @param textArea The textarea to italic text from.
 */
export function italicText(textArea: HTMLTextAreaElement) {
    const selectedText = getSelectionText(textArea).trim();
    let italic: string = '';

    // If the string is already italic (*{text}*) or if it's both italic and bold (***{text}***) remove the italic. 
    if (
        (/^\*[\w]/.test(selectedText) && /\w\*$/.test(selectedText)) ||
        (selectedText.startsWith('***') && selectedText.endsWith('***'))
    ) {
        italic = selectedText.substring(1, selectedText.length - 1);
    } else {
        italic = `*${selectedText}*`;
    }

    updateTextArea(textArea, italic);
}

/**
 * Makes the selected text a title by prepending it with # up to 6 times. If 6 delete them.
 * @param textArea The textarea to title from.
 */
export function titleText(textArea: HTMLTextAreaElement) {
    const selectedText = getSelectionText(textArea).trim();
    const selectedLine = getSelectedTextLine(textArea);
    let title: string = '';

    // If the selected text starts the line and has 6 # delete them.
    if (/^#{6} /.test(selectedText)) {
        title = selectedText.substring(7);
    } else {
        // If the text starts the line and there are less than 6 # add one.
        if (/^#{1,5} /.test(selectedText)) {
            title = '#' + selectedText;
        } else if (selectedLine) {
            // If there's text before the selected text then push it to a new line to title it.
            title = '\n\n# ' + selectedText;
        } else {
            title = '# ' + selectedText;
        }
    }

    updateTextArea(textArea, title);
}

/**
 * Strikethrough the selected text. Removes it if already strikethrough.
 * @param textArea The textarea to strikethrough text from.
 */
export function strikethroughText(textArea: HTMLTextAreaElement) {
    const selectedText = getSelectionText(textArea).trim();
    let strikethrough: string = '';

    // If the selected text starts and ends with ~~ remove them.
    if (/^\~\~/.test(selectedText) && /\~\~$/.test(selectedText)) {
        strikethrough = selectedText.substring(2, selectedText.length - 2);
    } else {
        strikethrough = `~~${selectedText}~~`;
    }

    updateTextArea(textArea, strikethrough);
}


export function insertTable(textArea: HTMLTextAreaElement) {
    let [_, selEnd] = getSelectionPos(textArea);

    insertAtCursor(textArea,
        `|  |  |
|--|--|
|  |  |`
    );

    textArea.setSelectionRange(selEnd + 2, selEnd + 2);
    textArea.focus();
}

export function urlText(textArea: HTMLTextAreaElement) {
    const [selStart, _] = getSelectionPos(textArea);
    const selectedText = getSelectionText(textArea);
    const linkText = `[${selectedText}](link)`;

    updateTextArea(textArea, linkText, true);
    textArea.setSelectionRange(selStart + 1, selStart + 1);
    textArea.focus();
}

/**
 * Gets the next value order that should go in an ordered list.
 * @param textArea The textarea to get the value from.
 * @param offset Determines an offset of where to get the order from.
 * @returns The next value in an ordered list or `undefined` if there's no list.
 */
function getNextOrder(textArea: HTMLTextAreaElement, offset: number = 0): number | undefined {
    const previousLine = getSelectedTextLine(textArea, offset);
    const previousOrder = previousLine?.match(/^(\d+)\./)?.at(0);

    if (previousOrder) return parseInt(previousOrder) + 1;
}

/**
 * Makes the selected text into a list.
 * @param textArea The textarea to make the list in.
 * @param ordered If the list should be ordered.
 */
export function listText(textArea: HTMLTextAreaElement, mode: "UNORDERED" | "ORDERED" | "QUOTE" = "UNORDERED") {
    const selectedText = getSelectionText(textArea);
    const lineBeforeText = getSelectedTextLine(textArea, -1);
    const lines = selectedText.split('\n');
    let list: string = '';

    // If no text has been selected just add a list item
    if (!selectedText) {
        let textToInsert = getSelectedTextLine(textArea) ? "\n\n" : "";

        switch (mode) {
            case "UNORDERED":
                insertAtCursor(textArea, textToInsert + "- ");
                break;
            case "ORDERED":
                insertAtCursor(textArea, textToInsert + "1. ");
                break;
            case "QUOTE":
                insertAtCursor(textArea, textToInsert + "> ");
        }

        textArea.focus();

        return;
    }

    // For ordered lists. If there's an order before the selection use that otherwise 1.
    const prevOrder = getNextOrder(textArea, -1);
    let currentOrder: number = prevOrder || 1;

    // If there's text before the selected text push it into a new line to make a new list.
    if (lineBeforeText && !prevOrder) list += '\n\n';

    lines.forEach((line: string, index: number) => {
        let listChar = '-';

        // If it's an ordered list get the previous order and add one to it.
        if (mode == "ORDERED") {
            listChar = `${currentOrder}.`;
            currentOrder++;
        }
        else if (mode == "QUOTE") listChar = ">";

        // If at the end of the list don't add a new line to the list.
        list += `${listChar} ${line}${index < lines.length - 1 ? '\n' : ' '}`;
    });

    updateTextArea(textArea, list);
}

/**
 * Inserts a value into the current cursor position without affecting the rest of the textarea.
 * @param textArea The textarea to insert into.
 * @param value The value to insert at the current cursor pos.
 */
function insertAtCursor(textArea: HTMLTextAreaElement, value: string) {
    const [selStart, selEnd] = getSelectionPos(textArea);
    textArea.value = textArea.value.slice(0, selStart) + value + textArea.value.slice(selEnd);

    const newCursorPos = selStart + value.length;
    textArea.setSelectionRange(newCursorPos, newCursorPos);
    textArea.focus();
}

/**
 * Adds an event listener to the given textarea so that every time enter is clicked it determines if a new list value 
 * should be automatically included.
 * @param textArea 
 */
export function updateListOnEnter(textArea: HTMLTextAreaElement) {
    textArea.addEventListener('keypress', (e) => {
        if (e.code === 'Enter') {
            const lastLine = getSelectedTextLine(textArea);
            const textBeforeCursor = getSelectedTextLine(textArea);
            const textAfterCursor = textArea.value.substring(textArea.selectionStart).split('\n')[0];

            const extraText = /\S+$/.test(textAfterCursor);
            const startsWithMarks = lastLine && /^(\-|\d+\.|\>)/.test(lastLine);

            if (textBeforeCursor && startsWithMarks) {
                e.preventDefault();

                const emptyLineRegex = /^(\-|\d+\.|\>)\s*$/;
                const unorderedStartRegex = /^\- \S+/;
                const orderedStartRegex = /^\d+\. \S+/;
                const quoteStartRegex = /^\> \S+/;

                // Here it checks the regex but since they all check for non whitespace characters (\S+)
                // I need to check for if there's text after because on Enter 'lastLine = >' which would be falsy
                // according to the above regex but it should be true when there's text after ending up in '> \n text'. 
                if (emptyLineRegex.test(lastLine) && !extraText) {
                    // If the last line is an empty list item remove it.
                    const [selStart, _] = getSelectionPos(textArea);

                    // Get the part of the text before the cursor
                    const beforeCursor = textArea.value.substring(0, selStart);

                    // Find the start of the current line
                    const lineStart = beforeCursor.lastIndexOf('\n') + 1; // +1 to move past the newline
                    // Find the end of the current line
                    const lineEnd = textArea.value.indexOf('\n', selStart);
                    const actualLineEnd = lineEnd === -1 ? textArea.value.length : lineEnd; // Handle the last line case

                    // Remove the current line
                    const updatedText = textArea.value.substring(0, lineStart) + textArea.value.substring(actualLineEnd + 1);

                    // Update the textarea value
                    textArea.value = updatedText;
                }
                else if (unorderedStartRegex.test(lastLine) || (/^\-/.test(lastLine) && textAfterCursor)) {
                    // If the last line is an unordered list add a new list element.
                    insertAtCursor(textArea, '\n- ');
                }
                else if (orderedStartRegex.test(lastLine) || (/^\d+\./.test(lastLine) && textAfterCursor)) {
                    // If the last line is an ordered list add the next order.
                    let offset = textAfterCursor ? -1 : 0;
                    let nextOrder = getNextOrder(textArea, offset);
                    if (nextOrder && offset === -1) { nextOrder += 1 };
                    insertAtCursor(textArea, `\n${nextOrder}. `);
                }
                else if (quoteStartRegex.test(lastLine) || (/^\>/.test(lastLine) && textAfterCursor)) {
                    // If the last line is a quote block continue it.
                    insertAtCursor(textArea, "\n> ");
                }
            }
        }
    });
}

export async function MdtoHTML(text: string): Promise<string> {
    const renderer = new marked.Renderer();
    marked.use({
        gfm: true,
        breaks: true
    });

    renderer.link = ({ href, title, text }) => {
        return `<a href="${href}" title="${title || ''}" target="_blank" rel="noopener noreferrer">${text}</a>`;
    };

    const html: string = await marked.parse(text, { renderer: renderer });
    const purifiedHTML = DOMPurify.sanitize(html, { ADD_ATTR: ['target'] });

    return purifiedHTML;
}
