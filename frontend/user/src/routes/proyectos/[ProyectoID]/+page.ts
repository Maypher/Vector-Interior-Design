import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const query = `
        query getProject($id: Int!) {
            project(id: $id) {
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
                        hideInProject
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

    const obraID = Number(params.ProyectoID);

    if (!Number.isInteger(obraID)) error(404, "Proyecto no existe");

    const projectData = (await graphql(query, { id: obraID }, fetch)).project;
    if (!projectData) error(404, "Proyecto no existe");

    return { projectData };
}
