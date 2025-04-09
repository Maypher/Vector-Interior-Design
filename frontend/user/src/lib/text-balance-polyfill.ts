// Thanks to Steffen and Dominik for the polyfill
// https://bleech.de/en/blog/the-ups-and-downs-of-text-wrap-balance-and-a-polyfill/
export default function () {
    if (!window.CSS.supports('text-wrap', 'balance')) {
        const elements = document.querySelectorAll('.text-balance');
        const resizeObserver = new ResizeObserver((entries) => {
            entries.forEach((entry) => relayout(entry.target as HTMLElement));
        })
        elements.forEach((element) => {
            relayout(element as HTMLElement);
            resizeObserver.observe(element);
        })
        window.addEventListener('resize', () => {
            elements.forEach((element) => {
                relayout(element as HTMLElement);
            })
        })
    }
}

function relayout(wrapper: HTMLElement, ratio = 1) {
    const container = wrapper.parentElement!;

    const update = (width: number) => (wrapper.style.maxWidth = width + 'px');

    wrapper.style.display = 'inline-block';
    wrapper.style.verticalAlign = 'top';
    // Reset wrapper width
    wrapper.style.maxWidth = '';

    // Get the initial container size
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Synchronously do binary search and calculate the layout
    let lower = width / 2 - 0.25;
    let upper = width + 0.5;
    let middle;

    if (width) {
        // Ensure we don't search widths lower than when the text overflows
        update(lower);
        lower = Math.max(wrapper.scrollWidth, lower);

        while (lower + 1 < upper) {
            middle = Math.round((lower + upper) / 2);
            update(middle);
            if (container.clientHeight === height) {
                upper = middle;
            } else {
                lower = middle;
            }
        }

        update(upper * ratio + width * (1 - ratio));

        let classList = wrapper.classList;
        if (classList.contains("text-center") || classList.contains("text-justify")) {
            container.classList.add("flex");
            container.classList.add("justify-center");
        }
        else if (classList.contains("text-left")) {
            container.classList.add("flex");
            container.classList.add("justify-start");
        }
        else if (classList.contains("text-right")) {
            container.classList.add("flex");
            container.classList.add("justify-end");
        }
    }
}
