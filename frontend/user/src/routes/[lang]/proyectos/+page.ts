import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, params }) => {
    const spanish = params.lang == 'es';

    const query = `
        query projects {
            projects {
                id
                name: ${spanish ? 'nameEs' : 'nameEn'}
                thumbnail {
                    filename
                    imageUrl
                    altText: ${spanish ? 'altTextEs' : 'altTextEn'}
                    altTextEn
                }
            }
        }
    `;

    const projects = (await graphql(query, {}, fetch))?.projects;

    if (projects == null || (Array.isArray(projects) && projects.length === 0)) error(403);

    return { projects };
}
