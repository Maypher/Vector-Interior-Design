import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch, parent }) => {
    const { selectedLanguage } = await parent();
    const english = selectedLanguage == 'en';

    const query = `
        query projects {
            projects {
                id
                name
                thumbnail {
                    filename
                    imageUrl
                    altText: ${english ? 'altTextEn' : 'altTextEs'}
                    altTextEn
                }
            }
        }
    `;

    const projects = (await graphql(query, {}, fetch)).projects;

    return { projects };
}
