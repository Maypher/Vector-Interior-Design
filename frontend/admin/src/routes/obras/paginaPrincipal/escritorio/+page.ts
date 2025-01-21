import graphql from "$lib/utilities/api";

export const load = async ({ fetch }) => {
    const query = `
        query {
            mainPageImages {
                id
                filename
                altText
                mainImageConfig {
                    id
                    descriptionEs
                    descriptionEn
                    descriptionFont
                    descriptionAlignment
                    desktopConfig {
                        imagePosition
                        descriptionPosition
                        descriptionBorders {
                            n
                            s
                            e
                            w
                        }
                        logoPosition
                        logoBorders {
                            n
                            s
                            e
                            w
                        }
                        descriptionLogoPosition
                        descriptionLogoBorders {
                            n
                            s
                            e
                            w
                        }
                        overflow
                    }
                }
            }
        }
    `;

    const mainPageImages = (await graphql(query, {}, fetch)).mainPageImages;

    return { mainPageImages };
}
