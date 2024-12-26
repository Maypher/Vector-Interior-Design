import { PUBLIC_graphql } from "$env/static/public";

/**
 * Helper function to query or mutate the Graphql API with all the required parameters.
 * @param query The query string to send to graphql.
 * @param variables The variables to be replaced in the query.
 * @param customFetch Used to pass sveltekit's custom fetch when calling from +page.ts/+layout.ts on ssr.
 * @returns The data requested by the query. Throws an error if the return status isn't ok.
 */
export default async function graphql(query: string, variables: Record<string, any>, customFetch: (input: string | URL | globalThis.Request, init?: RequestInit) => Promise<Response> = fetch): Promise<Record<string, any>> {
    const res = await customFetch(PUBLIC_graphql, {
        method: "POST",
        body: JSON.stringify({ query, variables }),
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (res.ok) return (await res.json()).data;
    else throw await res.text();
}
