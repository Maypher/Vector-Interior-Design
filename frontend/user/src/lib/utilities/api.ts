import { PUBLIC_apiURL } from "$env/static/public";
import { error } from "@sveltejs/kit";

/**
 * Helper function to query or mutate the Graphql API with all the required parameters.
 * @param query The query string to send to graphql.
 * @param variables The variables to be replaced in the query.
 * @returns The data requested by the query. Throws an error if the return status isn't ok.
 */
export default async function graphql(query: string,
    variables: Record<string, any> = {},
    customFetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response> = fetch): Promise<Record<string, any>> {
    try {
        const res = await customFetch(`https://${PUBLIC_apiURL}/graphql`, {
            method: "POST",
            body: JSON.stringify({ query, variables }),
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (res.ok) return (await res.json()).data;
        else error(res.status, await res.text());
    } catch {
        error(502);
    }
}
