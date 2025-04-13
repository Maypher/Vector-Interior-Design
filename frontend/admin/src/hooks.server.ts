import type { HandleFetch } from "@sveltejs/kit";
import { PUBLIC_apiPath } from "$env/static/public";

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
    if (request.url.includes(`${PUBLIC_apiPath}`)) {
        // clone the original request, but change the URL to the docker service

        const regex = new RegExp(`(.*)${PUBLIC_apiPath}(.*)?`);

        request = new Request(
            request.url.replace(regex,
                `http://admin-backend/$2`
            ),
            request
        );

        request.headers.set("cookie", event.request.headers.get("cookie")!);
    }

    return fetch(request);
};
