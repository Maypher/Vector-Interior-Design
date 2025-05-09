import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, params }) => {
    const spanish = params.lang === 'es';

    const query = `
        query mainPageImages {
            mainPageImages {
                filename
                imageUrl
                altText: ${spanish ? 'altTextEs' : 'altTextEn'}
                mainImageConfig {
                    description: ${spanish ? 'descriptionEs' : 'descriptionEn'}
                    descriptionFont
                    descriptionAlignment
                    descriptionFontSize
                    bgColor
                    imageSize
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

    const mainImages = (await graphql(query, {}, fetch))?.mainPageImages;

    if (mainImages == null || (Array.isArray(mainImages) && mainImages.length === 0)) error(403);

    return { mainImages };
}
