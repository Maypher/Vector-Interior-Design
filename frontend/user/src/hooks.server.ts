import type { Handle, HandleFetch } from "@sveltejs/kit";
import { PUBLIC_apiURL } from "$env/static/public";

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
    if (request.url.startsWith(`https://${PUBLIC_apiURL}`)) {
        // clone the original request, but change the URL
        request = new Request(
            request.url.replace(`https://${PUBLIC_apiURL}`, 'http://user-backend'),
            request
        );

        request.headers.set("cookie", event.request.headers.get("cookie")!);
    }

    return fetch(request);
};

export const handle: Handle = async ({ event, resolve }) => {
    const availableLanguages = ["en", "es"];

    let selectedLanguage = event.cookies.get('lang');

    if (!selectedLanguage) {
        const acceptedLanguages = event.request.headers.get("Accept-Language")?.split(',');
        if (acceptedLanguages) {
            const preferredLang = acceptedLanguages.find((x) => availableLanguages.includes(x.slice(0, 2)))?.slice(0, 2) || 'en';
            selectedLanguage = preferredLang;
        } else selectedLanguage = 'en';
    }

    (event.locals as any).language = selectedLanguage;

    return await resolve(event, {
        transformPageChunk: ({ html }) => html.replace("%%lang%%", selectedLanguage),
    });
}
