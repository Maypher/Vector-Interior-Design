import graphql from "$lib/utilities/api";

export const load = async ({ fetch }) => {
    const query = `
        query {
            sculptures {
                filename
                altTextEs
                altTextEn
                sculptureData {
                    descriptionEs
                    descriptionEn
                }
                desktopConfig {
                    groupAlignment
                }
            }
        }
    `;

    const sculptures = (await graphql(query, {}, fetch)).sculptures;

    return { sculptures }
}
