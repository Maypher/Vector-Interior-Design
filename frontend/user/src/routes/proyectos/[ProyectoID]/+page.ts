import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const query = `
        query getProject($id: Int!) {
            project(id: $id) {
                id
                name
                description
                area
                thumbnail {
                    filename
                    altText
                }
                spaces {
                    id
                    name
                    description
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
            projects {
                id
                name
            }
        }
    `;

    const projectId = Number(params.ProyectoID);

    if (!Number.isInteger(projectId)) error(404, "Proyecto no existe");

    const data = await graphql(query, { id: projectId }, fetch);

    const projectData = data.project;
    if (!projectData) error(404, "Proyecto no existe");

    const projects: { id: number, name: string }[] = data.projects;

    return { projectData, projects };
}
