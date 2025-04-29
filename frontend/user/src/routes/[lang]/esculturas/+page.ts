import graphql from "$lib/utilities/api";
import { error } from "@sveltejs/kit";

export const load = async ({ fetch, params }) => {
    const spanish = params.lang === 'es';

    const query = `
        query {
            sculptures {
                filename
                imageUrl
                altText: ${spanish ? 'altTextEs' : 'altTextEn'}
                sculptureData {
                    description: ${spanish ? 'descriptionEs' : 'descriptionEn'}
                    bgColor
                }
                desktopConfig {
                    groupAlignment
                }
            }
        }
    `;

    const sculptures = (await graphql(query, {}, fetch))?.sculptures;

    if (sculptures == null || (Array.isArray(sculptures) && sculptures.length === 0)) error(403);

    return { sculptures }
}
