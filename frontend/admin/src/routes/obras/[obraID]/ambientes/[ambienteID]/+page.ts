import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { spaceCreateSchema } from '$lib/utilities/yupSchemas';
import graphql from '$lib/utilities/api.js';

export const load = async ({ params, fetch }) => {
    const spaceID: number = +params.ambienteID;

    if (Number.isNaN(spaceID)) error(404, `Ambiente con ID ${spaceID} no existe.`);

    const query = `
        query getSpaces($id: Int!) {
            space(id: $id) {
                id
                name
                description
                images {
                    filename
                    altText
                    mainPage
                }
                project {
                    id
                    name
                    thumbnail {
                        filename
                    }
                }
            }
        }
    `;

    const variables = { id: spaceID };

    const spaceData = (await graphql(query, variables, fetch)).space;
    const formData = { name: spaceData.name, description: spaceData.description };
    const updateForm = await superValidate(formData, yup(spaceCreateSchema));
    return { spaceData, updateForm };
};
