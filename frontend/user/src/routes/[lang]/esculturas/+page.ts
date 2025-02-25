import graphql from "$lib/utilities/api";

export const load = async ({ fetch, parent }) => {
    const { selectedLanguage } = await parent();
    const english = selectedLanguage === 'en';

    const query = `
        query {
            sculptures {
                filename
                altText: ${english ? 'altTextEn' : 'altTextEs'}
                sculptureData {
                    description: ${english ? 'descriptionEn' : 'descriptionEs'}
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
