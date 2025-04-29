import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, parent }) => {
    const { selectedLanguage } = await parent();
    const english = selectedLanguage == 'en';

    const query = `
        query projects {
            projects {
                id
                name: ${english ? 'nameEn' : 'nameEs'}
                thumbnail {
                    filename
                    imageUrl
                    altText: ${english ? 'altTextEn' : 'altTextEs'}
                    altTextEn
                }
            }
        }
    `;

    const projects = (await graphql(query, {}, fetch))?.projects;

    if (projects == null || (Array.isArray(projects) && projects.length === 0)) error(403);

    return { projects };
}
