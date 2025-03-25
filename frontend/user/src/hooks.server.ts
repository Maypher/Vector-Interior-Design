import type { HandleFetch } from "@sveltejs/kit";
import { PUBLIC_graphql } from "$env/static/public";

export const handleFetch: HandleFetch = async ({ request, fetch }) => {
    if (request.url.startsWith(`https://${PUBLIC_graphql}`)) {
        // clone the original request, but change the URL
        request = new Request(
            request.url.replace(`https://${PUBLIC_graphql}`, 'http://user-backend/graphql'),
            request
        );
    }

    return fetch(request);
};
