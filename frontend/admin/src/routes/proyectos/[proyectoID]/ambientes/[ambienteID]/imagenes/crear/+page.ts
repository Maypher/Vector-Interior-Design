import { createImageSchema } from '$lib/utilities/yupSchemas.js';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';

export const load = async ({ params }) => {
    const ambienteID: number = +params.ambienteID;
    const projectId: number = +params.proyectoID;

    if (isNaN(ambienteID)) error(404, `Ambiente con ID ${ambienteID} no existe.`);

    const createForm = await superValidate(yup(createImageSchema));

    return { ambienteID, createForm, projectId };
};
