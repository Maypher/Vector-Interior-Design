import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const query = `
        query getProject($id: Int!) {
            project(id: $id) {
                id
                name
                descriptionEs
                descriptionEn
                area
                thumbnail {
                    filename
                    altTextEs
                    altTextEn
                }
                spaces {
                    id
                    name
                    images {
                        filename
                        altTextEs
                        altTextEn
                        descriptionEs
                        descriptionEn
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
            }
        }
    `;

    const projectId = Number(params.ProyectoID);

    if (!Number.isInteger(projectId)) error(404, "Proyecto no existente");

    const data = await graphql(query, { id: projectId }, fetch);

    const projectData = data.project;
    if (!projectData) error(404, "Proyecto no existente");
    // Used to determine if this is the final project to link to a different page
    const finalProject = data.projects.findIndex((project: { id: number }) => project.id === projectData.id) === data.projects.length - 1;

    return { projectData, finalProject };
}
