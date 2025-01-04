import { createObraSchema } from '$lib/utilities/yupSchemas.js';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';

export const load = async ({ params }) => {
    const ambienteID: number = +params.ambienteID;
    const obraID: number = +params.obraID;

    if (isNaN(ambienteID)) error(404, `Ambiente con ID ${ambienteID} no existe.`);

    const createForm = await superValidate(yup(createObraSchema));

    return { ambienteID, createForm, obraID };
};
