import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { spaceCreateSchema } from '$lib/utilities/yupSchemas';
import type { PageLoad } from './$types';
import graphql from '$lib/utilities/api';

export const load: PageLoad = async ({ params, fetch }) => {
    const createForm = await superValidate(yup(spaceCreateSchema));

    const query = `
        query project($id: Int!) {
            project(id: $id) {
                id
                nameEs
            }
        }
    `;

    const project = (await graphql(query, { id: parseInt(params.proyectoID) }, fetch)).project;

    return { createForm, projectId: params.proyectoID, project }
}
