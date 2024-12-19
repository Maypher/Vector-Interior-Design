import { PUBLIC_apiUrl } from '$env/static/public';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { ambienteCreateSchema } from '$lib/utilities/yupSchemas';

export const load = async ({ fetch, params }) => {
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
            }
        }
    `;

    const variables = { id: ambienteID };

    const res = await fetch(PUBLIC_apiUrl, {
        method: "POST",
        body: JSON.stringify({
            query, variables
        }),
        credentials: "include",
        headers: {
            "Content-type": "application/json"
        }
    });

    const ambienteData = (await res.json()).data.ambiente;
    const formData = { name: ambienteData.name, description: ambienteData.description };
    const updateForm = await superValidate(formData, yup(ambienteCreateSchema));
    return { ambienteData, updateForm, obraID };
};
