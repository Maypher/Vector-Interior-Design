import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch }) => {
    const query = `
        query obras {
            obras {
                obras {
                    id
                    name
                    thumbnail {
                        filename
                        altText
                    }
                }
            }
        }
    `;

    const obras = (await graphql(query, {}, fetch)).obras.obras;

    return { obras };
}
