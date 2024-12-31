import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch }) => {
    const query = `
        query mainPageImages {
            mainPageImages {
                filename
                altText
                mainImageConfig {
                    description
                    descriptionPos
                    descriptionFont
                    descriptionAlignment
                    descriptionFontSize
                    logoPos
                    overflow
                    logoBorders {
                        n
                        s
                        e
                        o
                    }
                    imageBorders {
                        n
                        s
                        e
                        o
                    }
                }
            }
        }
    `;

    const mainImages = (await graphql(query, {}, fetch)).mainPageImages;
    return { mainImages };
}
