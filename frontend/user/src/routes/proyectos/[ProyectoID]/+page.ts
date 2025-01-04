import graphql from '$lib/utilities/api.js'
import { error } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const query = `
        query getObra($id: Int!) {
            obra(id: $id) {
                name
                description
                area
                thumbnail {
                    filename
                    altText
                }
                ambientes {
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
                                o
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

    if (!Number.isInteger(obraID)) error(404, "Obra no existe");

    const obraData = (await graphql(query, { id: obraID }, fetch)).obra;

    if (!obraData) error(404, "Obra no existe");

    return { obraData };
}
