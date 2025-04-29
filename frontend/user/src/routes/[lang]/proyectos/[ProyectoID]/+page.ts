import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const spanish = params.lang === 'es';

    const query = `
        query getProject($id: Int!) {
            project(id: $id) {
                id
                name: ${spanish ? 'nameEs' : 'nameEn'}
                description: ${spanish ? 'descriptionEs' : 'descriptionEn'}
                area
                thumbnail {
                    filename
                    imageUrl
                    altText: ${spanish ? 'altTextEs' : 'altTextEn'}
                }
                spaces {
                    id
                    name
                    images {
                        filename
                        imageUrl
                        altText: ${spanish ? 'altTextEs' : 'altTextEn'}
                        description: ${spanish ? 'descriptionEs' : 'descriptionEn'}
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

    if (!Number.isInteger(projectId)) error(404, spanish ? "Proyecto inexistente" : 'Project not found');

    const data = await graphql(query, { id: projectId }, fetch);

    const projectData = data?.project;
    if (!projectData) error(404, spanish ? "Proyecto inexistente" : 'Project not found');

    const currentProjectIndex: number = data.projects.findIndex((project: { id: number }) => project.id === projectData.id);

    // Used to link to scroll to the next project on project end
    const nextProjectId = data.projects.at(currentProjectIndex + 1)?.id;
    // Used to determine if this is the final project to link to a different page
    const finalProject = currentProjectIndex === data.projects.length - 1;

    return { projectData, nextProjectId, finalProject };
}
