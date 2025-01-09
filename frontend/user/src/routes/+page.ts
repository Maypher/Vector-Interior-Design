import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch }) => {
    const query = `
        query mainPageImages {
            mainPageImages {
                filename
                altText
                mainImageConfig {
                    descriptionEn
                    descriptionEs
                    descriptionFont
                    descriptionAlignment
                    descriptionFontSize
                    phoneConfig {
                        descriptionPosition
                        logoPosition
                        overflow
                        logoBorders {
                            n
                            s
                            e
                            w
                        }
                        imageBorders {
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

    const mainImages = (await graphql(query, {}, fetch)).mainPageImages;
    return { mainImages };
}
