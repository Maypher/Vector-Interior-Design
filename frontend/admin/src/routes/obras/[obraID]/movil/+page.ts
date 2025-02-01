import graphql from "$lib/utilities/api";

export const load = async ({ fetch, params }) => {
    const query = `
                query getProject($id: Int!) {
                    project(id: $id) {
                        id
                        name
                        description
                        area
                        public
                        spaces {
                            id
                            name
                            images {
                                filename
                                altText
                                description
                                descriptionFont
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
        id: Number(params.obraID)
    }, fetch)).project;

    return { projectData };
}
