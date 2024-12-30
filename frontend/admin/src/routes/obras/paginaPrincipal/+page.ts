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
                    imageBorders {
                        n
                        s
                        e
                        o
                    }
                    logoBorders {
                        n
                        s
                        e
                        o
                    }
                }
                ambiente {
                    id
                    obra {
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
