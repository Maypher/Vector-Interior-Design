import graphql from '$lib/utilities/api.js'

export const load = async () => {
    const query = `
        query getObras($pageSize: Int) {
            obras(pageSize: $pageSize) {
                obras {
                    name
                    thumbnail {
                        filename
                        altText
                    }
                }
            }
        }
    `;

    const obras = (await graphql(query, { pageSize: 50 })).obras;
    return { obras };
}
