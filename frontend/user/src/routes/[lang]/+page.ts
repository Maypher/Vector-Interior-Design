import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch, parent }) => {
    const { selectedLanguage } = await parent();
    const english = selectedLanguage === 'en';

    const query = `
        query mainPageImages {
            mainPageImages {
                filename
                altText: ${english ? 'altTextEn' : 'altTextEs'}
                mainImageConfig {
                    description: ${english ? 'descriptionEn' : 'descriptionEs'}
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
                    desktopConfig {
                        overflow
                        imagePosition
                        descriptionPosition
                        descriptionLogoPosition
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
                    }
                }
            }
        }
    `;

    const mainImages = (await graphql(query, {}, fetch)).mainPageImages;
    return { mainImages };
}
