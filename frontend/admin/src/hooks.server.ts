import type { HandleFetch } from "@sveltejs/kit";
import { PUBLIC_apiURL } from "$env/static/public";

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
    if (request.url.startsWith(`https://${PUBLIC_apiURL}`)) {
        // clone the original request, but change the URL
        request = new Request(
            request.url.replace(`https://${PUBLIC_apiURL}`, 'http://admin-backend'),
            request
        );

        request.headers.set("cookie",
            event.request.headers.get("cookie")!
        );
    }

    return fetch(request);
};
