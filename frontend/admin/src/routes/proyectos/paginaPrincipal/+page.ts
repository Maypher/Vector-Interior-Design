import graphql from "$lib/utilities/api"

export const load = async ({ fetch }) => {
    const query = `
        query getMainPagesImages {
            mainPageImages {
                id
                filename
                imageUrl
                mainPage
                mainImageConfig  {
                    id
                    index
                }
                space {
                    id
                    project {
                        id
                        public
                    }
                }
            }
        }
    `;

    const mainPageData = (await graphql(query, {}, fetch)).mainPageImages;

    return { mainPageData };
}
