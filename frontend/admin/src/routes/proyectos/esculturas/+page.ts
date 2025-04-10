import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch }) => {
    const query = `
        query sculptures {
            sculptures {
                filename
                imageUrl
                altTextEs
                sculptureData {
                    id
                    descriptionEs
                    descriptionEn
                    bgColor
                }
                space {
                    id
                    project {
                        id
                    }
                }
            }
        }
    `;

    const sculptures = (await graphql(query, {}, fetch)).sculptures;

    return { sculptures };
}
