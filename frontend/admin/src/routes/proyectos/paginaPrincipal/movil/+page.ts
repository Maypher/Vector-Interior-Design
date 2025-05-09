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
                    descriptionAlignment
                    bgColor
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
            }
        }
    `;

    const mainPageImages = (await graphql(query, {}, fetch)).mainPageImages;

    return { mainPageImages };
}
