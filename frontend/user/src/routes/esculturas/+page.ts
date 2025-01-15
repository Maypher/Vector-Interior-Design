import graphql from "$lib/utilities/api";

export const load = async ({ fetch }) => {
    const query = `
        query {
            sculptures {
                filename
                altText
                sculptureData {
                    descriptionEs
                    descriptionEn
                }
            }
        }
    `;

    const sculptures = (await graphql(query, {}, fetch)).sculptures;

    return { sculptures }
}
