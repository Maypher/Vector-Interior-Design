import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { ambienteCreateSchema } from '$lib/utilities/yupSchemas';
import graphql from '$lib/utilities/api.js';

export const load = async ({ params }) => {
    const ambienteID: number = +params.ambienteID;
    const obraID: number = +params.obraID;

    if (Number.isNaN(ambienteID)) error(404, `Ambiente con ID ${ambienteID} no existe.`);

    const query = `
        query getAmbiente($id: Int!) {
            ambiente(id: $id) {
                id
                name
                description
                images {
                    filename
                    altText
                }
                obra {
                    id
                    name
                    thumbnail {
                        filename
                    }
                }
            }
        }
    `;

    const variables = { id: ambienteID };

    const ambienteData = (await graphql(query, variables)).ambiente;
    const formData = { name: ambienteData.name, description: ambienteData.description };
    const updateForm = await superValidate(formData, yup(ambienteCreateSchema));
    return { ambienteData, updateForm };
};
