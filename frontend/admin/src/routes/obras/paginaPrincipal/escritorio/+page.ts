import graphql from "$lib/utilities/api";

export const load = async ({ fetch }) => {
    const query = `
        query {
            mainPageImages {
                id
                filename
                imageUrl
                altTextEs
                mainImageConfig {
                    id
                    descriptionEs
                    descriptionEn
                    descriptionFont
                    bgColor
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
