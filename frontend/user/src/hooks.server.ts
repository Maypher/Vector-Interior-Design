import type { Handle, HandleFetch } from "@sveltejs/kit";
import { PUBLIC_apiPath } from "$env/static/public";

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
    console.log(request.url);
    if (request.url.includes(`${PUBLIC_apiPath}`)) {
        // clone the original request, but change the URL to the docker service

        const regex = new RegExp(`(.*)${PUBLIC_apiPath}(.*)?`);
        request = new Request(request.url.replace(regex, `http://user-backend/$2`), request);

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
