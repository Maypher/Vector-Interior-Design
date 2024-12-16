import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { ambienteCreateSchema } from '$lib/utilities/yupSchemas';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
    const createForm = await superValidate(yup(ambienteCreateSchema));

    return { createForm, obraID: params.obraID }
}
