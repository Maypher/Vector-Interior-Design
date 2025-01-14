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
                    descriptionEs
                    descriptionEn
                    descriptionAlignment
                    descriptionFont
                    descriptionFontSize
                    phoneConfig {
                        descriptionPosition
                        logoPosition
                        overflow
                        imageBorders {
                            n
                            s
                            e
                            w
                        }
                        logoBorders {
                            n
                            s
                            e
                            w
                        }
                    }
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
    console.log(mainPageData);

    return { mainPageData };
}
