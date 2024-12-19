import { type Obra } from '$lib/utilities/interfaces.js';
import { obraCreateSchema } from '$lib/utilities/yupSchemas.js';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { PUBLIC_apiUrl } from '$env/static/public';
import graphql from '$lib/utilities/api.js';

export async function load({ params, fetch }) {
    const obraID: number = +params.obraID;

    if (Number.isNaN(obraID)) error(404, `Obra con ID ${obraID} no existe.`);

    const query = `
                query GetObra($id: Int!) {
                    obra(id: $id) {
                        id
                        name
                        description
                        area
                        ambientes {
                            id
                            name
                        }
                    }
                }
           `;
    const variables = { id: obraID };

    const obraData = (await graphql(query, variables)).obra;

    const formData = { name: obraData.name, description: obraData.description, area: obraData.area };
    const updateForm = await superValidate(formData, yup(obraCreateSchema));

    if (obraData) return { updateForm, obraData };
    else error(404, `Obra con ID ${obraID} no existe.`);
}
