import graphql from '$lib/utilities/api.js'

export const load = async ({ fetch, params }) => {
    const query = `
        query getProject($id: Int!) {
            project(id: $id) {
                id
                name
                descriptionEs
                descriptionEn
                area
                public
                spaces {
                    id
                    name
                    images {
                        filename
                        imageUrl
                        altTextEs
                        descriptionEs
                        descriptionEn
                        descriptionFont
                        bgColor
                        desktopConfig {
                            groupAlignment
                            groupEnd
                            imageSize
                            imageBorders {
                                n
                                s
                                e
                                w
                            }
                            descriptionPosition
                            descriptionAlignment
                            descriptionBorders {
                                n
                                s
                                e
                                w
                            }
                            descriptionLogoPosition
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
        }
    `;

    const projectData = (await graphql(query, {
        id: Number(params.proyectoID)
    }, fetch)).project;

    return { projectData };
}
