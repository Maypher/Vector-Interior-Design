import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch }) => {
    const query = `
        query projects {
            projects {
                id
                name
                thumbnail {
                    filename
                    altText
                }
            }
        }
    `;

    const projects = (await graphql(query, {}, fetch)).projects;

    return { projects };
}
