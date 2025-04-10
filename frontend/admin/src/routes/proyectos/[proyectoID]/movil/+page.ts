import graphql from "$lib/utilities/api";

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
                                phoneConfig {
                                    borders {
                                        n
                                        s
                                        e
                                        w
                                    }
                                    alignment
                                    descriptionPos
                                    descriptionAlignment
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
