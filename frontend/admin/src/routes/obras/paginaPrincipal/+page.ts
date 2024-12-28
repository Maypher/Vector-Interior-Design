import graphql from "$lib/utilities/api"

export const load = async ({ fetch }) => {
    const query = `
        query getMainPagesImages {
            mainPageImages {
                id
                filename
                mainPage
                mainImageConfig  {
                    id
                    description
                    descriptionEn
                    descriptionPos
                    logoPos
                    overflow
                }
                ambiente {
                    id
                    obra {
                        id
                    }
                }
            }
        }
    `;

    const mainPageData = (await graphql(query, {}, fetch)).mainPageImages;
    return { mainPageData };
}
